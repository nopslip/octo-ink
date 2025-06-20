"""
Game Over State for the Octopus Ink Slime game.
Displays the game over screen with final score and high scores.
"""

import pygame
from src.states.game_state import GameState
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.utils.score_manager import ScoreManager


class GameOverState(GameState):
    """Game over state that displays the final score and high scores."""
    
    def __init__(self, game_engine):
        """
        Initialize the game over state.
        
        Args:
            game_engine: Reference to the main game engine
        """
        super().__init__(game_engine)
        self.title_font = None
        self.score_font = None
        self.menu_font = None
        self.menu_items = [
            {"text": "Play Again", "action": self._restart_game},
            {"text": "Return to Main Menu", "action": self._return_to_main_menu}
        ]
        self.selected_item = 0
        self.animation_time = 0
        
        # Final score and stats
        self.final_score = 0
        self.level_reached = 1
        self.high_score_rank = -1
        self.is_high_score = False
        
        # Name entry for high score
        self.entering_name = False
        self.player_name = ""
        self.name_cursor_visible = True
        self.name_cursor_timer = 0
        
        # UI elements
        self.ui_elements = {}
        
        # Fade in effect
        self.fade_alpha = 255
        self.fade_speed = 150  # Alpha units per second
    
    def enter(self, **kwargs):
        """
        Called when entering the game over state.
        
        Args:
            **kwargs: Optional parameters passed when transitioning to this state
        """
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Get final score and level
        self.final_score = kwargs.get("score", 0)
        self.level_reached = kwargs.get("level", 1)
        
        # Reset animation time
        self.animation_time = 0
        
        # Reset fade effect
        self.fade_alpha = 255
        
        # Check if this is a high score
        score_manager = ScoreManager.get_instance()
        self.is_high_score = score_manager.check_high_score()
        
        if self.is_high_score:
            self.entering_name = True
            self.player_name = ""
            self.name_cursor_visible = True
            self.name_cursor_timer = 0
        
        # Set up UI
        self._setup_ui()
        
        # Play game over music
        audio_manager = self.game_engine.audio_manager
        if audio_manager:
            audio_manager.play_music("game_over")
            audio_manager.play_sound("game_over")
    
    def exit(self):
        """Called when exiting the game over state."""
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
                if self.entering_name:
                    self._handle_name_input(event)
                else:
                    if event.key == pygame.K_UP:
                        self._select_previous_item()
                    elif event.key == pygame.K_DOWN:
                        self._select_next_item()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self._activate_selected_item()
                    elif event.key == pygame.K_ESCAPE:
                        self._return_to_main_menu()
            
            # Let UI manager handle events if not entering name
            if not self.entering_name and self.game_engine.ui_manager:
                self.game_engine.ui_manager.handle_event(event)
    
    def update(self, dt):
        """
        Update the game over state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update animation time
        self.animation_time += dt
        
        # Update fade effect
        if self.fade_alpha > 0:
            self.fade_alpha -= self.fade_speed * dt
            if self.fade_alpha < 0:
                self.fade_alpha = 0
        
        # Update name cursor blink
        if self.entering_name:
            self.name_cursor_timer += dt
            if self.name_cursor_timer >= 0.5:
                self.name_cursor_timer -= 0.5
                self.name_cursor_visible = not self.name_cursor_visible
        
        # Update UI
        if self.game_engine.ui_manager:
            self.game_engine.ui_manager.update(dt)
    
    def render(self, surface):
        """
        Render the game over state.
        
        Args:
            surface: Pygame surface to render to
        """
        # Draw background (dark gradient)
        self._draw_background(surface)
        
        # Draw game over title
        title_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        # Add pulsing effect to title
        scale = 1.0 + 0.05 * abs(pygame.math.sin(self.animation_time * 2))
        scaled_title = pygame.transform.scale(
            title_text, 
            (int(title_text.get_width() * scale), int(title_text.get_height() * scale))
        )
        scaled_rect = scaled_title.get_rect(center=title_rect.center)
        
        # Draw text shadow for better readability
        shadow = pygame.transform.scale(
            self.title_font.render("GAME OVER", True, BLACK),
            (scaled_title.get_width(), scaled_title.get_height())
        )
        shadow_rect = shadow.get_rect(center=(scaled_rect.centerx + 3, scaled_rect.centery + 3))
        surface.blit(shadow, shadow_rect)
        surface.blit(scaled_title, scaled_rect)
        
        # Draw final score
        score_text = self.score_font.render(f"Final Score: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(score_text, score_rect)
        
        # Draw level reached
        level_text = self.score_font.render(f"Level Reached: {self.level_reached}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
        surface.blit(level_text, level_rect)
        
        if self.entering_name:
            # Draw name entry prompt
            self._draw_name_entry(surface)
        else:
            # Draw high scores
            self._draw_high_scores(surface)
            
            # Draw menu items if not using UI manager
            if not self.game_engine.ui_manager:
                self._draw_menu_items(surface)
            else:
                # Let UI manager render UI elements
                self.game_engine.ui_manager.render(surface)
        
        # Draw fade overlay
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            surface.blit(fade_surface, (0, 0))
    
    def _setup_ui(self):
        """Set up UI elements using the UI manager."""
        if not self.game_engine.ui_manager or self.entering_name:
            return
            
        ui_manager = self.game_engine.ui_manager
        
        # Create a panel for the menu
        menu_panel_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 150,
            300,
            120
        )
        panel_id = ui_manager.create_panel(
            menu_panel_rect,
            "game_over_panel",
            bg_color=(0, 0, 0, 150),  # Semi-transparent black
            border_color=(150, 0, 0),
            border_width=2,
            border_radius=10
        )
        
        # Create buttons for menu items
        button_height = 40
        button_spacing = 20
        button_width = 250
        
        for i, item in enumerate(self.menu_items):
            button_rect = pygame.Rect(
                menu_panel_rect.centerx - button_width // 2,
                menu_panel_rect.y + 20 + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            
            ui_manager.create_button(
                button_rect,
                f"game_over_button_{i}",
                item["text"],
                item["action"],
                panel_id,
                bg_color=(100, 0, 0),
                hover_color=(150, 0, 0),
                text_color=WHITE,
                font_size=28
            )
    
    def _draw_background(self, surface):
        """
        Draw the game over background.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Create gradient from black to dark red
        for y in range(SCREEN_HEIGHT):
            # Calculate color based on y position
            red_val = int(50 * (y / SCREEN_HEIGHT))
            color = (red_val, 0, 0)
            
            # Draw horizontal line with this color
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw some particle effects
        for i in range(20):
            # Calculate position based on time
            x = (SCREEN_WIDTH // 2) + 200 * pygame.math.sin(self.animation_time + i * 0.5)
            y = 100 + i * 25 + 10 * pygame.math.cos(self.animation_time * 0.7 + i * 0.3)
            
            # Draw particle
            size = 2 + int(3 * abs(pygame.math.sin(self.animation_time * 0.5 + i)))
            alpha = 100 + int(155 * abs(pygame.math.sin(self.animation_time + i * 0.2)))
            
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                (255, 50, 50, alpha),
                (size, size),
                size
            )
            surface.blit(particle_surface, (x - size, y - size))
    
    def _draw_menu_items(self, surface):
        """
        Draw the menu items.
        
        Args:
            surface: Pygame surface to draw on
        """
        menu_y = SCREEN_HEIGHT - 120
        
        for i, item in enumerate(self.menu_items):
            # Determine text color and size based on selection
            if i == self.selected_item:
                color = (255, 200, 0)  # Gold for selected item
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
    
    def _draw_high_scores(self, surface):
        """
        Draw the high scores list.
        
        Args:
            surface: Pygame surface to draw on
        """
        score_manager = ScoreManager.get_instance()
        high_scores = score_manager.get_high_scores()
        
        # Draw high scores title
        title_text = self.score_font.render("High Scores", True, (200, 200, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 290))
        surface.blit(title_text, title_rect)
        
        # Draw high scores
        y_pos = 330
        for i, score in enumerate(high_scores[:5]):  # Show top 5 scores
            # Highlight the player's new high score
            if i == self.high_score_rank:
                color = (255, 255, 0)  # Bright yellow
                font = pygame.font.Font(None, 32)
            else:
                color = (200, 200, 200)
                font = pygame.font.Font(None, 28)
            
            score_text = font.render(
                f"{i+1}. {score['name']} - {score['score']} (Level {score['level']})",
                True, color
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            surface.blit(score_text, score_rect)
            
            y_pos += 35
    
    def _draw_name_entry(self, surface):
        """
        Draw the name entry interface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw prompt
        prompt_text = self.score_font.render("New High Score!", True, (255, 255, 0))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 290))
        surface.blit(prompt_text, prompt_rect)
        
        name_prompt = self.menu_font.render("Enter Your Name:", True, WHITE)
        name_prompt_rect = name_prompt.get_rect(center=(SCREEN_WIDTH // 2, 340))
        surface.blit(name_prompt, name_prompt_rect)
        
        # Draw name entry box
        box_width = 300
        box_height = 40
        box_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - box_width // 2,
            380,
            box_width,
            box_height
        )
        pygame.draw.rect(surface, (50, 50, 50), box_rect)
        pygame.draw.rect(surface, WHITE, box_rect, 2)
        
        # Draw entered name
        name_text = self.menu_font.render(self.player_name, True, WHITE)
        name_rect = name_text.get_rect(midleft=(box_rect.left + 10, box_rect.centery))
        surface.blit(name_text, name_rect)
        
        # Draw cursor
        if self.name_cursor_visible:
            cursor_x = name_rect.right + 2
            if cursor_x > box_rect.right - 10:
                cursor_x = box_rect.right - 10
            
            pygame.draw.line(
                surface,
                WHITE,
                (cursor_x, box_rect.top + 10),
                (cursor_x, box_rect.bottom - 10),
                2
            )
        
        # Draw instructions
        instructions = self.menu_font.render("Press Enter when done", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 440))
        surface.blit(instructions, instructions_rect)
    
    def _handle_name_input(self, event):
        """
        Handle keyboard input for name entry.
        
        Args:
            event: Pygame key event
        """
        if event.key == pygame.K_RETURN:
            # Submit name if not empty
            if self.player_name:
                self._submit_high_score()
            
        elif event.key == pygame.K_BACKSPACE:
            # Remove last character
            self.player_name = self.player_name[:-1]
            
        elif event.key == pygame.K_ESCAPE:
            # Cancel name entry
            self.entering_name = False
            self._setup_ui()
            
        elif event.unicode and len(self.player_name) < 15:
            # Add character if it's printable and name is not too long
            char = event.unicode
            if char.isprintable() and not char.isspace():
                self.player_name += char
                
                # Play key sound
                if self.game_engine.audio_manager:
                    self.game_engine.audio_manager.play_sound("button_click")
    
    def _submit_high_score(self):
        """Submit the high score with the entered name."""
        score_manager = ScoreManager.get_instance()
        self.high_score_rank = score_manager.add_high_score(self.player_name)
        self.entering_name = False
        
        # Play sound effect
        if self.game_engine.audio_manager:
            self.game_engine.audio_manager.play_sound("high_score")
        
        # Set up UI now that name entry is complete
        self._setup_ui()
    
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
    
    def _restart_game(self):
        """Restart the game."""
        # Reset score manager
        score_manager = ScoreManager.get_instance()
        score_manager.reset()
        
        # Transition to gameplay state
        self.transition_to("gameplay")
    
    def _return_to_main_menu(self):
        """Return to the main menu."""
        # Transition to main menu state
        self.transition_to("main_menu")