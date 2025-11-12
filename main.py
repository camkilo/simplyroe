# main.py
# Realm of Echoes - single-repo playable demo (FastAPI + simple SPA)
# Run: pip install -r requirements.txt
#      uvicorn main:app --reload --port 8000

import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os, json, hashlib, random, datetime, uuid
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json, os, random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from actions import attack, flee, encounter, gather
from game_state import player_state
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from actions import attack, flee, encounter, gather, explore
from game_state import player_state

app = FastAPI()

@app.get("/status")
def status():
    return JSONResponse(content=player_state)

@app.post("/action/{action_name}")
def do_action(action_name: str):
    if action_name == "attack":
        return {"result": attack()}
    elif action_name == "flee":
        return {"result": flee()}
    elif action_name == "encounter":
        return {"result": encounter()}
    elif action_name == "gather":
        return {"result": gather()}
    elif action_name == "explore":
        return {"result": explore()}
    return {"result": "Unknown action"}

app = FastAPI()

@app.get("/status")
def status():
    return JSONResponse(content=player_state)

@app.post("/action/{action_name}")
def do_action(action_name: str):
    if action_name == "attack":
        return {"result": attack()}
    elif action_name == "flee":
        return {"result": flee()}
    elif action_name == "encounter":
        return {"result": encounter()}
    elif action_name == "gather":
        return {"result": gather()}
    return {"result": "Unknown action"}

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHUNK_SIZE = 10
biomes = ['forest','water','mountain','desert','lava','ice','plains','swamp']
world_file = "world.json"
player_file = "players.json"

# Load or create world
if os.path.exists(world_file):
    with open(world_file,'r') as f:
        world = json.load(f)
else:
    world = {}

if os.path.exists(player_file):
    with open(player_file,'r') as f:
        players = json.load(f)
else:
    players = {}

def save_world():
    with open(world_file,'w') as f:
        json.dump(world,f)

def save_players():
    with open(player_file,'w') as f:
        json.dump(players,f)

def generate_chunk(cx,cy):
    chunk = {}
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            biome = random.choice(biomes)
            chunk[f"{x},{y}"] = {"biome":biome,"effect":None}
    return chunk

@app.get("/get_chunk")
def get_chunk(cx:int,cy:int):
    key = f"{cx},{cy}"
    if key not in world:
        world[key] = generate_chunk(cx,cy)
        save_world()
    return world[key]

@app.get("/gather")
def gather(player_id:str,cx:int,cy:int,x:int,y:int):
    # register player if new
    if player_id not in players:
        players[player_id] = {"inventory":[],"chunk_x":cx,"chunk_y":cy,"x":x,"y":y}
        save_players()
    biome = world[f"{cx},{cy}"][f"{x},{y}"]["biome"]
    item = random.choice(['Hydrogen','Oxygen','Carbon','Gold'])
    rarity = random.choices(['common','rare','epic'],[0.7,0.25,0.05])[0]
    effect = "glow" if rarity != 'common' else None
    world[f"{cx},{cy}"][f"{x},{y}"]["effect"] = effect
    players[player_id]["inventory"].append(item)
    save_world()
    save_players()
    return {"item":item,"rarity":rarity,"effect":effect}

@app.get("/craft")
def craft(player_id:str):
    if player_id not in players: return {"msg":"No player found"}
    inv = players[player_id]["inventory"]
    if not inv: return {"msg":"No items to craft"}
    crafted = "".join(inv[:2]) + " Compound"
    # spawn new tiles in nearby chunk
    cx = players[player_id]["chunk_x"]
    cy = players[player_id]["chunk_y"]
    new_tiles = []
    for _ in range(random.randint(1,3)):
        nx = random.randint(0,CHUNK_SIZE-1)
        ny = random.randint(0,CHUNK_SIZE-1)
        biome = random.choice(biomes)
        world[f"{cx},{cy}"][f"{nx},{ny}"] = {"biome":biome,"effect":"glow"}
        new_tiles.append({"x":nx,"y":ny,"biome":biome,"effect":"glow"})
    players[player_id]["inventory"] = []
    save_world()
    save_players()
    return {"item":crafted,"rarity":"rare","new_tiles":new_tiles}
app = FastAPI()  # ← must be before mounting anything

