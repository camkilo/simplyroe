
# Realm of Echoes — Living World

**A next-gen living web service where every player shapes a shared world through AI-driven creation, conversation, and emergent gameplay.**

## 🌟 Core Features

- **3D FPS Mode**: Immersive first-person 3D open world with amazing graphics (NEW!)
- **AI-Driven NPC Generation**: Create NPCs with unique names, traits, and 3-line backstories
- **Remix & Provenance**: Full lineage tracking for every creation with attribution
- **Social Sharing**: Share NPCs with auto-generated OG images and shareable links
- **Play Sessions**: Join rooms to interact with NPCs through branching dialogue
- **Leaderboard**: Weekly rankings for most remixed/shared content
- **Reputation System**: Earn reputation through creation, sharing, and remixing

## 🚀 Quick Start

### Installation
```bash
git clone <repo>
cd simplyroe
pip install -r requirements.txt
```

### Run the Server
```bash
python api.py
```

Visit:
- **3D FPS Mode**: http://localhost:8000 (default)
- **Classic 2D Mode**: http://localhost:8000/index.html
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### First Steps
1. Visit http://localhost:8000 for the **3D FPS Experience**
2. **Desktop**: Click to lock mouse pointer and start playing
3. **Desktop Controls**: Use WASD to move, mouse to look, E to gather, Left Click to attack
4. **Mobile Controls**: 
   - Touch joystick (bottom-left) to move
   - Drag right side of screen to look around
   - Tap screen to interact/attack
   - Use action buttons (bottom-right) for jump and gather
5. Or visit http://localhost:8000/index.html for the classic 2D experience
6. Create NPCs and explore the world!

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### NPCs
- `POST /api/npcs/create` - Create new NPC
- `GET /api/npcs/{id}` - Get NPC details
- `POST /api/npcs/remix` - Remix existing NPC
- `GET /api/npcs/popular` - Get popular NPCs
- `GET /api/npcs/trending` - Get trending NPCs

### Rooms & Sessions
- `POST /api/rooms/create` - Create play session
- `GET /api/rooms/{id}` - Get room details
- `POST /api/rooms/{id}/join` - Join room
- `POST /api/rooms/interact` - Interact with NPC

### Sharing
- `POST /api/share/{npc_id}` - Create share link
- `GET /share/{share_id}` - View shared NPC (with OG tags)
- `GET /api/share/{share_id}/image` - Get OG image

### Leaderboard
- `GET /api/leaderboard/weekly` - Weekly creator rankings
- `GET /api/leaderboard/remixed` - Most remixed NPCs
- `GET /api/stats` - Global platform stats

## 🏗️ Architecture

```
Backend: FastAPI (Python)
Frontend: 
  - 3D FPS: Three.js + WebGL 2.0 (default)
  - Classic: Vanilla JS + HTML/CSS
Storage: JSON files (PostgreSQL-ready)
Auth: JWT with bcrypt
Images: PIL for OG image generation
Real-time: WebSocket support (foundation ready)
Graphics: PBR materials, particle effects, dynamic lighting
```

## 📁 Project Structure

```
.
├── api.py                 # Main FastAPI application
├── auth.py               # Authentication & user management
├── npc_generator.py      # NPC creation & AI generation
├── rooms.py              # Play session management
├── sharing.py            # Social sharing & OG images
├── leaderboard.py        # Rankings & reputation
├── main.py               # Server entry point
├── frontend.html         # Classic web UI
├── static/
│   ├── fps3d.html       # 3D FPS interface (NEW)
│   ├── inventory-icons.js # Inventory art system (NEW)
│   └── index.html       # 2D world interface
├── docs/
│   ├── 3D_FPS_MODE.md   # 3D FPS documentation (NEW)
│   └── vision.md        # Core vision document
├── requirements.txt      # Python dependencies
└── .data/               # Data storage (auto-created)
    ├── users.json
    ├── npcs.json
    ├── rooms.json
    ├── shares.json
    └── share_images/
```

## 🎮 Core Gameplay Loops

1. **Create** → Players generate NPCs with AI-assisted backstories
2. **Play** → Join rooms and interact with NPCs through branching dialogue
3. **Iterate** → Remix and refine NPCs created by others
4. **Share** → Generate shareable links with auto-generated social previews
5. **Compete** → Climb leaderboards through remixes and shares

## 📱 Mobile Support

The 3D FPS mode now includes full mobile support with touch-based controls:

- **Virtual Joystick**: On-screen joystick (bottom-left) for character movement
- **Touch Camera**: Drag right side of screen to look around
- **Tap to Interact**: Tap screen to attack or interact with objects
- **Action Buttons**: Quick access buttons for jump and gather (bottom-right)
- **Optimized Performance**: Automatic quality adjustments for mobile devices

## 🔮 Next-Gen Features

- **Generative Collaborators**: NPCs with AI-driven dialogue (foundation ready)
- **Player-Owned Economy**: Reputation and provenance tracking
- **Remixability**: One-click remix with full attribution
- **Micro-Sessions**: 2-10 minute gameplay loops
- **Next-Gen Graphics**: PBR materials, advanced lighting, particle effects
- **Mobile-First**: Touch controls and performance optimization

## 🛠️ Development

### Running Tests
```bash
# Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/stats
```

### Future Enhancements
- [ ] Local LLM integration (llama.cpp)
- [ ] WebSocket real-time updates
- [ ] PostgreSQL migration
- [ ] Redis pub/sub for rooms
- [ ] Image generation for cosmetics
- [ ] Voice chat (WebRTC)
- [ ] Content moderation AI
- [x] Mobile-optimized UI with touch controls
- [x] Next-gen graphics with PBR materials

## 📖 Documentation

- `docs/vision.md` — Core vision and mechanics
- `/docs` endpoint — Interactive API documentation

## 🤝 Contributing

See `.github/CONTRIBUTING.md` for contribution guidelines.

Labels: `help wanted`, `bug`, `enhancement`, `feature`, `design`

## 📜 License

See LICENSE.md

---

**Built for infinite emergent systems where players shape reality** ⚔️✨
