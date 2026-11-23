# Changelog

## Milestone 1
- Problem statement, users, inputs/outputs and existing-solution gap (questionnaire).
- One baseline prompt (single free-text prompt asking for crops, irrigation, nutrients and pest control).

## 2026-11-22 — Milestone 2
- Split the single baseline prompt into a 4-step pipeline: P1 Intake & Validation, P2 Crop Recommendation, P3 Farm Plan & Calendar, P4 Pest Alert & Advisor (`prompts/final/`).
- Added retrieval (RAG): 27 curated knowledge-base passages (`code/knowledge_base.json`) and a tag + keyword retriever; P2–P4 must cite passage ids.
- P2 iterated v1 → v2 → v3 (`prompts/v1`, `v2`, `v3`): v2 added system role, structured profile, retrieved passages and JSON schema; v3 added a worked example, citation rule, ban on invented soil numbers, budget/water rules and language rule.
- Added input validation: invalid/off-topic input, farms outside India, impossible sensor values (pH > 14, soil temperature > 60 °C) and contradictory sensor data are flagged.
- Added routing (new crop plan / standing crop with problem / standing crop without problem).
- Built and published the web app (Advisor, Test runner, Prompt lab, Prompts & KB tabs) using Claude through the artifact runtime.
- Created 14 test inputs (6 normal, 6 edge, 2 invalid) and ran them; saved actual outputs in `test-data/`.
- Ran the prompt lab (v1/v2/v3 on 5 inputs + 2 consistency repeats); saved outputs and metrics.
- Changed tool choice from Milestone 1 plan (open-source LLM) to Claude for the prototype; open-source model kept as a later option.
- Added diagrams, Milestone 2 report, Business Model Canvas, reel script.

## 2026-11-22 (evening) — Interface redesign
- New look for the web app: Bricolage Grotesque headings with Hind body text (Latin + Devanagari), field-green and turmeric palette, plain-language hero ("Tell us about your field"), farmer-worded example cases.
- Pipeline progress shown as a furrow of seeds that sprout as each step finishes.
- Results renamed to Your farm / Crops to consider / Season plan / Pest watch; cost tags no longer use alarm colours; better mobile layout and keyboard focus; reduced-motion respected.
- No change to prompts, retrieval or pipeline logic.

## 2026-11-22 (night) — Render deployment
- Added `server/server.js` (Node, no dependencies): serves the app and proxies AI calls to the Anthropic Messages API using the `ANTHROPIC_API_KEY` environment variable; per-IP hourly limit.
- Added `render.yaml` and `package.json`.
- The page now uses the Claude artifact runtime when opened on claude.ai, and the server's `/api/sample` endpoint elsewhere. Prompts and pipeline unchanged.

## 2026-11-22 (23:00) — P1 fix after testing on gpt-oss-120b
- On the Render deployment (Groq, gpt-oss-120b) test 13 failed: P1 marked the farmer's input invalid because it asked for a pesticide dose. Added to P1 rule 6: farm input stays valid even if it asks for a dose or yield guarantee; later steps decline that part.

## 2026-11-23 — Render deployment: fix free-tier errors
- Fixed "Request too large ... tokens per minute (TPM): Limit 8000, Requested 9186": Groq counts max_tokens toward the per-minute limit; the server now sizes max_tokens so each request fits the limit.
- Fixed Prompt lab "Server error 502": AI calls are now queued one at a time and paced with Groq's x-ratelimit headers; waits are capped so Render never drops the request; the page retries automatically on 429/502/503.
- The server now lists the models the key can use at startup and picks the best one for the free tier (shown in the status pill and /api/health).
