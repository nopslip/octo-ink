"""Level Component for tracking level-specific entity properties."""

from typing import Dict, Any
from src.components.component import Component


class LevelComponent(Component):
    """Component that tracks level-specific entity properties.
    
    This component is attached to entities that need to have properties
    that change based on the current level, such as ink color, enemy
    behavior parameters, and scoring multipliers.
    """
    
    def __init__(self, level_id: int = 1):
        """Initialize the LevelComponent.
        
        Args:
            level_id: The current level ID (1-based)
        """
        super().__init__("level")
        
        # Level properties
        self.level_id: int = level_id
        self.ink_color: str = self._get_ink_color_for_level(level_id)
        self.scoring_multiplier: float = self._get_scoring_multiplier_for_level(level_id)
        
        # Level-specific behavior parameters
        self.behavior_params: Dict[str, Any] = self._get_behavior_params_for_level(level_id)
        
    def update(self, dt: float) -> None:
        """Update the level component.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # This component doesn't need to do anything during update
        pass
        
    def set_level(self, level_id: int) -> None:
        """Set the current level and update all level-specific properties.
        
        Args:
            level_id: The new level ID (1-based)
        """
        self.level_id = level_id
        self.ink_color = self._get_ink_color_for_level(level_id)
        self.scoring_multiplier = self._get_scoring_multiplier_for_level(level_id)
        self.behavior_params = self._get_behavior_params_for_level(level_id)
        
        # Update related components if needed
        self._update_related_components()
        
    def _update_related_components(self) -> None:
        """Update related components with new level-specific properties."""
        if not self.entity:
            return
            
        # Update ink slime component with new color
        ink_slime = self.entity.get_component("ink_slime")
        if ink_slime:
            ink_slime.set_ink_color(self.ink_color)
            
        # Update weapon component with level-specific parameters
        weapon = self.entity.get_component("weapon")
        if weapon and "weapon" in self.behavior_params:
            weapon_params = self.behavior_params["weapon"]
            if "cooldown" in weapon_params:
                weapon.base_cooldown = weapon_params["cooldown"]
            if "damage" in weapon_params:
                weapon.damage = weapon_params["damage"]
                
        # Update AI component with level-specific behavior
        ai = self.entity.get_component("ai")
        if ai and "ai" in self.behavior_params:
            ai_params = self.behavior_params["ai"]
            if "aggression" in ai_params:
                ai.aggression = ai_params["aggression"]
            if "awareness" in ai_params:
                ai.awareness = ai_params["awareness"]
                
    def _get_ink_color_for_level(self, level_id: int) -> str:
        """Get the ink color for a specific level.
        
        Args:
            level_id: The level ID
            
        Returns:
            The ink color string for the level
        """
        # Map level IDs to ink colors
        ink_colors = {
            1: "dark_blue",
            2: "purple",
            3: "green",
            4: "red",
            5: "rainbow"
        }
        
        return ink_colors.get(level_id, "dark_blue")
        
    def _get_scoring_multiplier_for_level(self, level_id: int) -> float:
        """Get the scoring multiplier for a specific level.
        
        Args:
            level_id: The level ID
            
        Returns:
            The scoring multiplier for the level
        """
        # Higher levels have higher scoring multipliers
        base_multiplier = 1.0
        level_bonus = (level_id - 1) * 0.2
        
        return base_multiplier + level_bonus
        
    def _get_behavior_params_for_level(self, level_id: int) -> Dict[str, Any]:
        """Get behavior parameters for a specific level.
        
        Args:
            level_id: The level ID
            
        Returns:
            Dictionary of behavior parameters for the level
        """
        # Define level-specific behavior parameters
        behavior_params = {
            # Level 1: Dark Blue Ink
            1: {
                "weapon": {
                    "cooldown": 0.5,
                    "damage": 10
                },
                "ai": {
                    "aggression": 0.3,
                    "awareness": 0.5
                },
                "movement": {
                    "speed_multiplier": 1.0
                }
            },
            # Level 2: Purple Ink
            2: {
                "weapon": {
                    "cooldown": 0.45,
                    "damage": 12
                },
                "ai": {
                    "aggression": 0.4,
                    "awareness": 0.6
                },
                "movement": {
                    "speed_multiplier": 1.1
                }
            },
            # Level 3: Green Ink
            3: {
                "weapon": {
                    "cooldown": 0.4,
                    "damage": 15
                },
                "ai": {
                    "aggression": 0.5,
                    "awareness": 0.7
                },
                "movement": {
                    "speed_multiplier": 1.2
                }
            },
            # Level 4: Red Ink
            4: {
                "weapon": {
                    "cooldown": 0.35,
                    "damage": 20
                },
                "ai": {
                    "aggression": 0.7,
                    "awareness": 0.8
                },
                "movement": {
                    "speed_multiplier": 1.3
                }
            },
            # Level 5: Rainbow Ink
            5: {
                "weapon": {
                    "cooldown": 0.3,
                    "damage": 25
                },
                "ai": {
                    "aggression": 0.9,
                    "awareness": 0.9
                },
                "movement": {
                    "speed_multiplier": 1.5
                }
            }
        }
        
        return behavior_params.get(level_id, behavior_params[1])
        
    def get_ink_color(self) -> str:
        """Get the current ink color.
        
        Returns:
            The current ink color string
        """
        return self.ink_color
        
    def get_scoring_multiplier(self) -> float:
        """Get the current scoring multiplier.
        
        Returns:
            The current scoring multiplier
        """
        return self.scoring_multiplier
        
    def get_behavior_param(self, category: str, param_name: str, default_value: Any = None) -> Any:
        """Get a specific behavior parameter.
        
        Args:
            category: The parameter category (e.g., "weapon", "ai")
            param_name: The parameter name
            default_value: Default value to return if parameter not found
            
        Returns:
            The parameter value or default_value if not found
        """
        if category in self.behavior_params and param_name in self.behavior_params[category]:
            return self.behavior_params[category][param_name]
        return default_value