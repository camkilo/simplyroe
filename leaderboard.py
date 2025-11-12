# leaderboard.py
# Leaderboard and reputation tracking

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

DATA_DIR = ".data"

def get_weekly_leaderboard() -> Dict:
    """
    Calculate weekly leaderboard based on NPC remixes, shares, and interactions
    """
    from npc_generator import load_npcs
    from sharing import load_shares
    from auth import load_users
    
    npcs = load_npcs()
    shares = load_shares()
    users = load_users()
    
    # Calculate cutoff for weekly stats (7 days ago)
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    
    # Track stats by creator
    creator_stats = defaultdict(lambda: {
        "username": "",
        "npcs_created": 0,
        "total_remixes": 0,
        "total_shares": 0,
        "total_interactions": 0,
        "reputation_score": 0
    })
    
    # Aggregate NPC stats
    for npc in npcs.values():
        creator_id = npc.get("creator_id")
        if not creator_id:
            continue
        
        # Get username
        user = users.get(creator_id)
        if user:
            creator_stats[creator_id]["username"] = user.get("username", "Unknown")
        
        # Only count recent creations for weekly board
        if npc.get("created_at", "") >= week_ago:
            creator_stats[creator_id]["npcs_created"] += 1
        
        # Count remixes and interactions (all time for popular NPCs)
        creator_stats[creator_id]["total_remixes"] += npc.get("remix_count", 0)
        creator_stats[creator_id]["total_interactions"] += npc.get("interactions", 0)
    
    # Aggregate share stats
    for share in shares.values():
        user_id = share.get("user_id")
        if not user_id:
            continue
        
        if share.get("created_at", "") >= week_ago:
            creator_stats[user_id]["total_shares"] += 1
        
        # Add view counts and remix conversions
        creator_stats[user_id]["total_interactions"] += share.get("view_count", 0)
        creator_stats[user_id]["total_remixes"] += share.get("remix_from_share", 0)
    
    # Calculate reputation scores
    for creator_id, stats in creator_stats.items():
        score = (
            stats["npcs_created"] * 10 +
            stats["total_remixes"] * 25 +
            stats["total_shares"] * 5 +
            stats["total_interactions"] * 1
        )
        stats["reputation_score"] = score
    
    # Sort by reputation score
    sorted_creators = sorted(
        [
            {"creator_id": cid, **stats}
            for cid, stats in creator_stats.items()
        ],
        key=lambda x: x["reputation_score"],
        reverse=True
    )
    
    return {
        "period": "weekly",
        "start_date": week_ago,
        "end_date": datetime.utcnow().isoformat() + "Z",
        "top_creators": sorted_creators[:20]
    }

def get_most_remixed_npcs(limit: int = 10) -> List[Dict]:
    """
    Get the most remixed NPCs of all time
    """
    from npc_generator import get_popular_npcs
    return get_popular_npcs(limit)

def get_trending_npcs(limit: int = 10) -> List[Dict]:
    """
    Get trending NPCs based on recent activity
    """
    from npc_generator import load_npcs
    
    npcs = load_npcs()
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    
    # Filter to recent NPCs and score them
    recent_npcs = []
    for npc in npcs.values():
        if npc.get("created_at", "") >= week_ago:
            score = (
                npc.get("remix_count", 0) * 3 +
                npc.get("share_count", 0) * 2 +
                npc.get("interactions", 0)
            )
            recent_npcs.append({
                **npc,
                "trending_score": score
            })
    
    # Sort by trending score
    sorted_npcs = sorted(
        recent_npcs,
        key=lambda x: x["trending_score"],
        reverse=True
    )
    
    return sorted_npcs[:limit]

def update_user_reputation(user_id: str):
    """
    Update a user's reputation score based on their content
    """
    from auth import load_users, save_users
    from npc_generator import load_npcs
    from sharing import load_shares
    
    users = load_users()
    user = users.get(user_id)
    
    if not user:
        return
    
    npcs = load_npcs()
    shares = load_shares()
    
    # Calculate reputation
    reputation = 0
    
    # Count user's NPCs and their impact
    for npc in npcs.values():
        if npc.get("creator_id") == user_id:
            reputation += 10  # Base for creating
            reputation += npc.get("remix_count", 0) * 25
            reputation += npc.get("share_count", 0) * 5
            reputation += npc.get("interactions", 0)
    
    # Count shares
    for share in shares.values():
        if share.get("user_id") == user_id:
            reputation += 5
            reputation += share.get("view_count", 0)
            reputation += share.get("remix_from_share", 0) * 15
    
    # Update user
    users[user_id]["reputation"] = reputation
    save_users(users)
    
    return reputation

def get_global_stats() -> Dict:
    """
    Get overall platform statistics
    """
    from npc_generator import load_npcs
    from sharing import load_shares
    from auth import load_users
    from rooms import load_rooms
    
    npcs = load_npcs()
    shares = load_shares()
    users = load_users()
    rooms = load_rooms()
    
    total_remixes = sum(npc.get("remix_count", 0) for npc in npcs.values())
    total_shares = len(shares)
    total_interactions = sum(npc.get("interactions", 0) for npc in npcs.values())
    
    return {
        "total_users": len(users),
        "total_npcs": len(npcs),
        "total_remixes": total_remixes,
        "total_shares": total_shares,
        "total_rooms": len(rooms),
        "total_interactions": total_interactions
    }