# Then mount static
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Your routes
@app.get("/hello")
def hello():
    return {"msg":"Hello World"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
APP_NAME = "Realm of Echoes (Single-Repo Playable Demo)"
DATA_DIR = ".data"
PLAYERS_FILE = os.path.join(DATA_DIR, "players.json")
BLUEPRINTS_FILE = os.path.join(DATA_DIR, "known_blueprints.json")
WORLD_FILE = os.path.join(DATA_DIR, "world_chronicle.json")

os.makedirs(DATA_DIR, exist_ok=True)
for path in (PLAYERS_FILE, BLUEPRINTS_FILE, WORLD_FILE):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({} if path != WORLD_FILE else {"events": []}, f, indent=2)

# --- Utilities ---
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def short_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:10]

# --- Game systems (engine) ---
BASE_STATS = {"strength": 5, "intelligence": 5, "agility": 5}
STARTER_ELEMENTS = ["Hydrogen", "Iron", "Gold", "Carbon", "Sulfur"]

class ActionPayload(BaseModel):
    player_id: str
    action: str
    payload: dict = {}

app = FastAPI(title=APP_NAME)

# --- Player management ---
def make_player(name: str):
    players = load_json(PLAYERS_FILE)
    pid = str(uuid.uuid4())
    players[pid] = {
        "id": pid,
        "name": name,
        "created_at": now_iso(),
        "level": 1,
        "xp": 0,
        "xp_to_next": 100,
        "stats": BASE_STATS.copy(),
        "inventory": {"elements": STARTER_ELEMENTS.copy(), "items": []},
        "location": "The Shattered Shore",
        "discoveries": [],
        "chronicle": []
    }
    players[pid]["chronicle"].append({"t": now_iso(), "e": f"{name} entered the world at {players[pid]['location']}."})
    save_json(PLAYERS_FILE, players)
    return players[pid]

def get_player(pid: str):
    players = load_json(PLAYERS_FILE)
    p = players.get(pid)
    if not p:
        raise HTTPException(status_code=404, detail="Player not found")
    return p

def update_player(p):
    players = load_json(PLAYERS_FILE)
    players[p["id"]] = p
    save_json(PLAYERS_FILE, players)
    return p

def add_world_event(e: str):
    world = load_json(WORLD_FILE)
    evt = {"t": now_iso(), "event": e}
    world.setdefault("events", []).insert(0, evt)
    # keep recent 200
    world["events"] = world["events"][:200]
    save_json(WORLD_FILE, world)

# --- XP & leveling ---
def grant_xp(p, amount, reason=None):
    p["xp"] += amount
    p["chronicle"].append({"t": now_iso(), "e": f"Gained {amount} XP{' ('+reason+')' if reason else ''}."})
    leveled = False
    while p["xp"] >= p["xp_to_next"]:
        p["xp"] -= p["xp_to_next"]
        p["level"] += 1
        p["xp_to_next"] = int(p["xp_to_next"] * 1.5)
        # stat award
        stat = random.choice(list(p["stats"].keys()))
        p["stats"][stat] += 1
        p["chronicle"].append({"t": now_iso(), "e": f"Leveled up! Now level {p['level']}. +1 {stat}."})
        add_world_event(f"{p['name']} reached level {p['level']}.")
        leveled = True
    return leveled

# --- Crafting & blueprint discovery ---
def craft_item(elements):
    # deterministic-ish name + slight RNG for power
    key = "-".join(sorted(elements))
    name = f"{''.join(e[0] for e in elements)}-{short_hash(key)} Artifact"
    power = round(10 + random.random()*90 + len(elements)*3, 2)
    rarity_roll = random.random()
    if rarity_roll > 0.97:
        rarity = "Legendary"
    elif rarity_roll > 0.85:
        rarity = "Epic"
    elif rarity_roll > 0.6:
        rarity = "Rare"
    elif rarity_roll > 0.3:
        rarity = "Uncommon"
    else:
        rarity = "Common"
    flavor = f"Forged from {', '.join(elements)} — it hums with echo-resonance."
    return {"name": name, "elements": elements, "power": power, "rarity": rarity, "flavor": flavor}

def discover_blueprint(player_name, elements):
    data = load_json(BLUEPRINTS_FILE)
    combo_key = "-".join(sorted(elements))
    h = short_hash(combo_key)
    if h in data:
        return {"already": True, "blueprint": data[h]}
    blue = {"id": h, "elements": elements, "discovered_by": player_name, "t": now_iso()}
    data[h] = blue
    save_json(BLUEPRINTS_FILE, data)
    add_world_event(f"Blueprint discovered: {', '.join(elements)} by {player_name}")
    return {"already": False, "blueprint": blue}

