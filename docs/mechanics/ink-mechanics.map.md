# Ink Mechanics

## Overview

The Ink Mechanics system is the core gameplay mechanic of the Ink Slime game, providing the primary offensive capability for the player and defining the central interaction between the player and enemy ships. This system manages how ink projectiles are created, fired, and interact with the game world.

Ink mechanics are fundamental to the game's identity and progression. The player controls an octopus that fires ink projectiles at enemy ships, causing them to take on ink and eventually sink. As the player progresses through levels, they gain access to different ink colors with increasingly powerful effects, creating a sense of progression and escalating challenge.

The system handles the creation and management of ink projectiles, their physical properties, collision detection with ships and other entities, visual effects when ink hits targets, and the accumulation of ink in ships that eventually leads to their sinking. It also manages the weapon system of the octopus, including the multi-arm firing mechanism that allows for strategic shooting patterns.

The Ink Mechanics system follows a component-based design pattern, with specialized components for ink projectiles (InkSlimeComponent), ship ink accumulation (ShipInkLoadComponent), and weapon management (WeaponComponent).

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Ink Mechanics System                      │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Weapon     │ │  Ink Slime  │ │  Ship Ink   │ │  Effect   │ │
│  │  Component  │ │  Component  │ │  Load       │ │  Manager  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Game Entity System                         │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Player     │ │  Ink Slime  │ │  Ship       │ │  Captain  │ │
│  │  Entity     │ │  Entity     │ │  Entity     │ │  Entity   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### Weapon Component

The Weapon Component is attached to the player (octopus) entity and manages the firing of ink projectiles. It implements a multi-arm firing system where the octopus has multiple arms positioned in a circular pattern, each capable of firing ink projectiles.

**Responsibilities:**
- Manage the octopus's 10 arms in a circular pattern
- Track cooldown timers for each arm
- Handle arm rotation and selection
- Create and fire ink projectiles
- Apply damage multipliers based on which arm is firing (center arm is more powerful)
- Manage continuous firing mode

#### Ink Slime Component

The Ink Slime Component is attached to ink projectile entities and manages their properties and collision effects. It handles what happens when ink hits ships or other targets.

**Responsibilities:**
- Store ink color and damage information
- Manage projectile lifetime
- Handle collision with ships and other entities
- Apply ink effects to ships when hit
- Create visual splatter effects on impact
- Play sound effects on impact

#### Ship Ink Load Component

The Ship Ink Load Component is attached to ship entities and tracks how much ink they have absorbed. Ships sink lower in the water as they take on more ink, and eventually sink completely when the ink load reaches maximum capacity.

**Responsibilities:**
- Track current ink load and maximum capacity
- Calculate sink level based on ink load
- Update ship's visual appearance as it takes on ink
- Trigger sinking animation when maximum load is reached
- Handle ship destruction and captain release

#### Effect Manager

The Effect Manager creates and manages visual effects related to ink mechanics, such as splatter effects when ink hits a target and sinking animations when ships go down.

**Responsibilities:**
- Create and manage visual effects
- Update effect animations
- Render effects to the screen
- Handle special effects like particles and screen shake

## Ink Mechanics Flow

