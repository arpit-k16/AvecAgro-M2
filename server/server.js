// AvecAgro web server for Render (no dependencies; Node 18+).
// Serves the single-page app and proxies AI calls to Groq (open models), Gemini or Anthropic,
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
let MODEL = process.env.MODEL || { groq: 'openai/gpt-oss-120b', gemini: 'gemini-2.5-flash', anthropic: 'claude-sonnet-5-5' }[PROVIDER] || '';
// Groq models in order of preference for this app (higher free-tier tokens-per-minute first). The first one the key can use is chosen at startup.
const GROQ_PREFS = (process.env.GROQ_MODELS || 'meta-llama/llama-4-scout-17b-16e-instruct,meta-llama/llama-4-maverick-17b-128e-instruct,llama-3.3-70b-versatile,openai/gpt-oss-120b,openai/gpt-oss-20b,qwen/qwen3-32b').split(',');
let groqModels = [];
const runLog = []; // recent test/lab results posted by the page (kept in memory, newest last)
const MAX_TOKENS = parseInt(process.env.MAX_TOKENS || '3000', 10);
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

// ---- Groq: pacing against free-tier tokens-per-minute (TPM) limits ----
const rl = { limit: 8000, remaining: null, resetAt: 0 };   // learned from x-ratelimit-* response headers
function parseReset(v) {             // "7.66s", "1m2.5s", "120ms" -> milliseconds
  if (!v) return 0; let ms = 0, m;
  if ((m = /([\d.]+)m(?!s)/.exec(v))) ms += parseFloat(m[1]) * 60000;
  if ((m = /([\d.]+)s/.exec(v)) && !/ms$/.test(v.trim()) || (m = /m([\d.]+)s/.exec(v))) ms += parseFloat(m[1]) * 1000;
  if ((m = /^([\d.]+)ms$/.exec(v.trim()))) ms = parseFloat(m[1]);
  return ms;
}
const estTokens = messages => Math.ceil(messages.reduce((n, m) => n + m.content.length, 0) / 3.2) + 20;
async function callGroq(messages, model, maxTokens) {
  const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST', headers: { authorization: 'Bearer ' + GROQ, 'content-type': 'application/json' },
    body: JSON.stringify(Object.assign({ model, messages, max_tokens: maxTokens, temperature: 0.2 }, /gpt-oss/.test(model) ? { reasoning_effort: 'low' } : {}))
  });
  const lim = parseInt(r.headers.get('x-ratelimit-limit-tokens') || '0', 10); if (lim) rl.limit = lim;
  const rem = r.headers.get('x-ratelimit-remaining-tokens'); if (rem !== null) rl.remaining = parseInt(rem, 10);
  const rs = parseReset(r.headers.get('x-ratelimit-reset-tokens')); if (rs) rl.resetAt = Date.now() + rs;
  const j = await r.json().catch(() => ({}));
  if (!r.ok) {
    const e = new Error((j.error && j.error.message) || `Groq error ${r.status}`); e.status = r.status;
    e.retryAfter = parseFloat(r.headers.get('retry-after') || '0'); e.tooLarge = r.status === 413 || /too large/i.test(e.message); throw e;
  }
  const c = (j.choices || [])[0] || {};
  return { text: (c.message && c.message.content) || '', truncated: c.finish_reason === 'length', modelApplied: j.model || model };
}
async function pickGroqModel() {
  try {
    const r = await fetch('https://api.groq.com/openai/v1/models', { headers: { authorization: 'Bearer ' + GROQ } });
    const j = await r.json(); groqModels = (j.data || []).filter(m => m.active !== false).map(m => m.id);
    if (!process.env.MODEL || !groqModels.includes(MODEL)) { const pick = GROQ_PREFS.find(m => groqModels.includes(m)); if (pick) MODEL = pick; }
    console.log('Groq models available:', groqModels.join(', ')); console.log('Using model:', MODEL);
  } catch (e) { console.log('Could not list Groq models:', e.message); }
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
// One AI call at a time (free tiers are per-minute), each paced so it fits the remaining token budget.
let queue = Promise.resolve();
function callAI(messages) {
  const job = queue.then(() => runAI(messages));
  queue = job.catch(() => {});
  return job;
}
async function runAI(messages) {
  if (PROVIDER !== 'groq') {
    const fn = PROVIDER === 'gemini' ? callGemini : callAnthropic;
    for (let a = 0; ; a++) { try { return await fn(messages, MODEL); } catch (e) { if (e.status === 429 && a < 2) { await sleep(8000 * (a + 1)); continue; } throw e; } }
  }
  const prompt = estTokens(messages);
  let maxTokens = Math.max(600, Math.min(MAX_TOKENS, rl.limit - prompt - 150));   // request must fit the per-minute limit on its own
  let budget = 45000;                                                             // stay well inside Render's request timeout
  for (let attempt = 0; attempt < 6; attempt++) {
    const need = prompt + maxTokens;
    if (rl.remaining !== null && rl.remaining < need && rl.resetAt > Date.now()) {  // wait for the window to refill
      const w = Math.min(rl.resetAt - Date.now() + 250, budget); if (w > 0) { await sleep(w); budget -= w; rl.remaining = null; }
    }
    try { return await callGroq(messages, MODEL, maxTokens); }
    catch (e) {
      if (e.tooLarge) { maxTokens = Math.max(400, Math.floor((rl.limit - prompt - 300) * 0.9)); continue; }
      if (e.status === 429) {
        const w = Math.min(Math.max((e.retryAfter || 0) * 1000, rl.resetAt - Date.now(), 3000), budget);
        if (w <= 0 || budget <= 0) { e.message = 'The free AI tier is busy for a few seconds. Please try again.'; throw e; }
        await sleep(w); budget -= w; continue;
      }
      throw e;
    }
  }
  const e = new Error('The free AI tier is busy. Please try again in a minute.'); e.status = 429; throw e;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-cache' });
      return fs.createReadStream(PAGE).pipe(res);
    }
    if (req.method === 'GET' && url.pathname === '/api/health') {
      return send(res, 200, { ok: !!KEY, provider: PROVIDER || null, model: KEY ? MODEL : null, available: groqModels, tpm: PROVIDER === 'groq' ? rl.limit : null });
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

server.listen(PORT, async () => { if (PROVIDER === 'groq') await pickGroqModel(); console.log(`AvecAgro listening on ${PORT} (provider ${PROVIDER || 'none'}, model ${MODEL || '-'})`); });