# --- Procedural events & encounters ---
ENEMIES = [
    {"name": "Dust Wraith", "hp": 20, "atk": 5, "agility": 6, "loot": ["Carbon"]},
    {"name": "Ironclad Rabble", "hp": 40, "atk": 8, "agility": 3, "loot": ["Iron", "Sulfur"]},
    {"name": "Echohound", "hp": 28, "atk": 6, "agility": 8, "loot": ["Leather", "Gold"]},
]

def roll_encounter(p):
    # encounter complexity increases with level
    lvl = p["level"]
    pool = ENEMIES.copy()
    enemy = random.choice(pool)
    # scale
    scale = 1 + (lvl-1)*0.15
    e = {
        "id": str(uuid.uuid4()),
        "name": enemy["name"],
        "max_hp": int(enemy["hp"]*scale),
        "hp": int(enemy["hp"]*scale),
        "atk": int(enemy["atk"]*scale),
        "agility": int(enemy["agility"]*scale),
        "loot": enemy["loot"]
    }
    return e

def attack_result(attacker_atk, defender_hp):
    return max(0, int(random.gauss(attacker_atk, attacker_atk*0.2)))

# --- API endpoints & SPA ---
SPAWN_PROMPTS = [
    "You find a shimmering cluster of elemental shards.",
    "A low hum stirs the air — someone once experimented here.",
    "A wandering merchant left a crate of strange things."
]

@app.post("/api/create_player")
async def api_create_player(req: Request):
    body = await req.json()
    name = body.get("name", "Anonymous")
    p = make_player(name)
    return JSONResponse({"player": p})

@app.get("/api/player/{pid}")
def api_get_player(pid: str):
    p = get_player(pid)
    # include some world snapshot
    world = load_json(WORLD_FILE)
    blueprints = load_json(BLUEPRINTS_FILE)
    return {"player": p, "world": {"events": world.get("events", [])[:10], "blueprints_count": len(blueprints)}}

