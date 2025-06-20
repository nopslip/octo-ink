"""
Pause Menu State for the Octopus Ink Slime game.
Displays a pause menu overlay during gameplay.
"""

import pygame
from src.states.game_state import GameState
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class PauseMenuState(GameState):
    """Pause menu state that overlays the gameplay state."""
    
    def __init__(self, game_engine):
        """
        Initialize the pause menu state.
        
        Args:
            game_engine: Reference to the main game engine
        """
        super().__init__(game_engine)
        self.title_font = None
        self.menu_font = None
        self.menu_items = [
            {"text": "Resume Game", "action": self._resume_game},
            {"text": "Options", "action": self._show_options},
            {"text": "Return to Main Menu", "action": self._return_to_main_menu}
        ]
        self.selected_item = 0
        self.animation_time = 0
        
        # Store a reference to the gameplay surface
        self.gameplay_surface = None
        
        # UI elements
        self.ui_elements = {}
        
        # Overlay alpha value for fade effect
        self.overlay_alpha = 0
        self.target_alpha = 180  # Target alpha for overlay
        self.fade_speed = 300    # Alpha units per second
    
    def enter(self, **kwargs):
        """
        Called when entering the pause menu state.
        
        Args:
            **kwargs: Optional parameters passed when transitioning to this state
        """
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Capture the current gameplay screen if provided
        if "gameplay_surface" in kwargs:
            self.gameplay_surface = kwargs["gameplay_surface"]
        
        # Reset overlay alpha for fade-in effect
        self.overlay_alpha = 0
        
        # Set up UI
        self._setup_ui()
        
        # Pause game music
        audio_manager = self.game_engine.audio_manager
        if audio_manager:
            audio_manager.pause_music()
            audio_manager.play_sound("menu_open")
    
    def exit(self):
        """Called when exiting the pause menu state."""
        # Clean up UI elements
        self.ui_elements = {}
        
        # Resume game music
        audio_manager = self.game_engine.audio_manager
        if audio_manager:
            audio_manager.unpause_music()
    
    def handle_events(self, events):
        """
        Process pygame events.
        
        Args:
            events: List of pygame events to process
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._resume_game()
                elif event.key == pygame.K_UP:
                    self._select_previous_item()
                elif event.key == pygame.K_DOWN:
                    self._select_next_item()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._activate_selected_item()
            
            # Let UI manager handle events
            if self.game_engine.ui_manager:
                self.game_engine.ui_manager.handle_event(event)
    
    def update(self, dt):
        """
        Update the pause menu state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update animation time
        self.animation_time += dt
        
        # Update overlay alpha for fade effect
        if self.overlay_alpha < self.target_alpha:
            self.overlay_alpha += self.fade_speed * dt
            if self.overlay_alpha > self.target_alpha:
                self.overlay_alpha = self.target_alpha
        
        # Update UI
        if self.game_engine.ui_manager:
            self.game_engine.ui_manager.update(dt)
    
    def render(self, surface):
        """
        Render the pause menu state.
        
        Args:
            surface: Pygame surface to render to
        """
        # Draw the gameplay screen underneath if available
        if self.gameplay_surface:
            surface.blit(self.gameplay_surface, (0, 0))
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(self.overlay_alpha)))
        surface.blit(overlay, (0, 0))
        
        # Draw pause menu title
        title_text = self.title_font.render("PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        
        # Draw text shadow for better readability
        shadow = self.title_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
        surface.blit(shadow, shadow_rect)
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
        
        # Create a panel for the menu
        menu_panel_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 - 150,
            400,
            300
        )
        panel_id = ui_manager.create_panel(
            menu_panel_rect,
            "pause_menu_panel",
            bg_color=(0, 0, 0, 200),  # Semi-transparent black
            border_color=WHITE,
            border_width=2,
            border_radius=10
        )
        
        # Create title label
        title_rect = pygame.Rect(
            menu_panel_rect.centerx - 100,
            menu_panel_rect.y + 20,
            200,
            50
        )
        ui_manager.create_label(
            title_rect,
            "pause_title",
            "PAUSED",
            panel_id,
            text_color=WHITE,
            font_size=48,
            align="center"
        )
        
        # Create buttons for menu items
        button_height = 50
        button_spacing = 20
        button_width = 300
        
        for i, item in enumerate(self.menu_items):
            button_rect = pygame.Rect(
                menu_panel_rect.centerx - button_width // 2,
                menu_panel_rect.y + 100 + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            
            ui_manager.create_button(
                button_rect,
                f"pause_button_{i}",
                item["text"],
                item["action"],
                panel_id,
                bg_color=(50, 50, 50),
                hover_color=(80, 80, 80),
                text_color=WHITE,
                font_size=28
            )
        
        # Create options panel if needed
        self._setup_options_panel(ui_manager, panel_id)
    
    def _setup_options_panel(self, ui_manager, parent_id):
        """
        Set up the options panel.
        
        Args:
            ui_manager: UI manager instance
            parent_id: ID of the parent panel
        """
        # Get parent panel
        parent_panel = ui_manager.get_element(parent_id)
        if not parent_panel:
            return
            
        parent_rect = parent_panel.get_absolute_rect()
        
        # Create options panel (initially hidden)
        options_panel_rect = pygame.Rect(
            parent_rect.right + 20,
            parent_rect.y,
            300,
            parent_rect.height
        )
        options_panel_id = ui_manager.create_panel(
            options_panel_rect,
            "options_panel",
            bg_color=(0, 0, 0, 200),
            border_color=WHITE,
            border_width=2,
            border_radius=10
        )
        
        # Hide the panel initially
        ui_manager.set_element_visible(options_panel_id, False)
        
        # Create title label
        title_rect = pygame.Rect(
            options_panel_rect.centerx - 100,
            options_panel_rect.y + 20,
            200,
            50
        )
        ui_manager.create_label(
            title_rect,
            "options_title",
            "OPTIONS",
            options_panel_id,
            text_color=WHITE,
            font_size=36,
            align="center"
        )
        
        # Create volume sliders
        label_width = 150
        slider_width = 200
        element_height = 30
        spacing = 20
        
        # Sound volume
        y_pos = options_panel_rect.y + 100
        
        sound_label_rect = pygame.Rect(
            options_panel_rect.x + 20,
            y_pos,
            label_width,
            element_height
        )
        ui_manager.create_label(
            sound_label_rect,
            "sound_volume_label",
            "Sound Volume:",
            options_panel_id,
            text_color=WHITE,
            font_size=24,
            align="left"
        )
        
        sound_slider_rect = pygame.Rect(
            options_panel_rect.x + 50,
            y_pos + element_height + 10,
            slider_width,
            element_height
        )
        ui_manager.create_progress_bar(
            sound_slider_rect,
            "sound_volume_slider",
            options_panel_id,
            value=0.7,
            bg_color=(50, 50, 50),
            fill_color=(0, 200, 0),
            border_color=WHITE
        )
        
        # Music volume
        y_pos += element_height * 2 + spacing * 2
        
        music_label_rect = pygame.Rect(
            options_panel_rect.x + 20,
            y_pos,
            label_width,
            element_height
        )
        ui_manager.create_label(
            music_label_rect,
            "music_volume_label",
            "Music Volume:",
            options_panel_id,
            text_color=WHITE,
            font_size=24,
            align="left"
        )
        
        music_slider_rect = pygame.Rect(
            options_panel_rect.x + 50,
            y_pos + element_height + 10,
            slider_width,
            element_height
        )
        ui_manager.create_progress_bar(
            music_slider_rect,
            "music_volume_slider",
            options_panel_id,
            value=0.5,
            bg_color=(50, 50, 50),
            fill_color=(0, 200, 0),
            border_color=WHITE
        )
        
        # Back button
        back_button_rect = pygame.Rect(
            options_panel_rect.centerx - 75,
            options_panel_rect.bottom - 70,
            150,
            40
        )
        ui_manager.create_button(
            back_button_rect,
            "options_back_button",
            "Back",
            self._hide_options,
            options_panel_id,
            bg_color=(50, 50, 50),
            hover_color=(80, 80, 80),
            text_color=WHITE,
            font_size=24
        )
    
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
                font = pygame.font.Font(None, int(36 * scale))
            else:
                color = WHITE
                font = self.menu_font
            
            # Render menu item
            text = font.render(item["text"], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 50))
            
            # Draw text shadow for better readability
            shadow = font.render(item["text"], True, BLACK)
            shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
            surface.blit(shadow, shadow_rect)
            
            # Draw text
            surface.blit(text, text_rect)
    
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
    
    def _resume_game(self):
        """Resume the game."""
        # Pop back to the gameplay state
        if self.game_engine.scene_manager:
            self.game_engine.scene_manager.pop_state()
        else:
            # Fallback if scene manager not available
            self.transition_to("gameplay")
    
    def _show_options(self):
        """Show the options panel."""
        if self.game_engine.ui_manager:
            # Hide main pause menu panel
            self.game_engine.ui_manager.set_element_visible("pause_menu_panel", False)
            
            # Show options panel
            self.game_engine.ui_manager.set_element_visible("options_panel", True)
    
    def _hide_options(self):
        """Hide the options panel."""
        if self.game_engine.ui_manager:
            # Show main pause menu panel
            self.game_engine.ui_manager.set_element_visible("pause_menu_panel", True)
            
            # Hide options panel
            self.game_engine.ui_manager.set_element_visible("options_panel", False)
    
    def _return_to_main_menu(self):
        """Return to the main menu."""
        # Transition to main menu state
        self.transition_to("main_menu")