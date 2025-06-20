"""
Object pooling system for reusing game objects.
This helps improve performance by reducing the need for frequent object creation and destruction.
"""

from typing import List, Callable, Dict, Any, Optional, TypeVar, Generic

T = TypeVar('T')

class ObjectPool(Generic[T]):
    """
    Generic object pool for reusing game objects.
    
    This class manages a pool of objects that can be reused instead of creating
    new objects and destroying them, which can be expensive operations.
    """
    
    def __init__(self, factory_func: Callable[[], T], reset_func: Callable[[T], None], initial_size: int = 10):
        """
        Initialize the object pool.
        
        Args:
            factory_func: Function that creates a new object when the pool is empty
            reset_func: Function that resets an object to its initial state before reuse
            initial_size: Initial number of objects to create in the pool
        """
        self.factory_func = factory_func
        self.reset_func = reset_func
        self.active_objects: List[T] = []
        self.inactive_objects: List[T] = []
        
        # Pre-populate the pool with initial objects
        for _ in range(initial_size):
            self.inactive_objects.append(self.factory_func())
            
        self.peak_active_count = 0
        self.total_created = initial_size
        
    def get(self) -> T:
        """
        Get an object from the pool. If the pool is empty, a new object is created.
        
        Returns:
            An object from the pool
        """
        if not self.inactive_objects:
            # Create a new object if none are available
            new_object = self.factory_func()
            self.total_created += 1
            self.active_objects.append(new_object)
        else:
            # Get an object from the inactive pool
            new_object = self.inactive_objects.pop()
            self.active_objects.append(new_object)
            
        # Update peak count for statistics
        if len(self.active_objects) > self.peak_active_count:
            self.peak_active_count = len(self.active_objects)
            
        return new_object
        
    def release(self, obj: T) -> None:
        """
        Return an object to the pool for reuse.
        
        Args:
            obj: The object to return to the pool
        """
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            self.reset_func(obj)
            self.inactive_objects.append(obj)
            
    def release_all(self) -> None:
        """Release all active objects back to the pool."""
        for obj in self.active_objects[:]:  # Create a copy to avoid modification during iteration
            self.release(obj)
            
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the object pool.
        
        Returns:
            Dictionary with pool statistics
        """
        return {
            "active_count": len(self.active_objects),
            "inactive_count": len(self.inactive_objects),
            "total_count": len(self.active_objects) + len(self.inactive_objects),
            "peak_active_count": self.peak_active_count,
            "total_created": self.total_created
        }


class ProjectilePool:
    """
    Specialized object pool for ink slime projectiles.
    
    This class provides a convenient interface for working with ink slime projectiles
    and integrates with the entity system.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """Get the singleton instance of the ProjectilePool."""
        if ProjectilePool._instance is None:
            ProjectilePool._instance = ProjectilePool()
        return ProjectilePool._instance
    
    def __init__(self):
        """Initialize the projectile pool."""
        self.pools: Dict[str, ObjectPool] = {}
        self.entity_factory = None
        self.entity_manager = None
        
    def initialize(self, entity_factory, entity_manager, initial_size: int = 20):
        """
        Initialize the projectile pool with the entity systems.
        
        Args:
            entity_factory: The entity factory for creating projectiles
            entity_manager: The entity manager for tracking entities
            initial_size: Initial number of projectiles to create in each pool
        """
        self.entity_factory = entity_factory
        self.entity_manager = entity_manager
        
        # Create pools for different ink colors
        ink_colors = ["dark_blue", "purple", "green", "red", "rainbow"]
        
        for color in ink_colors:
            self.pools[color] = ObjectPool(
                factory_func=lambda c=color: self._create_projectile(c),
                reset_func=self._reset_projectile,
                initial_size=initial_size
            )
            
    def _create_projectile(self, color: str):
        """
        Create a new projectile with the specified color.
        
        Args:
            color: The color of the ink projectile
            
        Returns:
            A new projectile entity
        """
        # Create a projectile at a far-off position (will be repositioned when used)
        projectile = self.entity_factory.create_ink_slime(-1000, -1000, 
                                                         direction=pygame.math.Vector2(0, 0),
                                                         color=color)
        
        # Deactivate it initially
        projectile.active = False
        
        return projectile
        
    def _reset_projectile(self, projectile):
        """
        Reset a projectile to its initial state for reuse.
        
        Args:
            projectile: The projectile to reset
        """
        # Move off-screen
        transform = projectile.get_component("transform")
        if transform:
            transform.position.x = -1000
            transform.position.y = -1000
            
        # Reset physics
        physics = projectile.get_component("physics")
        if physics:
            physics.velocity.x = 0
            physics.velocity.y = 0
            
        # Deactivate
        projectile.active = False
        
    def get_projectile(self, x: float, y: float, direction, color: str = "dark_blue"):
        """
        Get a projectile from the pool and position it.
        
        Args:
            x: X position to place the projectile
            y: Y position to place the projectile
            direction: Direction vector for the projectile
            color: Color of the ink projectile
            
        Returns:
            A projectile entity ready for use
        """
        # Get the appropriate pool
        if color not in self.pools:
            color = "dark_blue"  # Default fallback
            
        pool = self.pools[color]
        
        # Get a projectile from the pool
        projectile = pool.get()
        
        # Position and activate the projectile
        transform = projectile.get_component("transform")
        if transform:
            transform.position.x = x
            transform.position.y = y
            
        # Set direction
        physics = projectile.get_component("physics")
        if physics:
            physics.velocity = direction.normalize() * 300  # Projectile speed
            
        # Activate
        projectile.active = True
        
        return projectile
        
    def release_projectile(self, projectile):
        """
        Return a projectile to the pool.
        
        Args:
            projectile: The projectile to return to the pool
        """
        # Get the ink color to determine which pool to return to
        ink_component = projectile.get_component("ink_slime")
        if ink_component:
            color = ink_component.ink_color
            if color in self.pools:
                self.pools[color].release(projectile)
            else:
                self.pools["dark_blue"].release(projectile)  # Default fallback
                
    def get_stats(self):
        """
        Get statistics about all projectile pools.
        
        Returns:
            Dictionary with statistics for each color pool
        """
        stats = {}
        for color, pool in self.pools.items():
            stats[color] = pool.get_stats()
            
        return stats


# Import at the end to avoid circular imports
import pygame