"""Turtle entity implementation."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.collision_component import CollisionComponent
from src.components.ai_component import AIComponent
from src.components.animation_component import AnimationComponent
from src.components.shield_component import ShieldComponent


class Turtle(Entity):
    """Turtle entity that blocks ink shots with its shield."""
    
    def __init__(self, position: tuple, shield_health: int = 3):
        """Initialize a turtle entity.
        
        Args:
            position: Initial position (x, y)
            shield_health: Number of hits the shield can take
        """
        super().__init__(name="Turtle")
        
        # Add tags
        self.add_tag("turtle")
        self.add_tag("obstacle")
        self.add_tag("enemy")
        
        # Add components
        self._add_components(position, shield_health)
        
    def _add_components(self, position: tuple, shield_health: int) -> None:
        """Add all necessary components to the turtle.
        
        Args:
            position: Initial position
            shield_health: Shield durability
        """
        # Transform component
        transform = TransformComponent()
        transform.set_position(position[0], position[1])
        self.add_component(transform)
        
        # Physics component
        physics = PhysicsComponent()
        physics.mass = 2.0  # Heavier than normal entities
        physics.drag = 0.95  # High drag for slow movement
        self.add_component(physics)
        
        # Render component (placeholder until sprites are available)
        render = RenderComponent()
        render.shape = "ellipse"
        render.size = (50, 40)
        render.color = (0, 128, 0)  # Green for turtle
        self.add_component(render)
        
        # Collision component
        collision = CollisionComponent(
            width=50,
            height=40
        )
        self.add_component(collision)
        
        # AI component for defensive movement
        ai = AIComponent(
            ai_type="turtle",
            defensive_radius=100.0
        )
        self.add_component(ai)
        
        # Animation component
        animation = AnimationComponent()
        # Add turtle animations when sprites are available
        # animation.add_animation("idle", [...])
        # animation.add_animation("shield_active", [...])
        # animation.add_animation("shield_hit", [...])
        # animation.add_animation("shield_broken", [...])
        animation.current_animation = "idle"
        self.add_component(animation)
        
        # Shield component
        shield = ShieldComponent(
            max_health=shield_health,
            block_radius=40.0
        )
        self.add_component(shield)
        
    def on_projectile_blocked(self) -> None:
        """Handle when the turtle blocks a projectile."""
        shield = self.get_component("shield")
        animation = self.get_component("animation")
        
        if shield and shield.take_hit():
            # Shield blocked the hit
            if animation:
                # Play shield hit animation
                if shield.is_active():
                    animation.play("shield_hit", loop=False)
                    # TODO: Add callback to return to shield_active animation
                else:
                    # Shield broken
                    animation.play("shield_broken", loop=True)
                    
            # Play shield hit sound (when audio manager is available)
            # audio_manager.play_sound("shield_hit")
            
    def can_block_projectile(self, projectile_position: tuple) -> bool:
        """Check if turtle can block a projectile at given position.
        
        Args:
            projectile_position: Position of the projectile
            
        Returns:
            True if turtle's shield can block, False otherwise
        """
        shield = self.get_component("shield")
        if shield:
            return shield.can_block_projectile(projectile_position)
        return False
        
    def get_shield_status(self) -> dict:
        """Get the current shield status.
        
        Returns:
            Dictionary with shield information
        """
        shield = self.get_component("shield")
        if shield:
            return {
                "active": shield.is_active(),
                "health": shield.current_health,
                "max_health": shield.max_health,
                "percentage": shield.get_health_percentage()
            }
        return {
            "active": False,
            "health": 0,
            "max_health": 0,
            "percentage": 0.0
        }