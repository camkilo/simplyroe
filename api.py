# api.py
# Main API for the AI-driven living web service

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
import uvicorn
import os

# Import our modules
from auth import (
    create_user, authenticate_user, get_user_by_id, 
    create_access_token, decode_token, update_user
)
from npc_generator import (
    create_npc, get_npc, remix_npc, get_popular_npcs,
    increment_share_count, get_npc_lineage
)
from rooms import (
    create_room, get_room, join_room, leave_room,
    add_chat_message, add_npc_interaction, get_active_rooms,
    close_room, get_room_participants
)
from sharing import (
    create_share, get_share, increment_remix_from_share,
    get_user_shares, get_popular_shares
)
from leaderboard import (
    get_weekly_leaderboard, get_most_remixed_npcs,
    get_trending_npcs, update_user_reputation, get_global_stats
)
from moderation import (
    check_rate_limit, validate_npc_content, validate_message,
    get_user_rate_limit_status, report_content
)

app = FastAPI(title="Realm of Echoes - Living World API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for requests
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CreateNPCRequest(BaseModel):
    name: Optional[str] = None
    trait: Optional[str] = None
    backstory: Optional[str] = None

class RemixNPCRequest(BaseModel):
    original_npc_id: str
    name: Optional[str] = None
    trait: Optional[str] = None
    backstory: Optional[str] = None

class CreateRoomRequest(BaseModel):
    name: str
    npc_id: Optional[str] = None
    max_players: int = 4

class ChatMessageRequest(BaseModel):
    room_id: str
    message: str

class NPCInteractionRequest(BaseModel):
    room_id: str
    npc_id: str
    dialogue_id: str

# Helper to get current user from token
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# ===== Authentication Endpoints =====

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    user, error = create_user(req.email, req.password, req.username)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Create access token
    access_token = create_access_token({"user_id": user["id"]})
    
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    user, error = authenticate_user(req.email, req.password)
    
    if error:
        raise HTTPException(status_code=401, detail=error)
    
    # Create access token
    access_token = create_access_token({"user_id": user["id"]})
    
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/api/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    return {"user": user}

# ===== NPC Management Endpoints =====

@app.post("/api/npcs/create")
async def api_create_npc(req: CreateNPCRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    # Check rate limit
    allowed, error = check_rate_limit(user["id"], "npc_create")
    if not allowed:
        raise HTTPException(status_code=429, detail=error)
    
    # Validate content
    valid, error = validate_npc_content(req.name or "", req.trait or "", req.backstory or "")
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    npc = create_npc(
        creator_id=user["id"],
        name=req.name,
        trait=req.trait,
        custom_backstory=req.backstory
    )
    
    # Update user reputation
    update_user_reputation(user["id"])
    
    return {"npc": npc}

@app.get("/api/npcs/{npc_id}")
async def api_get_npc(npc_id: str):
    npc = get_npc(npc_id)
    
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    # Get lineage for attribution
    lineage = get_npc_lineage(npc_id)
    
    return {
        "npc": npc,
        "lineage": lineage
    }

@app.post("/api/npcs/remix")
async def api_remix_npc(req: RemixNPCRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    # Check rate limit
    allowed, error = check_rate_limit(user["id"], "npc_remix")
    if not allowed:
        raise HTTPException(status_code=429, detail=error)
    
    # Validate content if provided
    if req.name or req.trait or req.backstory:
        valid, error = validate_npc_content(req.name or "", req.trait or "", req.backstory or "")
        if not valid:
            raise HTTPException(status_code=400, detail=error)
    
    changes = {}
    if req.name:
        changes["name"] = req.name
    if req.trait:
        changes["trait"] = req.trait
    if req.backstory:
        changes["backstory"] = req.backstory
    
    new_npc = remix_npc(user["id"], req.original_npc_id, changes)
    
    if not new_npc:
        raise HTTPException(status_code=404, detail="Original NPC not found")
    
    # Update user reputation
    update_user_reputation(user["id"])
    
    return {"npc": new_npc}

@app.get("/api/npcs/popular")
async def api_get_popular_npcs(limit: int = 10):
    npcs = get_popular_npcs(limit)
    return {"npcs": npcs}

@app.get("/api/npcs/trending")
async def api_get_trending_npcs(limit: int = 10):
    npcs = get_trending_npcs(limit)
    return {"npcs": npcs}

# ===== Room/Session Endpoints =====

@app.post("/api/rooms/create")
async def api_create_room(req: CreateRoomRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    room = create_room(
        creator_id=user["id"],
        name=req.name,
        npc_id=req.npc_id,
        max_players=req.max_players
    )
    
    return {"room": room}

@app.get("/api/rooms/{room_id}")
async def api_get_room(room_id: str):
    room = get_room(room_id)
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Get NPC data if room has an NPC
    npc_data = None
    if room.get("npc_id"):
        npc_data = get_npc(room["npc_id"])
    
    # Get active participants
    participants = list(get_room_participants(room_id))
    
    return {
        "room": room,
        "npc": npc_data,
        "active_participants": participants
    }

@app.post("/api/rooms/{room_id}/join")
async def api_join_room(room_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    room = join_room(room_id, user["id"])
    
    if not room:
        raise HTTPException(status_code=400, detail="Cannot join room")
    
    return {"room": room}

@app.post("/api/rooms/{room_id}/leave")
async def api_leave_room(room_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    leave_room(room_id, user["id"])
    
    return {"success": True}

@app.post("/api/rooms/{room_id}/chat")
async def api_room_chat(room_id: str, req: ChatMessageRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    # Check rate limit
    allowed, error = check_rate_limit(user["id"], "chat_message")
    if not allowed:
        raise HTTPException(status_code=429, detail=error)
    
    # Validate message
    valid, error = validate_message(req.message)
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    success = add_chat_message(room_id, user["id"], req.message)
    
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {"success": True}

@app.post("/api/rooms/interact")
async def api_npc_interaction(req: NPCInteractionRequest, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    npc = get_npc(req.npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    # Find the dialogue response
    dialogue_tree = npc.get("dialogue_tree", [])
    response_text = "..."
    
    for node in dialogue_tree:
        if node["id"] == "start":
            for response in node.get("responses", []):
                if response["id"] == req.dialogue_id:
                    response_text = response["response"]
                    break
    
    # Record interaction
    add_npc_interaction(req.room_id, user["id"], req.npc_id, req.dialogue_id, response_text)
    
    # Increment NPC interaction count
    from npc_generator import load_npcs, save_npcs
    npcs = load_npcs()
    if req.npc_id in npcs:
        npcs[req.npc_id]["interactions"] = npcs[req.npc_id].get("interactions", 0) + 1
        save_npcs(npcs)
    
    return {
        "response": response_text,
        "npc_name": npc["name"]
    }

@app.get("/api/rooms")
async def api_get_active_rooms(limit: int = 20):
    rooms = get_active_rooms(limit)
    return {"rooms": rooms}

@app.post("/api/rooms/{room_id}/close")
async def api_close_room(room_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    success = close_room(room_id, user["id"])
    
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to close room")
    
    return {"success": True}

# ===== Sharing Endpoints =====

@app.post("/api/share/{npc_id}")
async def api_create_share(npc_id: str, authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    
    npc = get_npc(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    # Increment NPC share count
    increment_share_count(npc_id)
    
    # Create share
    share = create_share(user["id"], npc_id, npc)
    
    # Update user reputation
    update_user_reputation(user["id"])
    
    # Generate share URL
    share_url = f"/share/{share['id']}"
    
    return {
        "share": share,
        "share_url": share_url
    }

@app.get("/api/share/{share_id}")
async def api_get_share(share_id: str):
    share = get_share(share_id)
    
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    
    # Get NPC data
    npc = get_npc(share["npc_id"])
    
    return {
        "share": share,
        "npc": npc
    }

@app.get("/api/share/{share_id}/image")
async def api_get_share_image(share_id: str):
    share = get_share(share_id)
    
    if not share or not os.path.exists(share["image_path"]):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(share["image_path"], media_type="image/png")

@app.get("/api/shares/popular")
async def api_get_popular_shares(limit: int = 10):
    shares = get_popular_shares(limit)
    return {"shares": shares}

@app.get("/api/shares/user/{user_id}")
async def api_get_user_shares(user_id: str, limit: int = 20):
    shares = get_user_shares(user_id, limit)
    return {"shares": shares}

# ===== Leaderboard Endpoints =====

@app.get("/api/leaderboard/weekly")
async def api_get_weekly_leaderboard():
    leaderboard = get_weekly_leaderboard()
    return leaderboard

@app.get("/api/leaderboard/remixed")
async def api_get_most_remixed(limit: int = 10):
    npcs = get_most_remixed_npcs(limit)
    return {"npcs": npcs}

@app.get("/api/stats")
async def api_get_stats():
    stats = get_global_stats()
    return {"stats": stats}

# ===== Moderation Endpoints =====

@app.get("/api/moderation/rate-limits")
async def api_get_rate_limits(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    status = get_user_rate_limit_status(user["id"])
    return {"rate_limits": status}

# ===== Health Check =====

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "realm-of-echoes"}

# ===== HTML Frontend =====

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the 3D FPS application HTML"""
    html_file = "static/fps3d.html"
    if os.path.exists(html_file):
        with open(html_file, "r") as f:
            return HTMLResponse(f.read())
    else:
        return HTMLResponse("<h1>Realm of Echoes - API Running</h1><p>3D FPS mode not found. Use /docs for API documentation.</p>")

@app.get("/index.html", response_class=HTMLResponse)
async def classic_frontend():
    """Serve the classic 2D frontend"""
    html_file = "frontend.html"
    if os.path.exists(html_file):
        with open(html_file, "r") as f:
            return HTMLResponse(f.read())
    else:
        return HTMLResponse("<h1>Classic frontend not found</h1>")

# Share page for social sharing
@app.get("/share/{share_id}", response_class=HTMLResponse)
async def share_page(share_id: str):
    try:
        share = get_share(share_id)
        if not share:
            return HTMLResponse("<h1>Share not found</h1>", status_code=404)
        
        npc = get_npc(share["npc_id"])
        if not npc:
            return HTMLResponse("<h1>NPC not found</h1>", status_code=404)
        
        # HTML escape user content to prevent XSS
        import html
        safe_name = html.escape(npc['name'])
        safe_trait = html.escape(npc['trait'])
        safe_backstory = html.escape(npc['backstory'])
        safe_npc_id = html.escape(npc['id'])
        safe_share_id = html.escape(share_id)
        
        # Simple share page with OG meta tags
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{safe_name} - Realm of Echoes</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{safe_name} - {safe_trait}">
    <meta property="og:description" content="{safe_backstory[:200]}">
    <meta property="og:image" content="/api/share/{safe_share_id}/image">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{safe_name} - {safe_trait}">
    <meta name="twitter:description" content="{safe_backstory[:200]}">
    <meta name="twitter:image" content="/api/share/{safe_share_id}/image">
    
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: #0b1020;
            color: #dfe7ff;
            padding: 40px 20px;
            margin: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #0f1724;
            border: 1px solid #1f2a44;
            border-radius: 12px;
            padding: 40px;
        }}
        h1 {{
            color: #2563eb;
            margin-top: 0;
        }}
        .trait {{
            background: #14203a;
            padding: 8px 16px;
            border-radius: 999px;
            display: inline-block;
            margin: 12px 0;
            font-weight: 600;
        }}
        .backstory {{
            line-height: 1.6;
            margin: 24px 0;
        }}
        .actions {{
            margin-top: 32px;
        }}
        button {{
            background: #2563eb;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 12px;
        }}
        button:hover {{
            background: #1d4ed8;
        }}
        .secondary {{
            background: #1f2a44;
        }}
        .secondary:hover {{
            background: #2a3a54;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{safe_name}</h1>
        <div class="trait">• {safe_trait.upper()} •</div>
        <div class="backstory">{safe_backstory}</div>
        
        <div class="actions">
            <button onclick="window.location.href='/api/npcs/{safe_npc_id}'">View Full NPC</button>
            <button class="secondary" onclick="window.location.href='/'">Create Your Own</button>
        </div>
        
        <div style="margin-top: 32px; padding-top: 32px; border-top: 1px solid #1f2a44; color: #9fb0ff; font-size: 14px;">
            <p>Shared by a player in Realm of Echoes</p>
            <p>Views: {share.get('view_count', 0)} | Remixes: {share.get('remix_from_share', 0)}</p>
        </div>
    </div>
</body>
</html>
        """
        return HTMLResponse(html_content)
    except Exception as e:
        # Don't expose stack trace details to users
        return HTMLResponse("<h1>Error loading share</h1><p>An error occurred while loading this share.</p>", status_code=500)

if __name__ == "__main__":
    print("🌍 Starting Realm of Echoes - Living World API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
