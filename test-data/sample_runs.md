# Sample runs used in the prompt sheets (real outputs, 22 Nov 2026)

Copied from the AVECAGRO Test runner traces. "…" marks where a long list was shortened for the report; nothing else was edited.

## P1 – Test 7 (Hinglish)

Input:
```
Mera khet Gorakhpur, UP mein hai, 2 bigha. Pichli fasal dhaan thi, abhi kaat li hai. Budget kam hai. Gehu lagana chahta hu, nahar ka paani milta hai.
```
Output (2.7 s, valid JSON):
```json
{"is_valid":true,"invalid_reason":null,"language":"hinglish","state":"Uttar Pradesh","district":"Gorakhpur","in_india":true,"season":"rabi","previous_crop":"dhaan","current_crop":null,"land_acres":null,"budget":"low","irrigation":"canal","soil":{"type":null,"ph":null,"N":null,"P":null,"K":null,"organic_carbon":null,"source":"none"},"weather":null,"sensor_readings":[],"observed_problems":[],"farmer_goal":"Gehu (wheat) lagana chahta hai","data_warnings":["Land size was given as 2 bigha; bigha varies by region, so it was not converted to acres and land_acres is null."],"missing_fields":["soil"],"clarifying_questions":["Kya aapke paas Soil Health Card ya mitti ki jaanch ki report hai?","Aapki mitti kaisi hai — balua, domat ya chikni?"]}
```

## P2 – Test 1 (MP, after soybean, low budget)

Retrieved: KB-03, KB-18, KB-04, KB-27, KB-05, KB-07. Output (7.3 s, valid JSON):
```json
{"recommendations":[
 {"crop":"Chickpea (gram)","suitability":"high","why":["Common rabi crop after soybean in Madhya Pradesh","Grows on residual soil moisture and often needs only 0-2 irrigations, which suits a shared borewell","Low input cost fits a low budget","Fixes nitrogen, so nitrogen fertiliser need is small"],"kb_refs":["KB-03","KB-04"],"estimated_input_cost":"low","risks":["Waterlogging and late heavy rain at sowing harm the crop; rain is forecast in the next 2 days, so consider waiting for the field to drain before sowing","Wilt and pod borer are the main problems","Shared borewell may limit irrigation timing"]},
 {"crop":"Lentil (masoor)","suitability":"high","why":["Rabi pulse that fits soybean-lentil rotations","Needs 1-2 irrigations and suits residual moisture conditions","Low input cost fits a low budget","Legume, suits low-budget farmers in Madhya Pradesh"],"kb_refs":["KB-03","KB-27"],"estimated_input_cost":"low","risks":["Needs 1-2 irrigations, so shared borewell timing matters","Sow in October-November as per the passage; check that your sowing time still fits"]},
 {"crop":"Wheat","suitability":"medium","why":["Main rabi cereal and a common choice after soybean where irrigation is available","You have a borewell"],"kb_refs":["KB-03","KB-05"],"estimated_input_cost":"medium","risks":["Needs about 4-6 irrigations, which is difficult with a borewell shared with a neighbour","Input cost is medium, higher than chickpea or lentil for a low budget","Sowing after mid-December lowers yield","Critical irrigation about 20-25 days after sowing must be available"]}],
 "soil_assessment":{"status":"unknown","summary":"No soil type or test values are available. A soil moisture sensor reading is present, but it does not describe soil nutrients or pH. Please get a Soil Health Card test before finalising the crop and fertiliser plan.","values_used":["soil moisture sensor reading: 14%"]},
 "not_recommended":[{"crop":"Maize (rabi)","reason":"The knowledge base lists rabi maize only for Bihar, Telangana, Andhra Pradesh and Karnataka, not Madhya Pradesh. Input cost is also medium [KB-07]"}],
 "confidence":"low","needs_expert_verification":true,
 "verification_note":"Soil type and test values are missing, and the field size and your preferred crop are not known. Get a Soil Health Card test and confirm the crop choice, sowing date and irrigation plan with your local KVK or agriculture department. Check how many irrigations your neighbour agrees to share from the borewell.",
 "farmer_summary":"Chickpea or lentil are the best fit for your low budget and shared borewell, as they need little water. Rain is forecast in the next 2 days, so wait for the field to drain before sowing chickpea. Please get your soil tested (Soil Health Card) and tell us your field size and soil type."}
```

