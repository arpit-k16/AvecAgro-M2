"""Builds docs/M2_PE-B49-23_AvecAgro.pdf from the repo files (prompts, tests, results).
Links are read from docs/links.json so the PDF can be regenerated once repo/reel links exist."""
import json, re, html, pathlib, subprocess, base64

R = pathlib.Path(__file__).resolve().parent.parent
D = R / "docs"
links = json.loads((D / "links.json").read_text())
esc = html.escape


def img(path, width="100%"):
    p = R / path
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f'<img src="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}" style="width:{width}">'


def prompt(path):
    t = (R / path).read_text(encoding="utf-8")
    return dict(re.findall(r"=== (\w+) ===\n(.*?)(?=\n=== \w+ ===\n|\Z)", t, re.S))


def sample(section):
    t = (R / "test-data/sample_runs.md").read_text(encoding="utf-8")
    m = re.search(r"## " + re.escape(section) + r".*?\n(.*?)(?=\n## |\Z)", t, re.S)
    return m.group(1).strip()


def md_blocks(s):
    out = []
    for part in re.split(r"(```(?:json)?\n.*?```)", s, flags=re.S):
        if part.startswith("```"):
            body = re.sub(r"^```(?:json)?\n|```$", "", part)
            out.append(f"<pre>{esc(body.strip())}</pre>")
        elif part.strip():
            out.append("<p>" + esc(part.strip()).replace("\n", "<br>") + "</p>")
    return "".join(out)


team = [("Arpit Kumar (Leader)", "S24CSEU1793"), ("Shikhar Bhandari", "S24CSEU0499"), ("Devang Kumar Bharti", "S24CSEU0831"),
        ("Shikhar Shukla", "S24CSEU0500"), ("Lakshay Bansal", "S24CSEU0070")]
tests = json.loads((R / "test-data/test_results.json").read_text(encoding="utf-8"))

css = """
@page{size:A4;margin:16mm 15mm 16mm 15mm}
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:10pt;line-height:1.42;color:#1d2a1a}
h1{font-size:17pt;color:#2f6b2f;margin:0 0 8px;border-bottom:2px solid #2f6b2f;padding-bottom:4px;page-break-before:always}
h2{font-size:12.5pt;color:#2f6b2f;margin:16px 0 6px}
h3{font-size:11pt;margin:12px 0 4px}
table{border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:8.6pt}
th,td{border:1px solid #b9b6a4;padding:4px 5px;vertical-align:top;text-align:left}
th{background:#e7eedf}
pre{font-family:'DejaVu Sans Mono',monospace;font-size:7.4pt;line-height:1.3;background:#f5f4ee;border:1px solid #ddd9c8;padding:6px 8px;white-space:pre-wrap;word-break:break-word;margin:4px 0 8px}
.cover{text-align:center;padding-top:30mm}
.cover h1{border:0;font-size:26pt;page-break-before:avoid}
.kv td:first-child{width:32%;font-weight:bold;background:#f2f6ee}
.sheet{border:1.5px solid #7a8a6a;border-radius:6px;padding:8px 10px;margin:10px 0;page-break-inside:auto}
.sheet table td:first-child{width:24%;font-weight:bold;background:#f2f6ee}
.cap{font-size:8.6pt;color:#4a5a40;text-align:center;margin:2px 0 12px}
.pass{color:#2f6b2f;font-weight:bold}.fail{color:#a63a2b;font-weight:bold}
.small{font-size:8.6pt;color:#555}
figure{margin:6px 0;page-break-inside:avoid}
"""

