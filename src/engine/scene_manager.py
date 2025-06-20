"""
Scene Manager for the Octopus Ink Slime game.
Manages different game states and transitions between them.
"""

import pygame
from src.states.game_state import GameState
from src.states.main_menu_state import MainMenuState
from src.states.gameplay_state import GameplayState
from src.states.pause_menu_state import PauseMenuState
from src.states.game_over_state import GameOverState
from src.states.level_transition_state import LevelTransitionState


class SceneManager:
    """Manages game states and transitions between them."""
    
    def __init__(self, game_engine):
        """
        Initialize the scene manager.
        
        Args:
            game_engine: Reference to the main game engine
        """
        self.game_engine = game_engine
        self.states = {}
        self.current_state = None
        self.state_stack = []
        
        # Register default states
        self._register_default_states()
    
    def _register_default_states(self):
        """Register the default game states."""
        self.register_state("main_menu", MainMenuState(self.game_engine))
        self.register_state("gameplay", GameplayState(self.game_engine))
        self.register_state("pause_menu", PauseMenuState(self.game_engine))
        self.register_state("game_over", GameOverState(self.game_engine))
        self.register_state("level_transition", LevelTransitionState(self.game_engine))
    
    def register_state(self, state_name, state):
        """
        Register a new game state.
        
        Args:
            state_name: Unique identifier for the state
            state: Instance of a GameState subclass
        """
        if not isinstance(state, GameState):
            raise TypeError("State must be an instance of GameState")
        
        self.states[state_name] = state
    
    def change_state(self, state_name, **kwargs):
        """
        Change to a different state.
        
        Args:
            state_name: Name of the state to change to
            **kwargs: Optional parameters to pass to the new state
        """
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' not registered")
        
        # Exit current state if it exists
        if self.current_state:
            self.current_state.exit()
            
        # Clear UI elements when changing states
        if hasattr(self.game_engine, 'ui_manager') and self.game_engine.ui_manager:
            self.game_engine.ui_manager.clear_ui()
        
        # Enter new state
        self.current_state = self.states[state_name]
        self.current_state.enter(**kwargs)
    
    def push_state(self, state_name, **kwargs):
        """
        Push a new state onto the stack without exiting the current state.
        Useful for overlays like pause menus.
        
        Args:
            state_name: Name of the state to push
            **kwargs: Optional parameters to pass to the new state
        """
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' not registered")
        
        # Add current state to stack if it exists
        if self.current_state:
            self.state_stack.append(self.current_state)
            
        # Clear UI elements when changing states
        if hasattr(self.game_engine, 'ui_manager') and self.game_engine.ui_manager:
            self.game_engine.ui_manager.clear_ui()
        
        # Enter new state
        self.current_state = self.states[state_name]
        self.current_state.enter(**kwargs)
    
    def pop_state(self):
        """
        Pop the current state and return to the previous state on the stack.
        """
        if not self.state_stack:
            raise ValueError("No states to pop from stack")
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
            
        # Clear UI elements when changing states
        if hasattr(self.game_engine, 'ui_manager') and self.game_engine.ui_manager:
            self.game_engine.ui_manager.clear_ui()
        
        # Return to previous state
        self.current_state = self.state_stack.pop()
    
    def handle_events(self, events):
        """
        Process events for the current state.
        
        Args:
            events: List of pygame events to process
        """
        if self.current_state:
            self.current_state.handle_events(events)
    
    def update(self, dt):
        """
        Update the current state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        if self.current_state:
            self.current_state.update(dt)
            
            # Check for state transition
            if self.current_state.next_state:
                next_state_name, kwargs = self.current_state.next_state
                self.current_state.next_state = None
                self.change_state(next_state_name, **kwargs)
    
    def render(self, surface):
        """
        Render the current state.
        
        Args:
            surface: Pygame surface to render to
        """
        if self.current_state:
            self.current_state.render(surface)
    
    def start(self, initial_state="main_menu", **kwargs):
        """
        Start the scene manager with an initial state.
        
        Args:
            initial_state: Name of the initial state
            **kwargs: Optional parameters to pass to the initial state
        """
        print(f"Starting scene manager with initial state: {initial_state}")
        if initial_state not in self.states:
            print(f"Warning: State '{initial_state}' not found. Available states: {list(self.states.keys())}")
            # Fall back to main menu if available
            if "main_menu" in self.states:
                initial_state = "main_menu"
            else:
                # Just use the first available state
                initial_state = next(iter(self.states.keys()))
            print(f"Falling back to state: {initial_state}")
            
        self.change_state(initial_state, **kwargs)