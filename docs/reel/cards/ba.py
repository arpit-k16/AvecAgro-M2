import html, subprocess
def code_card(name, tag, color, title, left_title, left, right_title, right):
    h=f"""<html><body style="margin:0;width:1280px;height:720px;background:#f6f4ec;font-family:'DejaVu Sans';box-sizing:border-box;padding:30px 40px">
<div style="display:inline-block;background:{color};color:#fff;font-size:24px;font-weight:bold;padding:6px 16px;border-radius:8px">{tag}</div>
<span style="font-size:30px;font-weight:bold;margin-left:14px;color:#1f2a1c">{html.escape(title)}</span>
<div style="display:flex;gap:24px;margin-top:22px">
<div style="flex:1"><div style="font-size:20px;font-weight:bold;color:#444;margin-bottom:6px">{left_title}</div>
<pre style="font-family:'DejaVu Sans Mono';font-size:18px;line-height:1.35;background:#fff;border:2px solid #ccc;border-radius:8px;padding:12px;white-space:pre-wrap;height:520px;overflow:hidden;margin:0">{html.escape(left)}</pre></div>
<div style="flex:1"><div style="font-size:20px;font-weight:bold;color:#444;margin-bottom:6px">{right_title}</div>
<pre style="font-family:'DejaVu Sans Mono';font-size:18px;line-height:1.35;background:#fff;border:2px solid {color};border-radius:8px;padding:12px;white-space:pre-wrap;height:520px;overflow:hidden;margin:0">{html.escape(right)}</pre></div></div></body></html>"""
    open(name+'.html','w').write(h)
    subprocess.run(["google-chrome","--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1280,720",f"--screenshot={name}.png",name+".html"],capture_output=True,timeout=60)
code_card("03_before","BEFORE · v1","#a63a2b","Milestone 1 baseline prompt",
"Prompt v1 (one free-text instruction)",
"You are AVECAGRO, an AI farming assistant. Using the farmer's location, crop history, budget, available soil data, weather information, and sensor observations, provide practical, personalized agricultural guidance. Recommend suitable crops and explain the reasons. Suggest irrigation, nutrient management, and pest-control actions ... Never invent sensor readings or guarantee yield ...\n\n{farmer_input}\n\nTest 14 input:\nBhopal, MP. Rabi, wheat planned, canal.\nSensor: soil pH 15, soil temperature 90 C,\nsoil moisture 30%. Budget medium.",
"Actual v1 output (real run, excerpt)",
"Free text, 13.1 s, not parseable\n...\n**Nutrients (to be refined after a soil test)**\n- As a rough starting point, the commonly cited recommendation for irrigated timely-sown wheat is about 120:60:40 kg N:P2O5:K2O per hectare ...\n- Varieties commonly grown in Madhya Pradesh include sharbati types (e.g., MP 1202, HI 1544) and durum types (e.g., HI 8498, HI 8663) ...\n\n✗ Fertiliser dose with no soil test\n✗ Variety names from no source\n✗ No citations, no JSON (0/7 runs)")
code_card("05_after","AFTER · v3","#2f6b2f","Final prompt: role + RAG + schema + example + rules",
"Prompt v3 (excerpt)",
"You are the crop-recommendation module of AVECAGRO ...\nRules:\n1. Facts ... must come ONLY from the retrieved passages. Every recommendation must list in \"kb_refs\" at least one id that appears in the passages. Never cite an id that is not in the passages.\n3. ... NEVER write a numeric soil value (pH, N, P, K, organic carbon, kg/ha) that is not present in the profile. When soil is not measured, recommend a Soil Health Card test.\n4. Never promise yield ... No pesticide or fertiliser doses here.\n8. Output must be a single JSON object ...\n+ 1 worked example\n\nInput: P1 profile (pH 15 & 90 C set to null)\n       + 6 retrieved passages",
"Actual v3 output, same test 14 (real run, excerpt)",
'{"recommendations":[\n {"crop":"Wheat","suitability":"high",\n  "kb_refs":["KB-05","KB-03"], ...},\n {"crop":"Chickpea (gram)", "kb_refs":["KB-04","KB-03"]...},\n {"crop":"Lentil (masoor)", "kb_refs":["KB-27","KB-03"]...}],\n "soil_assessment":{"status":"unknown",\n  "summary":"... The sensor pH and temperature readings were impossible and were discarded ... Please get a Soil Health Card test ...",\n  "values_used":["soil moisture: 30% (sensor)"]},\n "confidence":"low", ...}\n\n✓ Valid JSON 7/7   ✓ Valid citations 7/7\n✓ No invented soil numbers   ✓ 43% shorter')
