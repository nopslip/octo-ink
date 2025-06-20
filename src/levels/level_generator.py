"""Level generator for the Octopus Ink Slime game.

This module handles the generation of enemy waves, obstacle placement,
and spawn point configuration based on level difficulty.
"""

import random
from typing import Dict, List, Tuple, Any, Optional
import pygame
from src.levels.level_data import LevelData


class LevelGenerator:
    """Generates level content based on difficulty parameters.
    
    The LevelGenerator creates enemy waves, places obstacles, and
    configures spawn points based on the current level's difficulty.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize the LevelGenerator.
        
        Args:
            screen_width: Width of the game screen in pixels
            screen_height: Height of the game screen in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level_data: Dict[str, Any] = {}
        self.entity_manager = None
        self.entity_factory = None
        
    def set_entity_systems(self, entity_manager, entity_factory) -> None:
        """Set the entity manager and factory for entity creation.
        
        Args:
            entity_manager: The entity manager instance
            entity_factory: The entity factory instance
        """
        self.entity_manager = entity_manager
        self.entity_factory = entity_factory
        
    def initialize_level(self, level_data: Dict[str, Any]) -> None:
        """Initialize a new level with the given level data.
        
        Args:
            level_data: The level configuration data
        """
        self.current_level_data = level_data
        
        # Clear existing entities if needed
        # This would typically be handled by the scene manager
        
        # Place initial obstacles
        self._place_obstacles()
        
    def generate_enemy_wave(self) -> List[Dict[str, Any]]:
        """Generate a wave of enemies based on current level difficulty.
        
        Returns:
            A list of enemy configuration dictionaries
        """
        if not self.current_level_data:
            return []
            
        enemies = []
        
        # Get level parameters
        ship_count = self.current_level_data["ship_count"]
        difficulty = self.current_level_data["difficulty_multiplier"]
        
        # Generate ships with captains
        for _ in range(ship_count):
            # Determine ship size based on difficulty
            size_weights = {
                "small": max(0.7 - (difficulty * 0.1), 0.3),
                "medium": 0.4,
                "large": min(0.3 + (difficulty * 0.1), 0.5)
            }
            
            sizes = list(size_weights.keys())
            weights = list(size_weights.values())
            ship_size = random.choices(sizes, weights=weights, k=1)[0]
            
            # Determine spawn position (from left or right side)
            direction = random.choice([-1, 1])
            ship_x = -50 if direction > 0 else self.screen_width + 50
            ship_y = random.randint(100, self.screen_height - 100)
            
            # Calculate ship speed based on level difficulty
            base_speed = self.current_level_data["ship_speed"]
            speed_variation = random.uniform(0.8, 1.2)
            ship_speed = base_speed * speed_variation
            
            # Ship health based on level and size
            base_health = self.current_level_data["ship_health"]
            size_multiplier = {"small": 0.8, "medium": 1.0, "large": 1.3}
            ship_health = base_health * size_multiplier[ship_size]
            
            # Create ship configuration
            ship_config = {
                "type": "ship",
                "position": (ship_x, ship_y),
                "size": ship_size,
                "direction": direction,
                "speed": ship_speed,
                "health": ship_health,
                "has_captain": True
            }
            
            enemies.append(ship_config)
            
        return enemies
        
    def spawn_enemy_wave(self) -> None:
        """Generate and spawn a wave of enemies in the game world."""
        if not self.entity_manager or not self.entity_factory:
            return
            
        enemy_configs = self.generate_enemy_wave()
        
        for config in enemy_configs:
            if config["type"] == "ship":
                # Create ship
                ship = self.entity_factory.create_ship(
                    config["position"][0],
                    config["position"][1],
                    config["size"],
                    config["direction"],
                    config["speed"],
                    config["health"]
                )
                
                # Create captain if needed
                if config["has_captain"]:
                    captain = self.entity_factory.create_captain(
                        config["position"][0],
                        config["position"][1]
                    )
                    
                    # Attach captain to ship
                    ship_component = ship.get_component("ship")
                    if ship_component:
                        ship_component.attach_captain(captain)
                        
    def spawn_turtles(self) -> None:
        """Spawn turtle obstacles based on level configuration."""
        if not self.entity_manager or not self.entity_factory:
            return
            
        turtle_count = self.current_level_data["turtle_count"]
        turtle_speed = self.current_level_data["turtle_speed"]
        
        for _ in range(turtle_count):
            # Determine spawn position (avoid edges)
            turtle_x = random.randint(100, self.screen_width - 100)
            turtle_y = random.randint(100, self.screen_height - 100)
            
            # Create turtle with random movement pattern
            movement_pattern = random.choice(["stationary", "linear", "circular"])
            
            self.entity_factory.create_turtle(
                turtle_x,
                turtle_y,
                movement_pattern,
                turtle_speed
            )
            
    def spawn_fish(self) -> Optional[Dict[str, Any]]:
        """Spawn bonus fish based on level configuration.
        
        Returns:
            The spawned fish entity or None if no fish was spawned
        """
        if not self.entity_manager or not self.entity_factory:
            return None
            
        # Check if fish should spawn based on spawn rate
        if random.random() > self.current_level_data["fish_spawn_rate"]:
            return None
            
        # Determine fish type
        fish_types = ["normal", "fast", "school"]
        fish_weights = [0.6, 0.3, 0.1]
        fish_type = random.choices(fish_types, weights=fish_weights, k=1)[0]
        
        # Determine spawn position
        fish_x = random.randint(50, self.screen_width - 50)
        fish_y = random.randint(50, self.screen_height - 50)
        
        # Apply value multiplier from level data
        value_multiplier = self.current_level_data["fish_value_multiplier"]
        
        if fish_type == "school":
            # Spawn a school of fish
            school_size = random.randint(3, 6)
            school = []
            
            for i in range(school_size):
                # Create fish in a loose formation
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                
                fish = self.entity_factory.create_fish(
                    fish_x + offset_x,
                    fish_y + offset_y,
                    "normal",
                    value_multiplier
                )
                
                school.append(fish)
                
            return {"type": "school", "entities": school}
        else:
            # Spawn a single fish
            fish = self.entity_factory.create_fish(
                fish_x,
                fish_y,
                fish_type,
                value_multiplier
            )
            
            return {"type": "single", "entity": fish}
            
    def _place_obstacles(self) -> None:
        """Place obstacles in the level based on level configuration."""
        if not self.entity_manager or not self.entity_factory:
            return
            
        # Get obstacle types from level data
        obstacle_types = self.current_level_data.get("obstacles", [])
        
        # Place each type of obstacle
        for obstacle_type in obstacle_types:
            # Number of obstacles depends on type
            count = {
                "seaweed": random.randint(5, 10),
                "rocks": random.randint(3, 7),
                "coral": random.randint(2, 5),
                "shipwreck": random.randint(1, 2),
                "volcanic_vents": random.randint(1, 3),
                "whirlpools": random.randint(1, 2)
            }.get(obstacle_type, 0)
            
            for _ in range(count):
                # Determine position (avoid center area where player starts)
                while True:
                    x = random.randint(50, self.screen_width - 50)
                    y = random.randint(50, self.screen_height - 50)
                    
                    # Check if position is far enough from center
                    center_x, center_y = self.screen_width // 2, self.screen_height // 2
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    
                    if distance > 150:  # Minimum distance from center
                        break
                        
                # Create obstacle (placeholder - would call entity factory)
                # self.entity_factory.create_obstacle(x, y, obstacle_type)
                
    def get_spawn_points(self) -> Dict[str, List[Tuple[int, int]]]:
        """Get spawn points for different entity types.
        
        Returns:
            Dictionary mapping entity types to lists of spawn positions
        """
        spawn_points = {
            "ship": [],
            "turtle": [],
            "fish": []
        }
        
        # Ship spawn points (edges of screen)
        left_edge = -50
        right_edge = self.screen_width + 50
        
        for y in range(100, self.screen_height - 100, 100):
            spawn_points["ship"].append((left_edge, y))
            spawn_points["ship"].append((right_edge, y))
            
        # Turtle spawn points (scattered around the level)
        for _ in range(10):
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(100, self.screen_height - 100)
            spawn_points["turtle"].append((x, y))
            
        # Fish spawn points (more central areas)
        for _ in range(15):
            x = random.randint(200, self.screen_width - 200)
            y = random.randint(200, self.screen_height - 200)
            spawn_points["fish"].append((x, y))
            
        return spawn_points
        
    def get_background_for_level(self) -> str:
        """Get the background image name for the current level.
        
        Returns:
            The name of the background image to use
        """
        return self.current_level_data.get("background", "shallow_water")