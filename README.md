# Octopus Ink Slime

![Octopus Ink Slime Logo](assets/images/logo.png)

A fast-paced underwater action game where you play as an octopus using ink slime to sink enemy ships!

## Game Description

In Octopus Ink Slime, you control a clever octopus armed with colorful ink slime. Your mission is to defend your underwater home from invading ships by shooting ink at them until they sink. As you progress through the levels, you'll encounter different types of ships, obstacles, and gain access to new ink colors with special properties.

### Key Features

- **Sequential Arm Firing**: Your octopus has 10 arms that fire in sequence, creating a continuous stream of ink projectiles.
- **Progressive Ink Colors**: Each level introduces a new ink color with unique properties and effects.
- **Multiple Enemy Types**: Battle against ships of various sizes, captains that panic when their ships sink, and turtles that can block your ink shots.
- **Bonus Targets**: Catch fish for bonus points and power-ups.
- **Dynamic Levels**: Five unique levels with increasing difficulty and different underwater environments.
- **Visual Effects**: Enjoy colorful splashes, explosions, and particle effects.

## Installation

### Prerequisites

- Python 3.7 or higher
- Pygame 2.0.0 or higher

### Option 1: Automatic Installation

1. Clone or download this repository
2. Run the setup script:

```bash
python setup.py
```

This will:
- Install all required dependencies
- Create necessary directories
- Set up the game environment
- Create a desktop shortcut (if supported on your platform)

### Option 2: Manual Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install pygame>=2.0.0 psutil>=5.8.0 numpy>=1.19.0 pillow>=8.0.0
```

3. Run the game:

```bash
python main.py
```

## Controls

- **Arrow Keys** or **WASD**: Move the octopus
- **Spacebar**: Hold to fire ink continuously
- **Escape**: Pause game / Access menu
- **F3**: Toggle debug mode
- **F4-F8**: Toggle various debug displays (when in debug mode)

## Gameplay Tips

1. **Aim Carefully**: Each ship requires multiple hits to sink. Focus your fire on one ship at a time for maximum efficiency.

2. **Watch Out for Turtles**: Turtles can block your ink shots with their shells. Try to maneuver around them or wait for them to turn.

3. **Catch Fish**: Fish not only give you bonus points but can also provide power-ups like temporary speed boosts or rapid-fire abilities.

4. **Use the Environment**: Some levels have currents or obstacles that can either help or hinder your movement. Learn to use them to your advantage.

5. **Captain Panic**: When a ship starts to sink, its captain will panic and jump overboard. These floating captains are vulnerable and worth extra points!

6. **Ink Management**: Different ink colors have different properties:
   - **Level 1 (Dark Blue)**: Basic damage
   - **Level 2 (Purple)**: Increased damage
   - **Level 3 (Green)**: High damage with splash effect
   - **Level 4 (Red)**: Very high damage with burning effect
   - **Level 5 (Rainbow)**: Maximum damage with special effects

7. **Movement Strategy**: Stay mobile to avoid enemy projectiles, but try to maintain a good firing position.

## Level Progression

1. **Level 1: Shallow Waters**
   - Slow ships, mostly open board
   - Dark Blue Ink
   - Easy difficulty

2. **Level 2: Coral Reef**
   - Medium speed ships, more obstacles
   - Purple Ink
   - Medium-Easy difficulty

3. **Level 3: Kelp Forest**
   - Medium-Fast ships, many obstacles
   - Green Ink
   - Medium difficulty

4. **Level 4: Deep Trench**
   - Fast ships, many obstacles with movement
   - Red Ink
   - Medium-Hard difficulty

5. **Level 5: Volcanic Vent**
   - Very fast ships, complex obstacle patterns
   - Rainbow Ink
   - Hard difficulty

## Debug Mode

Press **F3** to toggle debug mode, which displays:

- FPS counter
- Entity count
- Collision areas
- Entity boundaries
- Spatial grid

Additional debug toggles (when debug mode is active):
- **F4**: Toggle FPS display
- **F5**: Toggle entity count display
- **F6**: Toggle collision areas display
- **F7**: Toggle entity boundaries display
- **F8**: Toggle spatial grid display

## Performance Optimizations

The game includes several performance optimizations:

1. **Object Pooling**: Ink projectiles are reused instead of being created and destroyed repeatedly.
2. **Spatial Partitioning**: A grid-based system for efficient collision detection.
3. **Asset Caching**: Game assets are loaded once and reused throughout the game.

## Development

The game is built using a component-based architecture with the following key systems:

- **Entity Component System**: Entities are composed of various components that define their behavior.
- **Scene Management**: Different game states (menu, gameplay, etc.) are managed by a scene manager.
- **Level System**: Levels are defined by data files and generated procedurally.
- **Physics System**: Handles movement, collision detection, and response.
- **Rendering System**: Manages drawing entities, UI elements, and effects.

## Credits

### Development Team

- Game Design: Octopus Games Team
- Programming: Ink Slime Developers
- Art & Animation: Deep Sea Studios
- Sound & Music: Underwater Acoustics

### Assets

- Sound effects: Various sources with appropriate licenses
- Music: Original compositions for Octopus Ink Slime
- Fonts: Open-source fonts with appropriate licenses

### Special Thanks

- The Pygame community for their excellent library and support
- All the playtesters who provided valuable feedback
- You, for playing our game!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2025 Octopus Games. All rights reserved.