# AvecAgro – Milestone 2 reel (127 seconds)

File: `docs/reel/AvecAgro_M2_Reel.mp4` (1280×720, captions burned in, silent audio track).
Built by `docs/reel/make_reel.py` from screenshots of real runs in the published app (22 Nov 2026) and the real v1/v3 outputs saved in `test-data/`.
Optional: a teammate can record a voice-over reading the captions below (Q14 length stays 127 s).

| Time | Part | On screen | Caption / voice-over |
|---|---|---|---|
| 0:00–0:10 | 1. Problem | Title card | 86% of Indian farm holdings are small or marginal. Weather, pests, unknown soil and costs make decisions hard. AvecAgro is an AI assistant for crops, farm plans and pest alerts. |
| 0:10–0:15 | 2. Prompt experiment | Card | Same farmer input, same model: Milestone 1 prompt vs final prompt. |
| 0:15–0:28 | | v1 prompt + real v1 output (test 14) | v1: free text; it invents a fertiliser dose (120:60:40 kg/ha) and variety names with no source. |
| 0:28–0:34 | | Prompt lab row | Prompt lab marks “Invented soil numbers: YES” for v1. |
| 0:34–0:47 | | v3 prompt + real v3 output (test 14) | v3: grounded in retrieved passages, cited, valid JSON; impossible pH 15 / 90 °C readings discarded. |
| 0:47–0:55 | | Prompt lab summary | v1→v3: valid JSON 0/7→7/7, valid citations 0/7→7/7, 43% shorter than v2. |
| 0:55–1:30 | 3. Working demo | Advisor tab, Hinglish input (test 7) | Farmer types in Hinglish → P1 profile → P2 crops with sources in Hinglish → soil unknown, asks for Soil Health Card → P3 calendar → P4 watch-list. |
| 1:30–1:46 | | Advisor tab, test 13 | Asks for an exact chlorpyrifos dose and a yield guarantee → router runs P4 only → likely brown planthopper, declines dose and guarantee. |
| 1:46–1:52 | | Test runner table | 14 tests: 13 pass, 1 fail (retrieval miss), reported honestly. |
| 1:52–2:07 | 4. Progress & next steps | Card | Done: 4 prompts + retrieval, web app, 14 tests, v1→v3 log. Next: bigger expert-checked knowledge base, live IoT/weather feeds, Hindi voice input, field trials. |
