# UI System

## Overview

The UI System is a core component of the Ink Slime game that manages all user interface elements and interactions. It provides a structured way to create, organize, and control UI elements such as buttons, labels, progress bars, panels, and images that make up the game's interface.

The system is responsible for rendering UI elements, handling user input events, managing UI element hierarchies, and providing a consistent interface for other game systems to interact with the UI. It supports features such as nested UI elements, event propagation, and dynamic UI updates.

The UI System follows a component-based design pattern, with a central UI Manager that coordinates all UI elements. Each UI element inherits from a common base class, providing consistent behavior while allowing for specialized functionality in derived classes.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         UI Manager                              │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Element    │ │  Event      │ │  Rendering  │ │  Element  │ │
│  │  Management │ │  Handling   │ │  Pipeline   │ │  Creation │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        UI Elements                              │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │  Base UI    │ │  Interactive│ │  Display    │ │ Container │ │
│  │  Element    │ │  Elements   │ │  Elements   │ │ Elements  │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └─────┬─────┘ │
│         │               │               │              │       │
│         ▼               ▼               ▼              ▼       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ Positioning │ │   Button    │ │   Label     │ │   Panel   │ │
│  │ & Hierarchy │ │             │ │             │ │           │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│                  ┌─────────────┐ ┌─────────────┐               │
│                  │ Progress Bar│ │   Image     │               │
│                  │             │ │             │               │
│                  └─────────────┘ └─────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### UI Manager

The UI Manager is the central component that handles creation, management, and rendering of all UI elements. It serves as the main interface between the game and the UI system.

**Responsibilities:**
- Create and manage UI elements
- Handle user input events and route them to appropriate UI elements
- Render UI elements in the correct order
- Provide methods for updating UI element properties
- Manage UI element visibility and enabled states
- Track focus and hover states for interactive elements

#### UI Element Base Class

The UI Element is the base class for all UI components, providing common functionality and a consistent interface.

**Responsibilities:**
- Store position and size information
- Maintain parent-child relationships for nested UI elements
- Handle event propagation through the UI hierarchy
- Provide visibility and enabled state management
- Calculate absolute screen positions based on parent positions
- Render self and children in the correct order

#### Button Class

The Button class represents an interactive clickable UI element that triggers a callback when clicked.

**Responsibilities:**
- Render a clickable button with text
- Track hover and pressed states
- Handle mouse events (click, hover)
- Execute callback function when clicked
- Support visual feedback for different states (normal, hover, pressed)

#### Label Class

The Label class displays text within the UI system.

**Responsibilities:**
- Render text with specified font, size, and color
- Support different text alignment options (left, center, right)
- Update text content dynamically

#### Panel Class

The Panel class serves as a container for grouping related UI elements.

**Responsibilities:**
- Provide a background container for other UI elements
- Support optional background color and border
- Group related UI elements together
- Enable moving and managing multiple UI elements as a single unit

#### Progress Bar Class

The Progress Bar class visualizes numeric progress or status.

**Responsibilities:**
- Display a visual representation of a value within a range
- Update fill level based on current value
- Support customizable colors for background, fill, and border
- Optionally display percentage text

#### Image Class

The Image class displays images within the UI system.

**Responsibilities:**
- Load and display images from files or surfaces
- Support different scaling modes (fit, fill, stretch, none)
- Resize and position images appropriately

## UI Event Handling Flow

```
┌───────────────┐
│  Pygame Event │
│  Generated    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  UI Manager   │
│  Receives     │
│  Event        │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Process Root │
│  Elements     │◄─────────────┐
│  (in reverse) │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐     No       │
│  Element      │─────────────┐│
│  Visible &    │             ││
│  Enabled?     │             ││
└───────┬───────┘             ││
        │ Yes                 ││
        ▼                     ││
┌───────────────┐             ││
│  Process      │             ││
│  Children     │─────────────┘│
│  First        │              │
└───────┬───────┘              │
        │                      │
        ▼                      │
┌───────────────┐     No       │
│  Child        │─────────────┘
│  Handled      │
│  Event?       │
└───────┬───────┘
        │ Yes
        ▼
┌───────────────┐
│  Stop Event   │
│  Propagation  │
└───────────────┘
```

### Event Handling Process

1. **Event Generation**
   - A Pygame event is generated (mouse click, key press, etc.)
   - The event is passed to the UI Manager's handle_event method

