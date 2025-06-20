"""Transform Component for managing entity position, rotation, and scale."""

import pygame
from typing import Optional
from src.components.component import Component


class TransformComponent(Component):
    """Component that manages an entity's position, rotation, and scale in 2D space.
    
    The TransformComponent is one of the most fundamental components, as it defines
    where an entity exists in the game world and how it's oriented.
    """
    
    def __init__(self):
        """Initialize the TransformComponent."""
        super().__init__("transform")
        
        # Position in world coordinates
        self.position: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        
        # Previous position (useful for interpolation and collision resolution)
        self.previous_position: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        
        # Rotation in degrees (0 = facing right, positive = clockwise)
        self.rotation: float = 0.0
        
        # Scale factors for width and height
        self.scale: pygame.math.Vector2 = pygame.math.Vector2(1.0, 1.0)
        
        # Local origin offset (pivot point for rotation and scaling)
        self.origin: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        
        # Parent transform (for hierarchical transformations)
        self.parent: Optional['TransformComponent'] = None
        
    def update(self, dt: float) -> None:
        """Update the transform component.
        
        Currently just stores the previous position for interpolation purposes.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        self.previous_position = self.position.copy()
        
    def set_position(self, x: float, y: float) -> None:
        """Set the position of the transform.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position.x = x
        self.position.y = y
        
    def translate(self, dx: float, dy: float) -> None:
        """Move the transform by a relative amount.
        
        Args:
            dx: Change in X coordinate
            dy: Change in Y coordinate
        """
        self.position.x += dx
        self.position.y += dy
        
    def rotate(self, angle: float) -> None:
        """Rotate the transform by a relative amount.
        
        Args:
            angle: Angle to rotate in degrees
        """
        self.rotation += angle
        # Keep rotation in 0-360 range
        self.rotation = self.rotation % 360
        
    def set_rotation(self, angle: float) -> None:
        """Set the absolute rotation of the transform.
        
        Args:
            angle: Angle in degrees
        """
        self.rotation = angle % 360
        
    def set_scale(self, scale_x: float, scale_y: Optional[float] = None) -> None:
        """Set the scale of the transform.
        
        Args:
            scale_x: Scale factor for X axis
            scale_y: Scale factor for Y axis (if None, uses scale_x for uniform scaling)
        """
        self.scale.x = scale_x
        self.scale.y = scale_y if scale_y is not None else scale_x
        
    def get_world_position(self) -> pygame.math.Vector2:
        """Get the world position, taking parent transforms into account.
        
        Returns:
            The world position as a Vector2
        """
        if self.parent:
            parent_pos = self.parent.get_world_position()
            # Apply parent's rotation to this position
            offset = self.position.rotate(self.parent.get_world_rotation())
            # Apply parent's scale
            offset.x *= self.parent.scale.x
            offset.y *= self.parent.scale.y
            return parent_pos + offset
        return self.position.copy()
        
    def get_world_rotation(self) -> float:
        """Get the world rotation, taking parent transforms into account.
        
        Returns:
            The world rotation in degrees
        """
        if self.parent:
            return (self.rotation + self.parent.get_world_rotation()) % 360
        return self.rotation
        
    def get_world_scale(self) -> pygame.math.Vector2:
        """Get the world scale, taking parent transforms into account.
        
        Returns:
            The world scale as a Vector2
        """
        if self.parent:
            parent_scale = self.parent.get_world_scale()
            return pygame.math.Vector2(
                self.scale.x * parent_scale.x,
                self.scale.y * parent_scale.y
            )
        return self.scale.copy()
        
    def look_at(self, target_x: float, target_y: float) -> None:
        """Rotate the transform to look at a target position.
        
        Args:
            target_x: X coordinate of the target
            target_y: Y coordinate of the target
        """
        direction = pygame.math.Vector2(target_x - self.position.x, 
                                       target_y - self.position.y)
        if direction.length() > 0:
            self.rotation = direction.angle_to(pygame.math.Vector2(1, 0))
            
    def get_forward_vector(self) -> pygame.math.Vector2:
        """Get the forward direction vector based on current rotation.
        
        Returns:
            A normalized vector pointing in the forward direction
        """
        # In our coordinate system, 0 degrees points right
        rad = pygame.math.Vector2(1, 0).rotate(self.rotation)
        return rad.normalize()
        
    def get_right_vector(self) -> pygame.math.Vector2:
        """Get the right direction vector based on current rotation.
        
        Returns:
            A normalized vector pointing to the right
        """
        # Right vector is forward rotated 90 degrees clockwise
        return self.get_forward_vector().rotate(90)
        
    def distance_to(self, other_transform: 'TransformComponent') -> float:
        """Calculate the distance to another transform.
        
        Args:
            other_transform: The other transform component
            
        Returns:
            The distance between the two transforms
        """
        return self.position.distance_to(other_transform.position)
        
    def lerp_position(self, target_position: pygame.math.Vector2, t: float) -> None:
        """Linearly interpolate position towards a target.
        
        Args:
            target_position: The target position
            t: Interpolation factor (0-1)
        """
        self.position = self.position.lerp(target_position, t)
        
    def __repr__(self) -> str:
        """String representation of the transform.
        
        Returns:
            A string describing the transform's state
        """
        return (f"TransformComponent(pos={self.position}, "
                f"rot={self.rotation:.1f}, scale={self.scale})")