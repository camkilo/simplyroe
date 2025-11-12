# 3D FPS Mode - Realm of Echoes

## Overview
The 3D First-Person Shooter mode transforms Realm of Echoes into an immersive 3D open-world experience with amazing graphics powered by Three.js.

## Features

### Graphics & Visuals
- **Advanced Lighting System**
  - Directional sunlight with realistic shadows (4096x4096 shadow maps)
  - Hemisphere lighting for natural sky illumination
  - Dynamic point lights for atmospheric effects
  - Ambient occlusion and soft shadows
  
- **Material System**
  - Physically-based rendering (PBR) materials
  - Metallic and roughness properties per biome
  - Emissive materials for lava, crystals, and enemies
  - Specular highlights on water and ice

- **Particle Effects**
  - Resource gathering sparkles
  - Combat hit effects
  - Enemy death explosions
  - Physics-based particle movement with gravity

- **Animation System**
  - Bobbing resources with rotation
  - Enemy idle animations
  - Smooth camera movements
  - Dynamic shadows

### World Generation
- **8 Unique Biomes**
  - Forest: Dense with resources, greenery
  - Plains: Open grasslands
  - Desert: Sandy terrain with copper deposits
  - Water: Reflective, translucent surfaces
  - Mountain: Elevated rocky terrain
  - Ice: Frozen, slippery surfaces
  - Lava: Glowing, dangerous terrain
  - Swamp: Murky, herb-rich areas

- **Procedural Generation**
  - Infinite world generation
  - Height-mapped terrain
  - Biome-specific resource distribution
  - Dynamic enemy spawning

### Gameplay Systems

#### Movement
- **WASD** - Forward, backward, strafe
- **Mouse** - Look around (pointer lock)
- **Space** - Jump
- **Shift** - Sprint (2x speed)
- **Smooth physics** with acceleration/deceleration

#### Combat
- **Left Click** - Attack with raycasting
- **Visual feedback** on hits
- **Enemy AI** - Follows and attacks player
- **Health system** with damage calculation
- **Loot drops** on enemy death

#### Resource Gathering
- **E Key** - Gather resources in crosshair
- **8 Resource Types**: Wood, Stone, Iron, Copper, Herbs, Crystal, Ice, Mud
- **Visual distinction** with metallic/emissive properties
- **Animated resources** bob and rotate

#### Inventory System
- **5 Inventory Slots** with hotbar
- **1-5 Keys** - Quick select slots
- **Visual icons** for items
- **Rarity indicators** with color coding
- **Crafting system** - Combine 2+ items (Q key)

### HUD & Interface
- **Crosshair** - Center screen targeting
- **Stats Panel** 
  - Health
  - XP
  - Current biome
  - 3D coordinates
- **Controls Guide** - Always visible
- **Inventory Bar** - Bottom of screen
- **Message System** - Temporary notifications

## Controls

```
Movement:
  W - Move Forward
  S - Move Backward
  A - Strafe Left
  D - Strafe Right
  Space - Jump
  Shift - Sprint

Combat & Interaction:
  Left Click - Attack
  E - Gather Resources
  Q - Craft Items

Inventory:
  1-5 - Select Hotbar Slot

Camera:
  Mouse - Look Around
  ESC - Release Mouse Lock
```

## Technical Details

### Graphics Pipeline
- **Renderer**: WebGL 2.0 via Three.js
- **Shadows**: PCF soft shadows at 4096x4096 resolution
- **Fog**: Exponential fog (50-200 units)
- **Anti-aliasing**: MSAA enabled
- **Performance**: 60 FPS target

### Asset Loading
- **Three.js CDN**: v0.160.0
- **ES6 Modules**: Import maps for clean imports
- **No external assets**: All generated procedurally

### World Structure
- **Chunk Size**: 10x10 units
- **World Size**: 200x200 units (expandable)
- **Draw Distance**: 200 units with fog
- **Height Variation**: 0.2-5 units depending on biome

## Performance Tips

1. **Lower shadow quality** - Reduce shadow map size for better FPS
2. **Reduce particle count** - Modify particle system for older hardware
3. **Decrease draw distance** - Reduce fog far distance
4. **Disable shadows** - Set `renderer.shadowMap.enabled = false`

## Future Enhancements

- [ ] Normal maps for terrain detail
- [ ] Texture atlases for variety
- [ ] Advanced enemy models with animations
- [ ] Weather system (rain, snow)
- [ ] Day/night cycle
- [ ] Multiplayer support
- [ ] Sound effects and music
- [ ] Advanced crafting recipes
- [ ] Building system
- [ ] Questline integration

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+ (limited)
- ❌ IE11 (not supported)

## Accessibility

The 3D FPS mode requires:
- Mouse for camera control
- Keyboard for movement
- WebGL 2.0 support
- Minimum 4GB RAM recommended
- Dedicated GPU recommended for best experience

## Credits

Built with:
- [Three.js](https://threejs.org/) - 3D graphics library
- WebGL - Low-level graphics API
- Pointer Lock API - Mouse control
- ES6 Modules - Clean code structure
