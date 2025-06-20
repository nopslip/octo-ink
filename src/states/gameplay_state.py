"""Gameplay state for the Octopus Ink Slime game.

This module implements the main gameplay state where the player
controls the octopus and interacts with the game world.
"""

import pygame
from typing import Dict, Any, Optional

from src.states.game_state import GameState
from src.levels.level_manager import LevelManager
from src.levels.level_generator import LevelGenerator


class GameplayState(GameState):
    """Main gameplay state for the Octopus Ink Slime game.
    
    This state handles the core gameplay loop, including player input,
    enemy spawning, collision detection, and level progression.
    """
    
    def __init__(self, game_engine):
        """Initialize the gameplay state.
        
        Args:
            game_engine: The main game engine instance
        """
        super().__init__(game_engine)
        self.screen = game_engine.screen
        self.entity_manager = game_engine.entity_manager
        self.entity_factory = game_engine.entity_factory
        
        # Use the game engine's level systems
        self.level_manager = game_engine.level_manager
        self.level_generator = game_engine.level_generator
        
        # Game state
        self.score = 0
        self.paused = False
        
        # Timers
        self.wave_timer = 0.0
        self.wave_interval = 5.0  # Spawn enemies every 5 seconds
        self.fish_spawn_timer = 0.0
        self.fish_spawn_interval = 3.0  # Spawn fish every 3 seconds
        
        # Set up level completion callback
        if self.level_manager:
            self.level_manager.set_on_level_complete_callback(self._on_level_complete)
            self.level_manager.set_on_level_failed_callback(self._on_level_failed)
        
    def enter(self, **kwargs) -> None:
        """Called when entering this state."""
        # Set element_id for HUD rendering check
        self.element_id = "gameplay"
        
        # Initialize level if level manager exists
        if self.level_manager:
            level_data = self.level_manager.start_level()
            if self.level_generator:
                self.level_generator.initialize_level(level_data)
            
            # Update wave interval based on level data
            self.wave_interval = 5.0 / level_data["difficulty_multiplier"]
        
        # Create player entity
        self._create_player()
        
        # Set up initial wave of enemies
        if self.level_generator:
            self.level_generator.spawn_turtles()
            self.level_generator.spawn_enemy_wave()
        
        # Reset score for this level
        self.score = 0
        # Also update the game engine's score
        self.game_engine.score = 0
        
        # Reset timers
        self.wave_timer = 0.0
        self.fish_spawn_timer = 0.0
        
    def exit(self) -> None:
        """Called when exiting this state."""
        # Clean up entities if needed
        pass
        
    def update(self, dt: float) -> None:
        """Update the gameplay state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if self.paused:
            return
            
        # Update level manager
        self.level_manager.update(dt, self.score)
        
        # Update entity manager
        if self.entity_manager:
            self.entity_manager.update(dt)
            
        # Keep player within screen bounds
        self._constrain_player_to_screen()
        
        # Update enemy spawning
        self._update_enemy_spawning(dt)
        
        # Handle collisions
        self._handle_collisions()
        
        # Update captains on ships
        self._update_captains_on_ships()
        
        # Check for level completion
        if self.level_manager.is_level_completed():
            self._transition_to_level_complete()
            
    def render(self, surface: pygame.Surface) -> None:
        """Render the gameplay state.
        
        Args:
            surface: The surface to render to
        """
        # Clear screen with background color based on current level
        if self.level_manager:
            level_id = self.level_manager.get_current_level_id()
            bg_colors = {
                1: (0, 50, 100),    # Dark blue
                2: (50, 0, 100),    # Purple
                3: (0, 100, 50),    # Green
                4: (100, 0, 0),     # Red
                5: (50, 50, 100)    # Rainbow (base color, would be animated)
            }
            bg_color = bg_colors.get(level_id, (0, 50, 100))
            surface.fill(bg_color)
        else:
            # Default background color
            surface.fill((0, 50, 100))
        
        # Render entities (handled by game engine now)
        # The game engine will render entities when in gameplay state
        
        # Render HUD
        self._render_hud(surface)
        
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                
    def _create_player(self) -> None:
        """Create the player entity."""
        # Create player at center of screen
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        
        self.player = self.entity_factory.create_player(
            screen_center_x,
            screen_center_y
        )
        
        # Store player reference in game engine for compatibility
        self.game_engine.player = self.player
        
        # Add level component to player if level manager exists
        if self.level_manager:
            from src.components.level_component import LevelComponent
            level_component = LevelComponent(self.level_manager.get_current_level_id())
            self.player.add_component(level_component)
            
            # Update player's ink color based on level
            ink_color = self.level_manager.get_current_ink_color()
            weapon = self.player.get_component("weapon")
            if weapon:
                weapon.set_ink_color(ink_color)
            
        # Store screen bounds for player constraint
        self.screen_bounds = pygame.Rect(0, 0, self.screen.get_width(), self.screen.get_height())
        # Also store in game engine for compatibility
        self.game_engine.screen_bounds = self.screen_bounds
        
    def _constrain_player_to_screen(self) -> None:
        """Keep the player entity within screen boundaries."""
        if not hasattr(self, 'player') or not self.player:
            return
            
        transform = self.player.get_component("transform")
        collision = self.player.get_component("collision")
        
        if not transform or not collision:
            return
            
        # Get player bounds
        half_width = collision.width / 2
        half_height = collision.height / 2
        
        # Constrain X position
        if transform.position.x - half_width < 0:
            transform.position.x = half_width
        elif transform.position.x + half_width > self.screen_bounds.width:
            transform.position.x = self.screen_bounds.width - half_width
            
        # Constrain Y position
        if transform.position.y - half_height < 0:
            transform.position.y = half_height
        elif transform.position.y + half_height > self.screen_bounds.height:
            transform.position.y = self.screen_bounds.height - half_height
            
    def _update_enemy_spawning(self, dt: float) -> None:
        """Update enemy spawning timers and spawn enemies."""
        # Update wave timer
        self.wave_timer += dt
        if self.wave_timer >= self.wave_interval:
            self.wave_timer = 0.0
            self.level_generator.spawn_enemy_wave()
            
        # Update fish spawn timer
        self.fish_spawn_timer += dt
        if self.fish_spawn_timer >= self.fish_spawn_interval:
            self.fish_spawn_timer = 0.0
            self.level_generator.spawn_fish()
            
    def _handle_collisions(self) -> None:
        """Handle collisions between entities."""
        if not self.entity_manager:
            return
            
        # Get all projectiles
        projectiles = self.entity_manager.get_entities_with_tag("projectile")
        
        # Check projectile collisions with enemies
        for projectile in projectiles:
            if not projectile.active:
                continue
                
            proj_transform = projectile.get_component("transform")
            proj_collision = projectile.get_component("collision")
            
            if not proj_transform or not proj_collision:
                continue
                
            # Get ink slime component for damage and color
            ink_slime = projectile.get_component("ink_slime")
            if not ink_slime:
                continue
                
            # Check collision with ships
            ships = self.entity_manager.get_entities_with_tag("ship")
            for ship in ships:
                if self._check_collision(projectile, ship):
                    # Ship hit by ink
                    ship.on_ink_hit(ink_slime.ink_color, ink_slime.ink_damage)
                    
                    # Get level component for scoring multiplier
                    level_comp = self.player.get_component("level")
                    score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                    
                    # Add score
                    score_increase = int(10 * score_multiplier)
                    self.score += score_increase
                    self.game_engine.score += score_increase
                    projectile.destroy()
                    break
                    
            # Check collision with turtles (they block shots)
            if projectile.active:
                turtles = self.entity_manager.get_entities_with_tag("turtle")
                for turtle in turtles:
                    if turtle.can_block_projectile((proj_transform.position.x, proj_transform.position.y)):
                        turtle.on_projectile_blocked()
                        projectile.destroy()
                        break
                        
            # Check collision with fish
            if projectile.active:
                fish_entities = self.entity_manager.get_entities_with_tag("fish")
                for fish in fish_entities:
                    if self._check_collision(projectile, fish):
                        # Get level component for scoring multiplier
                        level_comp = self.player.get_component("level")
                        score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                        
                        # Add score with multiplier
                        score_increase = int(fish.get_point_value() * score_multiplier)
                        self.score += score_increase
                        self.game_engine.score += score_increase
                        fish.on_hit()
                        projectile.destroy()
                        break
                        
            # Check collision with floating captains
            if projectile.active:
                captains = self.entity_manager.get_entities_with_tag("captain")
                for captain in captains:
                    captain_comp = captain.get_component("captain")
                    if captain_comp and captain_comp.state == "floating":
                        if self._check_collision(projectile, captain):
                            # Get level component for scoring multiplier
                            level_comp = self.player.get_component("level")
                            score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                            
                            # Add score with multiplier
                            score_increase = int(captain.get_point_value() * score_multiplier)
                            self.score += score_increase
                            self.game_engine.score += score_increase
                            captain.destroy()
                            projectile.destroy()
                            break
                            
    def _check_collision(self, entity1, entity2) -> bool:
        """Check if two entities are colliding.
        
        Args:
            entity1: First entity
            entity2: Second entity
            
        Returns:
            True if entities are colliding
        """
        transform1 = entity1.get_component("transform")
        collision1 = entity1.get_component("collision")
        transform2 = entity2.get_component("transform")
        collision2 = entity2.get_component("collision")
        
        if not all([transform1, collision1, transform2, collision2]):
            return False
            
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
        
    def _update_captains_on_ships(self) -> None:
        """Update captain positions to follow their ships."""
        if not self.entity_manager:
            return
            
        captains = self.entity_manager.get_entities_with_tag("captain")
        for captain in captains:
            captain_comp = captain.get_component("captain")
            if captain_comp and captain_comp.state == "on_ship" and captain_comp.attached_ship:
                captain.update_position_on_ship(captain_comp.attached_ship)
                
                # Check if ship is sinking
                ship_ink = captain_comp.attached_ship.get_component("ship_ink_load")
                if ship_ink and ship_ink.is_sinking():
                    captain.start_panic()
                    
    def _render_hud(self, surface: pygame.Surface) -> None:
        """Render the HUD (Heads-Up Display).
        
        Args:
            surface: The surface to render to
        """
        font = pygame.font.Font(None, 24)
        
        # Level info
        level_id = self.level_manager.get_current_level_id()
        level_name = self.level_manager.get_current_level_data()["name"]
        level_text = f"Level {level_id}: {level_name}"
        level_surface = font.render(level_text, True, (255, 255, 255))
        surface.blit(level_surface, (10, 10))
        
        # Score
        score_text = f"Score: {self.score}"
        score_surface = font.render(score_text, True, (255, 255, 255))
        surface.blit(score_surface, (10, 40))
        
        # Time remaining
        time_remaining = int(self.level_manager.get_level_time_remaining())
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        time_surface = font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surface, (10, 70))
        
        # Level progress bar
        progress = self.level_manager.get_level_progress()
        bar_width = 200
        bar_height = 20
        bar_x = surface.get_width() - bar_width - 10
        bar_y = 10
        
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw progress
        progress_width = int(bar_width * progress)
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, progress_width, bar_height))
        
        # Draw border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Progress text
        progress_text = f"Progress: {int(progress * 100)}%"
        progress_surface = font.render(progress_text, True, (255, 255, 255))
        surface.blit(progress_surface, (bar_x + (bar_width - progress_surface.get_width()) // 2, bar_y + 25))
        
        # Ink color indicator
        ink_color = self.level_manager.get_current_ink_color()
        ink_color_rgb = {
            "dark_blue": (0, 0, 150),
            "purple": (150, 0, 150),
            "green": (0, 150, 0),
            "red": (150, 0, 0),
            "rainbow": (150, 150, 0)  # Yellow as placeholder for rainbow
        }.get(ink_color, (0, 0, 150))
        
        pygame.draw.circle(surface, ink_color_rgb, (surface.get_width() - 30, 70), 15)
        pygame.draw.circle(surface, (255, 255, 255), (surface.get_width() - 30, 70), 15, 2)
        
    def _on_level_complete(self, level_id: int, score: int) -> None:
        """Callback for when a level is completed.
        
        Args:
            level_id: The completed level ID
            score: The score achieved
        """
        print(f"Level {level_id} completed with score {score}!")
        
    def _on_level_failed(self, level_id: int, score: int) -> None:
        """Callback for when a level is failed.
        
        Args:
            level_id: The failed level ID
            score: The score achieved
        """
        print(f"Level {level_id} failed with score {score}!")
        
    def _transition_to_level_complete(self) -> None:
        """Transition to the level complete state."""
        # Use the scene manager to transition to the level complete state
        self.transition_to("level_transition", level_id=self.level_manager.get_current_level_id(), score=self.score)