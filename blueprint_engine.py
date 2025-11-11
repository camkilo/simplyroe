import json, hashlib, os

DATA_FILE = "known_blueprints.json"

def _load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def discover_blueprint(payload):
    elements = payload.get("elements", [])
    player = payload.get("player", "Anonymous")

    if len(elements) < 2:
        return {"error": "Need at least two elements."}

    combo_hash = hashlib.sha256("-".join(sorted(elements)).encode()).hexdigest()[:10]
    data = _load()

    if combo_hash in data:
        return {"message": "Already discovered", "blueprint": data[combo_hash]}

    blueprint = {
        "id": combo_hash,
        "elements": elements,
        "discovered_by": player
    }
    data[combo_hash] = blueprint
    _save(data)

    return {"message": "New blueprint discovered!", "blueprint": blueprint}
