"""Captain entity implementation."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.collision_component import CollisionComponent
from src.components.health_component import HealthComponent
from src.components.ai_component import AIComponent
from src.components.animation_component import AnimationComponent
from src.components.captain_component import CaptainComponent


class Captain(Entity):
    """Captain entity that rides on ships and has dramatic death sequence."""
    
    def __init__(self, position: tuple):
        """Initialize a captain entity.
        
        Args:
            position: Initial position (x, y)
        """
        super().__init__(name="Captain")
        
        # Add tags
        self.add_tag("captain")
        self.add_tag("enemy")
        
        # Add components
        self._add_components(position)
        
    def _add_components(self, position: tuple) -> None:
        """Add all necessary components to the captain.
        
        Args:
            position: Initial position
        """
        # Transform component
        transform = TransformComponent()
        transform.set_position(position[0], position[1])
        self.add_component(transform)
        
        # Physics component
        physics = PhysicsComponent()
        physics.gravity_scale = 0.0  # No gravity when on ship
        self.add_component(physics)
        
        # Render component (placeholder until sprites are available)
        render = RenderComponent()
        render.shape = "circle"
        render.size = (20, 20)
        render.color = (255, 200, 0)  # Yellow/gold for captain
        self.add_component(render)
        
        # Collision component
        collision = CollisionComponent(
            width=20,
            height=30
        )
        self.add_component(collision)
        
        # Health component
        health = HealthComponent(1)  # Captains die in one hit when floating
        self.add_component(health)
        
        # AI component
        ai = AIComponent(
            ai_type="captain",
            explosion_delay=2.0
        )
        self.add_component(ai)
        
        # Animation component
        animation = AnimationComponent()
        # Add captain animations when sprites are available
        # animation.add_animation("idle", [...])
        # animation.add_animation("captain_panic", [...])
        # animation.add_animation("head_explosion", [...])
        animation.current_animation = "idle"
        self.add_component(animation)
        
        # Captain-specific component
        captain = CaptainComponent()
        self.add_component(captain)
        
    def update_position_on_ship(self, ship_entity) -> None:
        """Update captain position to stay on ship.
        
        Args:
            ship_entity: The ship this captain is attached to
        """
        captain_comp = self.get_component("captain")
        transform = self.get_component("transform")
        
        if captain_comp and transform and captain_comp.state == "on_ship":
            # Get ship's captain attachment position
            if hasattr(ship_entity, 'get_captain_position'):
                new_position = ship_entity.get_captain_position()
                transform.set_position(new_position[0], new_position[1])
                
    def start_panic(self) -> None:
        """Start the panic sequence when ship sinks."""
        captain_comp = self.get_component("captain")
        physics = self.get_component("physics")
        
        if captain_comp:
            captain_comp.set_state("floating")
            
        if physics:
            # Enable gravity when floating
            physics.gravity_scale = 0.5
            
    def get_point_value(self) -> int:
        """Get the point value for destroying this captain.
        
        Returns:
            Points awarded for captain head explosion
        """
        return 500  # Bonus points for captain