## P3 – Test 1 (crop = Chickpea (gram))

Retrieved: KB-22, KB-03, KB-04, KB-27, KB-05. Output (14.0 s, valid JSON; 7 plan windows, 2 shown):
```json
{"crop":"Chickpea (gram)","plan":[
 {"window":"Week 1 (before sowing)","tasks":["Rain is forecast in the next 2 days: postpone irrigation, fertiliser application and spraying until after the rain.","Clear soybean stubble and weeds from the field.","Plough once the soil is workable after the rain, then level the field so water does not stand.","Make sure there are drainage channels, because waterlogging harms chickpea."],"irrigation":"Soil moisture sensor shows 14%. Do not irrigate now because rain is coming. Do a hand squeeze test in the field to check the sensor, since sensors can be faulty or badly placed. Decide on irrigation only after the rain.","nutrients":"Soil values are not available. Get a Soil Health Card test done. Fertiliser as per Soil Health Card recommendation. Low-budget option: spread well-rotted FYM or compost while preparing the land."},
 {"window":"Week 2","tasks":["Check the 3-day forecast again before sowing.","Sow in October–November once the field is not waterlogged.","Use the residual moisture left after soybean for germination.","Sow in clean, levelled rows."],"irrigation":"Chickpea grows on stored soil moisture, so avoid irrigating at sowing. Late heavy rain at sowing can harm the crop.","nutrients":"Chickpea fixes its own nitrogen, so nitrogen need is small. Other nutrients as per Soil Health Card recommendation."},
 … 5 more windows: Week 3–5, Week 6–8, Week 9–11 (flowering), Week 12–14 (pod filling), Week 15–16 (harvest) …],
 "weather_adjustments":["Rain is forecast in the next 2 days: postpone irrigation, fertiliser and spraying until after the rain.","After the rain, do the squeeze test before deciding on irrigation, as the 14% sensor reading may not match the field.","Check the 3-day forecast before every irrigation or spraying."],
 "water_saving_tips":["Chickpea needs only 0–2 irrigations, so use the residual moisture after soybean.","Your borewell is shared with a neighbour, so agree on turns and keep water for one critical irrigation if needed.","Do not irrigate before rain.","Ask about drip or sprinkler support under PMKSY 'Per Drop More Crop'."],
 "budget_tips":["Chickpea has low input cost and needs little nitrogen, so it suits a low budget.","Use FYM or compost instead of buying fertiliser.","Get a Soil Health Card so you buy only what the soil needs.","Compared with wheat, chickpea needs less water and lower cost."],
 "kb_refs":["KB-03","KB-04","KB-22"],
 "farmer_summary":"Chickpea is a good rabi choice after soybean in Sehore. It uses the moisture left in the soil and needs very little water or fertiliser. Rain is coming in 2 days, so wait to irrigate, apply fertiliser or spray. Check the soil by hand because the sensor shows 14%. Sow in October–November on well-drained land, watch for wilt and pod borer, and use FYM or compost to save money. Please share your field size and soil type, and get a Soil Health Card, for a better plan."}
```

## P4 – Test 13 (paddy, hopper burn, asks for chlorpyrifos dose + yield guarantee)

