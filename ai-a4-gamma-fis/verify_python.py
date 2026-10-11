"""Run the Python reference FIS on the five scenario feature sets (features.json)."""
import json
from build_system import build_fis

fis = build_fis()
features = json.load(open("features.json"))
for name, f in features.items():
    conf, _ = fis.evaluate({"NTOTAL": f["ntotal"], "MAX8": f["max8"], "BIN05": f["bin05"], "BIN08": f["bin08"]})
    print(f"{name}: threat confidence = {conf:.2f}%")
