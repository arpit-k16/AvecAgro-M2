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
| 9 | Main AI tool and model | Claude (Anthropic) in a custom web app via the Claude artifact runtime |
| 10 | Number of prompts | 4 |
| 11 | Prototype link | https://claude.ai/artifact/SS1SXmKDuY4BjQYXdUaxXp (must be shared publicly first – see checklist) |
| 12 | Repository / folder link | your GitHub repo or Drive folder link |
| 13 | Reel link | your Drive / unlisted YouTube link |
| 14 | Reel length (seconds) | 127 |
| 15 | Supporting document type | Business Model Canvas (BMC) |
| 16 | Upload supporting document | docs/AvecAgro_BMC.pdf |
| 17 | Number of test inputs | 14 |
| 18 | Number of prompt versions | 3 |
| 19 | Prototype status | Some modules working (7 of 8 modules working; "Live IoT / weather / drone data feeds" is Not started) |
| 20 | Names of working modules | Intake & Validation (P1)<br>Knowledge retrieval (RAG)<br>Crop Recommendation (P2)<br>Farm Plan & Calendar (P3)<br>Pest Alert & Advisor (P4)<br>Multilingual output<br>Web app UI |
| 21 | Upload Milestone 2 PDF | docs/M2_PE-B49-23_AvecAgro.pdf |
| 22 | Main task of each member | S24CSEU1793 – Arpit Kumar – P2 prompt v1–v3 iteration, prompt lab, M2 report<br>S24CSEU0499 – Shikhar Bhandari – P1 intake & validation prompt, edge/invalid tests 7–14<br>S24CSEU0831 – Devang Kumar Bharti – web app, pipeline & retriever code, prototype publishing<br>S24CSEU0500 – Shikhar Shukla – knowledge base (RAG), P3 farm-plan prompt, RAG & I/O diagrams<br>S24CSEU0070 – Lakshay Bansal – P4 pest prompt, normal tests 1–6, screenshots, reel, BMC |
| 23 | Anything the evaluator should know | Open the prototype while signed in to Claude (free account) and click "Allow use of Claude". Advisor tab: click an example and "Get advice" (30–60 s). Test runner re-runs all 14 tests; Prompt lab re-runs P2 v1/v2/v3. |
| 24 | Confirmation | Tick only after all 5 members agree to the Section 7 table |

## Checklist before submitting (about 10 minutes)

1. **Share the prototype**: open the artifact link → Share → make it viewable by anyone with the link. Test it in an incognito window (it should open after a Claude sign-in, with no access request).
2. **Upload the repository**: upload this whole `AvecAgro-M2` folder to a new public GitHub repo (or a Google Drive folder set to "Anyone with the link can view").
3. **Upload the reel**: `docs/reel/AvecAgro_M2_Reel.mp4` to Drive ("Anyone with the link") or YouTube (unlisted).
4. **Put the two links in the PDF**: send them to Claude to regenerate the PDF, or edit `docs/links.json` and run `python docs/build_report.py`.
5. Test every link in incognito, then submit the form once.
