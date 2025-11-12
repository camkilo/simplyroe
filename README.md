
# Realm of Echoes — Living World

**A next-gen living web service where every player shapes a shared world through AI-driven creation, conversation, and emergent gameplay.**

## 🌟 Core Features

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
- **App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### First Steps
1. Register an account at http://localhost:8000
2. Create your first NPC
3. Share it with the community
4. Remix other players' creations

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
Frontend: Vanilla JS + HTML/CSS (embedded)
Storage: JSON files (PostgreSQL-ready)
Auth: JWT with bcrypt
Images: PIL for OG image generation
Real-time: WebSocket support (foundation ready)
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
├── frontend.html         # Web UI
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

## 🔮 Next-Gen Features

- **Generative Collaborators**: NPCs with AI-driven dialogue (foundation ready)
- **Player-Owned Economy**: Reputation and provenance tracking
- **Remixability**: One-click remix with full attribution
- **Micro-Sessions**: 2-10 minute gameplay loops

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
- [ ] Mobile-optimized UI

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
