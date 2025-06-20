"""Fish entity implementation."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.collision_component import CollisionComponent
from src.components.ai_component import AIComponent
from src.components.animation_component import AnimationComponent


class Fish(Entity):
    """Fish entity that serves as bonus targets."""
    
    # Fish type configurations
    FISH_TYPES = {
        "normal": {
            "speed": 80,
            "points": 50,
            "size": (30, 20),
            "wander_interval": 2.0,
            "color": "silver"
        },
        "fast": {
            "speed": 150,
            "points": 100,
            "size": (25, 15),
            "wander_interval": 1.0,
            "color": "gold"
        },
        "school": {
            "speed": 60,
            "points": 25,
            "size": (20, 15),
            "wander_interval": 3.0,
            "color": "blue"
        }
    }
    
    def __init__(self, position: tuple, fish_type: str = "normal"):
        """Initialize a fish entity.
        
        Args:
            position: Initial position (x, y)
            fish_type: Type of fish ("normal", "fast", "school")
        """
        super().__init__(name=f"Fish_{fish_type}")
        
        self.fish_type = fish_type
        self.config = self.FISH_TYPES.get(fish_type, self.FISH_TYPES["normal"])
        
        # Add tags
        self.add_tag("fish")
        self.add_tag("bonus")
        self.add_tag(f"fish_{fish_type}")
        
        # Add components
        self._add_components(position)
        
    def _add_components(self, position: tuple) -> None:
        """Add all necessary components to the fish.
        
        Args:
            position: Initial position
        """
        # Transform component
        transform = TransformComponent()
        transform.set_position(position[0], position[1])
        self.add_component(transform)
        
        # Physics component
        physics = PhysicsComponent()
        physics.drag = 0.98  # Low drag for smooth swimming
        self.add_component(physics)
        
        # Render component (placeholder until sprites are available)
        render = RenderComponent()
        render.shape = "ellipse"
        render.size = self.config["size"]
        
        # Different colors for different fish types
        if self.fish_type == "normal":
            render.color = (192, 192, 192)  # Silver
        elif self.fish_type == "fast":
            render.color = (255, 215, 0)  # Gold
        else:  # school
            render.color = (0, 191, 255)  # Deep sky blue
            
        self.add_component(render)
        
        # Collision component
        collision = CollisionComponent(
            width=self.config["size"][0],
            height=self.config["size"][1]
        )
        self.add_component(collision)
        
        # AI component for wandering movement
        ai = AIComponent(
            ai_type="fish",
            wander_speed=self.config["speed"],
            wander_change_interval=self.config["wander_interval"]
        )
        self.add_component(ai)
        
        # Animation component
        animation = AnimationComponent()
        # Add fish animations when sprites are available
        # animation.add_animation("swim", [...])
        # animation.add_animation("hit", [...])
        animation.current_animation = "swim"
        self.add_component(animation)
        
    def on_hit(self) -> None:
        """Handle when the fish is hit by ink."""
        animation = self.get_component("animation")
        
        if animation:
            # Play hit animation
            animation.play("hit", loop=False)
            
        # Play bonus sound (when audio manager is available)
        # audio_manager.play_sound("bonus_collected")
        
        # Award points (when score manager is available)
        # score_manager.add_score(self.config["points"])
        
        # Destroy the fish
        self.destroy()
        
    def get_point_value(self) -> int:
        """Get the point value for hitting this fish.
        
        Returns:
            Points awarded for hitting this fish
        """
        return self.config["points"]
        
    def is_school_fish(self) -> bool:
        """Check if this is a school type fish.
        
        Returns:
            True if this is a school fish
        """
        return self.fish_type == "school"
        
    @staticmethod
    def create_school(center_position: tuple, count: int = 5) -> list:
        """Create a school of fish around a center position.
        
        Args:
            center_position: Center position for the school
            count: Number of fish in the school
            
        Returns:
            List of fish entities
        """
        import math
        school = []
        
        for i in range(count):
            # Arrange fish in a circle around center
            angle = (2 * math.pi * i) / count
            offset_x = math.cos(angle) * 40  # 40 pixel radius
            offset_y = math.sin(angle) * 40
            
            position = (
                center_position[0] + offset_x,
                center_position[1] + offset_y
            )
            
            fish = Fish(position, "school")
            school.append(fish)
            
        return school