"""
Main Menu State for the Octopus Ink Slime game.
Displays the title screen with game logo and menu options.
"""

import pygame
from src.states.game_state import GameState
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, OCEAN_BLUE, WHITE, BLACK, GAME_TITLE


class MainMenuState(GameState):
    """Main menu state that displays the title screen and menu options."""
    
    def __init__(self, game_engine):
        """
        Initialize the main menu state.
        
        Args:
            game_engine: Reference to the main game engine
        """
        super().__init__(game_engine)
        self.title_font = None
        self.menu_font = None
        self.logo_image = None
        self.background_image = None
        self.menu_items = [
            {"text": "Start Game", "action": self._start_game},
            {"text": "Options", "action": self._show_options},
            {"text": "Exit", "action": self._exit_game}
        ]
        self.selected_item = 0
        self.animation_time = 0
        self.bubble_particles = []
        
        # UI elements
        self.ui_elements = {}
    
    def enter(self, **kwargs):
        """
        Called when entering the main menu state.
        
        Args:
            **kwargs: Optional parameters passed when transitioning to this state
        """
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        
        # Load assets
        asset_manager = self.game_engine.asset_manager
        if asset_manager:
            # Try to load logo and background
            try:
                self.logo_image = asset_manager.load_image("assets/images/logo.png")
                self.background_image = asset_manager.load_image("assets/images/menu_background.png")
            except:
                print("Warning: Could not load menu images, using placeholder graphics")
        
        # Set up UI
        self._setup_ui()
        
        # Play menu music
        audio_manager = self.game_engine.audio_manager
        if audio_manager:
            audio_manager.play_music("main_menu")
    
    def exit(self):
        """Called when exiting the main menu state."""
        # Clean up UI elements
        self.ui_elements = {}
    
    def handle_events(self, events):
        """
        Process pygame events.
        
        Args:
            events: List of pygame events to process
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._select_previous_item()
                elif event.key == pygame.K_DOWN:
                    self._select_next_item()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._activate_selected_item()
                elif event.key == pygame.K_ESCAPE:
                    self._exit_game()
            
            # Let UI manager handle events
            if self.game_engine.ui_manager:
                self.game_engine.ui_manager.handle_event(event)
    
    def update(self, dt):
        """
        Update the main menu state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update animation time
        self.animation_time += dt
        
        # Update bubble particles
        self._update_bubbles(dt)
        
        # Create new bubbles randomly
        if len(self.bubble_particles) < 20 and pygame.time.get_ticks() % 20 == 0:
            self._create_bubble()
        
        # Update UI
        if self.game_engine.ui_manager:
            self.game_engine.ui_manager.update(dt)
    
    def render(self, surface):
        """
        Render the main menu state.
        
        Args:
            surface: Pygame surface to render to
        """
        # Draw background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            # Fallback to gradient background
            self._draw_gradient_background(surface)
        
        # Draw bubble particles
        self._draw_bubbles(surface)
        
        # Draw logo or title text
        if self.logo_image:
            logo_rect = self.logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            surface.blit(self.logo_image, logo_rect)
        else:
            # Fallback to text title
            title_text = self.title_font.render(GAME_TITLE, True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            surface.blit(title_text, title_rect)
        
        # Draw menu items if not using UI manager
        if not self.game_engine.ui_manager:
            self._draw_menu_items(surface)
        else:
            # Let UI manager render UI elements
            self.game_engine.ui_manager.render(surface)
    
    def _setup_ui(self):
        """Set up UI elements using the UI manager."""
        if not self.game_engine.ui_manager:
            return
            
        ui_manager = self.game_engine.ui_manager
        
        # Create buttons directly without a panel
        button_height = 60
        button_spacing = 40  # Increased spacing between buttons
        button_width = 250
        
        # Calculate starting Y position for buttons
        start_y = SCREEN_HEIGHT // 2 - 50  # Move buttons up a bit
        
        for i, item in enumerate(self.menu_items):
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                start_y + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            
            ui_manager.create_button(
                button_rect,
                f"button_{i}",
                item["text"],
                item["action"],
                None,  # No parent panel
                bg_color=(50, 100, 150),
                hover_color=(100, 150, 200),
                text_color=WHITE,
                font_size=36
            )
        
        # Create version label
        version_rect = pygame.Rect(
            10,
            SCREEN_HEIGHT - 30,
            200,
            20
        )
        ui_manager.create_label(
            version_rect,
            "version_label",
            "Version 1.0",
            text_color=(200, 200, 200),
            font_size=16,
            align="left"
        )
    
    def _draw_gradient_background(self, surface):
        """
        Draw a gradient background.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Create gradient from dark blue to lighter blue
        for y in range(SCREEN_HEIGHT):
            # Calculate color based on y position
            blue_val = int(50 + (y / SCREEN_HEIGHT) * 50)
            color = (0, blue_val, 100 + blue_val // 2)
            
            # Draw horizontal line with this color
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    
    def _draw_menu_items(self, surface):
        """
        Draw the menu items.
        
        Args:
            surface: Pygame surface to draw on
        """
        menu_y = SCREEN_HEIGHT // 2
        
        for i, item in enumerate(self.menu_items):
            # Determine text color and size based on selection
            if i == self.selected_item:
                color = (255, 255, 0)  # Yellow for selected item
                # Add pulsing effect to selected item
                scale = 1.0 + 0.1 * abs(pygame.math.sin(self.animation_time * 5))
                font = pygame.font.Font(None, int(48 * scale))
            else:
                color = WHITE
                font = self.menu_font
            
            # Render menu item
            text = font.render(item["text"], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 60))
            
            # Draw text shadow for better readability
            shadow = font.render(item["text"], True, BLACK)
            shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
            surface.blit(shadow, shadow_rect)
            
            # Draw text
            surface.blit(text, text_rect)
    
    def _create_bubble(self):
        """Create a new bubble particle."""
        import random
        
        bubble = {
            "x": random.randint(0, SCREEN_WIDTH),
            "y": SCREEN_HEIGHT + random.randint(10, 50),
            "size": random.randint(5, 20),
            "speed": random.uniform(30, 80),
            "wobble": random.uniform(0.5, 2.0),
            "wobble_speed": random.uniform(1.0, 3.0),
            "wobble_offset": random.uniform(0, 6.28)  # 0 to 2π
        }
        
        self.bubble_particles.append(bubble)
    
    def _update_bubbles(self, dt):
        """
        Update bubble particles.
        
        Args:
            dt: Time delta in seconds since last update
        """
        import math
        
        # Update each bubble
        for bubble in self.bubble_particles:
            # Move upward
            bubble["y"] -= bubble["speed"] * dt
            
            # Add wobble effect
            bubble["x"] += math.sin(
                self.animation_time * bubble["wobble_speed"] + bubble["wobble_offset"]
            ) * bubble["wobble"] * dt
        
        # Remove bubbles that have gone off screen
        self.bubble_particles = [b for b in self.bubble_particles if b["y"] > -b["size"]]
    
    def _draw_bubbles(self, surface):
        """
        Draw bubble particles.
        
        Args:
            surface: Pygame surface to draw on
        """
        for bubble in self.bubble_particles:
            # Draw bubble
            pygame.draw.circle(
                surface,
                (255, 255, 255, 128),  # Semi-transparent white
                (int(bubble["x"]), int(bubble["y"])),
                bubble["size"]
            )
            
            # Draw highlight
            highlight_size = bubble["size"] // 3
            if highlight_size > 0:
                pygame.draw.circle(
                    surface,
                    (255, 255, 255, 200),  # More opaque white
                    (int(bubble["x"] - bubble["size"] // 3), int(bubble["y"] - bubble["size"] // 3)),
                    highlight_size
                )
    
    def _select_next_item(self):
        """Select the next menu item."""
        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
        
        # Play sound effect
        if self.game_engine.audio_manager:
            self.game_engine.audio_manager.play_sound("menu_select")
    
    def _select_previous_item(self):
        """Select the previous menu item."""
        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
        
        # Play sound effect
        if self.game_engine.audio_manager:
            self.game_engine.audio_manager.play_sound("menu_select")
    
    def _activate_selected_item(self):
        """Activate the currently selected menu item."""
        # Play sound effect
        if self.game_engine.audio_manager:
            self.game_engine.audio_manager.play_sound("button_click")
            
        # Call the action function
        self.menu_items[self.selected_item]["action"]()
    
    def _start_game(self):
        """Start a new game."""
        # Play a sound effect if available
        if self.game_engine.audio_manager:
            self.game_engine.audio_manager.play_sound("button_click")
            
        print("Starting new game...")
        self.transition_to("gameplay")
    
    def _show_options(self):
        """Show the options menu."""
        # In a real implementation, this would transition to an options state
        # For now, just print a message
        print("Options menu not implemented yet")
    
    def _exit_game(self):
        """Exit the game."""
        self.game_engine.quit()