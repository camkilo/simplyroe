import random

# Sample enemies & loot
enemies = [
    {"name": "Goblin", "health": 30, "loot": ["Copper", "Stick"]},
    {"name": "Wolf", "health": 40, "loot": ["Fur", "Bone"]},
]

locations = ["forest", "cave", "river", "mountains"]

def spawn_enemy():
    return random.choice(enemies).copy()

def generate_loot(enemy):
    return random.choices(enemy["loot"], k=1)