# ---------- Section 1: cover ----------
h = f"""<div class="cover"><div style="font-size:11pt;color:#555">SCSE4041 Mini Project — Milestone 2</div>
<h1>AvecAgro – AI-Powered Precision Agriculture</h1>
<div style="font-size:11pt;margin-bottom:18px">Prompt-engineered AI farming assistant: crop recommendations, adaptive task calendars and pest-management guidance</div></div>
<h2>1. Cover page</h2>
<table class="kv">
<tr><td>Team ID</td><td>PE-B49-23</td></tr>
<tr><td>Team name</td><td>AvecAgro</td></tr>
<tr><td>Project title</td><td>AvecAgro – AI-Powered Precision Agriculture</td></tr>
<tr><td>Batch</td><td>B49 - B64</td></tr>
<tr><td>Faculty</td><td>Ankit Vijay Bansal</td></tr>
<tr><td>Team members</td><td>{'<br>'.join(f'{esc(n)} — {e}' for n, e in team)}</td></tr>
<tr><td>Prototype link</td><td>{esc(links['prototype'])}</td></tr>
<tr><td>Repository / folder link</td><td>{esc(links['repository'])}</td></tr>
<tr><td>Reel link</td><td>{esc(links['reel'])}</td></tr>
<tr><td>Main AI tool and model</td><td>Claude (Anthropic), called from our web app through the Claude artifact runtime (sample API, model tier "default")</td></tr>
<tr><td>Submission date</td><td>22 November 2026</td></tr>
</table>
<p class="small">Prototype access: open the link while signed in to Claude (free account) and click “Allow use of Claude”. The Test runner and Prompt lab tabs re-run every test in this report.</p>
"""

# ---------- Section 2 ----------
h += """<h1>2. Prompt and solution design</h1>
<h2>2(a) Design summary</h2>
<p><b>Problem and users.</b> Small and marginal farmers in India (86% of holdings, Agriculture Census 2015–16) make crop, irrigation and pest decisions without timely, personalised advice; soil tests are often missing and sensor data, when available, can be wrong. AvecAgro gives them safe, specific guidance in their own language.</p>
<p><b>Input and output.</b> Input: one free-text message (English, Hindi or Hinglish) with location, season, previous/standing crop, budget, water source, soil report, weather forecast and sensor/drone/rover observations. Output: (1) a validated farm profile with data warnings and missing-information questions, (2) up to 3 crop recommendations with knowledge-base citations, soil status (measured/estimated/unknown) and confidence, (3) a 6–8 window task calendar with irrigation and nutrient notes that react to rain forecasts and soil-moisture readings, (4) a pest alert (none/watch/warning/urgent) with IPM steps, drone-spray suitability and expert contact.</p>
<p><b>How many prompts and why.</b> Four prompts plus a retrieval step. Milestone 1 used one prompt for everything; its answers were long free text, mixed facts with guesses and could not be checked. Splitting the job lets each prompt have one narrow role and a strict JSON schema: <b>P1 Intake & Validation</b> (structure and sanity-check the input; stop invalid or out-of-region requests before any advice), <b>P2 Crop Recommendation</b>, <b>P3 Farm Plan & Calendar</b>, <b>P4 Pest Alert & Advisor</b>. Code routes between them: a new-crop plan runs P2→P3→P4 (watch-list); a standing crop with a problem runs P4 only; invalid input or a farm outside India stops after P1.</p>
<p><b>Tool and model.</b> Claude (Anthropic) through the Claude artifact runtime. It handles Hindi/Hinglish well, follows long rule lists and JSON schemas reliably (7/7 strict JSON in our lab), and lets us publish a working web app that evaluators open with a normal login and no API key in the code. Retrieval is our own JavaScript over a curated 27-passage knowledge base, so every crop or pest fact can be traced to a passage id.</p>
<p><b>What changed since Milestone 1.</b> (1) One baseline prompt → 4-prompt pipeline with routing; (2) added RAG with citation checking; (3) added input validation (invalid/off-topic input, non-India farms, impossible or contradictory sensor values); (4) JSON outputs rendered as farmer-friendly cards in a published web app; (5) Milestone 1 planned an open-source LLM — for the prototype we switched to Claude because it was available with no hosting cost and passed our JSON and language tests; an open-source model remains an option for offline use; (6) 14 test cases and a v1→v3 prompt lab with measured results.</p>
<h2>2(b) Diagrams</h2>
"""
for f, cap in [("1_prompt_workflow.png", "Figure 1. Prompt workflow"), ("2_task_decomposition.png", "Figure 2. Task decomposition"),
               ("3_input_output_flow.png", "Figure 3. Input–output flow"), ("4_system_architecture.png", "Figure 4. System architecture"),
               ("5_rag_pipeline.png", "Figure 5. RAG pipeline")]:
    w = "78%" if f.startswith("1_") else "100%"
    h += f'<figure style="text-align:center">{img("docs/diagrams/" + f, w)}<div class="cap">{cap} (drawn by the team for this prototype)</div></figure>'

