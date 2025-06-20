"""
Spatial partitioning system for efficient collision detection.
This system divides the game world into a grid to reduce the number of collision checks needed.
"""

from typing import Dict, List, Set, Tuple, Optional
import pygame
from src.entities.entity import Entity


class SpatialGrid:
    """
    Spatial partitioning grid for efficient collision detection.
    
    This class divides the game world into a grid of cells and tracks which entities
    are in each cell. This allows for more efficient collision detection by only
    checking entities that are in the same or adjacent cells.
    """
    
    def __init__(self, width: int, height: int, cell_size: int = 100):
        """
        Initialize the spatial grid.
        
        Args:
            width: Width of the game world in pixels
            height: Height of the game world in pixels
            cell_size: Size of each grid cell in pixels
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        # Calculate grid dimensions
        self.cols = (width // cell_size) + 1
        self.rows = (height // cell_size) + 1
        
        # Initialize grid cells
        self.grid: Dict[Tuple[int, int], List[Entity]] = {}
        
        # Entity to cell mapping for quick lookups
        self.entity_cells: Dict[int, Set[Tuple[int, int]]] = {}
        
        # Debug information
        self.collision_checks = 0
        self.potential_collisions = 0
        self.actual_collisions = 0
        
    def clear(self):
        """Clear all entities from the grid."""
        self.grid.clear()
        self.entity_cells.clear()
        
    def update(self, entities: List[Entity]):
        """
        Update the grid with the current positions of all entities.
        
        Args:
            entities: List of all active entities
        """
        # Clear the grid
        self.clear()
        
        # Add each entity to the appropriate grid cells
        for entity in entities:
            if not entity.active:
                continue
                
            # Get entity position and size
            transform = entity.get_component("transform")
            collision = entity.get_component("collision")
            
            if not transform or not collision:
                continue
                
            # Calculate entity bounds
            x = transform.position.x
            y = transform.position.y
            width = collision.width
            height = collision.height
            
            # Calculate grid cells that the entity overlaps
            min_col = max(0, int((x - width / 2) / self.cell_size))
            max_col = min(self.cols - 1, int((x + width / 2) / self.cell_size))
            min_row = max(0, int((y - height / 2) / self.cell_size))
            max_row = min(self.rows - 1, int((y + height / 2) / self.cell_size))
            
            # Add entity to each overlapping cell
            entity_id = entity.entity_id
            self.entity_cells[entity_id] = set()
            
            for col in range(min_col, max_col + 1):
                for row in range(min_row, max_row + 1):
                    cell_key = (col, row)
                    
                    # Create cell if it doesn't exist
                    if cell_key not in self.grid:
                        self.grid[cell_key] = []
                        
                    # Add entity to cell
                    self.grid[cell_key].append(entity)
                    self.entity_cells[entity_id].add(cell_key)
                    
    def get_potential_collisions(self, entity: Entity) -> List[Entity]:
        """
        Get all entities that could potentially collide with the given entity.
        
        Args:
            entity: The entity to check for potential collisions
            
        Returns:
            List of entities that could potentially collide with the given entity
        """
        # Reset collision check counter
        self.collision_checks += 1
        
        # Get entity ID
        entity_id = entity.entity_id
        
        # If entity is not in the grid, return empty list
        if entity_id not in self.entity_cells:
            return []
            
        # Get all cells that the entity overlaps
        cells = self.entity_cells[entity_id]
        
        # Get all entities in those cells
        potential_collisions = set()
        for cell_key in cells:
            if cell_key in self.grid:
                for other_entity in self.grid[cell_key]:
                    if other_entity.entity_id != entity_id and other_entity.active:
                        potential_collisions.add(other_entity)
                        
        # Update potential collisions counter
        self.potential_collisions += len(potential_collisions)
        
        return list(potential_collisions)
        
    def check_collision(self, entity1: Entity, entity2: Entity) -> bool:
        """
        Check if two entities are colliding using AABB collision detection.
        
        Args:
            entity1: First entity
            entity2: Second entity
            
        Returns:
            True if the entities are colliding, False otherwise
        """
        transform1 = entity1.get_component("transform")
        collision1 = entity1.get_component("collision")
        transform2 = entity2.get_component("transform")
        collision2 = entity2.get_component("collision")
        
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
        
        collision = rect1.colliderect(rect2)
        if collision:
            self.actual_collisions += 1
            
        return collision
        
    def get_nearby_entities(self, x: float, y: float, radius: float) -> List[Entity]:
        """
        Get all entities within a certain radius of a point.
        
        Args:
            x: X coordinate of the point
            y: Y coordinate of the point
            radius: Radius to check for entities
            
        Returns:
            List of entities within the radius
        """
        # Calculate grid cells that the radius overlaps
        min_col = max(0, int((x - radius) / self.cell_size))
        max_col = min(self.cols - 1, int((x + radius) / self.cell_size))
        min_row = max(0, int((y - radius) / self.cell_size))
        max_row = min(self.rows - 1, int((y + radius) / self.cell_size))
        
        # Get all entities in those cells
        nearby_entities = set()
        for col in range(min_col, max_col + 1):
            for row in range(min_row, max_row + 1):
                cell_key = (col, row)
                if cell_key in self.grid:
                    for entity in self.grid[cell_key]:
                        if entity.active:
                            nearby_entities.add(entity)
                            
        return list(nearby_entities)
        
    def get_entities_by_tag(self, tag: str) -> List[Entity]:
        """
        Get all entities with a specific tag.
        
        Args:
            tag: The tag to search for
            
        Returns:
            List of entities with the specified tag
        """
        entities = set()
        for cell_entities in self.grid.values():
            for entity in cell_entities:
                if tag in entity.tags and entity.active:
                    entities.add(entity)
                    
        return list(entities)
        
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the spatial grid.
        
        Returns:
            Dictionary with grid statistics
        """
        return {
            "cells": len(self.grid),
            "entities": len(self.entity_cells),
            "collision_checks": self.collision_checks,
            "potential_collisions": self.potential_collisions,
            "actual_collisions": self.actual_collisions,
            "collision_efficiency": (
                (self.potential_collisions / self.collision_checks) 
                if self.collision_checks > 0 else 0
            )
        }
        
    def render_debug(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """
        Render debug visualization of the spatial grid.
        
        Args:
            surface: Surface to render on
            camera_offset: Camera offset for rendering
        """
        # Draw grid lines
        for col in range(self.cols):
            x = col * self.cell_size - camera_offset[0]
            pygame.draw.line(
                surface, 
                (100, 100, 100), 
                (x, 0), 
                (x, self.height),
                1
            )
            
        for row in range(self.rows):
            y = row * self.cell_size - camera_offset[1]
            pygame.draw.line(
                surface, 
                (100, 100, 100), 
                (0, y), 
                (self.width, y),
                1
            )
            
        # Draw occupied cells
        for (col, row), entities in self.grid.items():
            if entities:
                rect = pygame.Rect(
                    col * self.cell_size - camera_offset[0],
                    row * self.cell_size - camera_offset[1],
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(
                    surface,
                    (50, 150, 50, 50),  # Semi-transparent green
                    rect
                )
                
                # Draw entity count
                font = pygame.font.Font(None, 20)
                text = font.render(str(len(entities)), True, (255, 255, 255))
                surface.blit(
                    text,
                    (col * self.cell_size + 5 - camera_offset[0],
                     row * self.cell_size + 5 - camera_offset[1])
                )