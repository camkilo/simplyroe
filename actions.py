from game_state import player_state
from world import spawn_enemy, generate_loot
import random

def encounter_enemy():
    if not player_state["enemy"]:
        player_state["enemy"] = spawn_enemy()
        return f"A wild {player_state['enemy']['name']} appears!"
    return f"You are already fighting a {player_state['enemy']['name']}!"

def attack():
    enemy = player_state["enemy"]
    if not enemy:
        return "No enemy to attack!"

    damage = random.randint(5, 15)
    enemy["health"] -= damage

    if enemy["health"] <= 0:
        loot = generate_loot(enemy)
        player_state["inventory"].extend(loot)
        player_state["xp"] += 10
        name = enemy["name"]
        player_state["enemy"] = None
        return f"You defeated the {name}! Loot: {loot}"
    
    # Enemy strikes back
    enemy_damage = random.randint(5, 10)
    player_state["health"] -= enemy_damage
    return (f"You hit the {enemy['name']} for {damage} damage. "
            f"Enemy hits back for {enemy_damage} damage. "
            f"Your HP: {player_state['health']} Enemy HP: {enemy['health']}")

def flee():
    if player_state["enemy"]:
        name = player_state["enemy"]["name"]
        player_state["enemy"] = None
        return f"You fled from the {name}!"
    return "No enemy to flee from."

def gather():
    resources = ["Copper", "Iron", "Wood", "Stone", "Herbs"]
    found = random.choices(resources, k=random.randint(1,3))
    player_state["inventory"].extend(found)
    player_state["xp"] += 5
    return f"You gathered: {found}"
