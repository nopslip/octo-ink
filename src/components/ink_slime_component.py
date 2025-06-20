"""Ink Slime Component for managing ink projectile properties and effects."""

from typing import Optional
from src.components.component import Component


class InkSlimeComponent(Component):
    """Component that manages ink slime projectile properties and collision effects.
    
    This component handles the visual and gameplay effects when ink slime
    hits ships or other targets.
    """
    
    def __init__(self, ink_color: str = "dark_blue", ink_damage: int = 10):
        """Initialize the InkSlimeComponent.
        
        Args:
            ink_color: Color of the ink (affects visual effects)
            ink_damage: Amount of ink load to add to ships on hit
        """
        super().__init__("ink_slime")
        
        # Ink properties
        self.ink_color: str = ink_color
        self.ink_damage: int = ink_damage
        self.splatter_effect: str = self._get_splatter_effect(ink_color)
        
        # Lifetime management
        self.lifetime: float = 5.0  # Seconds before auto-destruction
        self.age: float = 0.0
        
        # Physics properties
        self.has_gravity: bool = False  # Ink projectiles fly straight
        
    def _get_splatter_effect(self, ink_color: str) -> str:
        """Get the appropriate splatter effect name based on ink color.
        
        Args:
            ink_color: The color of the ink
            
        Returns:
            The name of the splatter effect to use
        """
        return f"splatter_{ink_color}"
        
    def update(self, dt: float) -> None:
        """Update the ink slime component.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Update age and check lifetime
        self.age += dt
        if self.age >= self.lifetime:
            # Mark entity for destruction
            if self.entity:
                self.entity.destroy()
                
    def on_collision(self, other_entity) -> None:
        """Handle collision with another entity.
        
        Args:
            other_entity: The entity that was collided with
        """
        if not other_entity:
            return
            
        # Check if collided with a ship
        if other_entity.has_tag("ship"):
            # Apply ink effects to the ship
            self._apply_ink_to_ship(other_entity)
            
            # Create splatter effect at collision point
            self._create_splatter_effect()
            
            # Play sound effect
            self._play_splat_sound()
            
            # Destroy the ink slime projectile
            if self.entity:
                self.entity.destroy()
                
        # Check if collided with other enemies (not ships)
        elif other_entity.has_tag("enemy"):
            # Still create effect and destroy projectile
            self._create_splatter_effect()
            self._play_splat_sound()
            if self.entity:
                self.entity.destroy()
                
    def _apply_ink_to_ship(self, ship_entity) -> None:
        """Apply ink load to a ship entity.
        
        Args:
            ship_entity: The ship entity to apply ink to
        """
        # Check if ship has ink load component
        ink_load = ship_entity.get_component("ink_load")
        if ink_load:
            ink_load.add_ink(self.ink_color, self.ink_damage)
        else:
            # If ship doesn't have ink load component, add one
            from src.components.ship_ink_load_component import ShipInkLoadComponent
            ink_load = ShipInkLoadComponent()
            ship_entity.add_component(ink_load)
            ink_load.add_ink(self.ink_color, self.ink_damage)
            
    def _create_splatter_effect(self) -> None:
        """Create a visual splatter effect at the current position."""
        if not self.entity:
            return
            
        transform = self.entity.get_component("transform")
        if not transform:
            return
            
        # TODO: When EffectManager is implemented, create splatter effect
        # For now, just log the effect
        position = transform.position
        # print(f"Splatter effect '{self.splatter_effect}' at ({position.x}, {position.y})")
        
    def _play_splat_sound(self) -> None:
        """Play the ink splat sound effect."""
        # TODO: When AudioManager is implemented, play sound
        # For now, just log the sound
        # print(f"Playing ink splat sound")
        pass
        
    def set_ink_color(self, color: str) -> None:
        """Change the ink color.
        
        Args:
            color: New ink color
        """
        self.ink_color = color
        self.splatter_effect = self._get_splatter_effect(color)