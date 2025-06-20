"""Health Component for managing entity health and damage."""

from src.components.component import Component


class HealthComponent(Component):
    """Component that manages health, damage, and death states."""
    
    def __init__(self, max_health: int = 100):
        """Initialize the HealthComponent.
        
        Args:
            max_health: Maximum health value
        """
        super().__init__("health")
        
        self.max_health: int = max_health
        self.current_health: int = max_health
        self.is_invulnerable: bool = False
        self.invulnerability_time: float = 0.0
        
    def update(self, dt: float) -> None:
        """Update health component state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Update invulnerability timer
        if self.is_invulnerable and self.invulnerability_time > 0:
            self.invulnerability_time -= dt
            if self.invulnerability_time <= 0:
                self.is_invulnerable = False
                
    def take_damage(self, amount: int) -> None:
        """Apply damage to the entity.
        
        Args:
            amount: Amount of damage to apply
        """
        if self.is_invulnerable:
            return
            
        self.current_health = max(0, self.current_health - amount)
        
        if self.current_health <= 0 and self.entity:
            # Mark entity for destruction
            self.entity.destroy()
            
    def heal(self, amount: int) -> None:
        """Heal the entity.
        
        Args:
            amount: Amount of health to restore
        """
        self.current_health = min(self.max_health, self.current_health + amount)
        
    def set_invulnerable(self, duration: float) -> None:
        """Make the entity temporarily invulnerable.
        
        Args:
            duration: Duration of invulnerability in seconds
        """
        self.is_invulnerable = True
        self.invulnerability_time = duration
        
    def get_health_percentage(self) -> float:
        """Get current health as a percentage.
        
        Returns:
            Health percentage (0.0 to 1.0)
        """
        return self.current_health / self.max_health if self.max_health > 0 else 0.0