import sys, html, subprocess
def card(name, title, lines, bg="#2f6b2f"):
    body = "".join(f"<li>{html.escape(l)}</li>" for l in lines)
    h = f"""<html><body style="margin:0;width:1280px;height:720px;background:{bg};color:#fff;font-family:'DejaVu Sans';display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box">
<div style="font-size:26px;opacity:.8">AvecAgro · Team PE-B49-23</div>
<div style="font-size:54px;font-weight:bold;margin:14px 0 26px">{html.escape(title)}</div>
<ul style="font-size:32px;line-height:1.5;margin:0;padding-left:36px">{body}</ul></body></html>"""
    open(name+".html","w").write(h)
    subprocess.run(["google-chrome","--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1280,720",f"--screenshot={name}.png",name+".html"],capture_output=True,timeout=60)
card("01_problem","The problem",["86% of Indian farm holdings are small or marginal","Unpredictable weather, pests, unknown soil, rising costs","Farmers need timely, personal, trustworthy advice","AvecAgro: AI assistant for crops, farm plan & pest alerts"])
card("02_experiment","Prompt experiment: P2 crop recommendation",["v1 = Milestone 1 baseline: one free-text prompt","v3 = role + RAG passages + JSON schema + example + rules","Same farmer input, same model — see the difference"])
card("04_progress","Progress & next steps",["Done: 4 prompts + retrieval, web app, 14 tests, v1→v3 log","Next (M3): bigger expert-checked knowledge base","Real IoT/weather feeds, Hindi voice input, farmer field trials"],bg="#24577a")
