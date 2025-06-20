"""Ship Ink Load Component for managing how much ink a ship has taken on."""

from src.components.component import Component


class ShipInkLoadComponent(Component):
    """Component that tracks how much ink a ship has absorbed.
    
    Ships sink lower in the water as they take on more ink, and eventually
    sink completely when the ink load reaches maximum capacity.
    """
    
    def __init__(self, max_ink_load: int = 100):
        """Initialize the ShipInkLoadComponent.
        
        Args:
            max_ink_load: Maximum ink the ship can take before sinking
        """
        super().__init__("ink_load")
        
        # Ink load properties
        self.current_ink_load: int = 0
        self.max_ink_load: int = max_ink_load
        self.sink_level: float = 0.0  # 0 to 1, where 1 is fully sunk
        
        # Visual offset for sinking effect
        self.base_y_offset: float = 0.0
        self.max_sink_offset: float = 20.0  # Maximum pixels to sink
        
        # Sinking state
        self.is_sinking: bool = False
        self.sink_timer: float = 0.0
        self.sink_duration: float = 2.0  # Time to fully sink
        
    def update(self, dt: float) -> None:
        """Update the ink load component.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Handle sinking animation
        if self.is_sinking:
            self.sink_timer += dt
            if self.sink_timer >= self.sink_duration:
                # Ship has fully sunk, destroy it
                if self.entity:
                    self.entity.destroy()
                    
    def add_ink(self, ink_color: str, amount: int) -> None:
        """Add ink to the ship's load.
        
        Args:
            ink_color: Color of the ink (for potential special effects)
            amount: Amount of ink to add
        """
        # Increase ink load
        self.current_ink_load = min(self.current_ink_load + amount, self.max_ink_load)
        
        # Calculate new sink level
        self.sink_level = self.current_ink_load / self.max_ink_load
        
        # Update ship's visual appearance based on sink level
        self._update_ship_appearance()
        
        # Check if ship should start sinking
        if self.current_ink_load >= self.max_ink_load and not self.is_sinking:
            self._start_sinking()
            
    def _update_ship_appearance(self) -> None:
        """Update the ship's visual appearance based on ink load."""
        if not self.entity:
            return
            
        # Update render component's Y offset to make ship appear lower in water
        render = self.entity.get_component("render")
        if render:
            # Calculate visual sink offset
            sink_offset = self.sink_level * self.max_sink_offset
            render.offset.y = self.base_y_offset + sink_offset
            
            # Optionally darken the ship based on ink load
            # This would require render component to support tinting
            # render.tint = (255 - int(self.sink_level * 100), 
            #                255 - int(self.sink_level * 100), 
            #                255 - int(self.sink_level * 100))
            
    def _start_sinking(self) -> None:
        """Start the sinking animation."""
        self.is_sinking = True
        self.sink_timer = 0.0
        
        # Disable ship's AI and movement
        ai = self.entity.get_component("ai")
        if ai:
            ai.enabled = False
            
        physics = self.entity.get_component("physics")
        if physics:
            # Slow down the ship dramatically
            physics.velocity.x *= 0.1
            physics.velocity.y *= 0.1
            physics.max_velocity.x *= 0.1
            physics.max_velocity.y *= 0.1
            
        # TODO: Create sinking animation/effect
        # effect_manager = EffectManager.get_instance()
        # effect_manager.create_effect("ship_sinking", self.entity.get_component("transform").position)
        
    def get_ink_percentage(self) -> float:
        """Get the current ink load as a percentage.
        
        Returns:
            Ink load percentage (0.0 to 1.0)
        """
        return self.sink_level
        
    def is_ship_sinking(self) -> bool:
        """Check if the ship is currently sinking.
        
        Returns:
            True if ship is in sinking animation
        """
        return self.is_sinking