# AvecAgro – AI-Powered Precision Agriculture

**SCSE4041 Mini Project · Milestone 2 · Team PE-B49-23 (AvecAgro) · Batch B49-B64 · Faculty: Ankit Vijay Bansal**

AvecAgro is an AI farming assistant for small and marginal farmers in India. A farmer types their situation (in English, Hindi or Hinglish): location, season, previous crop, budget, water source, soil report, weather forecast and any sensor / drone / rover observations. AvecAgro returns:

1. a validated farm profile, with warnings for impossible or contradictory sensor data,
2. up to 3 crop recommendations grounded in a curated knowledge base (with source ids),
3. a week-by-week task calendar with irrigation and nutrient notes that react to rain forecasts and soil-moisture readings,
4. a pest / disease alert with integrated pest management (IPM) steps, drone-spray suitability and when to call an expert.

## Prototype

**Live app:** https://claude.ai/artifact/SS1SXmKDuY4BjQYXdUaxXp
Open it while signed in to Claude (a free account works) and click **Allow use of Claude** when asked. Tabs:

- **Advisor** – type farm details or click an example, then *Get advice*.
- **Test runner** – runs the 14 saved test inputs through the full pipeline.
- **Prompt lab** – runs P2 versions v1, v2 and v3 on the same inputs and computes metrics.
- **Prompts & knowledge base** – shows the final prompts and all 27 knowledge-base passages.

## How it works

| Step | Prompt / component | Output |
|---|---|---|
| 1 | P1 Intake & Validation | structured profile JSON, validity, language, data warnings, missing fields |
| – | Retriever (JavaScript, tag + keyword scoring) | top-k passages from `code/knowledge_base.json` |
| 2 | P2 Crop Recommendation | 3 crops with KB citations, soil status, confidence |
| 3 | P3 Farm Plan & Calendar | 6–8 calendar windows, weather adjustments, water/budget tips |
| 4 | P4 Pest Alert & Advisor | alert level, likely pests with evidence, IPM steps, drone note |

Routing: invalid input or a farm outside India stops after P1; a new-crop plan runs P2 → P3 → P4 (watch-list); a standing crop with a problem runs P4 only.

Model: Claude, called through the Claude artifact runtime (`sample` API, model tier "default"). No API key is stored anywhere in this repository.

## Repository layout

```
README.md
CHANGELOG.md
prompts/
  v1/  v2/  v3/      P2 crop-recommendation prompt versions (iteration log)
  final/             P1–P4 final prompts, one file each
code/
  app_template.html  web app source (UI, pipeline, retriever, test runner, prompt lab)
  knowledge_base.json  27 curated agronomy passages used for retrieval
  build.py           embeds prompts/KB/tests into code/index.html
  index.html         built single-file app (what is published)
test-data/
  test_inputs.json   14 test inputs with expected outputs
  test_results.json  actual outputs of every test run (full pipeline traces)
  prompt_lab_results.json  raw outputs + metrics for P2 v1/v2/v3
docs/
  M2_PE-B49-23_AvecAgro.pdf   Milestone 2 report
  AvecAgro_BMC.pdf            supporting document (Business Model Canvas)
  diagrams/                   workflow, decomposition, I/O, architecture, RAG diagrams
  screenshots/                screenshots of real runs
  reel/                       AvecAgro_M2_Reel.mp4 (127 s), reel_script.md, build script
  FORM_ANSWERS.md             answers for the submission form
```

To rebuild the app after editing a prompt: `python code/build.py`, then republish `code/index.html`.

## Team

| Member | Enrollment no. | Main task |
|---|---|---|
| Arpit Kumar (leader) | S24CSEU1793 | P2 prompt v1–v3 iteration, prompt lab, M2 report |
| Shikhar Bhandari | S24CSEU0499 | P1 intake & validation prompt, edge/invalid test cases |
| Devang Kumar Bharti | S24CSEU0831 | Web app, pipeline & retriever code, architecture diagram |
| Shikhar Shukla | S24CSEU0500 | Knowledge base (RAG), P3 farm-plan prompt, RAG diagram |
| Lakshay Bansal | S24CSEU0070 | P4 pest prompt, normal test cases & screenshots, reel, BMC |

*AvecAgro gives guidance, not guarantees. Knowledge-base passages are summarised from public agronomy guidance and must be validated by local experts (KVK / agriculture department).*
