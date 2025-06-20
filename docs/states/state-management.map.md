# State Management System

## Overview

The State Management System is a core component of the Octopus Ink Slime game that handles different game states and transitions between them. It provides a structured way to organize game logic into distinct states (such as main menu, gameplay, pause menu, etc.) and manages the flow between these states.

The system follows the State pattern, allowing the game to change its behavior based on its internal state. This approach keeps the code organized, maintainable, and makes it easier to add new states or modify existing ones without affecting other parts of the game.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Scene Manager                             │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  State      │ │  State      │ │  State      │ │  State      │ │
│  │  Registry   │ │  Stack      │ │  Transition │ │  Lifecycle  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GameState (Abstract)                        │
└───────────┬───────────┬───────────┬───────────┬─────────────────┘
            │           │           │           │
            ▼           ▼           ▼           ▼
┌───────────────┐ ┌───────────┐ ┌─────────┐ ┌─────────────────────┐
│ MainMenuState │ │ GameState │ │ Pause   │ │ Other States        │
│               │ │           │ │ Menu    │ │ - GameOverState     │
│               │ │           │ │ State   │ │ - LevelTransition   │
└───────────────┘ └───────────┘ └─────────┘ └─────────────────────┘
```

### Key Components

#### Scene Manager

The Scene Manager is the central component that manages all game states. It maintains a registry of available states, a reference to the current active state, and a state stack for overlays like pause menus.

**Responsibilities:**
- Register and store game states
- Change between states
- Push and pop states from the stack
- Forward game events to the current state
- Update and render the current state

#### GameState (Abstract Base Class)

The GameState class defines the interface that all concrete state implementations must follow. It provides the structure for state lifecycle methods and game loop integration.

**Key Methods:**
- `enter()`: Called when entering the state
- `exit()`: Called when exiting the state
- `handle_events()`: Process input events
- `update()`: Update state logic
- `render()`: Render the state
- `transition_to()`: Request a transition to another state

#### Concrete State Implementations

The game includes several concrete state implementations that inherit from the GameState base class:

1. **MainMenuState**: Displays the title screen with game logo and menu options
2. **GameplayState**: Handles the main gameplay loop
3. **PauseMenuState**: Provides an overlay with pause options during gameplay
4. **GameOverState**: Shows the game over screen with final score and high scores
5. **LevelTransitionState**: Displays level completion stats and next level preview

## State Transition Flow

```
┌───────────────┐
│  Main Menu    │
│  State        │◄────────────────┐
└───────┬───────┘                 │
        │                         │
        │ Start Game              │
        ▼                         │
┌───────────────┐    Complete   ┌─┴─────────────┐
│  Gameplay     │───────────────►  Level        │
│  State        │◄───────────────  Transition   │
└───────┬───────┘    Next Level └───────────────┘
        │
        │ Pause                    Game Over
        ▼                              ▲
┌───────────────┐                      │
│  Pause Menu   │                      │
│  State        │                      │
└───────┬───────┘                      │
        │                              │
        │ Resume                       │
        └──────────────────┐           │
                           ▼           │
                     ┌─────────────────┴─┐
                     │  Game Over State  │
                     └───────────────────┘
```

### Common State Transitions

1. **Main Menu → Gameplay**
   - Triggered by: Player selecting "Start Game"
   - Implementation: `MainMenuState._start_game()` calls `transition_to("gameplay")`

2. **Gameplay → Pause Menu**
   - Triggered by: Player pressing ESC key
   - Implementation: `SceneManager.push_state("pause_menu")` (preserves gameplay state)

3. **Pause Menu → Gameplay**
   - Triggered by: Player selecting "Resume Game"
   - Implementation: `PauseMenuState._resume_game()` calls `SceneManager.pop_state()`

4. **Gameplay → Level Transition**
   - Triggered by: Player completing level objectives
   - Implementation: `GameplayState._transition_to_level_complete()` calls `transition_to("level_transition")`

5. **Level Transition → Gameplay**
   - Triggered by: Countdown timer completion or player skipping
   - Implementation: `LevelTransitionState._transition_to_next_level()`

6. **Gameplay → Game Over**
   - Triggered by: Player failing level objectives or game completion
   - Implementation: `transition_to("game_over")`

7. **Game Over → Main Menu**
   - Triggered by: Player selecting "Return to Main Menu"
   - Implementation: `GameOverState._return_to_main_menu()` calls `transition_to("main_menu")`

## API Reference

### Scene Manager API

#### State Registration

```python
# Register a new game state
scene_manager.register_state(state_name, state_instance)

# Example:
scene_manager.register_state("main_menu", MainMenuState(game_engine))
```

#### State Changes

```python
# Change to a different state
scene_manager.change_state(state_name, **kwargs)

# Example:
scene_manager.change_state("gameplay", difficulty="hard")
```

#### State Stack Operations

```python
# Push a state onto the stack (overlay)
scene_manager.push_state(state_name, **kwargs)

# Example:
scene_manager.push_state("pause_menu", gameplay_surface=current_surface)

# Pop the current state and return to previous
scene_manager.pop_state()
```

#### Game Loop Integration

```python
# Process events for current state
scene_manager.handle_events(events)

# Update current state
scene_manager.update(dt)

# Render current state
scene_manager.render(surface)
```

### GameState API

#### State Lifecycle

```python
# Called when entering the state
def enter(self, **kwargs):
    # Initialize state resources
    pass

# Called when exiting the state
def exit(self):
    # Clean up resources
    pass
```

#### Game Loop Methods

```python
# Process input events
def handle_events(self, events):
    # Handle user input
    pass

# Update state logic
def update(self, dt):
    # Update game objects
    pass

# Render the state
def render(self, surface):
    # Draw to the screen
    pass
```

#### State Transitions

```python
# Request a transition to another state
def transition_to(self, next_state, **kwargs):
    self.next_state = (next_state, kwargs)

# Example:
self.transition_to("game_over", score=self.score, level=self.level)
```

## Usage Examples

### Starting the Game

```python
# Initialize scene manager
scene_manager = SceneManager(game_engine)

# Register states
scene_manager.register_state("main_menu", MainMenuState(game_engine))
scene_manager.register_state("gameplay", GameplayState(game_engine))
scene_manager.register_state("pause_menu", PauseMenuState(game_engine))
scene_manager.register_state("game_over", GameOverState(game_engine))
scene_manager.register_state("level_transition", LevelTransitionState(game_engine))

# Start with main menu
scene_manager.start(initial_state="main_menu")
```

### Implementing a New State

```python
class CustomState(GameState):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        # Initialize state-specific variables
        
    def enter(self, **kwargs):
        # Setup when entering state
        pass
        
    def exit(self):
        # Cleanup when exiting state
        pass
        
    def handle_events(self, events):
        # Handle input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.transition_to("main_menu")
                    
    def update(self, dt):
        # Update logic
        pass
        
    def render(self, surface):
        # Render to screen
        pass

# Register the new state
scene_manager.register_state("custom_state", CustomState(game_engine))
```

### Transitioning Between States

```python
# From within a state class:
def _on_button_click(self):
    # Transition to gameplay with parameters
    self.transition_to("gameplay", difficulty="normal", level=1)
    
# From outside a state:
scene_manager.change_state("main_menu")
```

### Using State Stack for Overlays

```python
# Push pause menu on top of gameplay
scene_manager.push_state("pause_menu", gameplay_surface=current_surface)

# Return to gameplay
scene_manager.pop_state()