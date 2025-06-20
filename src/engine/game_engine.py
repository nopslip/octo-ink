"""
Core game engine for Octopus Ink Slime game.
Manages the main game loop and coordinates all subsystems.
"""

import pygame
import sys
import random
import os
# Try to import psutil, but make it optional
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
from typing import Optional, List
from src.entities.entity_manager import EntityManager
from src.entities.entity_factory import EntityFactory
from src.entities.ship import Ship
from src.entities.captain import Captain
from src.entities.turtle import Turtle
from src.entities.fish import Fish


class GameEngine:
    """Main game engine that coordinates all game systems."""
    
    def __init__(self):
        """Initialize the game engine."""
        self.running = False
        self.screen = None
        self.clock = None
        self.fps = 60
        
        # Entity system
        self.entity_manager = None
        self.entity_factory = None
        
        # Game managers
        self.scene_manager = None
        self.input_manager = None
        self.asset_manager = None
        self.physics_engine = None
        self.audio_manager = None
        self.ui_manager = None
        
        # Level system
        self.level_manager = None
        self.level_generator = None
        
        # Game state
        self.score = 0
        self.wave_timer = 0.0
        self.wave_interval = 5.0  # Spawn enemies every 5 seconds
        self.fish_spawn_timer = 0.0
        self.fish_spawn_interval = 3.0  # Spawn fish every 3 seconds
        
        # Debug mode
        self.debug_mode = False
        self.show_fps = False
        self.show_entity_count = False
        self.show_collision_areas = False
        self.show_entity_boundaries = False
        self.show_grid = False
        
        # Performance monitoring
        self.frame_times = []
        self.max_frame_times = 60  # Store last 60 frames for averaging
        
    def initialize(self, width: int = 800, height: int = 600, title: str = "Octopus Ink Slime"):
        """
        Initialize pygame and all game systems.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            title: Window title
        """
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Initialize clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Initialize Entity System
        self.entity_manager = EntityManager()
        self.entity_factory = EntityFactory()
        self.entity_factory.set_entity_manager(self.entity_manager)
        
        # Initialize Level System
        from src.levels.level_manager import LevelManager
        from src.levels.level_generator import LevelGenerator
        self.level_manager = LevelManager()
        self.level_generator = LevelGenerator(width, height)
        self.level_generator.set_entity_systems(self.entity_manager, self.entity_factory)
        
        # Initialize all managers
        from src.engine.scene_manager import SceneManager
        from src.engine.input_manager import InputManager
        from src.engine.asset_manager import AssetManager
        from src.engine.physics_engine import PhysicsEngine
        from src.engine.audio_manager import AudioManager
        from src.engine.ui_manager import UIManager
        
        self.scene_manager = SceneManager(self)
        self.input_manager = InputManager()
        self.asset_manager = AssetManager()
        self.physics_engine = PhysicsEngine()
        self.audio_manager = AudioManager.get_instance()
        self.ui_manager = UIManager((width, height))
        
        # Initialize optimization systems
        from src.utils.spatial_grid import SpatialGrid
        from src.utils.object_pool import ProjectilePool
        from src.utils.asset_cache import AssetCache
        from src.utils.effects_manager import EffectsManager
        
        # Initialize spatial grid for collision detection
        self.spatial_grid = SpatialGrid(width, height, cell_size=100)
        
        # Initialize projectile pool for object reuse
        self.projectile_pool = ProjectilePool.get_instance()
        self.projectile_pool.initialize(self.entity_factory, self.entity_manager)
        
        # Initialize asset cache for resource management
        self.asset_cache = AssetCache.get_instance()
        
        # Initialize effects manager for visual effects
        self.effects_manager = EffectsManager.get_instance()
        
        # Load default sounds
        self.audio_manager.load_default_sounds()
        
        # Start with the main menu state instead of creating test entities
        self.scene_manager.start("main_menu")
        
        print(f"Game engine initialized with resolution {width}x{height}")
        
    def run(self):
        """Main game loop."""
        if not self.screen:
            raise RuntimeError("Game engine not initialized. Call initialize() first.")
            
        self.running = True
        
        while self.running:
            # Calculate delta time in seconds
            dt = self.clock.tick(self.fps) / 1000.0
            
            # Calculate delta time in seconds
            dt = self.clock.tick(self.fps) / 1000.0
            
            # Store frame time for FPS calculation
            self.frame_times.append(dt)
            if len(self.frame_times) > self.max_frame_times:
                self.frame_times.pop(0)
            
            # Process events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Global debug toggles that work in any state
                    if event.key == pygame.K_F3:
                        # Toggle debug mode
                        self.debug_mode = not self.debug_mode
                        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
                        
                        # When debug mode is enabled, turn on all debug displays
                        if self.debug_mode:
                            self.show_fps = True
                            self.show_entity_count = True
                            self.show_collision_areas = True
                            self.show_entity_boundaries = True
                            self.show_grid = True
                        else:
                            # Turn off all debug displays
                            self.show_fps = False
                            self.show_entity_count = False
                            self.show_collision_areas = False
                            self.show_entity_boundaries = False
                            self.show_grid = False
                    # Additional debug toggles
                    elif self.debug_mode and event.key == pygame.K_F4:
                        self.show_fps = not self.show_fps
                    elif self.debug_mode and event.key == pygame.K_F5:
                        self.show_entity_count = not self.show_entity_count
                    elif self.debug_mode and event.key == pygame.K_F6:
                        self.show_collision_areas = not self.show_collision_areas
                    elif self.debug_mode and event.key == pygame.K_F7:
                        self.show_entity_boundaries = not self.show_entity_boundaries
                    elif self.debug_mode and event.key == pygame.K_F8:
                        self.show_grid = not self.show_grid
            
            # Let scene manager handle events first (this includes state-specific event handling)
            if self.scene_manager:
                self.scene_manager.handle_events(events)
            
            # Process input through input manager
            if self.input_manager:
                self.input_manager.process_input(events)
                
            # Let UI manager handle events
            if self.ui_manager:
                for event in events:  # Process all events for UI
                    self.ui_manager.handle_event(event)
            
            # Update current scene (this handles state-specific updates)
            if self.scene_manager:
                self.scene_manager.update(dt)
            
            # Only run gameplay-specific logic if we're in gameplay state
            if self.scene_manager and self.scene_manager.current_state:
                current_state = self.scene_manager.current_state
                if hasattr(current_state, '__class__') and current_state.__class__.__name__ == 'GameplayState':
                    # Update entity manager
                    if self.entity_manager:
                        self.entity_manager.update(dt)
                        
                    # Keep player within screen bounds
                    self._constrain_player_to_screen()
                    
                    # Update level manager
                    if self.level_manager:
                        self.level_manager.update(dt, self.score)
                    
                    # Update enemy spawning
                    self._update_enemy_spawning(dt)
                    
                    # Handle collisions
                    self._handle_collisions()
                    
                    # Update captain positions on ships
                    self._update_captains_on_ships()
                    
                    # Check for level completion
                    if self.level_manager and self.level_manager.is_level_completed():
                        self._handle_level_completion()
            
            # Update physics
            if self.physics_engine:
                self.physics_engine.update(dt)
                
            # Update UI
            if self.ui_manager:
                self.ui_manager.update(dt)
                
            # Update effects
            if hasattr(self, 'effects_manager'):
                self.effects_manager.update(dt)
            
            # Clear screen with default background
            self.screen.fill((0, 50, 100))  # Default dark blue ocean color
            
            # Render current scene (this handles state-specific rendering)
            if self.scene_manager:
                self.scene_manager.render(self.screen)
            
            # Only render gameplay-specific elements if we're in gameplay state
            if self.scene_manager and self.scene_manager.current_state:
                current_state = self.scene_manager.current_state
                if hasattr(current_state, '__class__') and current_state.__class__.__name__ == 'GameplayState':
                    # Render entities
                    if self.entity_manager:
                        self.entity_manager.render(self.screen)
                        
                    # Render visual effects
                    if hasattr(self, 'effects_manager'):
                        # Get camera offset from shake effect
                        camera_offset = (0, 0)
                        if self.effects_manager.camera_shake:
                            camera_offset = self.effects_manager.get_camera_offset()
                        
                        # Render effects with camera offset
                        self.effects_manager.render(self.screen, camera_offset)
                    
                    # Draw HUD if in gameplay
                    self._render_hud()
                    
            # Render UI (this should be rendered on top of everything)
            if self.ui_manager:
                self.ui_manager.render(self.screen)
            
            # Render debug information if debug mode is enabled
            if self.debug_mode:
                self._render_debug_info()
            
            # Update display
            pygame.display.flip()
            
    def quit(self):
        """Clean up and quit the game."""
        self.running = False
        pygame.quit()
        sys.exit()
        
    def _create_test_entities(self):
        """Create test entities for demonstration purposes."""
        # Initialize level 1
        if self.level_manager:
            level_data = self.level_manager.start_level()
            if self.level_generator:
                self.level_generator.initialize_level(level_data)
        
        # Create a player entity at the center of the screen
        self.player = self.entity_factory.create_player(
            self.screen.get_width() // 2,
            self.screen.get_height() // 2
        )
        
        # Add level component to player if level system is initialized
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
        
        # Create initial enemies for testing
        self._spawn_enemy_wave()
        
    def _render_hud(self):
        """Render the heads-up display during gameplay."""
        # Only render HUD if we're in gameplay state
        if not self.scene_manager or not hasattr(self.scene_manager, 'current_state'):
            return
            
        # Check if we're in gameplay state
        current_state = self.scene_manager.current_state
        if not current_state or not hasattr(current_state, 'element_id') or current_state.element_id != "gameplay":
            return
            
        # If we have a UI manager, use it to render the HUD
        if self.ui_manager:
            # Make sure HUD elements exist
            if not self.ui_manager.get_element("score_label"):
                self._setup_hud()
                
            # Update HUD values
            self.ui_manager.set_element_text("score_label", f"Score: {self.score}")
            
            # Update level display if available
            if self.level_manager:
                level_id = self.level_manager.get_current_level_id()
                self.ui_manager.set_element_text("level_label", f"Level: {level_id}")
                
            # Update health bar if player exists
            if hasattr(self, 'player') and self.player:
                health_component = self.player.get_component("health")
                if health_component:
                    health_percent = health_component.current_health / health_component.max_health
                    self.ui_manager.set_progress_bar_value("health_bar", health_percent)
        else:
            # Fallback to simple text rendering
            font = pygame.font.Font(None, 24)
            
            # Entity count
            entity_count = self.entity_manager.get_entity_count() if self.entity_manager else 0
            active_count = self.entity_manager.get_active_entity_count() if self.entity_manager else 0
            
            debug_texts = [
                f"Octopus Ink Slime",
                f"Score: {self.score}",
                f"Level: {self.level_manager.get_current_level_id() if self.level_manager else 1}",
                f"Entities: {entity_count} (Active: {active_count})",
                f"FPS: {int(self.clock.get_fps())}",
                "Arrow Keys: Move, Space: Shoot, ESC: Pause"
            ]
            
            y_offset = 10
            for text_str in debug_texts:
                text = font.render(text_str, True, (255, 255, 255))
                self.screen.blit(text, (10, y_offset))
                y_offset += 30
    
    def _setup_hud(self):
        """Set up the HUD UI elements."""
        if not self.ui_manager:
            return
            
        # Create score label
        score_rect = pygame.Rect(10, 10, 200, 30)
        self.ui_manager.create_label(
            score_rect,
            "score_label",
            f"Score: {self.score}",
            text_color=(255, 255, 255),
            font_size=24,
            align="left"
        )
        
        # Create level label
        level_rect = pygame.Rect(10, 40, 200, 30)
        level_id = self.level_manager.get_current_level_id() if self.level_manager else 1
        self.ui_manager.create_label(
            level_rect,
            "level_label",
            f"Level: {level_id}",
            text_color=(255, 255, 255),
            font_size=24,
            align="left"
        )
        
        # Create health bar
        health_label_rect = pygame.Rect(10, 70, 100, 20)
        self.ui_manager.create_label(
            health_label_rect,
            "health_label",
            "Health:",
            text_color=(255, 255, 255),
            font_size=20,
            align="left"
        )
        
        health_bar_rect = pygame.Rect(120, 70, 150, 20)
        self.ui_manager.create_progress_bar(
            health_bar_rect,
            "health_bar",
            value=1.0,
            bg_color=(50, 50, 50),
            fill_color=(0, 200, 0),
            border_color=(255, 255, 255),
            show_text=False
        )
        
        # Create ink label
        ink_label_rect = pygame.Rect(10, 100, 100, 20)
        self.ui_manager.create_label(
            ink_label_rect,
            "ink_label",
            "Ink:",
            text_color=(255, 255, 255),
            font_size=20,
            align="left"
        )
        
        # Create ink color indicator
        ink_color = self.level_manager.get_current_ink_color() if self.level_manager else "dark_blue"
        ink_color_rgb = {
            "dark_blue": (0, 0, 150),
            "purple": (150, 0, 150),
            "green": (0, 150, 0),
            "red": (150, 0, 0),
            "rainbow": (150, 150, 0)
        }.get(ink_color, (0, 0, 150))
        
        ink_color_rect = pygame.Rect(120, 100, 30, 20)
        self.ui_manager.create_panel(
            ink_color_rect,
            "ink_color_indicator",
            bg_color=ink_color_rgb,
            border_color=(255, 255, 255),
            border_width=1
        )
            
    def _render_debug_info(self):
        """Render debug information when debug mode is enabled."""
        # Create a font for debug text
        font = pygame.font.Font(None, 20)
        
        # Calculate current FPS
        if self.frame_times:
            current_fps = len(self.frame_times) / sum(self.frame_times)
        else:
            current_fps = 0
            
        # Get entity counts
        if self.entity_manager:
            entity_count = self.entity_manager.get_entity_count()
            active_count = self.entity_manager.get_active_entity_count()
            projectile_count = len(self.entity_manager.get_entities_with_tag("projectile"))
        else:
            entity_count = 0
            active_count = 0
            projectile_count = 0
            
        # Prepare debug text
        debug_texts = [
            f"DEBUG MODE (F3 to toggle)",
            f"FPS: {current_fps:.1f} (Target: {self.fps})",
            f"Entities: {entity_count} (Active: {active_count})",
            f"Projectiles: {projectile_count}",
            f"Memory: {psutil.Process().memory_info().rss / (1024 * 1024):.1f} MB" if PSUTIL_AVAILABLE else f"Memory: Not available (psutil not installed)",
            f"F4: Toggle FPS | F5: Toggle Entity Count",
            f"F6: Toggle Collision Areas | F7: Toggle Boundaries"
        ]
        
        # Draw semi-transparent background for debug panel
        debug_panel = pygame.Surface((300, len(debug_texts) * 20 + 10), pygame.SRCALPHA)
        debug_panel.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(debug_panel, (self.screen.get_width() - 310, 10))
        
        # Render debug text
        y_offset = 15
        for text_str in debug_texts:
            text = font.render(text_str, True, (255, 255, 0))  # Yellow text
            self.screen.blit(text, (self.screen.get_width() - 300, y_offset))
            y_offset += 20
            
        # Draw entity boundaries if enabled
        if self.show_entity_boundaries and self.entity_manager:
            for entity in self.entity_manager.entities.values():
                if not entity.active:
                    continue
                    
                transform = entity.get_component("transform")
                if not transform:
                    continue
                    
                # Draw a dot at entity position
                pygame.draw.circle(
                    self.screen,
                    (255, 0, 0),  # Red
                    (int(transform.position.x), int(transform.position.y)),
                    3
                )
                
                # Draw entity ID text
                id_text = font.render(str(entity.entity_id), True, (255, 255, 255))
                self.screen.blit(id_text, (transform.position.x + 5, transform.position.y - 10))
                
        # Draw collision areas if enabled
        if self.show_collision_areas and self.entity_manager:
            for entity in self.entity_manager.entities.values():
                if not entity.active:
                    continue
                    
                transform = entity.get_component("transform")
                collision = entity.get_component("collision")
                
                if not transform or not collision:
                    continue
                    
                # Draw collision rectangle
                rect = pygame.Rect(
                    transform.position.x - collision.width / 2,
                    transform.position.y - collision.height / 2,
                    collision.width,
                    collision.height
                )
                
                # Use different colors for different collision types
                if "player" in entity.tags:
                    color = (0, 255, 0, 128)  # Green for player
                elif "enemy" in entity.tags:
                    color = (255, 0, 0, 128)  # Red for enemies
                elif "projectile" in entity.tags:
                    color = (0, 0, 255, 128)  # Blue for projectiles
                else:
                    color = (255, 255, 0, 128)  # Yellow for other entities
                    
                # Create a surface with alpha for the collision area
                collision_surface = pygame.Surface((collision.width, collision.height), pygame.SRCALPHA)
                collision_surface.fill(color)
                self.screen.blit(collision_surface, rect)
                
                # Draw outline
                pygame.draw.rect(
                    self.screen,
                    color[:3],  # Remove alpha for outline
                    rect,
                    1  # Line width
                )
                
        # Draw spatial grid if enabled and available
        if self.show_grid and hasattr(self, 'spatial_grid'):
            self.spatial_grid.render_debug(self.screen)
            
    def _constrain_player_to_screen(self):
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
            
    def _update_enemy_spawning(self, dt: float):
        """Update enemy spawning timers and spawn enemies."""
        # If level generator is available, use it
        if self.level_generator:
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
        else:
            # Fall back to old method
            # Update wave timer
            self.wave_timer += dt
            if self.wave_timer >= self.wave_interval:
                self.wave_timer = 0.0
                self._spawn_enemy_wave()
                
            # Update fish spawn timer
            self.fish_spawn_timer += dt
            if self.fish_spawn_timer >= self.fish_spawn_interval:
                self.fish_spawn_timer = 0.0
                self._spawn_fish()
            
    def _spawn_enemy_wave(self):
        """Spawn a wave of enemies."""
        # Spawn a ship with captain
        ship_size = random.choice(["small", "medium", "large"])
        ship_y = random.randint(100, 400)
        direction = random.choice([-1, 1])
        ship_x = -50 if direction > 0 else self.screen.get_width() + 50
        
        # Create ship
        ship = Ship((ship_x, ship_y), ship_size, direction)
        self.entity_manager.add_entity(ship)
        
        # Create captain and attach to ship
        captain = Captain((ship_x, ship_y))
        self.entity_manager.add_entity(captain)
        ship.attach_captain(captain)
        
        # Spawn some turtles
        for _ in range(random.randint(1, 3)):
            turtle_x = random.randint(100, self.screen.get_width() - 100)
            turtle_y = random.randint(100, self.screen.get_height() - 100)
            turtle = Turtle((turtle_x, turtle_y))
            self.entity_manager.add_entity(turtle)
            
    def _spawn_fish(self):
        """Spawn bonus fish."""
        fish_type = random.choice(["normal", "fast", "school"])
        
        if fish_type == "school":
            # Spawn a school of fish
            center_x = random.randint(100, self.screen.get_width() - 100)
            center_y = random.randint(100, self.screen.get_height() - 100)
            school = Fish.create_school((center_x, center_y), count=5)
            for fish in school:
                self.entity_manager.add_entity(fish)
        else:
            # Spawn a single fish
            fish_x = random.randint(50, self.screen.get_width() - 50)
            fish_y = random.randint(50, self.screen.get_height() - 50)
            fish = Fish((fish_x, fish_y), fish_type)
            self.entity_manager.add_entity(fish)
            
    def _handle_collisions(self):
        """Handle collisions between entities."""
        if not self.entity_manager:
            return
            
        # Update spatial grid with current entity positions
        if hasattr(self, 'spatial_grid'):
            # Get all entities from the entity manager (using entities.values() instead of get_all_entities)
            all_entities = list(self.entity_manager.entities.values())
            self.spatial_grid.update(all_entities)
            
            # Get all projectiles
            projectiles = self.entity_manager.get_entities_with_tag("projectile")
            
            # Check projectile collisions with potential targets using spatial grid
            for projectile in projectiles:
                if not projectile.active:
                    continue
                    
                proj_transform = projectile.get_component("transform")
                proj_collision = projectile.get_component("collision")
                
                if not proj_transform or not proj_collision:
                    continue
                    
                # Get potential collision targets from spatial grid
                potential_targets = self.spatial_grid.get_potential_collisions(projectile)
                
                # Check collision with ships
                for entity in potential_targets:
                    if not entity.active:
                        continue
                        
                    # Handle ship collisions
                    if "ship" in entity.tags and self.spatial_grid.check_collision(projectile, entity):
                        ship = entity
                        # Get ink slime component for damage and color
                        ink_slime = projectile.get_component("ink_slime")
                        if ink_slime:
                            # Ship hit by ink
                            ship.on_ink_hit(ink_slime.ink_color, ink_slime.ink_damage)
                            
                            # Get level component for scoring multiplier
                            level_comp = self.player.get_component("level")
                            score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                            
                            # Add score with multiplier
                            self.score += int(10 * score_multiplier)
                            
                            # Create splash effect
                            if self.effects_manager:
                                self.effects_manager.create_splash(
                                    ship.get_component("transform").position.x,
                                    ship.get_component("transform").position.y,
                                    color=self._get_color_from_ink(ink_slime.ink_color)
                                )
                            
                            # Return projectile to pool instead of destroying
                            if hasattr(self, 'projectile_pool'):
                                self.projectile_pool.release_projectile(projectile)
                            else:
                                projectile.destroy()
                            break
                        else:
                            # Fallback if no ink slime component
                            ship.on_ink_hit("blue", 10)  # Placeholder ink values
                            self.score += 10
                            projectile.destroy()
                            break
                    
                    # Handle turtle collisions (they block shots)
                    elif "turtle" in entity.tags:
                        turtle = entity
                        if turtle.can_block_projectile((proj_transform.position.x, proj_transform.position.y)):
                            turtle.on_projectile_blocked()
                            
                            # Add shield flash effect
                            if self.effects_manager:
                                self.effects_manager.start_flash(0.1, (200, 200, 255))
                                
                            # Return projectile to pool instead of destroying
                            if hasattr(self, 'projectile_pool'):
                                self.projectile_pool.release_projectile(projectile)
                            else:
                                projectile.destroy()
                            break
                    
                    # Handle fish collisions
                    elif "fish" in entity.tags and self.spatial_grid.check_collision(projectile, entity):
                        fish = entity
                        # Get level component for scoring multiplier
                        level_comp = self.player.get_component("level")
                        score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                        
                        # Add score with multiplier
                        self.score += int(fish.get_point_value() * score_multiplier)
                        fish.on_hit()
                        
                        # Return projectile to pool instead of destroying
                        if hasattr(self, 'projectile_pool'):
                            self.projectile_pool.release_projectile(projectile)
                        else:
                            projectile.destroy()
                        break
                    
                    # Handle floating captain collisions
                    elif "captain" in entity.tags and self.spatial_grid.check_collision(projectile, entity):
                        captain = entity
                        captain_comp = captain.get_component("captain")
                        if captain_comp and captain_comp.state == "floating":
                            # Get level component for scoring multiplier
                            level_comp = self.player.get_component("level")
                            score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                            
                            # Add score with multiplier
                            self.score += int(captain.get_point_value() * score_multiplier)
                            
                            # Add explosion effect
                            if self.effects_manager:
                                transform = captain.get_component("transform")
                                if transform:
                                    self.effects_manager.create_explosion(
                                        transform.position.x,
                                        transform.position.y,
                                        color=(255, 100, 100),
                                        size="small"
                                    )
                            
                            captain.destroy()
                            
                            # Return projectile to pool instead of destroying
                            if hasattr(self, 'projectile_pool'):
                                self.projectile_pool.release_projectile(projectile)
                            else:
                                projectile.destroy()
                            break
        else:
            # Fallback to old collision detection method if spatial grid is not available
            self._handle_collisions_legacy()
    
    def _handle_collisions_legacy(self):
        """Legacy collision detection method (fallback)."""
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
                
            # Check collision with ships
            ships = self.entity_manager.get_entities_with_tag("ship")
            for ship in ships:
                if self._check_collision(projectile, ship):
                    # Get ink slime component for damage and color
                    ink_slime = projectile.get_component("ink_slime")
                    if ink_slime:
                        # Ship hit by ink
                        ship.on_ink_hit(ink_slime.ink_color, ink_slime.ink_damage)
                        
                        # Get level component for scoring multiplier
                        level_comp = self.player.get_component("level")
                        score_multiplier = level_comp.get_scoring_multiplier() if level_comp else 1.0
                        
                        # Add score with multiplier
                        self.score += int(10 * score_multiplier)
                        projectile.destroy()
                        break
                    else:
                        # Fallback if no ink slime component
                        ship.on_ink_hit("blue", 10)  # Placeholder ink values
                        self.score += 10
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
                        self.score += int(fish.get_point_value() * score_multiplier)
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
                            self.score += int(captain.get_point_value() * score_multiplier)
                            captain.destroy()
                            projectile.destroy()
                            break
                            
    def _get_color_from_ink(self, ink_color: str) -> tuple:
        """Convert ink color name to RGB tuple."""
        color_map = {
            "dark_blue": (0, 0, 150),
            "purple": (150, 0, 150),
            "green": (0, 150, 0),
            "red": (150, 0, 0),
            "rainbow": (150, 150, 0)
        }
        return color_map.get(ink_color, (0, 0, 150))
                            
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
        
    def _update_captains_on_ships(self):
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
                    
    def _handle_level_completion(self) -> None:
        """Handle level completion and transition to next level."""
        # Get level completion stats
        level_stats = self.level_manager.get_level_completion_stats()
        
        print(f"Level {level_stats['level_id']} completed!")
        print(f"Score: {level_stats['score']}")
        
        # Check if there are more levels
        if level_stats['level_id'] < self.level_manager.get_level_count():
            # Advance to next level
            self.level_manager.advance_to_next_level()
            
            # In a real implementation with a scene manager:
            # self.scene_manager.change_state("level_transition", level_stats)
            
            # For now, just reinitialize the level
            level_data = self.level_manager.get_current_level_data()
            self.level_generator.initialize_level(level_data)
            
            # Update player's ink color
            ink_color = self.level_manager.get_current_ink_color()
            if self.player:
                # Update level component
                level_comp = self.player.get_component("level")
                if level_comp:
                    level_comp.set_level(self.level_manager.get_current_level_id())
                
                # Update weapon directly as fallback
                weapon = self.player.get_component("weapon")
                if weapon:
                    weapon.set_ink_color(ink_color)
        else:
            # Game completed
            print("All levels completed! Game over!")
            # In a real implementation:
            # self.scene_manager.change_state("victory")