h += "<h2>2(c) Prompt sheets (one per final prompt)</h2>"
sheets = [
    ("P1", "Intake & Validation", "prompts/final/P1_intake_validation.txt", "Step 1 of 4 – runs first on every request",
     "Turn the farmer's free text into a validated profile JSON; reject invalid/off-topic input and flag impossible or contradictory data.",
     [("{today}", "today's date (ISO), used only to judge season / date conflicts"), ("{farmer_input}", "the farmer's raw message, any language")],
     "1 worked example (Hinglish input → profile JSON)", "Single JSON object: validity, language, location, season, crops, budget, irrigation, soil{…, source}, sensor_readings, observed_problems, farmer_goal, data_warnings, missing_fields, clarifying_questions",
     "P1 – Test 7 (Hinglish)"),
    ("P2", "Crop Recommendation (final = v3)", "prompts/final/P2_crop_recommendation.txt", "Step 2 of 4 – after P1 and retrieval (new-crop route only)",
     "Recommend up to 3 crops grounded only in retrieved passages, with citations, soil status and confidence.",
     [("{profile_json}", "P1 output (JSON string)"), ("{retrieved_chunks}", "top-6 knowledge-base passages, each prefixed [KB-id]"), ("{output_language}", "farmer's language from P1 (en / hi / hinglish) or the user's override")],
     "1 worked example (Rajasthan, kharif, rainfed → 2 crops)", "Single JSON object: recommendations[{crop, suitability, why[], kb_refs[], estimated_input_cost, risks[]}], soil_assessment, not_recommended[], confidence, needs_expert_verification, verification_note, farmer_summary",
     "P2 – Test 1"),
    ("P3", "Farm Plan & Task Calendar", "prompts/final/P3_farm_plan_calendar.txt", "Step 3 of 4 – for the top recommended (or standing) crop",
     "Produce a week-by-week calendar with irrigation and nutrient notes that react to rain forecasts and soil-moisture readings.",
     [("{crop}", "top crop from P2, or the standing crop"), ("{profile_json}", "P1 output"), ("{weather}", "weather note from P1 or 'not given'"), ("{retrieved_chunks}", "top-5 passages, KB-22 (irrigation/weather) always included"), ("{output_language}", "as in P2")],
     "0 (zero-shot; schema and rules only)", "Single JSON object: crop, plan[6–8 × {window, tasks[], irrigation, nutrients}], weather_adjustments[], water_saving_tips[], budget_tips[], kb_refs[], farmer_summary",
     "P3 – Test 1"),
    ("P4", "Pest Alert & Management Advisor", "prompts/final/P4_pest_alert_advisor.txt", "Step 4 of 4 – on observed problems, or a season watch-list",
     "Turn field observations into an alert level, likely pests with evidence and safe IPM steps; never give pesticide doses or yield guarantees.",
     [("{crop}", "standing crop or top recommended crop"), ("{observations}", "observed_problems from P1 + valid sensor readings, or 'No problems reported…'"), ("{profile_json}", "P1 output"), ("{retrieved_chunks}", "top-5 passages, KB-23 (IPM) always included"), ("{output_language}", "as in P2")],
     "0 (zero-shot; schema and rules only)", "Single JSON object: crop, alert_level, likely_issues[{name, confidence, evidence[], kb_refs[]}], immediate_actions[], ipm_steps[], do_not[], when_to_contact_expert, drone_spray_suitable, drone_note, watch_list[], farmer_summary",
     "P4 – Test 13"),
]
for pid, name, path, step, purpose, vars_, nex, fmt, samp in sheets:
    p = prompt(path)
    vrows = "".join(f"<tr><td>{esc(v)}</td><td>{esc(d)}</td></tr>" for v, d in vars_)
    h += f"""<div class="sheet"><h3>Prompt ID {pid} — {esc(name)}</h3>
<table><tr><td>Step in workflow</td><td>{esc(step)}</td></tr>
<tr><td>Purpose</td><td>{esc(purpose)}</td></tr>
<tr><td>Tool and model</td><td>Claude via Claude artifact runtime (sample API), model tier "default"</td></tr>
<tr><td>Settings</td><td>Default (temperature and max tokens are not exposed by the runtime; cache off). The system prompt is sent as the first user turn, followed by an assistant acknowledgement, because the runtime has no separate system field.</td></tr>
<tr><td>Number of examples</td><td>{esc(nex)}</td></tr>
<tr><td>Output format</td><td>{esc(fmt)}</td></tr></table>
<b>Full system prompt</b><pre>{esc(p['SYSTEM'].strip())}</pre>
<b>User prompt template</b><pre>{esc(p['USER'].strip())}</pre>
<b>Variables</b><table><tr><th>Variable</th><th>What it holds</th></tr>{vrows}</table>
<b>Sample run (real input and actual output)</b>{md_blocks(sample(samp))}</div>"""

