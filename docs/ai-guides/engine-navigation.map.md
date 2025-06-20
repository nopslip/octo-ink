# AI Agent Navigation Guide

## Overview

This guide is specifically designed to help AI agents (like Claude) effectively navigate, understand, and modify the Ink Slime game engine codebase. Unlike traditional documentation aimed at human developers, this guide provides structured pathways for AI agents to quickly comprehend the architecture, identify key components, and make targeted modifications with minimal exploration.

The Ink Slime game is a Python-based game using Pygame where the player controls an octopus that fires ink at enemy ships to sink them. The codebase follows a component-based entity system architecture, with clear separation between game engine systems, entities, components, and game states.

This guide will help AI agents:
- Understand the overall architecture and design patterns
- Locate key files for specific tasks
- Trace execution flow through the codebase
- Follow naming conventions and coding standards
- Make effective code modifications
- Troubleshoot common issues

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       Game Engine                               │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Scene      │ │  Entity     │ │  Physics    │ │  Asset    │ │
│  │  Manager    │ │  Manager    │ │  Engine     │ │  Manager  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Entity-Component System                      │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Entity     │ │  Component  │ │  Entity     │ │  Game     │ │
│  │  Base Class │ │  Base Class │ │  Factory    │ │  States   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Architectural Patterns

1. **Component-Based Entity System**:
   - Entities are containers for components
   - Components define behavior and properties
   - This allows for flexible entity composition

2. **State Machine Pattern**:
   - Game states manage different screens/modes
   - States handle their own events, updates, and rendering
   - Scene Manager controls state transitions

3. **Singleton Pattern**:
   - Used for global managers (EntityManager, AssetManager, etc.)
   - Ensures single instance access throughout the codebase

4. **Factory Pattern**:
   - EntityFactory creates pre-configured entities
   - Centralizes entity creation logic

5. **Observer Pattern**:
   - Used for event handling and callbacks
   - Components can react to events from other components

## File Structure and Organization

### Directory Structure

```
ink-slime/
├── assets/              # Game assets (images, sounds, fonts)
├── data/                # Game data (highscores, etc.)
├── docs/                # Documentation
│   ├── ai-guides/       # AI-specific documentation
│   ├── engine/          # Engine documentation
│   ├── entities/        # Entity system documentation
│   ├── levels/          # Level system documentation
│   ├── mechanics/       # Game mechanics documentation
│   ├── states/          # State management documentation
│   └── ui/              # UI system documentation
├── logs/                # Log files
└── src/                 # Source code
    ├── components/      # Component classes
    ├── engine/          # Core engine systems
    ├── entities/        # Entity classes
    ├── levels/          # Level management
    ├── states/          # Game state classes
    └── utils/           # Utility functions and helpers
```

### Key Files by System

#### Core Engine
- `main.py`: Entry point for the game
- `src/engine/game_engine.py`: Main game engine class
- `src/engine/scene_manager.py`: Manages game states
- `src/engine/input_manager.py`: Handles input processing
- `src/engine/physics_engine.py`: Handles physics and collisions

#### Entity System
- `src/entities/entity.py`: Base entity class
- `src/entities/entity_manager.py`: Manages all entities
- `src/entities/entity_factory.py`: Creates pre-configured entities
- `src/components/component.py`: Base component class

#### Game States
- `src/states/game_state.py`: Base game state class
- `src/states/gameplay_state.py`: Main gameplay state
- `src/states/main_menu_state.py`: Main menu state
- `src/states/pause_menu_state.py`: Pause menu state

#### Game Mechanics
- `src/components/weapon_component.py`: Handles weapon mechanics
- `src/components/ink_slime_component.py`: Manages ink projectiles
- `src/components/ship_ink_load_component.py`: Tracks ship ink absorption

## Entry Points for Common Tasks

### Fixing Bugs

1. **Gameplay Mechanics Bugs**:
   - Start with `src/states/gameplay_state.py`
   - Check relevant component classes in `src/components/`
   - Examine entity classes in `src/entities/`

