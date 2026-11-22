"""Build the single-file AVECAGRO web app (code/index.html).

Prompts are kept as plain text in prompts/ (single source of truth) and the
knowledge base / test inputs as JSON; this script embeds them into the page.
Usage:  python code/build.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def parse_prompt(path):
    text = path.read_text(encoding="utf-8")
    parts = dict(re.findall(r"=== (\w+) ===\n(.*?)(?=\n=== \w+ ===\n|\Z)", text, re.S))
    return {"meta": parts["META"].strip(), "system": parts["SYSTEM"].strip(), "user": parts["USER"].strip()}


prompts = {
    "P1": parse_prompt(ROOT / "prompts/final/P1_intake_validation.txt"),
    "P2": parse_prompt(ROOT / "prompts/final/P2_crop_recommendation.txt"),
    "P3": parse_prompt(ROOT / "prompts/final/P3_farm_plan_calendar.txt"),
    "P4": parse_prompt(ROOT / "prompts/final/P4_pest_alert_advisor.txt"),
    "P2_v1": parse_prompt(ROOT / "prompts/v1/P2_crop_recommendation_v1.txt"),
    "P2_v2": parse_prompt(ROOT / "prompts/v2/P2_crop_recommendation_v2.txt"),
    "P2_v3": parse_prompt(ROOT / "prompts/v3/P2_crop_recommendation_v3.txt"),
}
data = {
    "prompts": prompts,
    "kb": json.loads((ROOT / "code/knowledge_base.json").read_text(encoding="utf-8")),
    "tests": json.loads((ROOT / "test-data/test_inputs.json").read_text(encoding="utf-8")),
    "lab_tests": [1, 2, 4, 7, 14],
}
tpl = (ROOT / "code/app_template.html").read_text(encoding="utf-8")
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
out = tpl.replace("/*__DATA__*/null", blob)
(ROOT / "code/index.html").write_text(out, encoding="utf-8")
print("built code/index.html", len(out), "bytes;", len(data["kb"]), "KB passages;", len(data["tests"]), "tests")