# ---------- Section 3 ----------
h += """<h1>3. Implementation</h1>
<h2>What is built</h2>
<p>A single-page web app (published as a Claude artifact) containing: the 4-prompt pipeline with routing and JSON validation; a retriever over 27 curated agronomy passages (tag + keyword scoring, forced inclusion of rule passages); farmer-facing result cards (profile, crop cards with sources, calendar table, pest alert); a <b>Test runner</b> that runs all 14 test inputs and logs full traces to the app database; a <b>Prompt lab</b> that runs P2 v1/v2/v3 on the same inputs and computes metrics; and a <b>Prompts & knowledge base</b> tab showing every final prompt and passage. Prompts live as text files in the repository and <code>code/build.py</code> embeds them into the page, so the report, repository and app use the same prompt text.</p>
<h2>Module status</h2>
<table><tr><th>Module</th><th>What it does</th><th>Status</th><th>Notes</th></tr>
<tr><td>Intake & Validation (P1)</td><td>Free text → profile JSON; invalid / non-India / impossible-value checks; clarifying questions</td><td>Working</td><td>14/14 runs valid JSON; caught 'idk', off-topic, Nebraska, pH 15, 90 °C, 85% vs cracked soil</td></tr>
<tr><td>Knowledge retrieval (RAG)</td><td>Scores 27 passages by state, season, crop, keywords; returns top-k with ids</td><td>Working</td><td>Missed the lentil passage in test 7 (see limitations)</td></tr>
<tr><td>Crop Recommendation (P2)</td><td>Up to 3 grounded crops with citations, soil status, confidence</td><td>Working</td><td>v3: 7/7 valid JSON and valid citations in lab</td></tr>
<tr><td>Farm Plan & Calendar (P3)</td><td>6–8 window calendar; rain and sensor-aware irrigation; Soil-Health-Card-based nutrients</td><td>Working</td><td>Postponed irrigation in all rain-forecast tests (1, 8)</td></tr>
<tr><td>Pest Alert & Advisor (P4)</td><td>Alert level, likely pests, IPM order, no doses, drone suitability, expert contact</td><td>Working</td><td>Identified pink bollworm, fall armyworm, aphid, brown planthopper; refused dose + yield guarantee</td></tr>
<tr><td>Multilingual output</td><td>Answers in farmer's language (English / Hindi / Hinglish) or chosen language</td><td>Working</td><td>Hinglish verified in test 7; Hindi (Devanagari) selectable</td></tr>
<tr><td>Web app UI</td><td>Advisor, Test runner, Prompt lab, Prompts & KB tabs</td><td>Working</td><td>Needs Claude sign-in to run the AI</td></tr>
<tr><td>Live IoT / weather / drone data feeds</td><td>Pull sensor, IMD forecast and drone imagery automatically</td><td>Not started</td><td>Currently typed in by the farmer as text; planned for Milestone 3</td></tr>
</table>
<h2>Prompt iteration log (P2 Crop Recommendation)</h2>
<p class="small">Measured in the Prompt lab on 22 Nov 2026: each version ran on tests 1, 2, 4, 7 and 14, plus 2 repeats of test 1 (7 runs per version). v2 and v3 received the same P1 profile and the same retrieved passages. Raw outputs: <code>test-data/prompt_lab_results.json</code>, <code>test-data/sample_runs.md</code>.</p>
<table><tr><th style="width:7%">Version</th><th style="width:33%">What changed</th><th style="width:22%">Why it was changed</th><th>Result after the change</th></tr>
<tr><td>v1</td><td>First prompt (Milestone 1 baseline): one free-text instruction to recommend crops and give irrigation, nutrient and pest advice; raw farmer text appended.</td><td>Starting point</td><td>Free text, 0/7 valid JSON, 0/7 runs cited any source. Avg 4,260 characters, 16.7 s. In 1 of 6 runs without soil data it invented a fertiliser dose (test 14: “120:60:40 kg N:P2O5:K2O per hectare”) and variety names found in no source. First crop named varied across 3 runs of test 1 (soybean / soybean / wheat).</td></tr>
<tr><td>v2</td><td>Separate system role; structured P1 profile instead of raw text; retrieved KB passages as the only fact source; fixed JSON schema; scope cut to crop choice only (irrigation/pest moved to P3/P4).</td><td>v1 output could not be parsed by the app, mixed facts with guesses and could not be checked.</td><td>7/7 strict valid JSON; 6/6 no invented soil numbers; same top crop (chickpea) in 3/3 runs of test 1. But 1/7 runs cited a passage it was not given (test 4 cited KB-16), exactly 3 crops in 6/7, and answers got longer (avg 4,721 characters, farmer summaries up to 6 sentences); 12.6 s.</td></tr>
<tr><td>v3 (final)</td><td>Added 1 worked example; rule “cite only ids that appear in the passages”; ban on numeric soil values not in the profile; concrete budget/water rules; 2–3 sentence farmer summary in the farmer's language; output must start with “{”.</td><td>v2 still produced an invalid citation and long, hard-to-read summaries.</td><td>7/7 strict valid JSON; 7/7 valid citations; 6/6 no invented soil numbers; chickpea in 3/3 repeats of test 1; Hinglish answer for test 7. Avg length 2,705 characters (−43% vs v2) and 7.9 s per call (−37%). Exactly 3 crops in 6/7: test 7 returns 2 because only 2 retrieved passages supported rabi crops (intended by rule 5).</td></tr>
</table>
"""
for v in ["v1/P2_crop_recommendation_v1.txt", "v2/P2_crop_recommendation_v2.txt", "v3/P2_crop_recommendation_v3.txt"]:
    p = prompt("prompts/" + v)
    h += f"<h3>Full text — {esc(p['META'].strip().splitlines()[0].replace('Prompt: ', ''))}</h3><b>System prompt</b><pre>{esc(p['SYSTEM'].strip())}</pre><b>User prompt template</b><pre>{esc(p['USER'].strip())}</pre>"