@app.post("/api/action")
def api_action(payload: ActionPayload):
    p = get_player(payload.player_id)
    action = payload.action.lower()
    out = {"ok": False, "action": action}
    if action == "explore":
        text = random.choice(SPAWN_PROMPTS)
        # small chance to encounter
        encounter_chance = 0.5
        if random.random() < encounter_chance:
            enemy = roll_encounter(p)
            # register temporary encounter in player object
            p.setdefault("encounters", {})[enemy["id"]] = enemy
            update_player(p)
            out.update({"ok": True, "result": "encounter", "text": text, "enemy": enemy})
            return out
        else:
            # find random element or tell a story
            found = random.choice(STARTER_ELEMENTS + ["Copper", "Silver", "Sulfur", "Quartz"])
            p["inventory"].setdefault("elements", []).append(found)
            p["chronicle"].append({"t": now_iso(), "e": f"Found {found} while exploring."})
            grant_xp(p, 12, reason="Exploration")
            update_player(p)
            out.update({"ok": True, "result": "found", "text": f"{text} You discovered {found}."})
            return out

    if action == "fight":
        # payload must include enemy_id and type ("attack" or "flee")
        enemy_id = payload.payload.get("enemy_id")
        cmd = payload.payload.get("cmd", "attack")
        encounters = p.get("encounters", {})
        if enemy_id not in encounters:
            out.update({"error": "no such encounter"})
            return out
        enemy = encounters[enemy_id]
        # simple turn: compare agility
        player_ag = p["stats"]["agility"]
        enemy_ag = enemy["agility"]
        player_first = player_ag >= enemy_ag
        log = []
        if cmd == "flee":
            flee_chance = 0.4 + (p["stats"]["agility"]-5)*0.05
            if random.random() < flee_chance:
                del p["encounters"][enemy_id]
                p["chronicle"].append({"t": now_iso(), "e": f"Fled from {enemy['name']}."})
                update_player(p)
                out.update({"ok": True, "result": "fled", "log": ["You fled successfully."]})
                return out
            else:
                log.append("Failed to flee! The fight begins.")
        # fight loop
        while enemy["hp"] > 0:
            if player_first:
                dmg = attack_result(p["stats"]["strength"]+int(p["level"]/2), enemy["hp"])
                enemy["hp"] = max(0, enemy["hp"]-dmg)
                log.append(f"You hit {enemy['name']} for {dmg} damage. ({enemy['hp']} HP left)")
                if enemy["hp"] <= 0:
                    break
                # enemy hit
                edmg = attack_result(enemy["atk"], 9999)
                # player doesn't have hp in this demo; use agility to mitigate
                evade = random.random() < (p["stats"]["agility"] / 20)
                if evade:
                    log.append(f"You evaded {enemy['name']}'s attack.")
                else:
                    # penalty: small XP loss simulation as 'pain'
                    xp_loss = max(0, int(enemy["atk"]/4))
                    p["xp"] = max(0, p["xp"]-xp_loss)
                    log.append(f"You took a hit and lost {xp_loss} XP (simulated damage).")
            else:
                # enemy attacks first
                edmg = attack_result(enemy["atk"], 9999)
                evade = random.random() < (p["stats"]["agility"] / 20)
                if evade:
                    log.append(f"You evaded {enemy['name']}'s strike.")
                else:
                    xp_loss = max(0, int(enemy["atk"]/4))
                    p["xp"] = max(0, p["xp"]-xp_loss)
                    log.append(f"You took a hit and lost {xp_loss} XP (simulated damage).")
                # player retaliates
                dmg = attack_result(p["stats"]["strength"]+int(p["level"]/2), enemy["hp"])
                enemy["hp"] = max(0, enemy["hp"]-dmg)
                log.append(f"You hit {enemy['name']} for {dmg} damage. ({enemy['hp']} HP left)")
            # swap who goes first
            player_first = not player_first
            # safety break
            if len(log) > 30:
                break
        # outcome
        if enemy["hp"] <= 0:
            loot = enemy.get("loot", [])
            for it in loot:
                p["inventory"].setdefault("elements", []).append(it)
            xp_gain = 40 + random.randint(0, 20)
            grant_xp(p, xp_gain, reason=f"Defeated {enemy['name']}")
            p["chronicle"].append({"t": now_iso(), "e": f"Defeated {enemy['name']} and looted {', '.join(loot)}."})
            del p["encounters"][enemy_id]
            update_player(p)
            out.update({"ok": True, "result": "victory", "log": log, "loot": loot, "xp": xp_gain})
            return out
        else:
            # draw / stopped
            update_player(p)
            out.update({"ok": True, "result": "draw", "log": log})
            return out

    if action == "craft":
        elements = payload.payload.get("elements", [])
        if not elements or len(elements) < 2:
            out.update({"error": "Need 2+ elements to craft."})
            return out
        # Ensure player has elements
        inv = p["inventory"].get("elements", [])
        for e in elements:
            if e not in inv:
                out.update({"error": f"Missing element: {e}"})
                return out
        item = craft_item(elements)
        # small chance to discover blueprint permanently
        disc = discover_blueprint(p["name"], elements)
        # consume elements with some chance (not always)
        if random.random() < 0.75:
            for e in elements:
                try:
                    inv.remove(e)
                except ValueError:
                    pass
        p["inventory"].setdefault("items", []).append(item)
        grant_xp(p, 30, reason="Crafting")
        if not disc["already"]:
            p["discoveries"].append(disc["blueprint"]["id"])
            p["chronicle"].append({"t": now_iso(), "e": f"Discovered blueprint: {', '.join(elements)}."})
        update_player(p)
        out.update({"ok": True, "result": "crafted", "item": item, "discovered": disc})
        return out

    if action == "discover":
        # attempt discovery by experimenting random combos from inventory
        inv = p["inventory"].get("elements", [])
        if len(inv) < 2:
            out.update({"error": "Not enough elements to experiment."})
            return out
        # pick 2-3 random elements
        k = random.choice([2, 2, 3])
        elements = random.sample(inv, min(k, len(inv)))
        disc = discover_blueprint(p["name"], elements)
        if not disc["already"]:
            p["discoveries"].append(disc["blueprint"]["id"])
            grant_xp(p, 50, reason="Blueprint discovery")
            p["chronicle"].append({"t": now_iso(), "e": f"Experimented and discovered blueprint: {', '.join(elements)}."})
            add_world_event(f"{p['name']} discovered a new blueprint: {', '.join(elements)}")
            # small reward
            p["inventory"].setdefault("items", []).append({"name": f"Proto-{disc['blueprint']['id']}", "rarity": "Unique"})
            update_player(p)
            out.update({"ok": True, "result": "discovered", "blueprint": disc["blueprint"]})
            return out
        else:
            # failed discovery but maybe get small XP
            grant_xp(p, 8, reason="Failed experiment")
            p["chronicle"].append({"t": now_iso(), "e": f"Experimented with {', '.join(elements)} but found nothing new."})
            update_player(p)
            out.update({"ok": True, "result": "nothing", "msg": "Already discovered."})
            return out

    if action == "rest":
        # small XP and regen imitation
        grant_xp(p, 10, reason="Rest")
        p["chronicle"].append({"t": now_iso(), "e": "Rested and reflected."})
        update_player(p)
        out.update({"ok": True, "result": "rested"})
        return out

    out.update({"error": "Unknown action"})
    return out

