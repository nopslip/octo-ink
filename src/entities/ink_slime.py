"""Ink slime projectile entity."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.collision_component import CollisionComponent
from src.components.ink_slime_component import InkSlimeComponent
import pygame


class InkSlime(Entity):
    """Ink slime projectile fired by the octopus.
    
    These projectiles travel in straight lines and apply ink load
    to ships when they hit them.
    """
    
    def __init__(self, x: float, y: float, direction: pygame.math.Vector2, 
                 color: str = "dark_blue", speed: float = 500.0):
        """Initialize the InkSlime entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            direction: Direction vector (will be normalized)
            color: Ink color
            speed: Projectile speed in pixels per second
        """
        super().__init__(name=f"InkSlime_{color}")
        
        # Add tags
        self.add_tag("projectile")
        self.add_tag("player_projectile")
        self.add_tag("ink_slime")
        
        # Set up components
        self._setup_transform(x, y, direction)
        self._setup_render(color)
        self._setup_physics(direction, speed)
        self._setup_collision()
        self._setup_ink_slime(color)
        
    def _setup_transform(self, x: float, y: float, direction: pygame.math.Vector2) -> None:
        """Set up the transform component."""
        transform = TransformComponent()
        transform.set_position(x, y)
        # Set rotation based on direction
        if direction.length() > 0:
            transform.rotation = direction.angle_to(pygame.math.Vector2(1, 0))
        self.add_component(transform)
        
    def _setup_render(self, color: str) -> None:
        """Set up the render component."""
        render = RenderComponent(f"ink_{color}")
        
        # Color mapping for different ink types
        color_map = {
            "dark_blue": (0, 0, 139),
            "purple": (128, 0, 128),
            "green": (0, 128, 0),
            "red": (255, 0, 0),
            "rainbow": (255, 128, 0),  # Orange as placeholder for rainbow
            "black": (0, 0, 0)
        }
        
        # Use circle shape for ink projectile
        render.color = color_map.get(color, (0, 0, 139))
        render.shape = "circle"
        render.size = (12, 12)  # Small projectile
        self.add_component(render)
        
    def _setup_physics(self, direction: pygame.math.Vector2, speed: float) -> None:
        """Set up the physics component."""
        physics = PhysicsComponent()
        
        # Set velocity based on direction and speed
        if direction.length() > 0:
            velocity = direction.normalize() * speed
            physics.velocity = velocity
        
        physics.max_velocity = pygame.math.Vector2(speed, speed)
        physics.use_gravity = False  # Projectiles fly straight
        physics.friction = 0.0  # No friction for projectiles
        self.add_component(physics)
        
    def _setup_collision(self) -> None:
        """Set up the collision component."""
        collision = CollisionComponent(width=12, height=12)
        collision.collision_type = "projectile"
        self.add_component(collision)
        
    def _setup_ink_slime(self, color: str) -> None:
        """Set up the ink slime component."""
        # Different colors might have different ink damage
        ink_damage_map = {
            "dark_blue": 10,
            "purple": 12,
            "green": 15,
            "red": 20,
            "rainbow": 25,
            "black": 10
        }
        
        ink_damage = ink_damage_map.get(color, 10)
        ink_slime = InkSlimeComponent(ink_color=color, ink_damage=ink_damage)
        self.add_component(ink_slime)