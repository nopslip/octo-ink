"""Base Component class for the Entity-Component System."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Entity


class Component(ABC):
    """Base class for all components in the Entity-Component System.
    
    Components define specific behaviors and properties that can be
    attached to entities. Each component type should inherit from this
    base class and implement the update method.
    """
    
    def __init__(self, component_type: str):
        """Initialize the component.
        
        Args:
            component_type: A string identifier for this component type
        """
        self.component_type = component_type
        self.entity: 'Entity' = None
        self.enabled = True
        
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the component.
        
        This method is called every frame and should contain the
        component's update logic.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        pass
    
    def on_add(self) -> None:
        """Called when the component is added to an entity.
        
        Override this method to perform initialization that requires
        access to the entity or other components.
        """
        pass
    
    def on_remove(self) -> None:
        """Called when the component is removed from an entity.
        
        Override this method to perform cleanup when the component
        is removed.
        """
        pass
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the component.
        
        Disabled components will not be updated.
        
        Args:
            enabled: Whether the component should be enabled
        """
        self.enabled = enabled