```
┌───────────────┐
│  Player Input │
│  (Fire Button)│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Weapon       │
│  Component    │◄─────────────┐
│  Processes    │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐     No       │
│  Arm Ready    │─────────────┐│
│  (Cooldown    │             ││
│  Expired?)    │             ││
└───────┬───────┘             ││
        │ Yes                 ││
        ▼                     ││
┌───────────────┐             ││
│  Create Ink   │             ││
│  Slime        │             ││
│  Projectile   │             ││
└───────┬───────┘             ││
        │                     ││
        ▼                     ││
┌───────────────┐             ││
│  Set Arm      │             ││
│  Cooldown     │─────────────┘│
│               │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐              │
│  Move to      │              │
│  Next Arm     │──────────────┘
│               │
└───────────────┘

┌───────────────┐
│  Ink Slime    │
│  Projectile   │
│  Created      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Physics      │
│  Update       │
│  (Movement)   │
└───────┬───────┘
        │
        ▼
┌───────────────┐     No
│  Collision    │────────────┐
│  Detected?    │            │
└───────┬───────┘            │
        │ Yes                │
        ▼                    │
┌───────────────┐            │
│  Check        │            │
│  Collision    │            │
│  Target       │            │
└───────┬───────┘            │
        │                    │
        ▼                    │
┌───────────────┐     No     │
│  Is Target    │────┐       │
│  a Ship?      │    │       │
└───────┬───────┘    │       │
        │ Yes        │       │
        ▼            ▼       │
┌───────────────┐ ┌──────────┴─┐
│  Apply Ink    │ │ Create     │
│  to Ship      │ │ Splatter   │
│               │ │ Effect     │
└───────┬───────┘ └────────────┘
        │
        ▼
┌───────────────┐
│  Update Ship  │
│  Sink Level   │
└───────┬───────┘
        │
        ▼
┌───────────────┐     No
│  Max Ink      │────────────┐
│  Load         │            │
│  Reached?     │            │
└───────┬───────┘            │
        │ Yes                │
        ▼                    │
┌───────────────┐            │
│  Start Ship   │            │
│  Sinking      │            │
│  Animation    │            │
└───────┬───────┘            │
        │                    │
        ▼                    │
┌───────────────┐            │
│  Release      │            │
│  Captain      │            │
└───────┬───────┘            │
        │                    │
        ▼                    │
┌───────────────┐            │
│  Destroy      │            │
│  Ship         │            │
└───────────────┘            │
                             │
┌───────────────┐            │
│  Destroy Ink  │◄───────────┘
│  Projectile   │
└───────────────┘
```

### Ink Mechanics Process

1. **Projectile Creation**
   - Player presses the fire button
   - Weapon component checks if the current arm is ready to fire
   - If ready, creates an ink slime projectile in the direction of the arm
   - Sets cooldown for the arm and moves to the next arm

2. **Projectile Movement**
   - Ink slime projectile moves in a straight line
   - Physics component updates position based on velocity
   - Collision component checks for collisions with other entities

3. **Collision Detection**
   - When a collision is detected, the ink slime component handles the collision
   - If the collision is with a ship, ink is applied to the ship
   - A splatter effect is created at the collision point
   - The ink projectile is destroyed

4. **Ship Ink Accumulation**
   - Ship's ink load component tracks how much ink has been absorbed
   - As ink load increases, the ship visually sinks lower in the water
   - When the maximum ink load is reached, the ship starts sinking

5. **Ship Sinking**
   - Sinking animation plays
   - If the ship has a captain, the captain is released
   - Ship is destroyed and player is awarded points

## Ink Colors and Effects

The game features different ink colors with progressively more powerful effects:

| Color | Level | Damage | Visual Effect | Special Properties |
|-------|-------|--------|---------------|-------------------|
| Dark Blue | 1 | 10 | Basic blue splatter | Standard projectile |
| Purple | 2 | 12 | Purple splatter with bubbles | Increased damage |
| Green | 3 | 15 | Green splatter with foam | High damage |
| Red | 4 | 20 | Red splatter with steam | Very high damage |
| Rainbow | 5 | 25 | Colorful splatter with sparkles | Maximum damage, special visual effects |

Each ink color has a unique visual appearance and splatter effect when it hits a target. The damage value represents how much ink load is added to a ship when hit by a projectile of that color.

## API Reference

### Weapon Component API

