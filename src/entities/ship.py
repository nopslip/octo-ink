"""Ship entity implementation."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.collision_component import CollisionComponent
from src.components.health_component import HealthComponent
from src.components.ai_component import AIComponent
from src.components.animation_component import AnimationComponent
from src.components.ship_ink_load_component import ShipInkLoadComponent


class Ship(Entity):
    """Ship entity that can be sunk by ink slime."""
    
    # Ship size configurations
    SHIP_SIZES = {
        "small": {
            "health": 50,
            "ink_capacity": 30,
            "speed": 120,
            "width": 60,
            "height": 40,
            "points": 100
        },
        "medium": {
            "health": 100,
            "ink_capacity": 60,
            "speed": 100,
            "width": 80,
            "height": 50,
            "points": 200
        },
        "large": {
            "health": 150,
            "ink_capacity": 100,
            "speed": 80,
            "width": 100,
            "height": 60,
            "points": 300
        }
    }
    
    def __init__(self, position: tuple, size: str = "medium", direction: int = 1):
        """Initialize a ship entity.
        
        Args:
            position: Initial position (x, y)
            size: Ship size ("small", "medium", "large")
            direction: Initial movement direction (1 for right, -1 for left)
        """
        super().__init__(name=f"Ship_{size}")
        
        self.size = size
        self.config = self.SHIP_SIZES.get(size, self.SHIP_SIZES["medium"])
        self.captain_attachment_point = None  # Will be set after components are added
        
        # Add tags
        self.add_tag("ship")
        self.add_tag("enemy")
        self.add_tag(f"ship_{size}")
        
        # Add components
        self._add_components(position, direction)
        
    def _add_components(self, position: tuple, direction: int) -> None:
        """Add all necessary components to the ship.
        
        Args:
            position: Initial position
            direction: Movement direction
        """
        # Transform component
        transform = TransformComponent()
        transform.set_position(position[0], position[1])
        self.add_component(transform)
        
        # Physics component
        physics = PhysicsComponent()
        physics.velocity = (self.config["speed"] * direction, 0)
        self.add_component(physics)
        
        # Render component (placeholder until sprites are available)
        render = RenderComponent()
        render.shape = "rect"
        render.size = (self.config["width"], self.config["height"])
        # Different colors for different ship sizes
        if self.size == "small":
            render.color = (139, 69, 19)  # Brown
        elif self.size == "medium":
            render.color = (101, 67, 33)  # Dark brown
        else:  # large
            render.color = (61, 43, 31)  # Very dark brown
        self.add_component(render)
        
        # Collision component
        collision = CollisionComponent(
            width=self.config["width"],
            height=self.config["height"]
        )
        self.add_component(collision)
        
        # Health component
        health = HealthComponent(self.config["health"])
        self.add_component(health)
        
        # AI component for movement
        ai = AIComponent(
            ai_type="ship",
            ship_speed=self.config["speed"],
            direction=direction
        )
        self.add_component(ai)
        
        # Animation component
        animation = AnimationComponent()
        # Add ship animations when sprites are available
        # animation.add_animation("idle", [...])
        # animation.add_animation("sinking", [...])
        self.add_component(animation)
        
        # Ship ink load component
        ink_load = ShipInkLoadComponent(
            max_ink_load=self.config["ink_capacity"]
        )
        self.add_component(ink_load)
        
        # Set captain attachment point (on top of ship)
        self.captain_attachment_point = (0, -self.config["height"] / 2 - 10)
        
    def attach_captain(self, captain_entity) -> None:
        """Attach a captain to this ship.
        
        Args:
            captain_entity: The captain entity to attach
        """
        captain_comp = captain_entity.get_component("captain")
        if captain_comp:
            captain_comp.attach_to_ship(self)
            
    def get_captain_position(self) -> tuple:
        """Get the world position where a captain should be attached.
        
        Returns:
            World position for captain attachment
        """
        transform = self.get_component("transform")
        if transform and self.captain_attachment_point:
            return (
                transform.position.x + self.captain_attachment_point[0],
                transform.position.y + self.captain_attachment_point[1]
            )
        return (transform.position.x, transform.position.y) if transform else (0, 0)
        
    def on_ink_hit(self, ink_color: str, ink_amount: float) -> None:
        """Handle being hit by ink slime.
        
        Args:
            ink_color: Color of the ink that hit
            ink_amount: Amount of ink damage
        """
        ink_load = self.get_component("ship_ink_load")
        if ink_load:
            ink_load.add_ink(ink_amount)
            
            # Check if ship should sink
            if ink_load.is_sinking():
                self._start_sinking()
                
    def _start_sinking(self) -> None:
        """Start the sinking sequence."""
        # Change animation
        animation = self.get_component("animation")
        if animation:
            animation.play("sinking", loop=True)
            
        # Notify any attached captain
        # This would be handled by the game engine checking for captains on sinking ships
        
        # Award points (when score manager is available)
        # score_manager.add_score(self.config["points"])
        
    def get_point_value(self) -> int:
        """Get the point value for destroying this ship.
        
        Returns:
            Points awarded for sinking this ship
        """
        return self.config["points"]