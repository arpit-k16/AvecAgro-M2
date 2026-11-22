// AvecAgro web server for Render (no dependencies; Node 18+).
// Serves the single-page app and proxies AI calls to the Anthropic Messages API.
// The API key is read from the ANTHROPIC_API_KEY environment variable (set in Render's dashboard), never stored in code.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 10000;
const KEY = process.env.ANTHROPIC_API_KEY || '';
const MODEL = process.env.MODEL || 'claude-sonnet-5-5';
const MAX_TOKENS = parseInt(process.env.MAX_TOKENS || '4000', 10);
const LIMIT_PER_HOUR = parseInt(process.env.LIMIT_PER_HOUR || '120', 10); // AI calls per visitor IP per hour
const PAGE = path.join(__dirname, '..', 'code', 'index.html');

const hits = new Map(); // ip -> [timestamps]
function allowed(ip) {
  const now = Date.now(), hour = 3600e3;
  const list = (hits.get(ip) || []).filter(t => now - t < hour);
  if (list.length >= LIMIT_PER_HOUR) { hits.set(ip, list); return false; }
  list.push(now); hits.set(ip, list); return true;
}

function send(res, code, obj) {
  res.writeHead(code, { 'content-type': 'application/json', 'cache-control': 'no-store' });
  res.end(JSON.stringify(obj));
}

function readBody(req, max = 200000) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => { data += c; if (data.length > max) { reject(new Error('Request too large')); req.destroy(); } });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

// The page sends either a string or [{role, content}] (same shape as the Claude artifact "sample" API).
function toMessages(input) {
  if (typeof input === 'string') return [{ role: 'user', content: input }];
  if (Array.isArray(input) && input.length && input.every(m => (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string'))
    return input.map(m => ({ role: m.role, content: m.content }));
  throw new Error('input must be a string or a list of {role, content}');
}

async function callClaude(messages) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({ model: MODEL, max_tokens: MAX_TOKENS, messages })
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) {
    const err = new Error((j.error && j.error.message) || `Anthropic API error ${r.status}`);
    err.status = r.status; throw err;
  }
  const text = (j.content || []).filter(b => b.type === 'text').map(b => b.text).join('');
  return { text, truncated: j.stop_reason === 'max_tokens', modelApplied: j.model || MODEL };
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-cache' });
      return fs.createReadStream(PAGE).pipe(res);
    }
    if (req.method === 'GET' && url.pathname === '/api/health') {
      return send(res, 200, { ok: !!KEY, model: KEY ? MODEL : null });
    }
    if (req.method === 'POST' && url.pathname === '/api/sample') {
      if (!KEY) return send(res, 503, { error: 'The server has no ANTHROPIC_API_KEY set.' });
      const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
      if (!allowed(ip)) return send(res, 429, { error: 'Too many requests from this address. Try again in an hour.' });
      const body = JSON.parse(await readBody(req) || '{}');
      const out = await callClaude(toMessages(body.input));
      return send(res, 200, out);
    }
    send(res, 404, { error: 'Not found' });
  } catch (e) {
    send(res, e.status === 429 ? 429 : 500, { error: e.message || 'Server error' });
  }
});

server.listen(PORT, () => console.log(`AvecAgro listening on ${PORT} (model ${MODEL}, key ${KEY ? 'set' : 'MISSING'})`));
