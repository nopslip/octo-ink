"""Input Component for handling player input."""

import pygame
from src.components.component import Component


class InputComponent(Component):
    """Component that handles player input for controllable entities."""
    
    def __init__(self):
        """Initialize the InputComponent."""
        super().__init__("input")
        
        # Movement input
        self.move_left: bool = False
        self.move_right: bool = False
        self.move_up: bool = False
        self.move_down: bool = False
        
        # Action input
        self.shoot: bool = False
        self.shoot_pressed: bool = False  # For single shot detection
        self.was_shooting: bool = False  # Track previous shoot state
        
        # Arm rotation input (Alt key)
        self.rotate_arms: bool = False
        self.rotate_arms_pressed: bool = False  # For single press detection
        self.was_rotating: bool = False  # Track previous rotate state
        
        # Input sensitivity
        self.move_speed: float = 300.0  # pixels per second
        
    def update(self, dt: float) -> None:
        """Process input and update entity based on input state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.entity:
            return
            
        # Get keyboard state
        keys = pygame.key.get_pressed()
        
        # Update movement flags
        self.move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        self.move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        
        # Update shoot flag
        shoot_key = keys[pygame.K_SPACE]
        self.shoot_pressed = shoot_key and not self.shoot
        self.shoot = shoot_key
        
        # Update arm rotation flag (Alt key)
        rotate_key = keys[pygame.K_LALT] or keys[pygame.K_RALT]
        self.rotate_arms_pressed = rotate_key and not self.rotate_arms
        self.rotate_arms = rotate_key
        
        # Apply movement to physics component
        physics = self.entity.get_component("physics")
        if physics:
            # Calculate movement direction
            move_x = 0
            move_y = 0
            
            if self.move_left:
                move_x -= 1
            if self.move_right:
                move_x += 1
            if self.move_up:
                move_y -= 1
            if self.move_down:
                move_y += 1
                
            # Normalize diagonal movement
            if move_x != 0 and move_y != 0:
                move_x *= 0.707  # 1/sqrt(2)
                move_y *= 0.707
                
            # Apply movement
            physics.velocity.x = move_x * self.move_speed
            physics.velocity.y = move_y * self.move_speed
            
        # Handle shooting with continuous fire support
        weapon = self.entity.get_component("weapon")
        if weapon:
            # Start or stop continuous firing based on spacebar state
            if self.shoot and not self.was_shooting:
                # Just started pressing spacebar
                weapon.start_firing()
            elif not self.shoot and self.was_shooting:
                # Just released spacebar
                weapon.stop_firing()
            
            # Handle arm rotation on Alt key press (not hold)
            if self.rotate_arms_pressed:
                # Rotate arms to next position
                weapon.rotate_arms()
                
        # Update previous states
        self.was_shooting = self.shoot
        self.was_rotating = self.rotate_arms
        
    def set_move_speed(self, speed: float) -> None:
        """Set the movement speed.
        
        Args:
            speed: Movement speed in pixels per second
        """
        self.move_speed = max(0.0, speed)