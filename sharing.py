# sharing.py
# Content sharing with OG images and social features

import json
import os
import uuid
from datetime import datetime
from typing import Optional, Dict
from PIL import Image, ImageDraw, ImageFont
import io
import base64

DATA_DIR = ".data"
SHARES_FILE = os.path.join(DATA_DIR, "shares.json")
IMAGES_DIR = os.path.join(DATA_DIR, "share_images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

if not os.path.exists(SHARES_FILE):
    with open(SHARES_FILE, "w") as f:
        json.dump({}, f)

def load_shares():
    with open(SHARES_FILE, "r") as f:
        return json.load(f)

def save_shares(shares):
    with open(SHARES_FILE, "w") as f:
        json.dump(shares, f, indent=2)

def generate_og_image(npc_name: str, trait: str, backstory: str) -> str:
    """
    Generate an Open Graph preview image for sharing
    Returns: path to the generated image
    """
    # Create image
    width, height = 1200, 630
    bg_color = (11, 16, 32)  # Dark blue from the game theme
    text_color = (223, 231, 255)  # Light blue
    accent_color = (37, 99, 235)  # Blue accent
    
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use default font, fallback to basic
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        trait_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        trait_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([20, 20, width-20, height-20], outline=accent_color, width=3)
    
    # Draw title
    title_y = 80
    draw.text((60, title_y), npc_name, fill=text_color, font=title_font)
    
    # Draw trait badge
    trait_text = f"• {trait.upper()} •"
    trait_y = title_y + 70
    draw.text((60, trait_y), trait_text, fill=accent_color, font=trait_font)
    
    # Draw backstory (wrapped)
    backstory_y = trait_y + 60
    max_width = width - 120
    
    # Simple text wrapping
    words = backstory.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # Approximate width check (rough estimate)
        if len(test_line) * 12 < max_width:  # Rough character width estimation
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Limit to 3 lines as per backstory format
    lines = lines[:3]
    
    for i, line in enumerate(lines):
        draw.text((60, backstory_y + i * 35), line, fill=text_color, font=text_font)
    
    # Draw footer
    footer_y = height - 80
    draw.text((60, footer_y), "Realm of Echoes • Living World", fill=(159, 176, 255), font=text_font)
    
    # Save image
    image_id = str(uuid.uuid4())
    image_path = os.path.join(IMAGES_DIR, f"{image_id}.png")
    image.save(image_path, "PNG")
    
    return image_path

def create_share(user_id: str, npc_id: str, npc_data: Dict) -> Dict:
    """
    Create a shareable link for an NPC
    """
    shares = load_shares()
    
    share_id = str(uuid.uuid4())
    
    # Generate OG image
    image_path = generate_og_image(
        npc_data["name"],
        npc_data["trait"],
        npc_data["backstory"]
    )
    
    share = {
        "id": share_id,
        "user_id": user_id,
        "npc_id": npc_id,
        "npc_name": npc_data["name"],
        "image_path": image_path,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "view_count": 0,
        "remix_from_share": 0
    }
    
    shares[share_id] = share
    save_shares(shares)
    
    return share

def get_share(share_id: str) -> Optional[Dict]:
    shares = load_shares()
    share = shares.get(share_id)
    
    if share:
        # Increment view count
        shares[share_id]["view_count"] = share.get("view_count", 0) + 1
        save_shares(shares)
    
    return share

def increment_remix_from_share(share_id: str):
    """
    Track when someone remixes from a share link
    """
    shares = load_shares()
    if share_id in shares:
        shares[share_id]["remix_from_share"] = shares[share_id].get("remix_from_share", 0) + 1
        save_shares(shares)

def get_user_shares(user_id: str, limit: int = 20) -> list:
    """
    Get all shares created by a user
    """
    shares = load_shares()
    
    user_shares = [
        share for share in shares.values()
        if share["user_id"] == user_id
    ]
    
    # Sort by most recent
    sorted_shares = sorted(
        user_shares,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    
    return sorted_shares[:limit]

def get_popular_shares(limit: int = 10) -> list:
    """
    Get most viewed/remixed shares for leaderboard
    """
    shares = load_shares()
    
    share_list = list(shares.values())
    
    # Sort by view_count + remix_from_share
    sorted_shares = sorted(
        share_list,
        key=lambda x: x.get("view_count", 0) + x.get("remix_from_share", 0) * 5,  # Weight remixes higher
        reverse=True
    )
    
    return sorted_shares[:limit]
