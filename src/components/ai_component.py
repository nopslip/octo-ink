"""AI Component for controlling non-player entity behavior."""

import random
import math
from src.components.component import Component


class AIComponent(Component):
    """Component that controls AI behavior for non-player entities."""
    
    def __init__(self, ai_type: str = "idle", **kwargs):
        """Initialize the AIComponent.
        
        Args:
            ai_type: Type of AI behavior ("ship", "captain", "turtle", "fish", etc.)
            **kwargs: Additional parameters for specific AI types
        """
        super().__init__("ai")
        
        self.ai_type: str = ai_type
        self.target_entity = None
        self.patrol_points = []
        self.current_patrol_index = 0
        self.state = "idle"
        self.state_timer = 0.0
        
        # Ship AI specific
        self.ship_speed = kwargs.get('ship_speed', 100.0)
        self.direction = kwargs.get('direction', 1)  # 1 for right, -1 for left
        self.avoid_distance = kwargs.get('avoid_distance', 50.0)
        
        # Captain AI specific
        self.panic_timer = 0.0
        self.explosion_delay = kwargs.get('explosion_delay', 2.0)
        
        # Turtle AI specific
        self.shield_active = kwargs.get('shield_active', True)
        self.defensive_radius = kwargs.get('defensive_radius', 100.0)
        
        # Fish AI specific
        self.wander_speed = kwargs.get('wander_speed', 80.0)
        self.wander_timer = 0.0
        self.wander_direction = [0.0, 0.0]
        self.wander_change_interval = kwargs.get('wander_change_interval', 2.0)
        
    def update(self, dt: float) -> None:
        """Update AI behavior.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.entity:
            return
            
        self.state_timer += dt
        
        # Execute behavior based on AI type
        if self.ai_type == "ship":
            self._update_ship_ai(dt)
        elif self.ai_type == "captain":
            self._update_captain_ai(dt)
        elif self.ai_type == "turtle":
            self._update_turtle_ai(dt)
        elif self.ai_type == "fish":
            self._update_fish_ai(dt)
        elif self.ai_type == "patrol":
            self._update_patrol(dt)
        elif self.ai_type == "wander":
            self._update_wander(dt)
            
    def _update_ship_ai(self, dt: float) -> None:
        """Update ship AI behavior - move horizontally and avoid obstacles."""
        physics = self.entity.get_component("physics")
        transform = self.entity.get_component("transform")
        
        if not physics or not transform:
            return
            
        # Basic horizontal movement
        physics.velocity = (self.ship_speed * self.direction, 0)
        
        # Check screen boundaries and reverse direction
        if transform.position.x <= 50 and self.direction < 0:
            self.direction = 1
        elif transform.position.x >= 750 and self.direction > 0:
            self.direction = -1
            
        # TODO: Add obstacle avoidance when collision system is ready
        
    def _update_captain_ai(self, dt: float) -> None:
        """Update captain AI behavior based on state."""
        captain_comp = self.entity.get_component("captain")
        
        if not captain_comp:
            return
            
        if captain_comp.state == "on_ship":
            # Captain follows ship movement (handled by attachment)
            pass
        elif captain_comp.state == "floating":
            # Panic behavior - handled by captain component
            pass
            
    def _update_turtle_ai(self, dt: float) -> None:
        """Update turtle AI behavior - defensive movement and shield behavior."""
        physics = self.entity.get_component("physics")
        transform = self.entity.get_component("transform")
        shield = self.entity.get_component("shield")
        
        if not physics or not transform:
            return
            
        # Slow defensive movement pattern
        if self.state == "idle":
            # Move slowly in a defensive pattern
            self.state_timer += dt
            physics.velocity = (
                math.sin(self.state_timer * 0.5) * 30,
                math.cos(self.state_timer * 0.3) * 20
            )
            
        # Keep shield active
        if shield and not shield.active:
            shield.activate()
            
    def _update_fish_ai(self, dt: float) -> None:
        """Update fish AI behavior - wandering movement for bonus targets."""
        physics = self.entity.get_component("physics")
        transform = self.entity.get_component("transform")
        
        if not physics or not transform:
            return
            
        # Update wander timer
        self.wander_timer += dt
        
        # Change direction periodically
        if self.wander_timer >= self.wander_change_interval:
            self.wander_timer = 0.0
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            self.wander_direction = [
                math.cos(angle) * self.wander_speed,
                math.sin(angle) * self.wander_speed
            ]
            
        # Apply wandering velocity
        physics.velocity = tuple(self.wander_direction)
        
        # Keep fish within screen bounds
        if transform.position.x < 50 or transform.position.x > 750:
            self.wander_direction[0] *= -1
        if transform.position.y < 50 or transform.position.y > 550:
            self.wander_direction[1] *= -1
            
    def _update_patrol(self, dt: float) -> None:
        """Update patrol behavior."""
        if not self.patrol_points:
            return
            
        physics = self.entity.get_component("physics")
        transform = self.entity.get_component("transform")
        
        if not physics or not transform:
            return
            
        # Move towards current patrol point
        target = self.patrol_points[self.current_patrol_index]
        dx = target[0] - transform.position.x
        dy = target[1] - transform.position.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:  # Reached patrol point
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        else:
            # Move towards target
            physics.velocity = (dx/distance * 100, dy/distance * 100)
        
    def _update_wander(self, dt: float) -> None:
        """Update wander behavior."""
        physics = self.entity.get_component("physics")
        
        if not physics:
            return
            
        # Random movement
        if self.state_timer > 1.0:
            self.state_timer = 0.0
            physics.velocity = (
                random.uniform(-50, 50),
                random.uniform(-50, 50)
            )
        
    def set_target(self, target_entity) -> None:
        """Set the target entity for AI behaviors.
        
        Args:
            target_entity: The entity to target
        """
        self.target_entity = target_entity
        
    def set_state(self, new_state: str) -> None:
        """Change the AI state.
        
        Args:
            new_state: The new state to set
        """
        self.state = new_state
        self.state_timer = 0.0