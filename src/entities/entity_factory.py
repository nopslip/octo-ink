"""Entity Factory for creating game entities with predefined component configurations."""

from typing import Optional, Dict, Any
from src.entities.entity import Entity
from src.entities.entity_manager import EntityManager
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.health_component import HealthComponent
from src.components.input_component import InputComponent
from src.components.ai_component import AIComponent
from src.components.weapon_component import WeaponComponent
from src.components.collision_component import CollisionComponent
from src.components.animation_component import AnimationComponent
from src.components.ship_ink_load_component import ShipInkLoadComponent
import pygame


class EntityFactory:
    """Singleton factory for creating game entities.
    
    The EntityFactory provides methods to create different types of game entities
    with their appropriate components pre-configured. This ensures consistent
    entity creation throughout the game.
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance of EntityFactory exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(EntityFactory, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the EntityFactory."""
        if self._initialized:
            return
            
        self.entity_manager: Optional[EntityManager] = None
        self._initialized = True
        
    def set_entity_manager(self, entity_manager: EntityManager) -> None:
        """Set the entity manager that will track created entities.
        
        Args:
            entity_manager: The EntityManager instance
        """
        self.entity_manager = entity_manager
        
    def create_player(self, x: float, y: float) -> Entity:
        """Create a player (octopus) entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            
        Returns:
            The created player entity
        """
        from src.entities.player import Player
        
        # Create the player entity
        player = Player(x, y)
        
        if self.entity_manager:
            self.entity_manager.add_entity(player)
            
        return player
        
    def create_ship(self, x: float, y: float, ship_type: str = "small", direction: int = 1,
                   speed: float = None, health: float = None) -> Entity:
        """Create a ship entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            ship_type: Type of ship ("small", "medium", "large")
            direction: Direction of movement (1 for right, -1 for left)
            speed: Movement speed of the ship (optional)
            health: Health points of the ship (optional)
            
        Returns:
            The created ship entity
        """
        from src.entities.ship import Ship
        
        # Create a Ship instance instead of a generic Entity
        ship = Ship((x, y), ship_type, direction)
        
        if self.entity_manager:
            self.entity_manager.add_entity(ship)
            
        return ship
        
    def create_captain(self, x: float, y: float) -> Entity:
        """Create a captain entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            
        Returns:
            The created captain entity
        """
        captain = Entity(name="Captain")
        captain.add_tag("enemy")
        captain.add_tag("captain")
        
        # Add transform component
        transform = TransformComponent()
        transform.position = pygame.math.Vector2(x, y)
        captain.add_component(transform)
        
        # Add render component
        render = RenderComponent("captain")
        captain.add_component(render)
        
        # Add physics component
        physics = PhysicsComponent()
        physics.max_velocity = pygame.math.Vector2(100, 100)
        captain.add_component(physics)
        
        # Add AI component
        ai = AIComponent("aggressive")
        captain.add_component(ai)
        
        # Add health component
        health = HealthComponent(max_health=50)
        captain.add_component(health)
        
        # Add weapon component for shooting at player
        weapon = WeaponComponent()
        weapon.fire_rate = 1.0  # 1 shot per second
        weapon.projectile_speed = 300
        captain.add_component(weapon)
        
        # Add collision component
        collision = CollisionComponent(width=32, height=48)
        collision.collision_type = "enemy"
        captain.add_component(collision)
        
        # Add animation component
        animation = AnimationComponent()
        captain.add_component(animation)
        
        if self.entity_manager:
            self.entity_manager.add_entity(captain)
            
        return captain
        
    def create_turtle(self, x: float, y: float, movement_pattern: str = "stationary",
                     speed: float = None) -> Entity:
        """Create a turtle entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            movement_pattern: Movement pattern ("stationary", "linear", "circular")
            speed: Movement speed of the turtle (optional)
            
        Returns:
            The created turtle entity
        """
        from src.entities.turtle import Turtle
        
        # Create a Turtle instance instead of a generic Entity
        turtle = Turtle((x, y))
        
        # Set movement pattern if provided
        ai = turtle.get_component("ai")
        if ai and movement_pattern:
            # Use set_state instead of set_behavior (which doesn't exist)
            ai.set_state(movement_pattern)
            
        # Set speed if provided
        physics = turtle.get_component("physics")
        if physics and speed:
            physics.max_velocity = pygame.math.Vector2(speed, speed)
        
        if self.entity_manager:
            self.entity_manager.add_entity(turtle)
            
        return turtle
        
    def create_fish(self, x: float, y: float, fish_type: str = "normal", value_multiplier: float = 1.0) -> Entity:
        """Create a fish entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            fish_type: Type of fish ("normal", "fast", "school")
            value_multiplier: Multiplier for the fish's point value
            
        Returns:
            The created fish entity
        """
        from src.entities.fish import Fish
        
        # Create a Fish instance instead of a generic Entity
        fish = Fish((x, y), fish_type)
        
        # Apply value multiplier if needed
        if value_multiplier != 1.0:
            # This would need to be implemented in the Fish class
            # For now, we'll just note that the multiplier was provided
            pass
        
        if self.entity_manager:
            self.entity_manager.add_entity(fish)
            
        return fish
        
    def create_ink_slime(self, x: float, y: float, direction: pygame.math.Vector2,
                        color: str = "dark_blue") -> Entity:
        """Create an ink slime projectile entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            direction: Direction vector for the projectile
            color: Color of the ink ("dark_blue", "purple", "green", etc.)
            
        Returns:
            The created ink slime entity
        """
        from src.entities.ink_slime import InkSlime
        
        # Create the ink slime entity
        ink = InkSlime(x, y, direction, color)
        
        if self.entity_manager:
            self.entity_manager.add_entity(ink)
            
        return ink
        
    def create_enemy_projectile(self, x: float, y: float, 
                               direction: pygame.math.Vector2) -> Entity:
        """Create an enemy projectile entity.
        
        Args:
            x: Initial x position
            y: Initial y position
            direction: Direction vector for the projectile
            
        Returns:
            The created projectile entity
        """
        projectile = Entity(name="EnemyProjectile")
        projectile.add_tag("projectile")
        projectile.add_tag("enemy_projectile")
        
        # Add transform component
        transform = TransformComponent()
        transform.position = pygame.math.Vector2(x, y)
        transform.rotation = direction.angle_to(pygame.math.Vector2(1, 0))
        projectile.add_component(transform)
        
        # Add render component
        render = RenderComponent("cannonball")
        projectile.add_component(render)
        
        # Add physics component
        physics = PhysicsComponent()
        physics.velocity = direction.normalize() * 300  # projectile speed
        physics.max_velocity = pygame.math.Vector2(300, 300)
        physics.use_gravity = False
        projectile.add_component(physics)
        
        # Add collision component
        collision = CollisionComponent(width=12, height=12)
        collision.collision_type = "projectile"
        projectile.add_component(collision)
        
        if self.entity_manager:
            self.entity_manager.add_entity(projectile)
            
        return projectile