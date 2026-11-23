# Microsoft Form – answers to paste (team leader submits once)

Every number below matches the Milestone 2 PDF.

| Q | Question | Answer |
|---|---|---|
| 1 | Team ID | PE-B49-23 |
| 2 | Team name | AvecAgro |
| 3 | Project title | AvecAgro – AI-Powered Precision Agriculture |
| 4 | Team leader name | Arpit Kumar |
| 5 | Leader enrollment no. | S24CSEU1793 |
| 6 | Group (batch) | B49 - B64 |
| 7 | Enrollment numbers (one per line) | S24CSEU1793<br>S24CSEU0499<br>S24CSEU0831<br>S24CSEU0500<br>S24CSEU0070 |
| 8 | Project type (max 2) | Pick the options closest to: "Custom web app" and "RAG / document grounding" |
| 9 | Main AI tool and model | Claude (Anthropic) for development and all tests; public deployment runs the same prompts on open-weight gpt-oss-120b via Groq (Render web app) |
| 10 | Number of prompts | 4 |
| 11 | Prototype link | https://avecagro.onrender.com (no login needed) |
| 12 | Repository / folder link | https://github.com/arpit-k16/AvecAgro-M2 |
| 13 | Reel link | https://drive.google.com/file/d/14cfhjFbPGN_8EvaeNEtN4WtOqo4kPj-e/view?usp=sharing |
| 14 | Reel length (seconds) | 127 |
| 15 | Supporting document type | Business Model Canvas (BMC) |
| 16 | Upload supporting document | docs/AvecAgro_BMC.pdf |
| 17 | Number of test inputs | 14 |
| 18 | Number of prompt versions | 3 |
| 19 | Prototype status | Some modules working (8 modules working; live weather and IoT soil-sensor feeds now work, drone imagery analysis is not built. Choose "All modules working" only if your form lists weather/IoT as the module) |
| 20 | Names of working modules | Intake & Validation (P1)<br>Knowledge retrieval (RAG)<br>Crop Recommendation (P2)<br>Farm Plan & Calendar (P3)<br>Pest Alert & Advisor (P4)<br>Multilingual output<br>Web app UI<br>Live weather forecast (Open-Meteo)<br>IoT soil-sensor feed (/api/sensor) |
| 21 | Upload Milestone 2 PDF | docs/M2_PE-B49-23_AvecAgro.pdf |
| 22 | Main task of each member | S24CSEU1793 – Arpit Kumar – Team lead; P2 crop prompt v1–v3, Prompt lab (Claude + gpt-oss), report and form<br>S24CSEU0499 – Shikhar Bhandari – P1 intake & validation prompt and routing, Render deployment and rate-limit fixes, edge/invalid tests 7–14<br>S24CSEU0831 – Devang Kumar Bharti – web app, pipeline and retriever, JSON output format and language rule, ran all tests<br>S24CSEU0500 – Shikhar Shukla – knowledge base (RAG), P3 farm-plan prompt, live weather and IoT sensor module, RAG and I/O diagrams<br>S24CSEU0070 – Lakshay Bansal – P4 pest prompt, normal tests 1–6, task diagram, reel, screenshots, BMC |
| 23 | Anything the evaluator should know | No login needed. The free Render instance may take up to 1 minute to wake on first visit. Advisor tab: click an example and "Get advice". Measured results were produced with Claude; the public site runs the same prompts on gpt-oss-120b (Groq). |
| 24 | Confirmation | Tick only after all 5 members agree to the Section 7 table |

## Checklist before submitting (about 10 minutes)

1. **Prototype**: done – https://avecagro.onrender.com (open it once in incognito to wake it up before submitting).
2. **Repository**: done – https://github.com/arpit-k16/AvecAgro-M2 (public).
3. **Upload the reel**: `docs/reel/AvecAgro_M2_Reel.mp4` to Drive ("Anyone with the link") or YouTube (unlisted).
4. **Put the two links in the PDF**: send them to Claude to regenerate the PDF, or edit `docs/links.json` and run `python docs/build_report.py`.
5. Test every link in incognito, then submit the form once.
