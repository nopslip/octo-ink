"""
Base game state class that defines the interface for all game states.
All game states (main menu, gameplay, pause, etc.) should inherit from this class.
"""

import pygame
from abc import ABC, abstractmethod


class GameState(ABC):
    """Abstract base class for all game states."""
    
    def __init__(self, game_engine):
        """
        Initialize the game state.
        
        Args:
            game_engine: Reference to the main game engine
        """
        self.game_engine = game_engine
        self.next_state = None
    
    @abstractmethod
    def enter(self, **kwargs):
        """
        Called when entering this state.
        
        Args:
            **kwargs: Optional parameters passed when transitioning to this state
        """
        pass
    
    @abstractmethod
    def exit(self):
        """Called when exiting this state."""
        pass
    
    @abstractmethod
    def handle_events(self, events):
        """
        Process pygame events.
        
        Args:
            events: List of pygame events to process
        """
        pass
    
    @abstractmethod
    def update(self, dt):
        """
        Update the state logic.
        
        Args:
            dt: Time delta in seconds since last update
        """
        pass
    
    @abstractmethod
    def render(self, surface):
        """
        Render the state to the given surface.
        
        Args:
            surface: Pygame surface to render to
        """
        pass
    
    def transition_to(self, next_state, **kwargs):
        """
        Request a transition to another state.
        
        Args:
            next_state: The state to transition to
            **kwargs: Optional parameters to pass to the next state
        """
        self.next_state = (next_state, kwargs)