@app.get("/api/world")
def api_world():
    world = load_json(WORLD_FILE)
    blueprints = load_json(BLUEPRINTS_FILE)
    return {"events": world.get("events", [])[:50], "blueprints_count": len(blueprints)}

# --- Serve SPA ---
INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Realm of Echoes — Demo</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{font-family: Inter, system-ui, -apple-system, Arial; background:#0b1020;color:#dfe7ff;margin:0}
    .wrap{max-width:980px;margin:24px auto;padding:20px}
    header{display:flex;align-items:center;gap:12px}
    h1{margin:0;font-size:20px}
    .box{background:#0f1724;border:1px solid #1f2a44;padding:12px;border-radius:8px;margin-top:12px}
    button{background:#2563eb;color:white;border:none;padding:8px 12px;border-radius:6px;cursor:pointer}
    .muted{color:#9fb0ff;font-size:13px}
    .cols{display:flex;gap:12px}
    .col{flex:1}
    pre{white-space:pre-wrap;word-break:break-word}
    .pill{background:#14203a;padding:6px 8px;border-radius:999px;font-size:12px}
  </style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="pill">Realm of Echoes • Demo</div>
    <h1 id="title">Create your player</h1>
  </header>

  <div class="box" id="createBox">
    <label>Player name: <input id="name" value="AetherKnight" /></label>
    <button onclick="createPlayer()">Enter World</button>
    <div class="muted">This demo stores data server-side in JSON (no auth). For private testing, use a unique name.</div>
  </div>

  <div id="game" style="display:none">
    <div class="cols">
      <div class="col box">
        <h3>Player</h3>
        <div id="playerInfo"></div>
        <div style="margin-top:8px">
          <button onclick="doAction('explore')">Explore</button>
          <button onclick="doAction('discover')">Experiment</button>
          <button onclick="doAction('rest')">Rest</button>
        </div>
      </div>

      <div class="col box">
        <h3>Inventory</h3>
        <div id="inventory"></div>
        <div style="margin-top:8px">
          <button onclick="openCraft()">Craft (select elements)</button>
        </div>
      </div>

      <div class="col box">
        <h3>World Chronicle</h3>
        <div id="chronicle" style="max-height:300px;overflow:auto"></div>
      </div>
    </div>

    <div id="encounters" class="box" style="margin-top:12px;display:none">
      <h3>Encounter</h3>
      <div id="encounterBox"></div>
    </div>

    <div id="actionsLog" class="box" style="margin-top:12px">
      <h3>Recent</h3>
      <pre id="log"></pre>
    </div>

    <div id="craftBox" class="box" style="display:none;margin-top:12px">
      <h3>Crafting</h3>
      <div id="craftChoices"></div>
      <button onclick="submitCraft()">Craft Selected</button>
      <button onclick="closeCraft()">Cancel</button>
    </div>
  </div>
</div>

<script>
let player = null;
let playerId = localStorage.getItem('roe_pid') || null;

function log(msg){
  const p = document.getElementById('log');
  p.textContent = (new Date()).toLocaleTimeString()+ " — " + msg + "\\n" + p.textContent;
}

async function createPlayer(){
  const name = document.getElementById('name').value || 'Anon';
  const res = await fetch('/api/create_player', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name})});
  const data = await res.json();
  player = data.player;
  playerId = player.id;
  localStorage.setItem('roe_pid', playerId);
  document.getElementById('createBox').style.display = 'none';
  document.getElementById('game').style.display = 'block';
  document.getElementById('title').textContent = 'Welcome, ' + player.name;
  refresh();
}

async function refresh(){
  if(!playerId) return;
  const res = await fetch('/api/player/' + playerId);
  const doc = await res.json();
  player = doc.player;
  // render player
  document.getElementById('playerInfo').innerHTML = `
    <strong>${player.name}</strong> • Level ${player.level} (XP ${player.xp}/${player.xp_to_next})<br/>
    <span class="muted">Location:</span> ${player.location}<br/>
    <div class="muted">Stats: Str ${player.stats.strength}, Int ${player.stats.intelligence}, Agi ${player.stats.agility}</div>
  `;
  // inventory
  document.getElementById('inventory').innerHTML = `
    <div><strong>Elements:</strong> ${player.inventory.elements.join(', ')}</div>
    <div style="margin-top:6px"><strong>Items:</strong> ${player.inventory.items.map(i=>i.name||i).slice(0,8).join(', ') || '—'}</div>
  `;
  // chronicle
  document.getElementById('chronicle').innerHTML = player.chronicle.slice(0,15).map(c=>`<div><small class="muted">${new Date(c.t).toLocaleString()}</small><div>${c.e}</div></div>`).join('<hr/>');
  // encounters
  const encs = player.encounters || {};
  const encIds = Object.keys(encs || {});
  if(encIds.length>0){
    document.getElementById('encounters').style.display='block';
    const first = encs[encIds[0]];
    document.getElementById('encounterBox').innerHTML = `
      <div><strong>${first.name}</strong> • HP ${first.hp}/${first.max_hp}</div>
      <div style="margin-top:8px">
        <button onclick="fight('${first.id}','attack')">Attack</button>
        <button onclick="fight('${first.id}','flee')">Flee</button>
      </div>
    `;
  } else {
    document.getElementById('encounters').style.display='none';
    document.getElementById('encounterBox').innerHTML = '';
  }
}

async function doAction(action){
  if(!playerId) { alert('Create a player first'); return; }
  const res = await fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({player_id:playerId, action})});
  const doc = await res.json();
  if(doc.error) { log('Error: '+doc.error); return; }
  if(doc.result === 'encounter'){
    log('Encounter: ' + doc.enemy.name);
  } else if(doc.result === 'found'){
    log(doc.text);
  } else if(doc.result === 'rested'){
    log('You rested.');
  } else if(doc.result === 'discovered'){
    log('New blueprint discovered! ' + doc.blueprint.id);
  } else {
    log('Action: ' + action);
  }
  refresh();
}