2. **Rendering Issues**:
   - Check `src/components/render_component.py`
   - Look at the render methods in `src/engine/game_engine.py`
   - Examine the specific entity's render logic

3. **Collision Detection Problems**:
   - Start with `src/engine/physics_engine.py`
   - Check `src/components/collision_component.py`
   - Look at collision handling in `src/states/gameplay_state.py`

4. **Input Handling Issues**:
   - Check `src/engine/input_manager.py`
   - Look at `src/components/input_component.py`
   - Examine event handling in relevant game states

### Adding Features

1. **New Entity Type**:
   - Create a new entity class in `src/entities/`
   - Add factory method in `src/entities/entity_factory.py`
   - Implement necessary components

2. **New Component Type**:
   - Create a new component class in `src/components/`
   - Inherit from `src/components/component.py`
   - Implement required methods

3. **New Game State**:
   - Create a new state class in `src/states/`
   - Inherit from `src/states/game_state.py`
   - Register the state in `src/engine/scene_manager.py`

4. **New Game Mechanic**:
   - Identify which components need modification
   - Update or create new components
   - Modify relevant entity classes
   - Update gameplay state if necessary

## Common Patterns and Conventions

### Naming Conventions

1. **Files**:
   - Snake case: `game_engine.py`, `entity_manager.py`
   - Descriptive of the primary class/functionality

2. **Classes**:
   - PascalCase: `GameEngine`, `EntityManager`
   - Noun phrases describing the object

3. **Methods and Functions**:
   - Snake case: `update()`, `handle_events()`
   - Verb phrases describing the action

4. **Private Methods and Attributes**:
   - Prefixed with underscore: `_update_enemy_spawning()`, `_instance`
   - Indicates internal use only

### Coding Patterns

1. **Component Access Pattern**:
   ```python
   # Getting a component from an entity
   transform = entity.get_component("transform")
   if transform:
       # Use the component
       transform.position.x += 10
   ```

2. **Entity Creation Pattern**:
   ```python
   # Creating an entity through the factory
   player = entity_factory.create_player(x, y)
   
   # Adding a custom component
   custom_component = CustomComponent()
   player.add_component(custom_component)
   ```

3. **State Transition Pattern**:
   ```python
   # Transitioning to another state
   self.transition_to("game_over", score=self.score)
   ```

4. **Singleton Access Pattern**:
   ```python
   # Getting a singleton instance
   entity_manager = EntityManager.get_instance()
   ```

## Tracing Execution Flow

### Game Initialization Flow

1. `main.py` creates a `GameEngine` instance
2. `GameEngine.initialize()` sets up all subsystems
3. `SceneManager` is initialized with default states
4. `SceneManager.start()` transitions to the initial state (usually "main_menu")
5. `GameEngine.run()` starts the main game loop

### Game Loop Flow

1. `GameEngine.run()` main loop:
   - Calculate delta time
   - Process events
   - Update current state
   - Update physics
   - Render current state
   - Update display

2. State update flow:
   - `SceneManager.update()` calls current state's update method
   - Current state updates its logic
   - Entity updates cascade to component updates

3. Rendering flow:
   - `SceneManager.render()` calls current state's render method
   - Current state renders its elements
   - Entities render through their render components

### Entity Lifecycle Flow

1. Entity creation:
   - `EntityFactory` creates entity with predefined components
   - `EntityManager.add_entity()` adds to pending list
   - Entity is fully added during next update cycle

2. Entity update:
   - `EntityManager.update()` calls `entity.update()`
   - Entity updates all its components
   - Components perform their specific behaviors

3. Entity destruction:
   - `entity.destroy()` marks entity for destruction
   - `EntityManager` removes it during next update cycle
   - All components' `on_remove()` methods are called

## Decision Tree for File Examination

When approaching a task, use this decision tree to determine which files to examine:

```
Is the task related to...
├── Game mechanics?
│   ├── Ink shooting? → weapon_component.py, ink_slime_component.py
│   ├── Ship sinking? → ship_ink_load_component.py, ship.py
│   ├── Enemy behavior? → ai_component.py, relevant entity classes
│   └── Collisions? → physics_engine.py, collision_component.py
├── Visual elements?
│   ├── Rendering? → render_component.py, animation_component.py
│   ├── Effects? → effects_manager.py, effect_component.py
│   └── UI? → ui_manager.py, relevant state classes
├── Game flow?
│   ├── State transitions? → scene_manager.py, relevant state classes
│   ├── Level progression? → level_manager.py, level_generator.py
│   └── Game over conditions? → gameplay_state.py, game_over_state.py
└── Core systems?
    ├── Entity management? → entity_manager.py, entity_factory.py
    ├── Input handling? → input_manager.py, input_component.py
    └── Asset loading? → asset_manager.py, asset_cache.py
```

## Common AI Agent Tasks and Approaches

### Task 1: Fix a collision detection bug

**Approach:**
1. Examine `src/engine/physics_engine.py` to understand collision detection
2. Check `src/components/collision_component.py` for component-specific logic
3. Look at collision handling in `src/states/gameplay_state.py`
4. Identify the specific collision case that's failing
5. Fix the bug in the appropriate location

**Example:**
```python
# In gameplay_state.py, fix incorrect collision detection between projectiles and ships
def _check_collision(self, entity1, entity2) -> bool:
    transform1 = entity1.get_component("transform")
    collision1 = entity1.get_component("collision")
    transform2 = entity2.get_component("transform")
    collision2 = entity2.get_component("collision")
    
    if not all([transform1, collision1, transform2, collision2]):
        return False
        
    # Fix: Account for rotation in collision detection
    if collision1.use_rotated_rect or collision2.use_rotated_rect:
        # Implement rotated rectangle collision detection
        return self._check_rotated_collision(transform1, collision1, transform2, collision2)
    else:
        # Simple AABB collision detection
        rect1 = pygame.Rect(
            transform1.position.x - collision1.width / 2,
            transform1.position.y - collision1.height / 2,
            collision1.width,
            collision1.height
        )
        
        rect2 = pygame.Rect(
            transform2.position.x - collision2.width / 2,
            transform2.position.y - collision2.height / 2,
            collision2.width,
            collision2.height
        )
        
        return rect1.colliderect(rect2)
```

### Task 2: Add a new power-up entity

**Approach:**
1. Create a new entity class in `src/entities/power_up.py`
2. Add a factory method in `src/entities/entity_factory.py`
3. Implement necessary components
4. Add collision handling in `src/states/gameplay_state.py`

**Example:**
```python
# In entity_factory.py, add a new factory method
def create_power_up(self, x: float, y: float, power_up_type: str = "speed") -> Entity:
    """Create a power-up entity.
    
    Args:
        x: Initial x position
        y: Initial y position
        power_up_type: Type of power-up ("speed", "damage", "health")
        
    Returns:
        The created power-up entity
    """
    from src.entities.power_up import PowerUp
    
    # Create the power-up entity
    power_up = PowerUp(x, y, power_up_type)
    
    if self.entity_manager:
        self.entity_manager.add_entity(power_up)
        
    return power_up
```

### Task 3: Modify the weapon system to add a new ink type

**Approach:**
1. Update `src/components/weapon_component.py` to support the new ink type
2. Modify `src/components/ink_slime_component.py` to implement new behavior
3. Update level data to include the new ink type
4. Add visual effects for the new ink type

**Example:**
```python
# In weapon_component.py, update the ink color mapping
def set_ink_color(self, color: str) -> None:
    """Set the ink color for this weapon.
    
    Args:
        color: The ink color to use
    """
    self.ink_color = color
    
    # Update damage based on ink color
    damage_map = {
        "dark_blue": 10,
        "purple": 12,
        "green": 15,
        "red": 20,
        "rainbow": 25,
        "acid": 18  # New acid ink type
    }
    
    self.ink_damage = damage_map.get(color, 10)
    
    # Update special effects based on ink color
    effect_map = {
        "dark_blue": None,
        "purple": "bubble",
        "green": "foam",
        "red": "steam",
        "rainbow": "sparkle",
        "acid": "corrosion"  # New effect for acid ink
    }
    
    self.special_effect = effect_map.get(color)
```

