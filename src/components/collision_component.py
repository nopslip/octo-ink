"""Collision Component for managing entity collision detection."""

import pygame
from typing import Optional, Callable
from src.components.component import Component


class CollisionComponent(Component):
    """Component that manages collision detection and response."""
    
    def __init__(self, width: float = 32, height: float = 32):
        """Initialize the CollisionComponent.
        
        Args:
            width: Width of the collision box
            height: Height of the collision box
        """
        super().__init__("collision")
        
        # Collision box dimensions
        self.width: float = width
        self.height: float = height
        
        # Collision properties
        self.collision_type: str = "default"
        self.is_trigger: bool = False  # If True, doesn't block movement
        self.collision_mask: int = 1  # Bit mask for collision filtering
        
        # Collision callbacks
        self.on_collision_enter: Optional[Callable] = None
        self.on_collision_stay: Optional[Callable] = None
        self.on_collision_exit: Optional[Callable] = None
        
        # Offset from entity position
        self.offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        
    def update(self, dt: float) -> None:
        """Update collision component.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Collision detection is typically handled by the physics engine
        pass
        
    def get_rect(self) -> pygame.Rect:
        """Get the collision rectangle in world space.
        
        Returns:
            The collision rectangle
        """
        if not self.entity:
            return pygame.Rect(0, 0, self.width, self.height)
            
        transform = self.entity.get_component("transform")
        if not transform:
            return pygame.Rect(0, 0, self.width, self.height)
            
        position = transform.get_world_position() + self.offset
        
        # Create rectangle centered on position
        rect = pygame.Rect(
            position.x - self.width / 2,
            position.y - self.height / 2,
            self.width,
            self.height
        )
        
        return rect
        
    def check_collision(self, other: 'CollisionComponent') -> bool:
        """Check if this collision component overlaps with another.
        
        Args:
            other: The other collision component to check
            
        Returns:
            True if collision detected, False otherwise
        """
        return self.get_rect().colliderect(other.get_rect())
        
    def set_size(self, width: float, height: float) -> None:
        """Set the size of the collision box.
        
        Args:
            width: New width
            height: New height
        """
        self.width = width
        self.height = height