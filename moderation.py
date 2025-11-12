# moderation.py
# Content moderation and rate limiting

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from collections import defaultdict

DATA_DIR = ".data"
RATE_LIMITS_FILE = os.path.join(DATA_DIR, "rate_limits.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(RATE_LIMITS_FILE):
    with open(RATE_LIMITS_FILE, "w") as f:
        json.dump({}, f)

# In-memory rate limiting (would use Redis in production)
rate_limit_tracker: Dict[str, List[datetime]] = defaultdict(list)

# Rate limits (per hour)
RATE_LIMITS = {
    "npc_create": 10,      # 10 NPCs per hour
    "npc_remix": 20,       # 20 remixes per hour
    "share_create": 15,    # 15 shares per hour
    "room_create": 5,      # 5 rooms per hour
    "chat_message": 100    # 100 messages per hour
}

# Content filters - simple keyword blocking for MVP
BLOCKED_WORDS = [
    # Add inappropriate words here
    "spam", "scam", "hack"
]

def check_rate_limit(user_id: str, action: str) -> tuple[bool, Optional[str]]:
    """
    Check if user is within rate limits for an action
    Returns: (allowed, error_message)
    """
    if action not in RATE_LIMITS:
        return True, None
    
    key = f"{user_id}:{action}"
    now = datetime.utcnow()
    
    # Clean up old entries (older than 1 hour)
    rate_limit_tracker[key] = [
        timestamp for timestamp in rate_limit_tracker[key]
        if now - timestamp < timedelta(hours=1)
    ]
    
    # Check if limit exceeded
    limit = RATE_LIMITS[action]
    if len(rate_limit_tracker[key]) >= limit:
        return False, f"Rate limit exceeded. Max {limit} {action} per hour."
    
    # Add current timestamp
    rate_limit_tracker[key].append(now)
    
    return True, None

def filter_content(text: str) -> tuple[bool, Optional[str]]:
    """
    Filter content for inappropriate words
    Returns: (passed, reason)
    """
    if not text:
        return True, None
    
    text_lower = text.lower()
    
    # Check for blocked words
    for word in BLOCKED_WORDS:
        if word in text_lower:
            return False, f"Content contains inappropriate word: {word}"
    
    # Check length limits
    if len(text) > 5000:
        return False, "Content too long (max 5000 characters)"
    
    # Check for excessive repetition (simple check)
    words = text_lower.split()
    if len(words) > 10:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            return False, "Content appears to be spam (too repetitive)"
    
    return True, None

def report_content(user_id: str, content_type: str, content_id: str, reason: str):
    """
    Report inappropriate content for review
    In production, this would create a moderation queue
    """
    from auth import load_users, save_users
    
    users = load_users()
    
    # Track reports
    if "reports" not in users[user_id]:
        users[user_id]["reports"] = []
    
    report = {
        "content_type": content_type,
        "content_id": content_id,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    users[user_id]["reports"].append(report)
    save_users(users)
    
    # In production: send to moderation queue, alert admins, etc.
    return report

def get_user_rate_limit_status(user_id: str) -> Dict:
    """
    Get current rate limit status for a user
    """
    now = datetime.utcnow()
    status = {}
    
    for action, limit in RATE_LIMITS.items():
        key = f"{user_id}:{action}"
        
        # Clean up old entries
        rate_limit_tracker[key] = [
            timestamp for timestamp in rate_limit_tracker[key]
            if now - timestamp < timedelta(hours=1)
        ]
        
        current = len(rate_limit_tracker[key])
        status[action] = {
            "current": current,
            "limit": limit,
            "remaining": max(0, limit - current)
        }
    
    return status

def validate_npc_content(name: str, trait: str, backstory: str) -> tuple[bool, Optional[str]]:
    """
    Validate NPC content before creation
    """
    # Check name
    if name:
        passed, reason = filter_content(name)
        if not passed:
            return False, f"Name validation failed: {reason}"
        
        if len(name) > 100:
            return False, "Name too long (max 100 characters)"
    
    # Check trait
    if trait:
        passed, reason = filter_content(trait)
        if not passed:
            return False, f"Trait validation failed: {reason}"
        
        if len(trait) > 50:
            return False, "Trait too long (max 50 characters)"
    
    # Check backstory
    if backstory:
        passed, reason = filter_content(backstory)
        if not passed:
            return False, f"Backstory validation failed: {reason}"
        
        if len(backstory) > 1000:
            return False, "Backstory too long (max 1000 characters)"
    
    return True, None

def validate_message(message: str) -> tuple[bool, Optional[str]]:
    """
    Validate chat message
    """
    if not message or len(message.strip()) == 0:
        return False, "Message cannot be empty"
    
    if len(message) > 500:
        return False, "Message too long (max 500 characters)"
    
    return filter_content(message)