## Troubleshooting Guide

### Common Issue 1: Entity not appearing in game

**Diagnosis:**
1. Check if the entity was properly added to the EntityManager
2. Verify the entity has a RenderComponent
3. Ensure the entity's position is within the visible screen area
4. Check if the entity is marked as active

**Solution:**
```python
# Ensure entity is added to the manager
entity_manager.add_entity(entity)

# Check if entity has a render component
render = entity.get_component("render")
if not render:
    entity.add_component(RenderComponent("sprite_name"))

# Ensure entity is within screen bounds
transform = entity.get_component("transform")
if transform:
    # Set position to center of screen
    transform.position = pygame.math.Vector2(screen_width/2, screen_height/2)

# Make sure entity is active
entity.set_active(True)
```

### Common Issue 2: Collision not being detected

**Diagnosis:**
1. Check if both entities have CollisionComponent
2. Verify collision dimensions are appropriate
3. Ensure entities are in the same spatial partition
4. Check if collision types are compatible

**Solution:**
```python
# Ensure both entities have collision components
collision1 = entity1.get_component("collision")
collision2 = entity2.get_component("collision")

if not collision1:
    entity1.add_component(CollisionComponent(width=32, height=32))
    
if not collision2:
    entity2.add_component(CollisionComponent(width=32, height=32))

# Verify collision dimensions match sprite size
render1 = entity1.get_component("render")
if render1 and collision1:
    # Adjust collision size to match sprite
    collision1.width = render1.sprite.get_width()
    collision1.height = render1.sprite.get_height()

# Ensure collision types are compatible
if collision1 and collision2:
    collision1.collision_type = "projectile"
    collision2.collision_type = "ship"
```

### Common Issue 3: Component not updating correctly

**Diagnosis:**
1. Check if the component is enabled
2. Verify the component is properly attached to an entity
3. Ensure the entity is active
4. Check for logical errors in the component's update method

**Solution:**
```python
# Ensure component is enabled
component.set_enabled(True)

# Verify component is attached to entity
if component.entity is None:
    entity.add_component(component)

# Make sure entity is active
entity.set_active(True)

# Debug component update logic
def update(self, dt):
    print(f"Updating {self.component_type} with dt={dt}")
    # Original update logic
    super().update(dt)
    print(f"After update: {self.some_property}")
```

### Common Issue 4: Game state not transitioning correctly

**Diagnosis:**
1. Check if the state is properly registered with the SceneManager
2. Verify the transition_to method is called correctly
3. Ensure the target state exists
4. Check for errors in the state's enter or exit methods

**Solution:**
```python
# Ensure state is registered
scene_manager.register_state("my_state", MyState(game_engine))

# Verify transition call
self.transition_to("my_state", param1=value1)

# Debug state transitions
def enter(self, **kwargs):
    print(f"Entering state with kwargs: {kwargs}")
    # Original enter logic
    
def exit(self):
    print("Exiting state")
    # Original exit logic
```

## Conclusion

This AI Agent Navigation Guide provides a structured approach for AI agents to navigate and modify the Ink Slime game engine codebase. By following the patterns, conventions, and decision trees outlined in this guide, AI agents can efficiently locate relevant code, understand its purpose, and make appropriate modifications.

Remember these key principles when working with this codebase:
1. Follow the component-based architecture
2. Use the entity factory for creating entities
3. Respect the state machine pattern for game flow
4. Understand the entity lifecycle for proper management
5. Use the decision tree to quickly locate relevant files

By adhering to these guidelines, AI agents can effectively assist in developing, debugging, and enhancing the Ink Slime game.