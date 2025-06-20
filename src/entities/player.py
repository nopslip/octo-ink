"""Player entity class for the Octopus character."""

from src.entities.entity import Entity
from src.components.transform_component import TransformComponent
from src.components.render_component import RenderComponent
from src.components.physics_component import PhysicsComponent
from src.components.input_component import InputComponent
from src.components.weapon_component import WeaponComponent
from src.components.collision_component import CollisionComponent
from src.components.health_component import HealthComponent
import pygame


class OctopusRenderComponent(RenderComponent):
    """Custom render component for the octopus that shows its arms."""
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the octopus with its arms."""
        if not self.visible or not self.entity:
            return
            
        # Get transform component for position
        transform = self.entity.get_component("transform")
        if not transform:
            return
            
        position = transform.get_world_position()
        
        # Get weapon component to draw arms
        weapon = self.entity.get_component("weapon")
        
        # Draw arms first (behind body)
        if weapon:
            arm_positions = weapon.get_arm_positions()
            for i, arm_pos in enumerate(arm_positions):
                arm = weapon.arms[i]
                arm_role = weapon.get_arm_role(i)
                
                # Set arm line color and thickness based on role
                if arm_role == "center":
                    # Center arm (more powerful) - thicker and brighter
                    line_color = (180, 0, 180)  # Bright purple
                    line_thickness = 5
                elif arm_role == "side":
                    # Side arm - medium thickness
                    line_color = (140, 0, 140)  # Medium purple
                    line_thickness = 3
                else:
                    # Inactive arm - thin and faded
                    line_color = (80, 0, 80)  # Dark purple
                    line_thickness = 1
                
                # Draw arm line from body center to arm tip
                pygame.draw.line(surface, line_color,
                               (int(position.x), int(position.y)),
                               (int(arm_pos.x), int(arm_pos.y)), line_thickness)
                
                # Draw arm tip circle
                # Color arm tips based on role and cooldown
                if arm["cooldown"] > 0:
                    # Red when on cooldown (darker for inactive arms)
                    if arm_role == "inactive":
                        tip_color = (100, 25, 25)  # Dark red
                        tip_size = 3
                    else:
                        tip_color = (200, 50, 50)  # Bright red
                        tip_size = 6 if arm_role == "center" else 5
                else:
                    # Green when ready to fire (darker for inactive arms)
                    if arm_role == "inactive":
                        tip_color = (25, 100, 25)  # Dark green
                        tip_size = 3
                    else:
                        tip_color = (50, 200, 50)  # Bright green
                        tip_size = 6 if arm_role == "center" else 5
                
                pygame.draw.circle(surface, tip_color,
                                 (int(arm_pos.x), int(arm_pos.y)), tip_size)
        
        # Draw octopus body (on top of arms)
        super().render(surface)


class Player(Entity):
    """Player entity representing the octopus character.
    
    The player is an octopus with 10 arms that can shoot ink slime
    projectiles in a sequential pattern.
    """
    
    def __init__(self, x: float = 0, y: float = 0):
        """Initialize the Player entity.
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(name="Player_Octopus")
        
        # Add player tag
        self.add_tag("player")
        
        # Configure all components
        self._setup_transform(x, y)
        self._setup_render()
        self._setup_physics()
        self._setup_input()
        self._setup_weapon()
        self._setup_collision()
        self._setup_health()
        
    def _setup_transform(self, x: float, y: float) -> None:
        """Set up the transform component."""
        transform = TransformComponent()
        transform.set_position(x, y)
        self.add_component(transform)
        
    def _setup_render(self) -> None:
        """Set up the render component with custom octopus rendering."""
        render = OctopusRenderComponent("octopus")
        # For now, use a placeholder circle
        render.color = (128, 0, 128)  # Purple color for octopus
        render.shape = "circle"
        render.size = (60, 60)  # Octopus body size
        self.add_component(render)
        
    def _setup_physics(self) -> None:
        """Set up the physics component."""
        physics = PhysicsComponent()
        physics.max_velocity = pygame.math.Vector2(300, 300)  # Movement speed
        physics.friction = 5.0  # Higher friction for responsive controls
        physics.use_gravity = False  # No gravity for top-down game
        self.add_component(physics)
        
    def _setup_input(self) -> None:
        """Set up the input component."""
        input_comp = InputComponent()
        input_comp.move_speed = 300.0  # Pixels per second
        self.add_component(input_comp)
        
    def _setup_weapon(self) -> None:
        """Set up the weapon component with 3-arm system and manual rotation."""
        weapon = WeaponComponent(arm_count=10, base_cooldown=0.5)
        weapon.projectile_speed = 500.0
        weapon.ink_color = "dark_blue"  # Starting ink color
        
        # Configure damage values for different arm types
        weapon.damage = 10  # Base damage
        weapon.center_damage_multiplier = 1.5  # Center arm does 50% more damage
        weapon.side_damage_multiplier = 0.8  # Side arms do 20% less damage
        
        # Set high fire rate for rapid shooting
        weapon.set_fire_rate(10.0)  # 10 shots per second when holding spacebar
        
        # Initialize with arms 0, 1, 2 active (1 is center)
        weapon.active_arm_index = 1
        
        self.add_component(weapon)
        
    def _setup_collision(self) -> None:
        """Set up the collision component."""
        collision = CollisionComponent(width=60, height=60)
        collision.collision_type = "player"
        self.add_component(collision)
        
    def _setup_health(self) -> None:
        """Set up the health component."""
        health = HealthComponent(max_health=100)
        self.add_component(health)
        
    def set_ink_color(self, color: str) -> None:
        """Change the octopus's ink color.
        
        Args:
            color: New ink color (e.g., "dark_blue", "purple", "green", "red", "rainbow")
        """
        weapon = self.get_component("weapon")
        if weapon:
            weapon.set_ink_color(color)