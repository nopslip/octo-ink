"""Base Entity class for the Entity-Component System."""

from typing import Dict, List, Optional, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.components.component import Component


class Entity:
    """Base class for all entities in the game.
    
    Entities are containers for components. They represent game objects
    like the player, enemies, projectiles, etc. The behavior of an entity
    is determined by the components attached to it.
    """
    
    def __init__(self, entity_id: Optional[str] = None, name: str = "Entity"):
        """Initialize the entity.
        
        Args:
            entity_id: Unique identifier for the entity. If None, a UUID will be generated.
            name: Human-readable name for the entity (for debugging)
        """
        self.entity_id = entity_id or str(uuid.uuid4())
        self.name = name
        self.components: Dict[str, 'Component'] = {}
        self.tags: List[str] = []
        self.active = True
        self.marked_for_destruction = False
        
    def add_component(self, component: 'Component') -> 'Component':
        """Add a component to the entity.
        
        Args:
            component: The component to add
            
        Returns:
            The added component
        """
        if component.component_type in self.components:
            # Remove existing component of the same type
            self.remove_component(component.component_type)
            
        self.components[component.component_type] = component
        component.entity = self
        component.on_add()
        return component
        
    def get_component(self, component_type: str) -> Optional['Component']:
        """Get a component by type.
        
        Args:
            component_type: The type of component to retrieve
            
        Returns:
            The component if found, None otherwise
        """
        return self.components.get(component_type)
        
    def has_component(self, component_type: str) -> bool:
        """Check if the entity has a component of the given type.
        
        Args:
            component_type: The type of component to check for
            
        Returns:
            True if the entity has the component, False otherwise
        """
        return component_type in self.components
        
    def remove_component(self, component_type: str) -> Optional['Component']:
        """Remove a component from the entity.
        
        Args:
            component_type: The type of component to remove
            
        Returns:
            The removed component if found, None otherwise
        """
        component = self.components.pop(component_type, None)
        if component:
            component.on_remove()
            component.entity = None
        return component
        
    def add_tag(self, tag: str) -> None:
        """Add a tag to the entity.
        
        Tags are useful for categorizing entities (e.g., "enemy", "player", "projectile")
        
        Args:
            tag: The tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
            
    def has_tag(self, tag: str) -> bool:
        """Check if the entity has a specific tag.
        
        Args:
            tag: The tag to check for
            
        Returns:
            True if the entity has the tag, False otherwise
        """
        return tag in self.tags
        
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the entity.
        
        Args:
            tag: The tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
            
    def update(self, dt: float) -> None:
        """Update all components of the entity.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.active:
            return
            
        # Update all enabled components
        for component in list(self.components.values()):
            if component.enabled:
                component.update(dt)
                
    def render(self, surface) -> None:
        """Render the entity.
        
        This method looks for a render component and calls its render method.
        
        Args:
            surface: The surface to render to (pygame Surface)
        """
        if not self.active:
            return
            
        render_component = self.get_component("render")
        if render_component and render_component.enabled:
            render_component.render(surface)
            
    def destroy(self) -> None:
        """Mark the entity for destruction.
        
        The entity will be removed from the entity manager on the next update.
        """
        self.marked_for_destruction = True
        self.active = False
        
        # Clean up all components
        for component in list(self.components.values()):
            component.on_remove()
        self.components.clear()
        
    def set_active(self, active: bool) -> None:
        """Set the active state of the entity.
        
        Inactive entities are not updated or rendered.
        
        Args:
            active: Whether the entity should be active
        """
        self.active = active