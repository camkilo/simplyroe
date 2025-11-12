# rooms.py
# Room-based play sessions and real-time interactions

import json
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Set
import random

DATA_DIR = ".data"
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(ROOMS_FILE):
    with open(ROOMS_FILE, "w") as f:
        json.dump({}, f)

# In-memory active sessions (would use Redis in production)
active_sessions: Dict[str, Set[str]] = {}  # room_id -> set of user_ids

def load_rooms():
    with open(ROOMS_FILE, "r") as f:
        return json.load(f)

def save_rooms(rooms):
    with open(ROOMS_FILE, "w") as f:
        json.dump(rooms, f, indent=2)

def create_room(creator_id: str, name: str, npc_id: Optional[str] = None, max_players: int = 4) -> Dict:
    """
    Create a new play session room
    """
    rooms = load_rooms()
    
    room_id = str(uuid.uuid4())
    
    room = {
        "id": room_id,
        "name": name,
        "creator_id": creator_id,
        "npc_id": npc_id,
        "max_players": max_players,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "active": True,
        "players": [creator_id],
        "chat_log": [],
        "interactions": []
    }
    
    rooms[room_id] = room
    save_rooms(rooms)
    
    # Track active session
    active_sessions[room_id] = {creator_id}
    
    return room

def get_room(room_id: str) -> Optional[Dict]:
    rooms = load_rooms()
    return rooms.get(room_id)

def join_room(room_id: str, user_id: str) -> Optional[Dict]:
    """
    Add a player to a room
    """
    rooms = load_rooms()
    room = rooms.get(room_id)
    
    if not room:
        return None
    
    if not room.get("active", False):
        return None
    
    if len(room["players"]) >= room["max_players"]:
        return None
    
    if user_id not in room["players"]:
        room["players"].append(user_id)
        rooms[room_id] = room
        save_rooms(rooms)
    
    # Track active session
    if room_id not in active_sessions:
        active_sessions[room_id] = set()
    active_sessions[room_id].add(user_id)
    
    return room

def leave_room(room_id: str, user_id: str):
    """
    Remove a player from a room
    """
    if room_id in active_sessions:
        active_sessions[room_id].discard(user_id)
        
        # Clean up empty rooms
        if len(active_sessions[room_id]) == 0:
            del active_sessions[room_id]

def add_chat_message(room_id: str, user_id: str, message: str):
    """
    Add a chat message to the room log
    """
    rooms = load_rooms()
    room = rooms.get(room_id)
    
    if not room:
        return False
    
    chat_entry = {
        "user_id": user_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    room["chat_log"].append(chat_entry)
    
    # Keep last 100 messages
    room["chat_log"] = room["chat_log"][-100:]
    
    rooms[room_id] = room
    save_rooms(rooms)
    
    return True

def add_npc_interaction(room_id: str, user_id: str, npc_id: str, dialogue_id: str, response_text: str):
    """
    Record an NPC interaction in the room
    """
    rooms = load_rooms()
    room = rooms.get(room_id)
    
    if not room:
        return False
    
    interaction = {
        "user_id": user_id,
        "npc_id": npc_id,
        "dialogue_id": dialogue_id,
        "response": response_text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    room["interactions"].append(interaction)
    
    # Keep last 50 interactions
    room["interactions"] = room["interactions"][-50:]
    
    rooms[room_id] = room
    save_rooms(rooms)
    
    return True

def get_active_rooms(limit: int = 20) -> List[Dict]:
    """
    Get list of active rooms
    """
    rooms = load_rooms()
    
    active_rooms = [
        room for room in rooms.values()
        if room.get("active", False) and len(room["players"]) < room["max_players"]
    ]
    
    # Sort by most recent
    sorted_rooms = sorted(
        active_rooms,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    
    return sorted_rooms[:limit]

def close_room(room_id: str, user_id: str) -> bool:
    """
    Close a room (only creator can do this)
    """
    rooms = load_rooms()
    room = rooms.get(room_id)
    
    if not room or room["creator_id"] != user_id:
        return False
    
    room["active"] = False
    rooms[room_id] = room
    save_rooms(rooms)
    
    # Clean up active sessions
    if room_id in active_sessions:
        del active_sessions[room_id]
    
    return True

def get_room_participants(room_id: str) -> Set[str]:
    """
    Get current active participants in a room
    """
    return active_sessions.get(room_id, set())
