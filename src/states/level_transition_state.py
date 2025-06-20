"""Level transition state for the Octopus Ink Slime game.

This module implements the level transition state that is shown
between levels, displaying level completion stats and a preview
of the next level.
"""

import pygame
import math
from typing import Dict, Any, Optional, List

from src.states.game_state import GameState
from src.levels.level_data import LevelData


class LevelTransitionState(GameState):
    """Level transition state for the Octopus Ink Slime game.
    
    This state is shown between levels and displays level completion
    statistics, a preview of the next level, and a countdown timer.
    """
    
    def __init__(self, game_engine):
        """Initialize the level transition state.
        
        Args:
            game_engine: The main game engine instance
        """
        self.game_engine = game_engine
        self.screen = game_engine.screen
        
        # Level completion stats
        self.level_stats: Dict[str, Any] = {}
        
        # Transition timing
        self.transition_duration: float = 5.0  # Seconds to show transition screen
        self.timer: float = 0.0
        
        # Animation properties
        self.fade_in_duration: float = 0.5
        self.fade_out_duration: float = 0.5
        self.fade_alpha: int = 0  # 0-255
        
        # Next level preview
        self.next_level_data: Optional[Dict[str, Any]] = None
        
        # UI elements
        self.ui_elements: List[Dict[str, Any]] = []
        
    def enter(self, level_stats: Dict[str, Any]) -> None:
        """Called when entering this state.
        
        Args:
            level_stats: Statistics for the completed level
        """
        self.level_stats = level_stats
        
        # Get next level data
        next_level_id = level_stats["next_level_id"]
        if next_level_id <= LevelData.get_level_count():
            self.next_level_data = LevelData.get_level_data(next_level_id)
        else:
            self.next_level_data = None  # Game completed
            
        # Reset timer
        self.timer = 0.0
        self.fade_alpha = 0
        
        # Set up UI elements
        self._setup_ui_elements()
        
    def exit(self) -> None:
        """Called when exiting this state."""
        pass
        
    def update(self, dt: float) -> None:
        """Update the level transition state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Update timer
        self.timer += dt
        
        # Handle fade in/out
        if self.timer < self.fade_in_duration:
            # Fade in
            self.fade_alpha = int(255 * (self.timer / self.fade_in_duration))
        elif self.timer > self.transition_duration - self.fade_out_duration:
            # Fade out
            time_left = self.transition_duration - self.timer
            self.fade_alpha = int(255 * (time_left / self.fade_out_duration))
        else:
            # Fully visible
            self.fade_alpha = 255
            
        # Check if transition is complete
        if self.timer >= self.transition_duration:
            self._transition_to_next_level()
            
        # Update UI animations
        self._update_ui_animations(dt)
        
    def render(self, surface: pygame.Surface) -> None:
        """Render the level transition state.
        
        Args:
            surface: The surface to render to
        """
        # Fill background with a dark color
        surface.fill((20, 20, 40))
        
        # Render UI elements
        self._render_ui_elements(surface)
        
        # Render countdown
        self._render_countdown(surface)
        
        # Apply fade effect
        fade_surface = pygame.Surface((surface.get_width(), surface.get_height()))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(255 - self.fade_alpha)
        surface.blit(fade_surface, (0, 0))
        
    def handle_events(self, events):
        """
        Process pygame events.
        
        Args:
            events: List of pygame events to process
        """
        for event in events:
            self.handle_event(event)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a pygame event.
        
        Args:
            event: The pygame event to handle
        """
        # Skip transition on space or enter
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._transition_to_next_level()
                
    def _setup_ui_elements(self) -> None:
        """Set up UI elements for the transition screen."""
        self.ui_elements = []
        
        # Screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Title
        self.ui_elements.append({
            "type": "text",
            "text": f"Level {self.level_stats['level_id']} Complete!",
            "position": (screen_width // 2, 80),
            "color": (255, 255, 255),
            "font_size": 48,
            "align": "center",
            "animation": {
                "type": "scale",
                "start_scale": 0.5,
                "end_scale": 1.0,
                "duration": 0.5,
                "timer": 0.0
            }
        })
        
        # Level name
        self.ui_elements.append({
            "type": "text",
            "text": self.level_stats["level_name"],
            "position": (screen_width // 2, 130),
            "color": (200, 200, 255),
            "font_size": 32,
            "align": "center",
            "animation": {
                "type": "fade",
                "start_alpha": 0,
                "end_alpha": 255,
                "duration": 0.7,
                "timer": 0.0
            }
        })
        
        # Score
        self.ui_elements.append({
            "type": "text",
            "text": f"Score: {self.level_stats['score']}",
            "position": (screen_width // 2, 200),
            "color": (255, 255, 0),
            "font_size": 36,
            "align": "center",
            "animation": {
                "type": "slide",
                "start_pos": (screen_width + 200, 200),
                "end_pos": (screen_width // 2, 200),
                "duration": 0.6,
                "timer": 0.0
            }
        })
        
        # Time used
        self.ui_elements.append({
            "type": "text",
            "text": f"Time: {int(self.level_stats['time_used'])} seconds",
            "position": (screen_width // 2, 250),
            "color": (200, 200, 200),
            "font_size": 24,
            "align": "center",
            "animation": {
                "type": "slide",
                "start_pos": (screen_width + 200, 250),
                "end_pos": (screen_width // 2, 250),
                "duration": 0.7,
                "timer": 0.0
            }
        })
        
        # Divider
        self.ui_elements.append({
            "type": "line",
            "start_pos": (screen_width // 4, 300),
            "end_pos": (screen_width * 3 // 4, 300),
            "color": (150, 150, 150),
            "width": 2,
            "animation": {
                "type": "grow",
                "start_width": 0,
                "end_width": screen_width // 2,
                "duration": 0.8,
                "timer": 0.0
            }
        })
        
        # Next level section
        if self.next_level_data:
            # Next level title
            self.ui_elements.append({
                "type": "text",
                "text": f"Next: Level {self.next_level_data['level_id']}",
                "position": (screen_width // 2, 350),
                "color": (255, 200, 100),
                "font_size": 36,
                "align": "center",
                "animation": {
                    "type": "fade",
                    "start_alpha": 0,
                    "end_alpha": 255,
                    "duration": 1.0,
                    "timer": 0.0
                }
            })
            
            # Next level name
            self.ui_elements.append({
                "type": "text",
                "text": self.next_level_data["name"],
                "position": (screen_width // 2, 400),
                "color": (255, 200, 100),
                "font_size": 28,
                "align": "center",
                "animation": {
                    "type": "fade",
                    "start_alpha": 0,
                    "end_alpha": 255,
                    "duration": 1.2,
                    "timer": 0.0
                }
            })
            
            # Next level description
            self.ui_elements.append({
                "type": "text",
                "text": self.next_level_data["description"],
                "position": (screen_width // 2, 450),
                "color": (200, 200, 200),
                "font_size": 20,
                "align": "center",
                "animation": {
                    "type": "fade",
                    "start_alpha": 0,
                    "end_alpha": 255,
                    "duration": 1.4,
                    "timer": 0.0
                }
            })
            
            # Ink color preview
            ink_color = self.next_level_data["ink_color"]
            ink_color_rgb = {
                "dark_blue": (0, 0, 150),
                "purple": (150, 0, 150),
                "green": (0, 150, 0),
                "red": (150, 0, 0),
                "rainbow": (150, 150, 0)  # Yellow as placeholder for rainbow
            }.get(ink_color, (0, 0, 150))
            
            self.ui_elements.append({
                "type": "circle",
                "position": (screen_width // 2, 520),
                "radius": 30,
                "color": ink_color_rgb,
                "border_color": (255, 255, 255),
                "border_width": 2,
                "animation": {
                    "type": "pulse",
                    "min_scale": 0.8,
                    "max_scale": 1.2,
                    "period": 2.0,
                    "timer": 0.0
                }
            })
        else:
            # Game complete message
            self.ui_elements.append({
                "type": "text",
                "text": "Congratulations!",
                "position": (screen_width // 2, 350),
                "color": (255, 215, 0),  # Gold
                "font_size": 48,
                "align": "center",
                "animation": {
                    "type": "scale",
                    "start_scale": 0.5,
                    "end_scale": 1.2,
                    "duration": 1.0,
                    "timer": 0.0
                }
            })
            
            self.ui_elements.append({
                "type": "text",
                "text": "You have completed all levels!",
                "position": (screen_width // 2, 420),
                "color": (255, 255, 255),
                "font_size": 28,
                "align": "center",
                "animation": {
                    "type": "fade",
                    "start_alpha": 0,
                    "end_alpha": 255,
                    "duration": 1.2,
                    "timer": 0.0
                }
            })
            
    def _update_ui_animations(self, dt: float) -> None:
        """Update UI element animations.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        for element in self.ui_elements:
            if "animation" in element:
                animation = element["animation"]
                animation["timer"] += dt
                
                # Cap timer at duration
                if "duration" in animation:
                    animation["timer"] = min(animation["timer"], animation["duration"])
                    
    def _render_ui_elements(self, surface: pygame.Surface) -> None:
        """Render UI elements.
        
        Args:
            surface: The surface to render to
        """
        for element in self.ui_elements:
            element_type = element["type"]
            
            # Apply animations
            if "animation" in element:
                animation = element["animation"]
                animation_type = animation["type"]
                progress = min(1.0, animation["timer"] / animation["duration"]) if "duration" in animation else 0.0
                
                if animation_type == "fade":
                    alpha = int(animation["start_alpha"] + (animation["end_alpha"] - animation["start_alpha"]) * progress)
                    if "color" in element:
                        r, g, b = element["color"]
                        element["render_color"] = (r, g, b, alpha)
                elif animation_type == "slide":
                    start_x, start_y = animation["start_pos"]
                    end_x, end_y = animation["end_pos"]
                    x = start_x + (end_x - start_x) * progress
                    y = start_y + (end_y - start_y) * progress
                    element["render_position"] = (x, y)
                elif animation_type == "scale":
                    scale = animation["start_scale"] + (animation["end_scale"] - animation["start_scale"]) * progress
                    element["render_scale"] = scale
                elif animation_type == "grow":
                    width = animation["start_width"] + (animation["end_width"] - animation["start_width"]) * progress
                    element["render_width"] = width
                elif animation_type == "pulse":
                    # Continuous pulsing
                    period = animation["period"]
                    phase = (animation["timer"] % period) / period
                    scale = animation["min_scale"] + (animation["max_scale"] - animation["min_scale"]) * (0.5 + 0.5 * math.sin(phase * 2 * math.pi))
                    element["render_scale"] = scale
                    
            # Render based on element type
            if element_type == "text":
                self._render_text_element(surface, element)
            elif element_type == "line":
                self._render_line_element(surface, element)
            elif element_type == "circle":
                self._render_circle_element(surface, element)
                
    def _render_text_element(self, surface: pygame.Surface, element: Dict[str, Any]) -> None:
        """Render a text UI element.
        
        Args:
            surface: The surface to render to
            element: The text element to render
        """
        font = pygame.font.Font(None, element["font_size"])
        
        # Get text color with alpha if animated
        if "render_color" in element and len(element["render_color"]) == 4:
            r, g, b, a = element["render_color"]
            text_color = (r, g, b)
            alpha = a
        else:
            text_color = element["color"]
            alpha = 255
            
        # Create text surface
        text_surface = font.render(element["text"], True, text_color)
        
        # Apply scale if animated
        if "render_scale" in element:
            scale = element["render_scale"]
            original_size = text_surface.get_size()
            scaled_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            text_surface = pygame.transform.scale(text_surface, scaled_size)
            
        # Get position
        if "render_position" in element:
            position = element["render_position"]
        else:
            position = element["position"]
            
        # Adjust position based on alignment
        align = element.get("align", "left")
        if align == "center":
            position = (position[0] - text_surface.get_width() // 2, position[1] - text_surface.get_height() // 2)
        elif align == "right":
            position = (position[0] - text_surface.get_width(), position[1] - text_surface.get_height() // 2)
            
        # Apply alpha if needed
        if alpha < 255:
            text_surface.set_alpha(alpha)
            
        # Draw text
        surface.blit(text_surface, position)
        
    def _render_line_element(self, surface: pygame.Surface, element: Dict[str, Any]) -> None:
        """Render a line UI element.
        
        Args:
            surface: The surface to render to
            element: The line element to render
        """
        # Get line properties
        start_pos = element["start_pos"]
        
        # Handle grow animation
        if "render_width" in element:
            width = element["render_width"]
            center_x = (element["start_pos"][0] + element["end_pos"][0]) // 2
            end_pos = (center_x + width // 2, element["end_pos"][1])
            start_pos = (center_x - width // 2, element["start_pos"][1])
        else:
            end_pos = element["end_pos"]
            
        # Draw line
        pygame.draw.line(
            surface,
            element["color"],
            start_pos,
            end_pos,
            element.get("width", 1)
        )
        
    def _render_circle_element(self, surface: pygame.Surface, element: Dict[str, Any]) -> None:
        """Render a circle UI element.
        
        Args:
            surface: The surface to render to
            element: The circle element to render
        """
        # Get circle properties
        position = element["position"]
        radius = element["radius"]
        
        # Apply scale if animated
        if "render_scale" in element:
            radius = int(radius * element["render_scale"])
            
        # Draw filled circle
        pygame.draw.circle(
            surface,
            element["color"],
            position,
            radius
        )
        
        # Draw border if specified
        if "border_color" in element:
            pygame.draw.circle(
                surface,
                element["border_color"],
                position,
                radius,
                element.get("border_width", 1)
            )
            
    def _render_countdown(self, surface: pygame.Surface) -> None:
        """Render the countdown timer.
        
        Args:
            surface: The surface to render to
        """
        # Only show countdown in the last 3 seconds
        time_left = self.transition_duration - self.timer
        if time_left <= 3.0:
            # Calculate size based on time left (pulsing effect)
            seconds_left = int(time_left) + 1
            fraction = time_left - int(time_left)
            size = int(72 * (1.0 + 0.5 * (1.0 - fraction)))
            
            # Render countdown number
            font = pygame.font.Font(None, size)
            text = str(seconds_left)
            text_surface = font.render(text, True, (255, 255, 255))
            
            # Position at bottom center
            x = surface.get_width() // 2 - text_surface.get_width() // 2
            y = surface.get_height() - 100 - text_surface.get_height() // 2
            
            surface.blit(text_surface, (x, y))
            
    def _transition_to_next_level(self) -> None:
        """Transition to the next level or game over if all levels complete."""
        if self.next_level_data:
            # Transition to gameplay state with next level
            print("Transitioning to next level")
            # In a real implementation, we would do something like:
            # self.game_engine.scene_manager.change_state("gameplay")
        else:
            # All levels complete, transition to game over or victory state
            print("All levels complete! Transitioning to victory screen")
            # In a real implementation, we would do something like:
            # self.game_engine.scene_manager.change_state("victory")