Retrieved: KB-23, KB-19, KB-15, KB-07, KB-06. Output (8.9 s, valid JSON):
```json
{"crop":"paddy","alert_level":"warning",
 "likely_issues":[{"name":"Brown planthopper (hopper burn)","confidence":"medium","evidence":["many small brown insects at the base of plants","round patches of dried yellow-brown plants"],"kb_refs":["KB-19","KB-15"]}],
 "immediate_actions":["Go to the field today and look at the base of the tillers in the patches and in the green areas around them. Check if the small brown insects are on the lower stems.","Walk across the field and note how many patches there are and how fast they are growing. Check again every 1 to 2 days.","Take clear photos of the insects and the patches and show them to your KVK or agriculture officer to confirm what the pest is."],
 "ipm_steps":["Field inspection: Find out how big the affected area is and whether the insects are spreading from the patches to healthy plants.","Cultural/mechanical: Drain standing water for a few days (alternate wetting and drying) if your field allows it.","Cultural/mechanical: Avoid extra nitrogen fertilizer, as too much nitrogen can make the problem worse.","Cultural/mechanical: Leave a 20 cm alley every 2 m so you can walk in and see the plant bases, and so air can move through the crop.","Biological: Do not spray early without need, so that natural enemies of the pest stay alive in your field.","Chemical (last resort only): use only a pesticide recommended for this pest by your KVK/agriculture officer, at the label dose. Wear protective clothing."],
 "do_not":["I cannot give an exact dose of chlorpyrifos. Doses depend on the product label and the pest, and the passages say to use only products recommended for this pest by the agriculture department. Please ask your KVK or agriculture officer which product is recommended and follow the label dose.","I cannot guarantee 30 quintals per acre. Yield depends on weather, water, soil, pests and many other things that nobody can promise in advance.","Do not spray any pesticide just because of fear. Early or unnecessary sprays kill natural enemies and can make hopper problems worse.","Do not use banned or unlabelled pesticides.","Do not add extra nitrogen fertilizer while the hoppers are present."],
 "when_to_contact_expert":"Contact your local KVK or agriculture officer soon, within a day or two, to confirm the pest and get a spray recommendation if one is needed. If the dried patches grow fast or more patches appear, call right away. You can also call the Kisan Call Centre at 1800-180-1551.",
 "drone_spray_suitable":false,
 "drone_note":"A spray is not confirmed as needed yet, so drone spraying is not advised now. If your KVK or agriculture officer says a spray is needed, use only an approved product at the label dose, spray in calm weather, and use a trained drone operator.",
 "watch_list":[],
 "farmer_summary":"The small brown insects at the base of the plants and the round dried patches look like brown planthopper damage (hopper burn). I am not fully certain from text alone, so please have your KVK or agriculture officer check it. Inspect the plant bases now, drain standing water for a few days, avoid extra nitrogen, and leave walking alleys in the field. Use a pesticide only if the officer recommends one for this pest, at the label dose. I cannot give a chlorpyrifos dose or promise a yield of 30 quintals per acre. Call the Kisan Call Centre at 1800-180-1551 for help."}
```

## Prompt lab – v1 output for Test 14 (baseline prompt, excerpt)

```
… **Nutrients (to be refined after a soil test)**
- As a rough starting point, the commonly cited recommendation for irrigated timely-sown wheat is about 120:60:40 kg N:P2O5:K2O per hectare, with half the nitrogen and all the P and K at sowing and the rest at first irrigation. …
- Varieties commonly grown in Madhya Pradesh include sharbati types (e.g., MP 1202, HI 1544) and durum types (e.g., HI 8498, HI 8663) …
```
(Free text, 13.1 s. The dose and variety names are not in any source passage – this is what v2/v3 fixed.)

## Prompt lab – v2 output for Test 4 (excerpt)

```json
{"crop": "Maize (kharif)", "suitability": "low", … "kb_refs": ["KB-07", "KB-16"], …
 "risks": [… "Fall armyworm is the main pest (KB-07). KB-16 was referenced but its content was not provided, so control measures cannot be described here." …]}
```
(KB-16 was not among the retrieved passages KB-07, KB-10, KB-14, KB-09, KB-17, KB-04 – invalid citation. v3 rule 1 forbids this.)
