"""Level data for the Octopus Ink Slime game.

This module defines the configuration for each level in the game,
including difficulty parameters, enemy properties, and visual themes.
"""

from typing import Dict, List, Any


class LevelData:
    """Static class containing level configuration data."""

    # Level configurations
    LEVELS: List[Dict[str, Any]] = [
        # Level 1: Dark Blue Ink
        {
            "level_id": 1,
            "name": "Dark Depths",
            "description": "Begin your journey in the shallow waters with dark blue ink.",
            "ship_speed": 80,  # pixels per second
            "ship_count": 1,
            "ship_health": 100,
            "turtle_count": 2,
            "turtle_speed": 30,
            "fish_spawn_rate": 0.2,  # probability per second
            "fish_value_multiplier": 1.0,
            "ink_color": "dark_blue",
            "ink_damage": 10,
            "ink_amount": 100,
            "background": "shallow_water",
            "obstacles": ["seaweed", "rocks"],
            "time_limit": 120,  # seconds
            "score_target": 1000,
            "difficulty_multiplier": 1.0
        },
        
        # Level 2: Purple Ink
        {
            "level_id": 2,
            "name": "Purple Haze",
            "description": "The waters grow deeper as your ink turns purple.",
            "ship_speed": 100,
            "ship_count": 2,
            "ship_health": 120,
            "turtle_count": 3,
            "turtle_speed": 40,
            "fish_spawn_rate": 0.25,
            "fish_value_multiplier": 1.2,
            "ink_color": "purple",
            "ink_damage": 12,
            "ink_amount": 120,
            "background": "medium_water",
            "obstacles": ["seaweed", "rocks", "coral"],
            "time_limit": 150,
            "score_target": 2000,
            "difficulty_multiplier": 1.3
        },
        
        # Level 3: Green Ink
        {
            "level_id": 3,
            "name": "Emerald Abyss",
            "description": "Your ink turns green as you venture into the abyss.",
            "ship_speed": 120,
            "ship_count": 2,
            "ship_health": 140,
            "turtle_count": 4,
            "turtle_speed": 50,
            "fish_spawn_rate": 0.3,
            "fish_value_multiplier": 1.5,
            "ink_color": "green",
            "ink_damage": 15,
            "ink_amount": 140,
            "background": "deep_water",
            "obstacles": ["seaweed", "rocks", "coral", "shipwreck"],
            "time_limit": 180,
            "score_target": 3500,
            "difficulty_multiplier": 1.6
        },
        
        # Level 4: Red Ink
        {
            "level_id": 4,
            "name": "Crimson Tide",
            "description": "The waters turn red with your powerful ink.",
            "ship_speed": 140,
            "ship_count": 3,
            "ship_health": 160,
            "turtle_count": 5,
            "turtle_speed": 60,
            "fish_spawn_rate": 0.35,
            "fish_value_multiplier": 1.8,
            "ink_color": "red",
            "ink_damage": 20,
            "ink_amount": 160,
            "background": "volcanic_water",
            "obstacles": ["seaweed", "rocks", "coral", "shipwreck", "volcanic_vents"],
            "time_limit": 210,
            "score_target": 5000,
            "difficulty_multiplier": 2.0
        },
        
        # Level 5: Rainbow Ink
        {
            "level_id": 5,
            "name": "Rainbow Depths",
            "description": "Your ink transforms into a magnificent rainbow as you face the ultimate challenge.",
            "ship_speed": 160,
            "ship_count": 4,
            "ship_health": 200,
            "turtle_count": 6,
            "turtle_speed": 70,
            "fish_spawn_rate": 0.4,
            "fish_value_multiplier": 2.0,
            "ink_color": "rainbow",
            "ink_damage": 25,
            "ink_amount": 200,
            "background": "mystical_water",
            "obstacles": ["seaweed", "rocks", "coral", "shipwreck", "volcanic_vents", "whirlpools"],
            "time_limit": 240,
            "score_target": 7500,
            "difficulty_multiplier": 2.5
        }
    ]
    
    @staticmethod
    def get_level_data(level_id: int) -> Dict[str, Any]:
        """Get the configuration data for a specific level.
        
        Args:
            level_id: The ID of the level to get data for (1-based)
            
        Returns:
            A dictionary containing the level configuration
            
        Raises:
            ValueError: If the level_id is invalid
        """
        if level_id < 1 or level_id > len(LevelData.LEVELS):
            raise ValueError(f"Invalid level ID: {level_id}. Must be between 1 and {len(LevelData.LEVELS)}")
            
        return LevelData.LEVELS[level_id - 1]
    
    @staticmethod
    def get_level_count() -> int:
        """Get the total number of levels.
        
        Returns:
            The total number of levels in the game
        """
        return len(LevelData.LEVELS)
    
    @staticmethod
    def get_ink_color_for_level(level_id: int) -> str:
        """Get the ink color for a specific level.
        
        Args:
            level_id: The ID of the level
            
        Returns:
            The ink color string for the level
        """
        level_data = LevelData.get_level_data(level_id)
        return level_data["ink_color"]