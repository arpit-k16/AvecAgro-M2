// AvecAgro web server for Render (no dependencies; Node 18+).
// Serves the single-page app and proxies AI calls to Groq (open-source Llama models), Gemini or Anthropic,
// whichever key is set in the environment (Render dashboard). Keys are never stored in code.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 10000;
const GROQ = process.env.GROQ_API_KEY || '';
const GEMINI = process.env.GEMINI_API_KEY || '';
const ANTHROPIC = process.env.ANTHROPIC_API_KEY || '';
const PROVIDER = GROQ ? 'groq' : GEMINI ? 'gemini' : ANTHROPIC ? 'anthropic' : '';
const KEY = GROQ || GEMINI || ANTHROPIC;
const MODEL = process.env.MODEL || { groq: 'llama-3.3-70b-versatile', gemini: 'gemini-2.5-flash', anthropic: 'claude-sonnet-5-5' }[PROVIDER] || '';
const FALLBACK_MODEL = process.env.FALLBACK_MODEL || (PROVIDER === 'groq' ? 'openai/gpt-oss-120b' : '');
const runLog = []; // recent test/lab results posted by the page (kept in memory, newest last)
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

async function callGroq(messages, model) {
  const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST', headers: { authorization: 'Bearer ' + GROQ, 'content-type': 'application/json' },
    body: JSON.stringify({ model, messages, max_tokens: MAX_TOKENS, temperature: 0.2 })
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error((j.error && j.error.message) || `Groq error ${r.status}`); e.status = r.status; throw e; }
  const c = (j.choices || [])[0] || {};
  return { text: (c.message && c.message.content) || '', truncated: c.finish_reason === 'length', modelApplied: j.model || model };
}
async function callGemini(messages, model) {
  const contents = messages.map(m => ({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text: m.content }] }));
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${GEMINI}`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ contents, generationConfig: { temperature: 0.2, maxOutputTokens: MAX_TOKENS } })
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error((j.error && j.error.message) || `Gemini error ${r.status}`); e.status = r.status; throw e; }
  const cand = (j.candidates || [])[0] || {};
  return { text: ((cand.content && cand.content.parts) || []).map(p => p.text || '').join(''), truncated: cand.finishReason === 'MAX_TOKENS', modelApplied: model };
}
async function callAnthropic(messages, model) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST', headers: { 'x-api-key': ANTHROPIC, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({ model, max_tokens: MAX_TOKENS, messages })
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error((j.error && j.error.message) || `Anthropic error ${r.status}`); e.status = r.status; throw e; }
  return { text: (j.content || []).filter(b => b.type === 'text').map(b => b.text).join(''), truncated: j.stop_reason === 'max_tokens', modelApplied: j.model || model };
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function callAI(messages) {
  const fn = { groq: callGroq, gemini: callGemini, anthropic: callAnthropic }[PROVIDER];
  for (let attempt = 0; attempt < 3; attempt++) {
    try { return await fn(messages, MODEL); }
    catch (e) {
      if (e.status === 429 && attempt < 2) { await sleep(6000 * (attempt + 1)); continue; }   // per-minute limit: wait and retry
      if ((e.status === 429 || e.status === 404 || e.status === 400) && FALLBACK_MODEL) return await fn(messages, FALLBACK_MODEL);
      throw e;
    }
  }
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-cache' });
      return fs.createReadStream(PAGE).pipe(res);
    }
    if (req.method === 'GET' && url.pathname === '/api/health') {
      return send(res, 200, { ok: !!KEY, provider: PROVIDER || null, model: KEY ? MODEL : null });
    }
    if (req.method === 'POST' && url.pathname === '/api/sample') {
      if (!KEY) return send(res, 503, { error: 'The server has no AI key set (GROQ_API_KEY, GEMINI_API_KEY or ANTHROPIC_API_KEY).' });
      const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
      if (!allowed(ip)) return send(res, 429, { error: 'Too many requests from this address. Try again in an hour.' });
      const body = JSON.parse(await readBody(req) || '{}');
      const out = await callAI(toMessages(body.input));
      return send(res, 200, out);
    }
    if (req.method === 'POST' && url.pathname === '/api/log') {
      const body = JSON.parse(await readBody(req, 400000) || '{}');
      runLog.push({ at: new Date().toISOString(), ...body }); if (runLog.length > 60) runLog.shift();
      return send(res, 200, { ok: true });
    }
    if (req.method === 'GET' && url.pathname === '/api/log') return send(res, 200, runLog);
    send(res, 404, { error: 'Not found' });
  } catch (e) {
    send(res, e.status === 429 ? 429 : 500, { error: e.message || 'Server error' });
  }
});

server.listen(PORT, () => console.log(`AvecAgro listening on ${PORT} (provider ${PROVIDER || 'none'}, model ${MODEL || '-'})`));