h += f'<figure>{img("docs/screenshots/prompt_lab_summary.jpg", "80%")}<div class="cap">Prompt lab summary computed by the app after the v1/v2/v3 runs (22 Nov 2026).</div></figure>'

# ---------- Section 4 ----------
h += """<h1>4. Demonstration and testing</h1>
<h2>Test table</h2>
<p class="small">14 inputs: 6 Normal, 6 Edge, 2 Invalid. All run through the full pipeline in the Test runner on 22 Nov 2026. Inputs: <code>test-data/test_inputs.json</code>; actual outputs: <code>test-data/test_results.json</code>.</p>
<table><tr><th>No.</th><th style="width:20%">Input (short)</th><th>Type</th><th style="width:22%">Expected output</th><th>Actual output (short)</th><th>Pass / Fail</th></tr>"""
for t in tests:
    cls = "pass" if t["result"] == "Pass" else "fail"
    note = f"<br><i>Note: {esc(t['notes'])}</i>" if t["notes"] else ""
    short = next(x["short"] for x in json.loads((R / "test-data/test_inputs.json").read_text()) if x["no"] == t["no"])
    h += f"<tr><td>{t['no']}</td><td>{esc(short)}</td><td>{t['type']}</td><td>{esc(t['expected'])}</td><td>{esc(t['actual'])}{note}</td><td class='{cls}'>{t['result']}</td></tr>"
