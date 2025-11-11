import random

# Possible locations
locations_pool = ["forest", "cave", "river", "mountains", "desert", "swamp"]

# Enemies per location
enemy_types = {
    "forest": [{"name": "Goblin", "health": 30, "loot": ["Stick", "Copper"]}],
    "cave": [{"name": "Bat", "health": 20, "loot": ["Fur"]}],
    "river": [{"name": "Crocodile", "health": 40, "loot": ["Scale", "Bone"]}],
    "mountains": [{"name": "Wolf", "health": 40, "loot": ["Fur", "Bone"]}],
    "desert": [{"name": "Scorpion", "health": 35, "loot": ["Venom", "Sandstone"]}],
    "swamp": [{"name": "Slime", "health": 25, "loot": ["Herbs", "Mud"]}]
}

# Resources to gather
resources = ["Copper", "Iron", "Wood", "Stone", "Herbs"]

def spawn_enemy(location):
    enemies = enemy_types.get(location, [])
    if enemies:
        return random.choice(enemies).copy()
    return None

def generate_loot(enemy):
    return random.choices(enemy["loot"], k=random.randint(1,2))

def discover_new_location(current_discovered):
    undiscovered = [loc for loc in locations_pool if loc not in current_discovered]
    if not undiscovered:
        return random.choice(locations_pool)  # all discovered, repeat
    return random.choice(undiscovered)

def gather_resources():
    return random.choices(resources, k=random.randint(1,3))
