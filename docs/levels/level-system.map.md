# Level System

## Overview

The Level System is a core component of the Ink Slime game that manages level progression, generation, and configuration. It provides a structured way to create varied gameplay experiences as players progress through the game, with increasing difficulty and changing environments.

The system is responsible for defining level properties, generating level content (enemies, obstacles, collectibles), tracking player progress within levels, and managing transitions between levels. Each level features unique characteristics such as different ink colors, enemy behaviors, and environmental elements that create distinct gameplay challenges.

The Level System follows a modular design pattern, separating level data definition, level generation logic, and level progression management into distinct components that work together to create a cohesive gameplay experience.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Level Manager                            │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  Level      │ │  Level      │ │  Level      │ │  Level      │ │
│  │  Progression│ │  Tracking   │ │  Completion │ │  Transition │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Level Generator                           │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  Enemy      │ │  Obstacle   │ │  Spawn      │ │  Background │ │
│  │  Generation │ │  Placement  │ │  Points     │ │  Selection  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Level Data                              │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  Level      │ │  Enemy      │ │  Visual     │ │  Difficulty │ │
│  │  Properties │ │  Properties │ │  Themes     │ │  Parameters │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### Level Manager

The Level Manager is the central component that handles level progression, tracks the player's progress within a level, and manages transitions between levels.

**Responsibilities:**
- Track current level and load level configurations
- Monitor level progress and completion criteria
- Handle level transitions and advancement
- Provide level state information to other game systems
- Manage level timers and score targets

#### Level Generator

The Level Generator creates the actual content of each level based on the configuration provided by the Level Data. It handles the procedural generation of enemy waves, obstacle placement, and spawn point configuration.

**Responsibilities:**
- Generate enemy waves based on level difficulty
- Place obstacles throughout the level
- Configure spawn points for different entity types
- Create bonus entities like fish
- Select appropriate backgrounds and visual elements

#### Level Data

The Level Data component defines the configuration for each level in the game. It contains static data that specifies the properties, difficulty parameters, and visual themes for each level.

**Responsibilities:**
- Define level properties (name, description, time limits)
- Specify enemy properties (health, speed, count)
- Define visual themes (backgrounds, ink colors)
- Set difficulty parameters for each level
- Provide a consistent interface for accessing level data

#### Level Component

The Level Component connects the level system to individual game entities. It attaches to entities that need level-specific properties and behaviors.

**Responsibilities:**
- Store level-specific entity properties
- Update entity behaviors based on current level
- Provide level-specific parameters to other components
- Adjust entity attributes when level changes

## Level Progression Flow

```
┌───────────────┐
│  Initialize   │
│  Level System │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Load Level   │◄─────────────┐
│  Data         │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐              │
│  Generate     │              │
│  Level Content│              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐              │
│  Start Level  │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐              │
│  Update Level │              │
│  Progress     │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐     No       │
│  Level        │─────────────┐│
│  Completed?   │             ││
└───────┬───────┘             ││
        │ Yes                 ││
        ▼                     ││
┌───────────────┐     No      ││
│  Final Level? │─────────────┘│
└───────┬───────┘              │
        │ Yes                  │
        ▼                      │
┌───────────────┐              │
│  Game         │              │
│  Complete     │              │
└───────────────┘              │
```

### Level Progression Stages

1. **Level Initialization**
   - Level Manager loads level data for the current level
   - Level Generator initializes with level parameters
   - Level-specific properties are set (ink color, enemy behavior, etc.)

2. **Level Generation**
   - Obstacles are placed based on level configuration
   - Spawn points are determined for enemies and collectibles
   - Background and visual elements are selected

3. **Level Gameplay**
   - Player interacts with the generated level
   - Level Manager tracks progress toward completion criteria
   - Enemy waves are generated dynamically during gameplay

4. **Level Completion**
   - Level Manager detects when completion criteria are met
   - Level completion statistics are calculated
   - Transition to next level is prepared

5. **Level Transition**
   - Level completion stats are displayed
   - Next level is loaded and initialized
   - Gameplay continues with new level parameters

## API Reference

### Level Manager API

#### Level Initialization and Control

```python
# Initialize a level
level_data = level_manager.start_level()

# Update level progress
level_manager.update(dt, current_score)

# Advance to the next level
success = level_manager.advance_to_next_level()

# Restart the current level
level_manager.restart_current_level()

# Set a specific level
level_manager.set_level(level_id)
```

