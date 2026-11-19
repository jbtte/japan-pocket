"""Generate the day catalog from data/*.json; standard library only."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
entries = []
for path in sorted(DATA.glob("*.json")):
    if path.name.startswith("_") or path.name == "days.json":
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["id", "date", "title", "city", "stops"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"{path.name}: missing {', '.join(missing)}")
    if not isinstance(data["stops"], list):
        raise ValueError(f"{path.name}: stops must be an array")
    ids = [s["id"] for s in data["stops"]]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path.name}: duplicate stop IDs")
    entries.append({
        "id": data["id"],
        "file": path.name,
        "date": data["date"],
        "label": f"Dia {data.get('dayNumber', '?')} · {data['city']}",
        "subtitle": data.get("subtitle", data["title"]),
    })
if len({e["id"] for e in entries}) != len(entries):
    raise ValueError("Duplicate day IDs")
entries.sort(key=lambda e: (e["date"], e["id"]))
(DATA / "days.json").write_text(json.dumps({"siteTitle":"Japão 2026","days":entries}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Catalog generated: {len(entries)} day(s)")