h += "</table><p><b>Result: 13 Pass, 1 Fail.</b></p><h2>Screenshots of real runs</h2>"
for f, cap in [("test14_profile_warnings.jpg", "Test 14 (Edge) — P1 flags pH 15 and 90 °C as impossible, sets them to null and asks for a soil test."),
               ("test13_pest_alert.jpg", "Test 13 (Edge) — P4 identifies likely brown planthopper and declines the chlorpyrifos dose and the 30 q/acre guarantee (re-run in the Advisor tab)."),
               ("test07_hinglish_crops.jpg", "Test 7 (Edge) — Hinglish input answered in Hinglish; only 2 crops because the lentil passage was not retrieved (the failed test).")]:
    h += f'<figure>{img("docs/screenshots/" + f, "86%")}<div class="cap">{cap}</div></figure>'
h += """<h2>Known limitations and what we will try next</h2>
<table><tr><th>Limitation</th><th>What we will try next</th></tr>
<tr><td>Keyword retrieval can miss a relevant passage (test 7 lost the lentil passage because UP-specific paddy/BPH passages scored higher; test 14 missed the wheat yellow-rust passage because MP is not in its state list).</td><td>Add crop-rotation tags and embedding-based retrieval, retrieve per candidate crop, and grow the knowledge base by state with expert review.</td></tr>
<tr><td>When key facts are missing (test 9: season unknown) the pipeline still produces a full generic calendar.</td><td>Make P1 confidence gate P3: if season or crop status is unknown, show the clarifying questions first and plan only after the farmer answers.</td></tr>
<tr><td>P1 sometimes puts context into the wrong field (test 1: “borewell is shared” stored as an observed problem, so P4 discussed it).</td><td>Add an explicit “constraints” field and a second example to P1.</td></tr>
<tr><td>Sensor, weather and drone data are typed in by the farmer; nothing is read live, and the knowledge base (27 passages) is written by the team from public guidance, not yet validated by an agronomist.</td><td>Connect a real soil-moisture sensor feed and IMD forecast API in Milestone 3; get KVK / faculty review of every passage.</td></tr>
</table>
"""