#### Level State Queries

```python
# Get current level ID
level_id = level_manager.get_current_level_id()

# Get current level data
level_data = level_manager.get_current_level_data()

# Get level progress
progress = level_manager.get_level_progress()

# Get time remaining
time_remaining = level_manager.get_level_time_remaining()

# Check if level is completed
is_completed = level_manager.is_level_completed()

# Get level completion statistics
stats = level_manager.get_level_completion_stats()
```

#### Event Callbacks

```python
# Set callback for level completion
level_manager.set_on_level_complete_callback(callback_function)

# Set callback for level failure
level_manager.set_on_level_failed_callback(callback_function)
```

### Level Generator API

#### Level Content Generation

```python
# Initialize a level with configuration data
level_generator.initialize_level(level_data)

# Generate an enemy wave
enemy_configs = level_generator.generate_enemy_wave()

# Spawn an enemy wave in the game world
level_generator.spawn_enemy_wave()

# Spawn turtle obstacles
level_generator.spawn_turtles()

# Spawn bonus fish
fish = level_generator.spawn_fish()
```

#### Level Environment

```python
# Get spawn points for different entity types
spawn_points = level_generator.get_spawn_points()

# Get the background for the current level
background = level_generator.get_background_for_level()
```

### Level Data API

```python
# Get data for a specific level
level_data = LevelData.get_level_data(level_id)

# Get the total number of levels
level_count = LevelData.get_level_count()

# Get ink color for a specific level
ink_color = LevelData.get_ink_color_for_level(level_id)
```

### Level Component API

```python
# Create a level component for an entity
level_component = LevelComponent(level_id)

# Set the current level for an entity
level_component.set_level(level_id)

# Get the current ink color
ink_color = level_component.get_ink_color()

# Get the scoring multiplier for the current level
multiplier = level_component.get_scoring_multiplier()

# Get a specific behavior parameter
param_value = level_component.get_behavior_param("weapon", "damage", default=10)
```

## Examples

### Level Configuration Example

```python
# Example level configuration from LevelData
level_3 = {
    "level_id": 3,
    "name": "Emerald Abyss",
    "description": "Your ink turns green as you venture into the abyss.",
    "ship_speed": 120,
    "ship_count": 2,
    "ship_health": 140,
    "turtle_count": 4,
    "turtle_speed": 50,
    "fish_spawn_rate": 0.3,
    "fish_value_multiplier": 1.5,
    "ink_color": "green",
    "ink_damage": 15,
    "ink_amount": 140,
    "background": "deep_water",
    "obstacles": ["seaweed", "rocks", "coral", "shipwreck"],
    "time_limit": 180,
    "score_target": 3500,
    "difficulty_multiplier": 1.6
}
```

### Level Initialization Example

```python
# Initialize the level system
level_manager = LevelManager()
level_generator = LevelGenerator(screen_width, screen_height)

# Connect to entity systems
level_generator.set_entity_systems(entity_manager, entity_factory)

# Start the first level
level_data = level_manager.start_level()
level_generator.initialize_level(level_data)

# Set up level completion callback
def on_level_complete(level_id, score):
    # Show level completion screen
    scene_manager.change_state("level_transition")

level_manager.set_on_level_complete_callback(on_level_complete)
```

### Level Update Example

```python
# In the game update loop
def update(dt):
    # Update game entities
    entity_manager.update(dt)
    
    # Update level manager with current score
    level_manager.update(dt, score_manager.get_current_score())
    
    # Spawn enemies periodically
    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        level_generator.spawn_enemy_wave()
        spawn_timer = 0
        
    # Spawn bonus fish occasionally
    fish_timer += dt
    if fish_timer >= fish_interval:
        level_generator.spawn_fish()
        fish_timer = 0
```

### Level Transition Example

```python
# When transitioning to the next level
def advance_to_next_level():
    # Get completion stats for display
    stats = level_manager.get_level_completion_stats()
    
    # Advance to next level
    if level_manager.advance_to_next_level():
        # Load new level data
        level_data = level_manager.get_current_level_data()
        
        # Initialize the new level
        level_generator.initialize_level(level_data)
        
        # Update player's ink color
        player_entity = entity_manager.get_player()
        level_component = player_entity.get_component("level")
        level_component.set_level(level_manager.get_current_level_id())
        
        # Start the new level
        return True
    else:
        # No more levels, game complete
        scene_manager.change_state("game_complete")
        return False