2. **Root Element Processing**
   - UI Manager processes root elements in reverse order (top to bottom visually)
   - Elements that are not visible or enabled are skipped

3. **Hierarchical Processing**
   - Each element processes its children first (in reverse order)
   - This ensures that elements drawn on top receive events first

4. **Event Handling**
   - If an element or its children handle the event, propagation stops
   - This prevents multiple elements from responding to the same event

5. **Specific Element Handling**
   - Button elements handle mouse events (click, hover)
   - Other interactive elements process relevant events
   - Non-interactive elements pass events to their children

## API Reference

### UI Manager API

#### Element Creation

```python
# Create a button
button_id = ui_manager.create_button(
    rect=pygame.Rect(100, 100, 200, 50),
    element_id="start_button",
    text="Start Game",
    callback=start_game_function
)

# Create a label
label_id = ui_manager.create_label(
    rect=pygame.Rect(100, 200, 200, 30),
    element_id="score_label",
    text="Score: 0"
)

# Create a progress bar
progress_id = ui_manager.create_progress_bar(
    rect=pygame.Rect(100, 250, 200, 20),
    element_id="health_bar",
    value=100.0,
    max_value=100.0
)

# Create a panel
panel_id = ui_manager.create_panel(
    rect=pygame.Rect(50, 50, 300, 400),
    element_id="main_panel",
    bg_color=(50, 50, 50, 200)
)

# Create an image
image_id = ui_manager.create_image(
    rect=pygame.Rect(150, 300, 100, 100),
    element_id="player_avatar",
    image="assets/images/player.png"
)
```

#### Element Management

```python
# Get a UI element by ID
element = ui_manager.get_element("start_button")

# Remove a UI element
ui_manager.remove_element("temp_message")

# Set text of a label or button
ui_manager.set_element_text("score_label", "Score: 1000")

# Set progress bar value
ui_manager.set_progress_bar_value("health_bar", 75.0)

# Set element visibility
ui_manager.set_element_visible("debug_panel", False)

# Set element enabled state
ui_manager.set_element_enabled("quit_button", True)

# Clear all UI elements
ui_manager.clear_ui()
```

#### Core UI Loop

```python
# Update UI elements
ui_manager.update(delta_time)

# Render UI elements
ui_manager.render(screen_surface)

# Handle events
handled = ui_manager.handle_event(event)
```

### UI Element API

#### Base UI Element

```python
# Add a child element
parent_element.add_child(child_element)

# Get absolute position (accounting for parent positions)
abs_rect = element.get_absolute_rect()

# Update element
element.update(delta_time)

# Render element
element.render(surface)

# Handle event
handled = element.handle_event(event)
```

#### Button-Specific API

```python
# Create a button
button = Button(
    rect=pygame.Rect(100, 100, 200, 50),
    element_id="start_button",
    text="Start Game",
    callback=start_game_function,
    bg_color=(100, 100, 200),
    hover_color=(150, 150, 255),
    text_color=(255, 255, 255),
    font_size=24
)
```

#### Progress Bar-Specific API

```python
# Create a progress bar
progress_bar = ProgressBar(
    rect=pygame.Rect(100, 200, 200, 20),
    element_id="health_bar",
    value=75.0,
    min_value=0.0,
    max_value=100.0,
    bg_color=(50, 50, 50),
    fill_color=(0, 200, 0),
    show_text=True
)

# Set progress value
progress_bar.set_value(50.0)

# Get percentage
percentage = progress_bar.get_percentage()
```

#### Image-Specific API

```python
# Create an image element
image = Image(
    rect=pygame.Rect(100, 100, 200, 200),
    element_id="character_portrait",
    image="assets/images/character.png",
    scale_mode="fit"
)

# Set a new image
image.set_image("assets/images/character_alt.png")
```

## Examples

### Main Menu UI Example