# ---------- Section 5 ----------
h += f"""<h1>5. Repository</h1>
<p>Repository / folder link: <b>{esc(links['repository'])}</b></p>
<div style="display:flex;gap:12px;align-items:flex-start"><div style="flex:1">{img("docs/screenshots/github_repo.jpg", "100%")}<div class="cap">The public GitHub repository (22 Nov 2026).</div></div><div style="flex:1.2">{img("docs/screenshots/repo_tree.png", "100%")}<div class="cap">Folder structure inside the repository.</div></div></div>
<h2>What changed since Milestone 1</h2>
<ul><li>Added <code>prompts/v1–v3</code> (P2 iterations) and <code>prompts/final</code> (P1–P4), one file per prompt.</li>
<li>Added <code>code/</code>: web app source, 27-passage knowledge base for retrieval, and the build script that embeds the prompts.</li>
<li>Added <code>test-data/</code>: 14 test inputs, actual outputs, prompt-lab metrics and sample runs.</li>
<li>Added <code>docs/</code>: 5 diagrams, screenshots, this report, the Business Model Canvas and the reel script; dated changes in <code>CHANGELOG.md</code>. No API keys are stored anywhere.</li></ul>
"""

# ---------- Section 6 ----------
h += f"""<h1>6. Supporting document — Business Model Canvas</h1>
<p class="small">Same document uploaded at Q16 as <b>AvecAgro_BMC.pdf</b>.</p>
{img("docs/bmc_page.png", "100%")}
"""

# ---------- Section 7 ----------
h += """<h1>7. Team contribution</h1>
<p class="small">Total = 100%. All members have reviewed and agreed to this table.</p>
<table style="table-layout:fixed;word-break:break-word"><tr><th style="width:13%">Member name</th><th style="width:16%">Enrollment no.</th><th style="width:12%">Role</th><th style="width:25%">Tasks done in Milestone 2</th><th style="width:25%">Evidence</th><th style="width:9%;font-size:7.5pt">Contribution (%)</th></tr>
<tr><td>Arpit Kumar (Leader)</td><td>S24CSEU1793</td><td>Prompt design lead</td><td>Wrote P2 v1→v2→v3, designed and ran the Prompt lab, compiled this report and the form</td><td>prompts/v1–v3/P2_*.txt, prompts/final/P2_crop_recommendation.txt, test-data/prompt_lab_results.json, Section 3 log</td><td>20</td></tr>
<tr><td>Shikhar Bhandari</td><td>S24CSEU0499</td><td>Input validation &amp; testing</td><td>Wrote P1 Intake &amp; Validation; designed edge and invalid tests 7–14 and judged Pass/Fail</td><td>prompts/final/P1_intake_validation.txt, test-data/test_inputs.json (tests 7–14), Section 4 table</td><td>20</td></tr>
<tr><td>Devang Kumar Bharti</td><td>S24CSEU0831</td><td>Developer</td><td>Built the web app, pipeline routing, JSON parsing, retriever, Test runner; published the prototype</td><td>code/app_template.html, code/build.py, prototype link, Figure 4</td><td>20</td></tr>
<tr><td>Shikhar Shukla</td><td>S24CSEU0500</td><td>Knowledge base &amp; planning</td><td>Curated the 27 knowledge-base passages; wrote P3 Farm Plan &amp; Calendar; drew the RAG and I/O diagrams</td><td>code/knowledge_base.json, prompts/final/P3_farm_plan_calendar.txt, Figures 3 and 5</td><td>20</td></tr>
<tr><td>Lakshay Bansal</td><td>S24CSEU0070</td><td>Pest module, demo &amp; business</td><td>Wrote P4 Pest Alert; designed normal tests 1–6; took screenshots; made the reel and the Business Model Canvas</td><td>prompts/final/P4_pest_alert_advisor.txt, test-data/test_inputs.json (tests 1–6), docs/screenshots/, docs/reel/, AvecAgro_BMC.pdf</td><td>20</td></tr>
</table>
"""

doc = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{h}</body></html>"
(D / "report.html").write_text(doc, encoding="utf-8")
out = D / "M2_PE-B49-23_AvecAgro.pdf"
subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out}", str(D / "report.html")], capture_output=True, timeout=180)
print("wrote", out, out.stat().st_size // 1024, "KB")
