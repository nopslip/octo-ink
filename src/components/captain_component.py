"""Captain Component for managing captain-specific behavior."""

import random
from src.components.component import Component


class CaptainComponent(Component):
    """Component that manages captain behavior and death effects."""
    
    def __init__(self):
        """Initialize the CaptainComponent."""
        super().__init__("captain")
        
        self.state = "on_ship"  # States: on_ship, floating, dead
        self.panic_timer = 0.0
        self.explosion_timer = 0.0
        self.explosion_delay = 2.0  # Seconds before head explodes
        self.attached_ship = None  # Reference to the ship entity
        
    def update(self, dt: float) -> None:
        """Update captain behavior based on state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.entity:
            return
            
        if self.state == "floating":
            # Update panic animation
            animation = self.entity.get_component("animation")
            if animation and animation.current_animation != "captain_panic":
                animation.play("captain_panic", loop=True)
            
            # Update floating physics
            physics = self.entity.get_component("physics")
            if physics:
                # Add some random movement to simulate floating
                physics.velocity = (
                    random.uniform(-20, 20),
                    random.uniform(-10, 0)  # Mostly upward
                )
            
            # Update explosion timer
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_delay:
                self._explode_head()
                
    def set_state(self, new_state: str) -> None:
        """Change the captain's state.
        
        Args:
            new_state: The new state to set ("on_ship", "floating", "dead")
        """
        self.state = new_state
        
        if new_state == "floating":
            # Reset timers
            self.panic_timer = 0.0
            self.explosion_timer = 0.0
            
            # Detach from ship
            self.attached_ship = None
            
            # Play panic sound (when audio manager is available)
            # audio_manager = self.entity.entity_manager.game_engine.audio_manager
            # audio_manager.play_sound("captain_panic")
            
    def attach_to_ship(self, ship_entity) -> None:
        """Attach the captain to a ship.
        
        Args:
            ship_entity: The ship entity to attach to
        """
        self.attached_ship = ship_entity
        self.state = "on_ship"
        
        # Position captain on ship
        if ship_entity:
            ship_transform = ship_entity.get_component("transform")
            captain_transform = self.entity.get_component("transform")
            
            if ship_transform and captain_transform:
                # Position captain on top of ship
                captain_transform.set_position(
                    ship_transform.position.x,
                    ship_transform.position.y - 30  # Above the ship
                )
                
    def detach_from_ship(self) -> None:
        """Detach the captain from the ship when it sinks."""
        self.set_state("floating")
        
    def _explode_head(self) -> None:
        """Trigger the head explosion effect."""
        # Get position for effect
        transform = self.entity.get_component("transform")
        if not transform:
            return
            
        position = (transform.position.x, transform.position.y)
        
        # Create head explosion effect (when effect manager is available)
        # effect_manager = self.entity.entity_manager.game_engine.effect_manager
        # effect_manager.create_effect("head_explosion", position)
        
        # Play explosion sound (when audio manager is available)
        # audio_manager = self.entity.entity_manager.game_engine.audio_manager
        # audio_manager.play_sound("head_explosion")
        
        # Award bonus points (when score manager is available)
        # score_manager = self.entity.entity_manager.game_engine.score_manager
        # score_manager.add_score(500)  # Bonus points for captain
        
        # Mark entity for destruction
        self.state = "dead"
        self.entity.destroy()
        
    def on_ship_sinking(self) -> None:
        """Called when the attached ship starts sinking."""
        if self.state == "on_ship":
            self.detach_from_ship()