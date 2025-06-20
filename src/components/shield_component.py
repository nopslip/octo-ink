"""Shield Component for blocking ink shots."""

from src.components.component import Component


class ShieldComponent(Component):
    """Component that provides shield functionality for entities like turtles."""
    
    def __init__(self, max_health: int = 3, block_radius: float = 40.0):
        """Initialize the ShieldComponent.
        
        Args:
            max_health: Maximum shield durability (hits it can take)
            block_radius: Radius around entity where shield blocks projectiles
        """
        super().__init__("shield")
        
        self.max_health = max_health
        self.current_health = max_health
        self.block_radius = block_radius
        self.active = True
        self.recharge_timer = 0.0
        self.recharge_delay = 5.0  # Seconds before shield starts recharging
        self.recharge_rate = 1.0  # Health points per second
        self.hit_cooldown = 0.0  # Prevents multiple hits in same frame
        self.hit_cooldown_duration = 0.1
        
        # Visual feedback
        self.flash_timer = 0.0
        self.flash_duration = 0.2
        self.is_flashing = False
        
    def update(self, dt: float) -> None:
        """Update shield state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.entity:
            return
            
        # Update hit cooldown
        if self.hit_cooldown > 0:
            self.hit_cooldown -= dt
            
        # Update flash effect
        if self.is_flashing:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_duration:
                self.is_flashing = False
                self.flash_timer = 0.0
                
        # Handle shield recharging
        if not self.active and self.current_health < self.max_health:
            self.recharge_timer += dt
            
            if self.recharge_timer >= self.recharge_delay:
                # Start recharging
                self.current_health += self.recharge_rate * dt
                
                if self.current_health >= self.max_health:
                    self.current_health = self.max_health
                    self.active = True
                    self.recharge_timer = 0.0
                    
    def take_hit(self, damage: int = 1) -> bool:
        """Handle shield being hit by a projectile.
        
        Args:
            damage: Amount of damage to shield
            
        Returns:
            True if shield blocked the hit, False if shield is down
        """
        if not self.active or self.hit_cooldown > 0:
            return False
            
        # Apply damage
        self.current_health -= damage
        self.hit_cooldown = self.hit_cooldown_duration
        
        # Trigger visual feedback
        self.is_flashing = True
        self.flash_timer = 0.0
        
        # Update render component for visual feedback
        render = self.entity.get_component("render")
        if render:
            # Could modify sprite color or add shield effect
            pass
            
        # Check if shield is depleted
        if self.current_health <= 0:
            self.current_health = 0
            self.active = False
            self.recharge_timer = 0.0
            
        return True
        
    def can_block_projectile(self, projectile_position: tuple) -> bool:
        """Check if shield can block a projectile at given position.
        
        Args:
            projectile_position: Position of the projectile
            
        Returns:
            True if shield can block, False otherwise
        """
        if not self.active:
            return False
            
        transform = self.entity.get_component("transform")
        if not transform:
            return False
            
        # Calculate distance from entity center to projectile
        dx = projectile_position[0] - transform.position[0]
        dy = projectile_position[1] - transform.position[1]
        distance_squared = dx * dx + dy * dy
        
        return distance_squared <= self.block_radius * self.block_radius
        
    def activate(self) -> None:
        """Activate the shield."""
        if self.current_health > 0:
            self.active = True
            
    def deactivate(self) -> None:
        """Deactivate the shield."""
        self.active = False
        
    def get_health_percentage(self) -> float:
        """Get shield health as percentage.
        
        Returns:
            Shield health from 0.0 to 1.0
        """
        return self.current_health / self.max_health if self.max_health > 0 else 0.0
        
    def is_active(self) -> bool:
        """Check if shield is currently active.
        
        Returns:
            True if shield is active, False otherwise
        """
        return self.active and self.current_health > 0