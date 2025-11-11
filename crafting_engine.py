import random

def craft_item(payload):
    elements = payload.get("elements", [])
    if not elements or len(elements) < 2:
        return {"error": "At least two elements required."}

    rarity = random.choice(["Common", "Uncommon", "Rare", "Epic", "Legendary"])
    combined = "-".join(sorted(elements)).title()

    item = {
        "name": f"{combined} Artifact",
        "rarity": rarity,
        "power": round(random.uniform(10, 100), 2),
        "flavor_text": f"Forged through resonance of {', '.join(elements)}."
    }

    return {"crafted": item}
