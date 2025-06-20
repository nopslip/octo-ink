"""Weapon Component for managing shooting mechanics."""

import pygame
import math
from typing import List, Dict, Any
from src.components.component import Component


class WeaponComponent(Component):
    """Component that manages weapon and shooting mechanics.
    
    For the octopus, this implements a 3-arm firing system with manual rotation.
    The center arm fires a more powerful shot, while the two side arms fire
    slightly weaker shots.
    """
    
    def __init__(self, arm_count: int = 10, base_cooldown: float = 0.5):
        """Initialize the WeaponComponent.
        
        Args:
            arm_count: Number of arms (default 10 for octopus)
            base_cooldown: Base cooldown time between shots per arm
        """
        super().__init__("weapon")
        
        # Weapon properties
        self.projectile_speed: float = 500.0  # Pixels per second
        self.damage: int = 10  # Base damage value
        self.center_damage_multiplier: float = 1.5  # Center arm does 50% more damage
        self.side_damage_multiplier: float = 0.8  # Side arms do 20% less damage
        self.ink_color: str = "dark_blue"  # Default ink color
        
        # Arm system
        self.arm_count: int = arm_count
        self.active_arm_index: int = 0  # Center/main arm index
        self.base_cooldown: float = base_cooldown
        self.arm_length: float = 50.0  # Distance from center to arm tip
        
        # Rotation control
        self.rotation_cooldown: float = 0.0  # Cooldown for arm rotation
        self.rotation_cooldown_time: float = 0.1  # Seconds between allowed rotations
        
        # Initialize arms with positions and individual cooldowns
        self.arms: List[Dict[str, Any]] = []
        self._initialize_arms()
        
        # Continuous firing state
        self.is_firing: bool = False
        self.fire_timer: float = 0.0
        self.fire_interval: float = 0.1  # Time between shots when holding fire
        
    def _initialize_arms(self) -> None:
        """Initialize arm positions in a circular pattern."""
        for i in range(self.arm_count):
            # Distribute arms evenly around the octopus
            angle = (i / self.arm_count) * 2 * math.pi
            self.arms.append({
                "index": i,
                "angle": angle,
                "cooldown": 0.0,
                "position": (math.cos(angle), math.sin(angle))  # Unit vector
            })
            
    def update(self, dt: float) -> None:
        """Update weapon cooldowns and handle continuous firing.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Update individual arm cooldowns
        for arm in self.arms:
            if arm["cooldown"] > 0:
                arm["cooldown"] -= dt
        
        # Update rotation cooldown
        if self.rotation_cooldown > 0:
            self.rotation_cooldown -= dt
                
        # Handle continuous firing
        if self.is_firing:
            self.fire_timer -= dt
            if self.fire_timer <= 0:
                self.try_shoot()
                self.fire_timer = self.fire_interval
                
    def try_shoot(self) -> bool:
        """Attempt to shoot projectiles from the three active arms.
        
        Returns:
            True if at least one shot was fired, False otherwise
        """
        if not self.entity:
            return False
        
        # Get the three active arms (center and two adjacent)
        active_arms = self.get_active_arms()
        shot_fired = False
        
        # Try to fire from each active arm
        for i, arm in enumerate(active_arms):
            if arm["cooldown"] <= 0:
                # Determine if this is the center arm or a side arm
                is_center = i == 1  # Index 1 is the center arm in the active_arms list
                
                # Fire from this arm with appropriate damage multiplier
                if self._fire_from_arm(arm, is_center):
                    # Set cooldown for this arm
                    arm["cooldown"] = self.base_cooldown
                    shot_fired = True
        
        return shot_fired
        
    def _fire_from_arm(self, arm: Dict[str, Any], is_center: bool = False) -> bool:
        """Fire a projectile from a specific arm.
        
        Args:
            arm: The arm dictionary containing position and angle info
            is_center: Whether this is the center (more powerful) arm
            
        Returns:
            True if projectile was created successfully
        """
        # Get entity position from transform component
        transform = self.entity.get_component("transform")
        if not transform:
            return False
            
        # Calculate firing position based on arm angle and entity position
        entity_pos = transform.position
        firing_position = (
            entity_pos.x + arm["position"][0] * self.arm_length,
            entity_pos.y + arm["position"][1] * self.arm_length
        )
        
        # Calculate firing direction (outward from the arm)
        direction = pygame.math.Vector2(arm["position"][0], arm["position"][1])
        
        # Determine damage multiplier based on whether this is center or side arm
        damage_multiplier = self.center_damage_multiplier if is_center else self.side_damage_multiplier
        
        # Create ink slime projectile using entity factory
        from src.entities.entity_factory import EntityFactory
        entity_factory = EntityFactory()
        
        # Create the projectile
        projectile = entity_factory.create_ink_slime(
            firing_position[0],
            firing_position[1],
            direction,
            self.ink_color
        )
        
        # Apply damage multiplier to the ink slime component
        if projectile:
            ink_slime_comp = projectile.get_component("ink_slime")
            if ink_slime_comp:
                # Apply the damage multiplier to the base ink damage
                base_damage = ink_slime_comp.ink_damage
                ink_slime_comp.ink_damage = int(base_damage * damage_multiplier)
        
        return True
        
    def start_firing(self) -> None:
        """Start continuous firing mode."""
        self.is_firing = True
        self.fire_timer = 0.0  # Fire immediately
        
    def stop_firing(self) -> None:
        """Stop continuous firing mode."""
        self.is_firing = False
        
    def set_fire_rate(self, shots_per_second: float) -> None:
        """Set the fire rate of the weapon.
        
        Args:
            shots_per_second: Number of shots per second
        """
        self.fire_interval = 1.0 / max(0.1, shots_per_second)
        
    def set_ink_color(self, color: str) -> None:
        """Set the ink color for projectiles.
        
        Args:
            color: The ink color (e.g., "dark_blue", "purple", "green", "red", "rainbow")
        """
        self.ink_color = color
        
    def rotate_arms(self) -> bool:
        """Rotate the active arms to the next position.
        
        Returns:
            True if rotation was successful, False if on cooldown
        """
        # Check if rotation is on cooldown
        if self.rotation_cooldown > 0:
            return False
            
        # Rotate to next arm position
        self.active_arm_index = (self.active_arm_index + 1) % self.arm_count
        
        # Set rotation cooldown
        self.rotation_cooldown = self.rotation_cooldown_time
        
        return True
        
    def get_active_arms(self) -> List[Dict[str, Any]]:
        """Get the three currently active arms (center and two adjacent).
        
        Returns:
            List of three arm dictionaries in order [left, center, right]
        """
        # Calculate indices for the three active arms
        center_idx = self.active_arm_index
        left_idx = (center_idx - 1) % self.arm_count
        right_idx = (center_idx + 1) % self.arm_count
        
        # Return the three arms in order [left, center, right]
        return [self.arms[left_idx], self.arms[center_idx], self.arms[right_idx]]
        
    def get_arm_positions(self) -> List[pygame.math.Vector2]:
        """Get the world positions of all arms (useful for rendering).
        
        Returns:
            List of arm tip positions in world coordinates
        """
        if not self.entity:
            return []
            
        transform = self.entity.get_component("transform")
        if not transform:
            return []
            
        entity_pos = transform.position
        positions = []
        
        for arm in self.arms:
            world_pos = pygame.math.Vector2(
                entity_pos.x + arm["position"][0] * self.arm_length,
                entity_pos.y + arm["position"][1] * self.arm_length
            )
            positions.append(world_pos)
            
        return positions
        
    def is_arm_active(self, arm_index: int) -> bool:
        """Check if an arm is currently active.
        
        Args:
            arm_index: The index of the arm to check
            
        Returns:
            True if the arm is one of the three active arms
        """
        active_arms = self.get_active_arms()
        for arm in active_arms:
            if arm["index"] == arm_index:
                return True
        return False
        
    def get_arm_role(self, arm_index: int) -> str:
        """Get the role of an arm (center, side, or inactive).
        
        Args:
            arm_index: The index of the arm to check
            
        Returns:
            "center" if center arm, "side" if side arm, "inactive" otherwise
        """
        if arm_index == self.active_arm_index:
            return "center"
            
        active_arms = self.get_active_arms()
        for arm in active_arms:
            if arm["index"] == arm_index:
                return "side"
                
        return "inactive"