```python
# Initialize UI Manager
ui_manager = UIManager(screen_size=(800, 600))

# Create a background panel
panel_id = ui_manager.create_panel(
    rect=pygame.Rect(200, 100, 400, 400),
    element_id="main_menu_panel",
    bg_color=(30, 30, 50),
    border_color=(100, 100, 200),
    border_width=2,
    border_radius=10
)

# Add a title label
ui_manager.create_label(
    rect=pygame.Rect(0, 30, 400, 50),
    element_id="title_label",
    text="INK SLIME",
    text_color=(200, 200, 255),
    font_size=48,
    parent_id="main_menu_panel"
)

# Add menu buttons
ui_manager.create_button(
    rect=pygame.Rect(100, 120, 200, 50),
    element_id="start_button",
    text="Start Game",
    callback=start_game,
    parent_id="main_menu_panel"
)

ui_manager.create_button(
    rect=pygame.Rect(100, 190, 200, 50),
    element_id="options_button",
    text="Options",
    callback=show_options,
    parent_id="main_menu_panel"
)

ui_manager.create_button(
    rect=pygame.Rect(100, 260, 200, 50),
    element_id="highscores_button",
    text="High Scores",
    callback=show_highscores,
    parent_id="main_menu_panel"
)

ui_manager.create_button(
    rect=pygame.Rect(100, 330, 200, 50),
    element_id="quit_button",
    text="Quit Game",
    callback=quit_game,
    parent_id="main_menu_panel"
)
```

### In-Game HUD Example

```python
# Initialize UI Manager
ui_manager = UIManager(screen_size=(800, 600))

# Create score label
ui_manager.create_label(
    rect=pygame.Rect(20, 20, 200, 30),
    element_id="score_label",
    text="Score: 0",
    text_color=(255, 255, 255),
    align="left"
)

# Create health bar
ui_manager.create_progress_bar(
    rect=pygame.Rect(20, 60, 200, 20),
    element_id="health_bar",
    value=100.0,
    max_value=100.0,
    bg_color=(50, 50, 50),
    fill_color=(0, 200, 0),
    border_color=(0, 0, 0),
    show_text=True
)

# Create ink meter
ui_manager.create_progress_bar(
    rect=pygame.Rect(20, 90, 200, 20),
    element_id="ink_meter",
    value=100.0,
    max_value=100.0,
    bg_color=(50, 50, 50),
    fill_color=(0, 0, 200),
    border_color=(0, 0, 0),
    show_text=True
)

# Create level indicator
ui_manager.create_label(
    rect=pygame.Rect(600, 20, 180, 30),
    element_id="level_label",
    text="Level: 1",
    text_color=(255, 255, 255),
    align="right"
)

# Create time remaining indicator
ui_manager.create_label(
    rect=pygame.Rect(600, 60, 180, 30),
    element_id="time_label",
    text="Time: 2:00",
    text_color=(255, 255, 255),
    align="right"
)

# Create pause button
ui_manager.create_button(
    rect=pygame.Rect(730, 20, 50, 50),
    element_id="pause_button",
    text="||",
    callback=pause_game
)
```

### Dialog Box Example

```python
# Create a dialog box
dialog_panel_id = ui_manager.create_panel(
    rect=pygame.Rect(200, 150, 400, 300),
    element_id="dialog_panel",
    bg_color=(50, 50, 70),
    border_color=(100, 100, 200),
    border_width=2,
    border_radius=5
)

# Add title
ui_manager.create_label(
    rect=pygame.Rect(0, 20, 400, 40),
    element_id="dialog_title",
    text="Level Complete!",
    text_color=(200, 200, 255),
    font_size=32,
    parent_id="dialog_panel"
)

# Add content
ui_manager.create_label(
    rect=pygame.Rect(50, 80, 300, 30),
    element_id="score_result",
    text="Score: 5,250",
    text_color=(255, 255, 255),
    align="left",
    parent_id="dialog_panel"
)

ui_manager.create_label(
    rect=pygame.Rect(50, 120, 300, 30),
    element_id="time_result",
    text="Time: 1:45",
    text_color=(255, 255, 255),
    align="left",
    parent_id="dialog_panel"
)

ui_manager.create_label(
    rect=pygame.Rect(50, 160, 300, 30),
    element_id="bonus_result",
    text="Bonus: +1,000",
    text_color=(255, 255, 100),
    align="left",
    parent_id="dialog_panel"
)

# Add buttons
ui_manager.create_button(
    rect=pygame.Rect(80, 220, 100, 40),
    element_id="retry_button",
    text="Retry",
    callback=retry_level,
    parent_id="dialog_panel"
)

ui_manager.create_button(
    rect=pygame.Rect(220, 220, 100, 40),
    element_id="next_button",
    text="Next Level",
    callback=next_level,
    parent_id="dialog_panel"
)