```python
# Initialize weapon component
weapon = WeaponComponent(arm_count=10, base_cooldown=0.5)

# Start continuous firing
weapon.start_firing()

# Stop firing
weapon.stop_firing()

# Set fire rate
weapon.set_fire_rate(shots_per_second=5.0)

# Set ink color
weapon.set_ink_color("purple")

# Manually rotate arms
weapon.rotate_arms()

# Get active arms
active_arms = weapon.get_active_arms()

# Get arm positions (for rendering)
arm_positions = weapon.get_arm_positions()

# Check if an arm is active
is_active = weapon.is_arm_active(arm_index=3)

# Get arm role (center, side, or inactive)
arm_role = weapon.get_arm_role(arm_index=3)
```

### Ink Slime Component API

```python
# Create an ink slime component
ink_slime = InkSlimeComponent(ink_color="dark_blue", ink_damage=10)

# Set ink color
ink_slime.set_ink_color("purple")

# Handle collision (called automatically by collision system)
ink_slime.on_collision(other_entity)

# Get splatter effect name
splatter_effect = ink_slime._get_splatter_effect("green")
```

### Ship Ink Load Component API

```python
# Create a ship ink load component
ink_load = ShipInkLoadComponent(max_ink_load=100)

# Add ink to the ship
ink_load.add_ink(ink_color="dark_blue", amount=10)

# Get current ink percentage
percentage = ink_load.get_ink_percentage()

# Check if ship is sinking
is_sinking = ink_load.is_ship_sinking()
```

### Entity Factory API for Ink Slime

```python
# Create an ink slime projectile
entity_factory = EntityFactory()
ink_slime = entity_factory.create_ink_slime(
    x=100.0,
    y=200.0,
    direction=pygame.math.Vector2(1, 0),
    color="dark_blue"
)
```

## Examples

### Basic Firing Example

```python
# Player input handling
def handle_input(player, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start firing when space is pressed
                weapon = player.get_component("weapon")
                if weapon:
                    weapon.start_firing()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # Stop firing when space is released
                weapon = player.get_component("weapon")
                if weapon:
                    weapon.stop_firing()
```

### Ship Sinking Example

```python
# Ship hit by ink projectile
def on_ship_hit(ship, ink_projectile):
    # Get components
    ink_slime = ink_projectile.get_component("ink_slime")
    ink_load = ship.get_component("ink_load")
    
    if ink_slime and ink_load:
        # Apply ink to ship
        ink_color = ink_slime.ink_color
        ink_damage = ink_slime.ink_damage
        ink_load.add_ink(ink_color, ink_damage)
        
        # Check if ship is now sinking
        if ink_load.is_ship_sinking():
            print(f"Ship is sinking! Current ink load: {ink_load.current_ink_load}")
```

### Ink Color Progression Example

```python
# Level manager updating ink color based on level
def update_player_ink_color(player, level_number):
    # Map level number to ink color
    ink_colors = {
        1: "dark_blue",
        2: "purple",
        3: "green",
        4: "red",
        5: "rainbow"
    }
    
    # Get the appropriate color for this level
    ink_color = ink_colors.get(level_number, "dark_blue")
    
    # Update player's weapon component
    weapon = player.get_component("weapon")
    if weapon:
        weapon.set_ink_color(ink_color)
        print(f"Player now using {ink_color} ink!")
```

### Multi-Arm Firing Example

```python
# Example of manual arm rotation for strategic firing
def rotate_arms_strategically(player):
    weapon = player.get_component("weapon")
    if weapon:
        # Get current active arms
        active_arms = weapon.get_active_arms()
        
        # Check if center arm is pointing in desired direction
        center_arm = active_arms[1]  # Index 1 is the center arm
        
        # If not pointing in desired direction, rotate until it is
        desired_angle = calculate_desired_angle()  # Custom function
        current_angle = center_arm["angle"]
        
        while abs(current_angle - desired_angle) > 0.1:
            weapon.rotate_arms()
            active_arms = weapon.get_active_arms()
            center_arm = active_arms[1]
            current_angle = center_arm["angle"]
        
        # Now fire with the properly positioned arm
        weapon.try_shoot()