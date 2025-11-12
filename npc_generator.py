# npc_generator.py
# AI-driven NPC generation and management

import json
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict
import random

DATA_DIR = ".data"
NPCS_FILE = os.path.join(DATA_DIR, "npcs.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(NPCS_FILE):
    with open(NPCS_FILE, "w") as f:
        json.dump({}, f)

# NPC trait lists for generation
TRAITS = [
    "curious", "brave", "cautious", "cheerful", "mysterious", "grumpy", 
    "wise", "mischievous", "loyal", "ambitious", "quiet", "energetic",
    "protective", "cunning", "noble", "humble", "passionate", "stoic"
]

BACKGROUNDS = [
    "Once a wandering merchant who lost everything in a storm",
    "Former royal guard seeking redemption for past failures",
    "Mysterious sage who appeared after the great eclipse",
    "Young apprentice searching for their missing mentor",
    "Exiled noble trying to reclaim their family's honor",
    "Ancient being trapped in mortal form by a curse",
    "Survivor of a destroyed village seeking vengeance",
    "Traveling bard collecting stories from across the realm",
    "Reformed thief trying to make amends for their crimes",
    "Scholar obsessed with uncovering forbidden knowledge"
]

DIALOGUE_STARTERS = [
    "Greetings, traveler. What brings you to these parts?",
    "Ah, a new face. I haven't seen you around here before.",
    "You look like someone who could use a good story.",
    "Be careful around here. Not everything is as it seems.",
    "I've been waiting for someone like you to arrive.",
    "The winds of fate have brought you here for a reason.",
    "Welcome, friend. Or perhaps... foe?",
    "Another soul lost in this vast world, I see."
]

def load_npcs():
    with open(NPCS_FILE, "r") as f:
        return json.load(f)

def save_npcs(npcs):
    with open(NPCS_FILE, "w") as f:
        json.dump(npcs, f, indent=2)

def generate_ai_backstory(name: str, trait: str, use_ai: bool = False) -> str:
    """
    Generate NPC backstory. For MVP, uses templates.
    In production, this would call a local LLM via llama.cpp
    """
    if use_ai:
        # TODO: Integrate with llama.cpp or local LLM
        # For now, use template-based generation
        pass
    
    # Template-based backstory (3 lines as per requirements)
    templates = [
        f"{name} was born in the shadow of the mountains. Their {trait} nature often got them into trouble. Now they seek adventure in the wider world.",
        f"Once a simple villager, {name}'s {trait} personality led them to great discoveries. They carry the weight of ancient secrets. Their journey has only just begun.",
        f"{name} wandered the lands for years, their {trait} spirit never broken. They've seen kingdoms rise and fall. Now they offer wisdom to those who listen.",
        f"In the depths of the forest, {name} found their calling. Their {trait} demeanor hides a powerful determination. They protect what matters most to them.",
        f"{name} emerged from the ruins of the old world, {trait} and resolute. They speak of visions and prophecies yet to unfold. Some say they hold the key to the future."
    ]
    
    return random.choice(templates)

def generate_dialogue_tree(npc_name: str, trait: str, backstory: str) -> List[Dict]:
    """
    Generate branching dialogue options for the NPC
    """
    starter = random.choice(DIALOGUE_STARTERS)
    
    dialogue_tree = [
        {
            "id": "start",
            "text": starter,
            "responses": [
                {
                    "id": "ask_about_past",
                    "text": "Tell me about yourself.",
                    "response": f"Ah, my story... {backstory.split('.')[0]}. But that's enough about me."
                },
                {
                    "id": "ask_quest",
                    "text": "Do you need any help?",
                    "response": f"Perhaps. I've been seeking someone {trait} enough to assist me with a delicate matter."
                },
                {
                    "id": "farewell",
                    "text": "I must go.",
                    "response": "Safe travels, friend. May we meet again."
                }
            ]
        }
    ]
    
    return dialogue_tree

def create_npc(
    creator_id: str,
    name: Optional[str] = None,
    trait: Optional[str] = None,
    custom_backstory: Optional[str] = None,
    parent_npc_id: Optional[str] = None
) -> Dict:
    """
    Create a new NPC with AI-generated or custom content
    """
    npcs = load_npcs()
    
    npc_id = str(uuid.uuid4())
    
    # Generate or use provided values
    if not name:
        prefixes = ["Elder", "Young", "Master", "Dame", "Sir", "Captain", "Sage"]
        suffixes = ["the Wise", "the Bold", "the Swift", "the Kind", "the Mysterious"]
        name = f"{random.choice(prefixes)} {random.choice(['Aldric', 'Thora', 'Zephyr', 'Lyra', 'Kael', 'Nyx', 'Orion', 'Iris'])} {random.choice(suffixes)}"
    
    if not trait:
        trait = random.choice(TRAITS)
    
    if not custom_backstory:
        backstory = generate_ai_backstory(name, trait)
    else:
        backstory = custom_backstory
    
    # Generate dialogue
    dialogue_tree = generate_dialogue_tree(name, trait, backstory)
    
    # Track lineage for remixes
    lineage = []
    if parent_npc_id:
        parent = npcs.get(parent_npc_id)
        if parent:
            lineage = parent.get("lineage", []) + [parent_npc_id]
    
    npc = {
        "id": npc_id,
        "name": name,
        "trait": trait,
        "backstory": backstory,
        "dialogue_tree": dialogue_tree,
        "creator_id": creator_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "remix_count": 0,
        "share_count": 0,
        "parent_id": parent_npc_id,
        "lineage": lineage,
        "interactions": 0
    }
    
    npcs[npc_id] = npc
    save_npcs(npcs)
    
    return npc

def get_npc(npc_id: str) -> Optional[Dict]:
    npcs = load_npcs()
    return npcs.get(npc_id)

def remix_npc(user_id: str, original_npc_id: str, changes: Dict) -> Optional[Dict]:
    """
    Create a remix of an existing NPC with modifications
    """
    original = get_npc(original_npc_id)
    if not original:
        return None
    
    # Increment remix count on original
    npcs = load_npcs()
    npcs[original_npc_id]["remix_count"] += 1
    save_npcs(npcs)
    
    # Create new NPC with modified attributes
    new_npc = create_npc(
        creator_id=user_id,
        name=changes.get("name", original["name"]),
        trait=changes.get("trait", original["trait"]),
        custom_backstory=changes.get("backstory", original["backstory"]),
        parent_npc_id=original_npc_id
    )
    
    return new_npc

def get_popular_npcs(limit: int = 10) -> List[Dict]:
    """
    Get most remixed/shared NPCs for leaderboard
    """
    npcs = load_npcs()
    npc_list = list(npcs.values())
    
    # Sort by remix_count + share_count
    sorted_npcs = sorted(
        npc_list,
        key=lambda x: x.get("remix_count", 0) + x.get("share_count", 0),
        reverse=True
    )
    
    return sorted_npcs[:limit]

def increment_share_count(npc_id: str):
    """
    Increment share count when NPC is shared
    """
    npcs = load_npcs()
    if npc_id in npcs:
        npcs[npc_id]["share_count"] = npcs[npc_id].get("share_count", 0) + 1
        save_npcs(npcs)

def get_npc_lineage(npc_id: str) -> List[Dict]:
    """
    Get the full lineage of an NPC for attribution
    """
    npcs = load_npcs()
    npc = npcs.get(npc_id)
    if not npc:
        return []
    
    lineage_data = []
    for ancestor_id in npc.get("lineage", []):
        ancestor = npcs.get(ancestor_id)
        if ancestor:
            lineage_data.append({
                "id": ancestor_id,
                "name": ancestor["name"],
                "creator_id": ancestor["creator_id"]
            })
    
    return lineage_data
