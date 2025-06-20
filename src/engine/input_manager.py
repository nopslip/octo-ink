"""Input manager for processing player input events."""

import pygame
from typing import List, Dict, Optional, Set


class InputManager:
    """
    Manages input processing for the game.
    
    Processes pygame events and maintains the state of input devices.
    This class serves as a central point for handling all input-related
    functionality, including keyboard, mouse, and potentially gamepad input.
    """
    
    def __init__(self):
        """Initialize the input manager."""
        # Track pressed keys
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        
        # Track mouse state
        self.mouse_position = (0, 0)
        self.mouse_buttons_pressed: Set[int] = set()
        self.mouse_buttons_just_pressed: Set[int] = set()
        self.mouse_buttons_just_released: Set[int] = set()
        
        # Input mapping (can be customized)
        self.key_mapping = {
            "move_left": [pygame.K_LEFT, pygame.K_a],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "move_up": [pygame.K_UP, pygame.K_w],
            "move_down": [pygame.K_DOWN, pygame.K_s],
            "shoot": [pygame.K_SPACE],
            "pause": [pygame.K_ESCAPE, pygame.K_p]
        }
        
    def process_input(self, events: List[pygame.event.Event]) -> None:
        """
        Process input events from pygame.
        
        Args:
            events: List of pygame events to process
        """
        # Clear the "just" states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_buttons_just_pressed.clear()
        self.mouse_buttons_just_released.clear()
        
        # Update mouse position
        self.mouse_position = pygame.mouse.get_pos()
        
        # Process events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)
                self.keys_just_released.add(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons_pressed.add(event.button)
                self.mouse_buttons_just_pressed.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.mouse_buttons_pressed:
                    self.mouse_buttons_pressed.remove(event.button)
                self.mouse_buttons_just_released.add(event.button)
    
    def is_key_pressed(self, key: int) -> bool:
        """
        Check if a key is currently pressed.
        
        Args:
            key: Pygame key constant to check
            
        Returns:
            True if the key is currently pressed, False otherwise
        """
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """
        Check if a key was just pressed this frame.
        
        Args:
            key: Pygame key constant to check
            
        Returns:
            True if the key was just pressed, False otherwise
        """
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """
        Check if a key was just released this frame.
        
        Args:
            key: Pygame key constant to check
            
        Returns:
            True if the key was just released, False otherwise
        """
        return key in self.keys_just_released
    
    def is_action_pressed(self, action: str) -> bool:
        """
        Check if any key mapped to an action is currently pressed.
        
        Args:
            action: Action name to check
            
        Returns:
            True if any key mapped to the action is pressed, False otherwise
        """
        if action not in self.key_mapping:
            return False
            
        return any(self.is_key_pressed(key) for key in self.key_mapping[action])
    
    def is_action_just_pressed(self, action: str) -> bool:
        """
        Check if any key mapped to an action was just pressed this frame.
        
        Args:
            action: Action name to check
            
        Returns:
            True if any key mapped to the action was just pressed, False otherwise
        """
        if action not in self.key_mapping:
            return False
            
        return any(self.is_key_just_pressed(key) for key in self.key_mapping[action])
    
    def is_action_just_released(self, action: str) -> bool:
        """
        Check if any key mapped to an action was just released this frame.
        
        Args:
            action: Action name to check
            
        Returns:
            True if any key mapped to the action was just released, False otherwise
        """
        if action not in self.key_mapping:
            return False
            
        return any(self.is_key_just_released(key) for key in self.key_mapping[action])
    
    def get_mouse_position(self) -> tuple:
        """
        Get the current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return self.mouse_position
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        Check if a mouse button is currently pressed.
        
        Args:
            button: Mouse button to check (1=left, 2=middle, 3=right)
            
        Returns:
            True if the button is pressed, False otherwise
        """
        return button in self.mouse_buttons_pressed
    
    def is_mouse_button_just_pressed(self, button: int) -> bool:
        """
        Check if a mouse button was just pressed this frame.
        
        Args:
            button: Mouse button to check (1=left, 2=middle, 3=right)
            
        Returns:
            True if the button was just pressed, False otherwise
        """
        return button in self.mouse_buttons_just_pressed
    
    def is_mouse_button_just_released(self, button: int) -> bool:
        """
        Check if a mouse button was just released this frame.
        
        Args:
            button: Mouse button to check (1=left, 2=middle, 3=right)
            
        Returns:
            True if the button was just released, False otherwise
        """
        return button in self.mouse_buttons_just_released