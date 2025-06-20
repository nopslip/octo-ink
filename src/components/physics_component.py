"""Physics Component for managing entity physics properties."""

import pygame
from src.components.component import Component


class PhysicsComponent(Component):
    """Component that manages physics properties like velocity and acceleration."""
    
    def __init__(self):
        """Initialize the PhysicsComponent."""
        super().__init__("physics")
        
        # Movement properties
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.acceleration: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.max_velocity: pygame.math.Vector2 = pygame.math.Vector2(500, 500)
        
        # Physics properties
        self.mass: float = 1.0
        self.friction: float = 0.1
        self.use_gravity: bool = True
        self.gravity_scale: float = 1.0
        
    def update(self, dt: float) -> None:
        """Update physics calculations.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Apply acceleration to velocity
        self.velocity += self.acceleration * dt
        
        # Clamp velocity to max values
        if abs(self.velocity.x) > self.max_velocity.x:
            self.velocity.x = self.max_velocity.x if self.velocity.x > 0 else -self.max_velocity.x
        if abs(self.velocity.y) > self.max_velocity.y:
            self.velocity.y = self.max_velocity.y if self.velocity.y > 0 else -self.max_velocity.y
            
        # Apply friction
        if self.velocity.length() > 0:
            friction_force = self.velocity.normalize() * self.friction * dt
            if friction_force.length() > self.velocity.length():
                self.velocity = pygame.math.Vector2(0, 0)
            else:
                self.velocity -= friction_force
                
        # Update position based on velocity
        if self.entity:
            transform = self.entity.get_component("transform")
            if transform:
                transform.translate(self.velocity.x * dt, self.velocity.y * dt)