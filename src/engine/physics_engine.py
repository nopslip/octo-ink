"""Physics engine for handling collision detection and physics simulation."""

import pygame
from typing import List, Dict, Tuple, Optional, Set


class PhysicsEngine:
    """
    Handles physics simulation and collision detection for game entities.
    
    Manages movement, collision detection, and physics responses between
    entities in the game world.
    """
    
    def __init__(self):
        """Initialize the physics engine."""
        # Collision groups for efficient collision detection
        self.collision_groups: Dict[str, List] = {
            "player": [],
            "enemy": [],
            "projectile": [],
            "obstacle": [],
            "pickup": []
        }
        
        # Physics settings
        self.gravity = 0.0  # No gravity in a top-down game
        self.friction = 0.9  # Friction coefficient (0-1)
        
        # Spatial partitioning for optimization
        self.grid_size = 100  # Size of each grid cell in pixels
        self.spatial_grid: Dict[Tuple[int, int], List] = {}
        
    def register_entity(self, entity, collision_group: str) -> None:
        """
        Register an entity with the physics engine.
        
        Args:
            entity: The entity to register
            collision_group: The collision group to add the entity to
        """
        if collision_group in self.collision_groups:
            if entity not in self.collision_groups[collision_group]:
                self.collision_groups[collision_group].append(entity)
                
    def unregister_entity(self, entity) -> None:
        """
        Unregister an entity from the physics engine.
        
        Args:
            entity: The entity to unregister
        """
        for group in self.collision_groups.values():
            if entity in group:
                group.remove(entity)
                
    def update(self, dt: float) -> None:
        """
        Update physics for all registered entities.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Clear spatial grid
        self.spatial_grid.clear()
        
        # Update all entities
        all_entities = []
        for group in self.collision_groups.values():
            all_entities.extend(group)
            
        # Update physics for each entity
        for entity in all_entities:
            if not hasattr(entity, 'active') or entity.active:
                self._update_entity_physics(entity, dt)
                
        # Build spatial grid
        self._build_spatial_grid(all_entities)
        
        # Check collisions
        self._check_collisions()
        
    def _update_entity_physics(self, entity, dt: float) -> None:
        """
        Update physics for a single entity.
        
        Args:
            entity: The entity to update
            dt: Delta time in seconds
        """
        # Get required components
        physics = entity.get_component("physics") if hasattr(entity, 'get_component') else None
        transform = entity.get_component("transform") if hasattr(entity, 'get_component') else None
        
        if not physics or not transform:
            return
            
        # Apply gravity
        physics.velocity.y += self.gravity * dt
        
        # Apply friction
        if physics.apply_friction:
            physics.velocity.x *= self.friction ** dt
            physics.velocity.y *= self.friction ** dt
            
        # Update position based on velocity
        transform.position.x += physics.velocity.x * dt
        transform.position.y += physics.velocity.y * dt
        
        # Apply rotation if entity has angular velocity
        if hasattr(physics, 'angular_velocity') and physics.angular_velocity != 0:
            transform.rotation += physics.angular_velocity * dt
            
    def _build_spatial_grid(self, entities: List) -> None:
        """
        Build spatial grid for efficient collision detection.
        
        Args:
            entities: List of entities to add to the grid
        """
        for entity in entities:
            if not hasattr(entity, 'active') or entity.active:
                transform = entity.get_component("transform") if hasattr(entity, 'get_component') else None
                collision = entity.get_component("collision") if hasattr(entity, 'get_component') else None
                
                if not transform or not collision:
                    continue
                    
                # Calculate grid cells that entity overlaps
                min_x = int((transform.position.x - collision.width / 2) / self.grid_size)
                max_x = int((transform.position.x + collision.width / 2) / self.grid_size)
                min_y = int((transform.position.y - collision.height / 2) / self.grid_size)
                max_y = int((transform.position.y + collision.height / 2) / self.grid_size)
                
                # Add entity to all overlapping grid cells
                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        cell = (x, y)
                        if cell not in self.spatial_grid:
                            self.spatial_grid[cell] = []
                        self.spatial_grid[cell].append(entity)
                        
    def _check_collisions(self) -> None:
        """Check for collisions between entities and handle responses."""
        # Check collisions between specific groups
        self._check_group_collisions("projectile", "enemy")
        self._check_group_collisions("player", "enemy")
        self._check_group_collisions("player", "pickup")
        self._check_group_collisions("projectile", "obstacle")
        
    def _check_group_collisions(self, group1: str, group2: str) -> None:
        """
        Check for collisions between two groups of entities.
        
        Args:
            group1: First collision group
            group2: Second collision group
        """
        # Get entities from groups
        entities1 = self.collision_groups.get(group1, [])
        entities2 = self.collision_groups.get(group2, [])
        
        # Check each entity in group1 against each in group2
        for entity1 in entities1:
            if not hasattr(entity1, 'active') or not entity1.active:
                continue
                
            # Use spatial partitioning to only check nearby entities
            nearby_entities = self._get_nearby_entities(entity1)
            
            for entity2 in nearby_entities:
                if (entity2 in entities2 and 
                    (not hasattr(entity2, 'active') or entity2.active) and
                    entity1 != entity2):
                    
                    # Check for collision
                    if self._entities_colliding(entity1, entity2):
                        # Handle collision
                        self._handle_collision(entity1, entity2)
                        
    def _get_nearby_entities(self, entity) -> List:
        """
        Get entities that are in the same grid cells as the given entity.
        
        Args:
            entity: The entity to find nearby entities for
            
        Returns:
            List of nearby entities
        """
        transform = entity.get_component("transform") if hasattr(entity, 'get_component') else None
        collision = entity.get_component("collision") if hasattr(entity, 'get_component') else None
        
        if not transform or not collision:
            return []
            
        # Calculate grid cells that entity overlaps
        min_x = int((transform.position.x - collision.width / 2) / self.grid_size)
        max_x = int((transform.position.x + collision.width / 2) / self.grid_size)
        min_y = int((transform.position.y - collision.height / 2) / self.grid_size)
        max_y = int((transform.position.y + collision.height / 2) / self.grid_size)
        
        # Get all entities in overlapping cells
        nearby = set()
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cell = (x, y)
                if cell in self.spatial_grid:
                    nearby.update(self.spatial_grid[cell])
                    
        # Remove the entity itself
        if entity in nearby:
            nearby.remove(entity)
            
        return list(nearby)
        
    def _entities_colliding(self, entity1, entity2) -> bool:
        """
        Check if two entities are colliding.
        
        Args:
            entity1: First entity
            entity2: Second entity
            
        Returns:
            True if entities are colliding, False otherwise
        """
        transform1 = entity1.get_component("transform") if hasattr(entity1, 'get_component') else None
        collision1 = entity1.get_component("collision") if hasattr(entity1, 'get_component') else None
        transform2 = entity2.get_component("transform") if hasattr(entity2, 'get_component') else None
        collision2 = entity2.get_component("collision") if hasattr(entity2, 'get_component') else None
        
        if not all([transform1, collision1, transform2, collision2]):
            return False
            
        # Simple AABB collision detection
        rect1 = pygame.Rect(
            transform1.position.x - collision1.width / 2,
            transform1.position.y - collision1.height / 2,
            collision1.width,
            collision1.height
        )
        
        rect2 = pygame.Rect(
            transform2.position.x - collision2.width / 2,
            transform2.position.y - collision2.height / 2,
            collision2.width,
            collision2.height
        )
        
        return rect1.colliderect(rect2)
        
    def _handle_collision(self, entity1, entity2) -> None:
        """
        Handle collision between two entities.
        
        Args:
            entity1: First entity
            entity2: Second entity
        """
        # Call collision handlers on both entities
        if hasattr(entity1, 'on_collision'):
            entity1.on_collision(entity2)
            
        if hasattr(entity2, 'on_collision'):
            entity2.on_collision(entity1)
            
        # Check for specific component collision handlers
        for component_name in ["collision", "physics", "ink_slime"]:
            component1 = entity1.get_component(component_name) if hasattr(entity1, 'get_component') else None
            if component1 and hasattr(component1, 'on_collision'):
                component1.on_collision(entity2)
                
            component2 = entity2.get_component(component_name) if hasattr(entity2, 'get_component') else None
            if component2 and hasattr(component2, 'on_collision'):
                component2.on_collision(entity1)