async function fight(eid, cmd){
  const res = await fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({player_id:playerId, action:'fight', payload:{enemy_id:eid, cmd}})});
  const doc = await res.json();
  if(doc.log) doc.log.forEach(l=>log(l));
  if(doc.result === 'victory'){
    log('Victory! Loot: ' + (doc.loot||[]).join(', ') + ' (+XP ' + doc.xp + ')');
  }
  refresh();
}

function openCraft(){
  const arr = player.inventory.elements || [];
  if(arr.length < 2){ alert('Not enough elements to craft'); return; }
  document.getElementById('craftBox').style.display='block';
  const choices = arr.map(e=>`<label style="display:inline-block;margin:4px;padding:6px;background:#07203a;border-radius:6px"><input type="checkbox" value="${e}" /> ${e}</label>`).join('');
  document.getElementById('craftChoices').innerHTML = choices;
}

function closeCraft(){ document.getElementById('craftBox').style.display='none'; }

async function submitCraft(){
  const boxes = Array.from(document.querySelectorAll('#craftChoices input:checked')).map(i=>i.value);
  if(boxes.length < 2){ alert('Select 2+ elements'); return; }
  const res = await fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({player_id:playerId, action:'craft', payload:{elements:boxes}})});
  const doc = await res.json();
  if(doc.item){
    log('Crafted: ' + doc.item.name + ' (' + doc.item.rarity + ')');
    if(doc.discovered && !doc.discovered.already) log('You discovered a new blueprint!');
  } else if(doc.error){
    log('Craft error: '+doc.error);
  }
  closeCraft();
  refresh();
}

// auto-refresh every 4s to keep UI synced
setInterval(()=>{ if(playerId) refresh(); }, 4000);

if(playerId){
  // try to fetch player to auto-load
  fetch('/api/player/' + playerId).then(r=>r.json()).then(d=>{
    if(d.player){
      player = d.player;
      document.getElementById('createBox').style.display='none';
      document.getElementById('game').style.display='block';
      document.getElementById('title').textContent = 'Welcome back, ' + player.name;
      refresh();
    } else {
      localStorage.removeItem('roe_pid');
    }
  }).catch(()=>localStorage.removeItem('roe_pid'));
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(INDEX_HTML)

# --- run server (if executed directly) ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
