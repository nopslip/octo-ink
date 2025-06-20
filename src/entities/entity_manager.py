"""Entity Manager for tracking and updating all entities in the game."""

from typing import Dict, List, Optional, Set
from src.entities.entity import Entity


class EntityManager:
    """Manages all entities in the game.
    
    The EntityManager is responsible for:
    - Tracking all active entities
    - Updating entities each frame
    - Rendering entities
    - Managing entity lifecycle (creation and destruction)
    - Providing query methods to find entities by tags or components
    """
    
    def __init__(self):
        """Initialize the EntityManager."""
        self.entities: Dict[str, Entity] = {}
        self.entities_to_add: List[Entity] = []
        self.entities_to_remove: List[str] = []
        self.tag_index: Dict[str, Set[str]] = {}  # tag -> set of entity_ids
        
    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the manager.
        
        The entity will be added at the end of the current frame to avoid
        modifying the entity list during iteration.
        
        Args:
            entity: The entity to add
        """
        self.entities_to_add.append(entity)
        
    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity from the manager.
        
        The entity will be removed at the end of the current frame to avoid
        modifying the entity list during iteration.
        
        Args:
            entity_id: The ID of the entity to remove
        """
        if entity_id in self.entities:
            self.entities_to_remove.append(entity_id)
            
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID.
        
        Args:
            entity_id: The ID of the entity to retrieve
            
        Returns:
            The entity if found, None otherwise
        """
        return self.entities.get(entity_id)
        
    def get_entities_with_tag(self, tag: str) -> List[Entity]:
        """Get all entities with a specific tag.
        
        Args:
            tag: The tag to search for
            
        Returns:
            List of entities with the given tag
        """
        entity_ids = self.tag_index.get(tag, set())
        return [self.entities[entity_id] for entity_id in entity_ids if entity_id in self.entities]
        
    def get_entities_with_component(self, component_type: str) -> List[Entity]:
        """Get all entities that have a specific component type.
        
        Args:
            component_type: The type of component to search for
            
        Returns:
            List of entities with the given component type
        """
        return [entity for entity in self.entities.values() 
                if entity.has_component(component_type)]
        
    def get_entities_with_tags_and_components(self, tags: List[str] = None, 
                                             components: List[str] = None) -> List[Entity]:
        """Get all entities that have all specified tags and components.
        
        Args:
            tags: List of tags the entity must have (all required)
            components: List of component types the entity must have (all required)
            
        Returns:
            List of entities matching all criteria
        """
        result = []
        for entity in self.entities.values():
            # Check tags
            if tags:
                if not all(entity.has_tag(tag) for tag in tags):
                    continue
                    
            # Check components
            if components:
                if not all(entity.has_component(comp) for comp in components):
                    continue
                    
            result.append(entity)
            
        return result
        
    def update(self, dt: float) -> None:
        """Update all entities.
        
        This method:
        1. Processes pending entity additions
        2. Updates all active entities
        3. Processes pending entity removals
        
        Args:
            dt: Delta time in seconds since the last update
        """
        # Add pending entities
        self._process_entity_additions()
        
        # Update all active entities
        for entity in list(self.entities.values()):
            if entity.active and not entity.marked_for_destruction:
                entity.update(dt)
                
            # Check if entity was marked for destruction during update
            if entity.marked_for_destruction:
                self.remove_entity(entity.entity_id)
                
        # Remove pending entities
        self._process_entity_removals()
        
    def render(self, surface) -> None:
        """Render all entities.
        
        Args:
            surface: The surface to render to (pygame Surface)
        """
        # Sort entities by their y-position for proper layering (if they have transform)
        entities_list = list(self.entities.values())
        
        def get_sort_key(entity):
            transform = entity.get_component("transform")
            if transform:
                return transform.position.y
            return 0
            
        entities_list.sort(key=get_sort_key)
        
        # Render all active entities
        for entity in entities_list:
            if entity.active:
                entity.render(surface)
                
    def clear(self) -> None:
        """Remove all entities from the manager."""
        # Mark all entities for destruction
        for entity in self.entities.values():
            entity.destroy()
            
        # Clear all data structures
        self.entities.clear()
        self.entities_to_add.clear()
        self.entities_to_remove.clear()
        self.tag_index.clear()
        
    def _process_entity_additions(self) -> None:
        """Process pending entity additions."""
        for entity in self.entities_to_add:
            self.entities[entity.entity_id] = entity
            
            # Update tag index
            for tag in entity.tags:
                if tag not in self.tag_index:
                    self.tag_index[tag] = set()
                self.tag_index[tag].add(entity.entity_id)
                
        self.entities_to_add.clear()
        
    def _process_entity_removals(self) -> None:
        """Process pending entity removals."""
        for entity_id in self.entities_to_remove:
            entity = self.entities.pop(entity_id, None)
            if entity:
                # Remove from tag index
                for tag in entity.tags:
                    if tag in self.tag_index:
                        self.tag_index[tag].discard(entity_id)
                        if not self.tag_index[tag]:
                            del self.tag_index[tag]
                            
        self.entities_to_remove.clear()
        
    def get_entity_count(self) -> int:
        """Get the total number of entities.
        
        Returns:
            The number of entities currently managed
        """
        return len(self.entities)
        
    def get_active_entity_count(self) -> int:
        """Get the number of active entities.
        
        Returns:
            The number of active entities
        """
        return sum(1 for entity in self.entities.values() if entity.active)