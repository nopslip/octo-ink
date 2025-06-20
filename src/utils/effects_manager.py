"""
Visual effects system for the Octopus Ink Slime game.
Handles screen transitions, particle effects, camera shake, and flash effects.
"""

import random
import math
import pygame
from typing import Dict, List, Tuple, Optional, Callable, Any
from src.utils.asset_cache import AssetCache


class Particle:
    """
    Represents a single particle in a particle system.
    """
    
    def __init__(self, x: float, y: float, velocity: Tuple[float, float], 
                color: Tuple[int, int, int], size: float, lifetime: float,
                gravity: float = 0.0, damping: float = 1.0,
                image: Optional[pygame.Surface] = None):
        """
        Initialize a particle.
        
        Args:
            x: Initial x position
            y: Initial y position
            velocity: Initial velocity as (vx, vy)
            color: RGB color of the particle
            size: Size of the particle in pixels
            lifetime: How long the particle lives in seconds
            gravity: Gravity effect on the particle
            damping: Velocity damping factor (1.0 = no damping)
            image: Optional image to use instead of a circle
        """
        self.x = x
        self.y = y
        self.vx, self.vy = velocity
        self.color = color
        self.size = size
        self.initial_size = size
        self.lifetime = lifetime
        self.age = 0.0
        self.gravity = gravity
        self.damping = damping
        self.image = image
        self.rotation = 0.0
        self.rotation_speed = random.uniform(-5.0, 5.0)
        self.alpha = 255
        
    def update(self, dt: float) -> bool:
        """
        Update the particle state.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            True if the particle is still alive, False if it should be removed
        """
        # Update age
        self.age += dt
        if self.age >= self.lifetime:
            return False
            
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += self.gravity * dt
        
        # Apply damping
        self.vx *= self.damping
        self.vy *= self.damping
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update size (shrink as it ages)
        life_factor = 1.0 - (self.age / self.lifetime)
        self.size = self.initial_size * life_factor
        
        # Update alpha (fade out as it ages)
        self.alpha = int(255 * life_factor)
        
        return True
        
    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """
        Render the particle.
        
        Args:
            surface: Surface to render on
            camera_offset: Camera offset for rendering
        """
        # Calculate screen position
        screen_x = self.x - camera_offset[0]
        screen_y = self.y - camera_offset[1]
        
        if self.image:
            # Render image
            # Create a copy of the image with the current size
            scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.size), int(self.size))
            )
            
            # Rotate the image
            if self.rotation != 0:
                scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
                
            # Set alpha
            scaled_image.set_alpha(self.alpha)
            
            # Calculate position (center of the image)
            img_rect = scaled_image.get_rect()
            img_rect.center = (screen_x, screen_y)
            
            # Draw the image
            surface.blit(scaled_image, img_rect)
        else:
            # Render circle
            # Create a temporary surface for the circle with alpha
            circle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                circle_surface,
                (*self.color, self.alpha),
                (int(self.size), int(self.size)),
                int(self.size)
            )
            
            # Draw the circle surface
            surface.blit(
                circle_surface,
                (screen_x - self.size, screen_y - self.size)
            )


class ParticleSystem:
    """
    Manages a collection of particles for effects like explosions, smoke, etc.
    """
    
    def __init__(self, max_particles: int = 1000):
        """
        Initialize the particle system.
        
        Args:
            max_particles: Maximum number of particles allowed
        """
        self.particles: List[Particle] = []
        self.max_particles = max_particles
        self.asset_cache = AssetCache.get_instance()
        
    def update(self, dt: float):
        """
        Update all particles.
        
        Args:
            dt: Time delta in seconds
        """
        # Update particles and remove dead ones
        self.particles = [p for p in self.particles if p.update(dt)]
        
    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """
        Render all particles.
        
        Args:
            surface: Surface to render on
            camera_offset: Camera offset for rendering
        """
        for particle in self.particles:
            particle.render(surface, camera_offset)
            
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], 
                        count: int = 50, size: float = 5.0, speed: float = 200.0,
                        lifetime: float = 1.0, gravity: float = 100.0):
        """
        Create an explosion effect at the specified position.
        
        Args:
            x: X position of the explosion center
            y: Y position of the explosion center
            color: Base color of the particles
            count: Number of particles to create
            size: Size of the particles
            speed: Speed of the particles
            lifetime: Lifetime of the particles in seconds
            gravity: Gravity effect on the particles
        """
        # Limit to max particles
        count = min(count, self.max_particles - len(self.particles))
        
        # Create particles
        for _ in range(count):
            # Randomize color slightly
            r, g, b = color
            r = min(255, max(0, r + random.randint(-20, 20)))
            g = min(255, max(0, g + random.randint(-20, 20)))
            b = min(255, max(0, b + random.randint(-20, 20)))
            
            # Randomize velocity
            angle = random.uniform(0, 2 * math.pi)
            velocity = random.uniform(0.5, 1.0) * speed
            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity
            
            # Randomize size and lifetime
            particle_size = random.uniform(0.5, 1.5) * size
            particle_lifetime = random.uniform(0.8, 1.2) * lifetime
            
            # Create particle
            particle = Particle(
                x, y, 
                (vx, vy), 
                (r, g, b), 
                particle_size, 
                particle_lifetime,
                gravity,
                0.95  # Damping
            )
            
            self.particles.append(particle)
            
    def create_splash(self, x: float, y: float, color: Tuple[int, int, int], 
                     count: int = 30, size: float = 3.0, speed: float = 150.0,
                     lifetime: float = 0.8, gravity: float = 200.0):
        """
        Create a splash effect at the specified position.
        
        Args:
            x: X position of the splash center
            y: Y position of the splash center
            color: Base color of the particles
            count: Number of particles to create
            size: Size of the particles
            speed: Speed of the particles
            lifetime: Lifetime of the particles in seconds
            gravity: Gravity effect on the particles
        """
        # Limit to max particles
        count = min(count, self.max_particles - len(self.particles))
        
        # Create particles
        for _ in range(count):
            # Randomize color slightly
            r, g, b = color
            r = min(255, max(0, r + random.randint(-20, 20)))
            g = min(255, max(0, g + random.randint(-20, 20)))
            b = min(255, max(0, b + random.randint(-20, 20)))
            
            # Randomize velocity (mostly upward)
            angle = random.uniform(-math.pi * 0.8, -math.pi * 0.2)
            velocity = random.uniform(0.5, 1.0) * speed
            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity
            
            # Randomize size and lifetime
            particle_size = random.uniform(0.5, 1.5) * size
            particle_lifetime = random.uniform(0.8, 1.2) * lifetime
            
            # Create particle
            particle = Particle(
                x, y, 
                (vx, vy), 
                (r, g, b), 
                particle_size, 
                particle_lifetime,
                gravity,
                0.95  # Damping
            )
            
            self.particles.append(particle)
            
    def create_trail(self, x: float, y: float, color: Tuple[int, int, int], 
                    count: int = 5, size: float = 2.0, speed: float = 50.0,
                    lifetime: float = 0.5, direction: Tuple[float, float] = (0, 0)):
        """
        Create a trail effect at the specified position.
        
        Args:
            x: X position of the trail start
            y: Y position of the trail start
            color: Base color of the particles
            count: Number of particles to create
            size: Size of the particles
            speed: Speed of the particles
            lifetime: Lifetime of the particles in seconds
            direction: Direction vector for the trail
        """
        # Limit to max particles
        count = min(count, self.max_particles - len(self.particles))
        
        # Normalize direction
        dir_x, dir_y = direction
        length = math.sqrt(dir_x * dir_x + dir_y * dir_y)
        if length > 0:
            dir_x /= length
            dir_y /= length
        else:
            dir_x, dir_y = 0, -1  # Default to upward
            
        # Create particles
        for _ in range(count):
            # Randomize color slightly
            r, g, b = color
            r = min(255, max(0, r + random.randint(-10, 10)))
            g = min(255, max(0, g + random.randint(-10, 10)))
            b = min(255, max(0, b + random.randint(-10, 10)))
            
            # Randomize velocity (opposite to direction)
            angle = math.atan2(-dir_y, -dir_x) + random.uniform(-0.2, 0.2)
            velocity = random.uniform(0.5, 1.0) * speed
            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity
            
            # Randomize position slightly
            px = x + random.uniform(-5, 5)
            py = y + random.uniform(-5, 5)
            
            # Randomize size and lifetime
            particle_size = random.uniform(0.8, 1.2) * size
            particle_lifetime = random.uniform(0.8, 1.2) * lifetime
            
            # Create particle
            particle = Particle(
                px, py, 
                (vx, vy), 
                (r, g, b), 
                particle_size, 
                particle_lifetime,
                0.0,  # No gravity
                0.9   # Damping
            )
            
            self.particles.append(particle)
            
    def create_bubble_trail(self, x: float, y: float, count: int = 3, 
                           size: float = 3.0, speed: float = 30.0,
                           lifetime: float = 1.5):
        """
        Create bubbles rising from the specified position.
        
        Args:
            x: X position of the bubble start
            y: Y position of the bubble start
            count: Number of bubbles to create
            size: Size of the bubbles
            speed: Speed of the bubbles
            lifetime: Lifetime of the bubbles in seconds
        """
        # Limit to max particles
        count = min(count, self.max_particles - len(self.particles))
        
        # Create bubbles
        for _ in range(count):
            # Bubble color (light blue, semi-transparent)
            color = (200, 220, 255)
            
            # Randomize velocity (mostly upward with some wobble)
            vx = random.uniform(-10, 10)
            vy = -random.uniform(0.8, 1.2) * speed
            
            # Randomize position slightly
            px = x + random.uniform(-10, 10)
            py = y + random.uniform(-5, 5)
            
            # Randomize size and lifetime
            bubble_size = random.uniform(0.5, 1.5) * size
            bubble_lifetime = random.uniform(0.8, 1.2) * lifetime
            
            # Create bubble particle
            particle = Particle(
                px, py, 
                (vx, vy), 
                color, 
                bubble_size, 
                bubble_lifetime,
                -20.0,  # Negative gravity (buoyancy)
                0.98    # Slight damping
            )
            
            self.particles.append(particle)
            
    def clear(self):
        """Clear all particles."""
        self.particles.clear()


class ScreenTransition:
    """
    Handles screen transition effects between game states.
    """
    
    def __init__(self):
        """Initialize the screen transition system."""
        self.active = False
        self.progress = 0.0
        self.duration = 1.0
        self.transition_type = "fade"
        self.direction = "out"  # "in" or "out"
        self.color = (0, 0, 0)  # Black by default
        self.callback = None
        self.next_state = None
        
    def start(self, transition_type: str, direction: str, duration: float = 1.0, 
             color: Tuple[int, int, int] = (0, 0, 0), callback: Optional[Callable] = None,
             next_state: Optional[str] = None):
        """
        Start a screen transition.
        
        Args:
            transition_type: Type of transition ("fade", "wipe", "circle", "pixelate")
            direction: Direction of transition ("in" or "out")
            duration: Duration of the transition in seconds
            color: Color to use for the transition
            callback: Function to call when the transition completes
            next_state: Name of the next state to transition to (if any)
        """
        self.active = True
        self.progress = 0.0
        self.transition_type = transition_type
        self.direction = direction
        self.duration = max(0.1, duration)  # Minimum duration of 0.1 seconds
        self.color = color
        self.callback = callback
        self.next_state = next_state
        
    def update(self, dt: float) -> bool:
        """
        Update the transition progress.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            True if the transition is complete, False otherwise
        """
        if not self.active:
            return False
            
        # Update progress
        self.progress += dt / self.duration
        
        # Check if transition is complete
        if self.progress >= 1.0:
            self.progress = 1.0
            self.active = False
            
            # Call callback if provided
            if self.callback:
                self.callback()
                
            return True
            
        return False
        
    def render(self, surface: pygame.Surface):
        """
        Render the transition effect.
        
        Args:
            surface: Surface to render on
        """
        if not self.active and self.progress == 0.0:
            return
            
        # Get surface dimensions
        width, height = surface.get_size()
        
        # Calculate alpha based on direction
        if self.direction == "in":
            # Fade in: 255 -> 0
            alpha = int(255 * (1.0 - self.progress))
        else:
            # Fade out: 0 -> 255
            alpha = int(255 * self.progress)
            
        if self.transition_type == "fade":
            # Create overlay surface with alpha
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.color, alpha))
            surface.blit(overlay, (0, 0))
            
        elif self.transition_type == "wipe":
            # Wipe effect (horizontal)
            overlay = pygame.Surface((width, height))
            overlay.fill(self.color)
            
            if self.direction == "in":
                # Wipe in: right to left
                wipe_width = int(width * (1.0 - self.progress))
                surface.blit(overlay, (0, 0), (0, 0, wipe_width, height))
            else:
                # Wipe out: left to right
                wipe_width = int(width * self.progress)
                surface.blit(overlay, (0, 0), (0, 0, wipe_width, height))
                
        elif self.transition_type == "circle":
            # Circle effect
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.color, alpha))
            
            # Calculate circle radius
            if self.direction == "in":
                # Circle closing in
                radius = int(math.sqrt(width*width + height*height) * (1.0 - self.progress))
            else:
                # Circle expanding
                radius = int(math.sqrt(width*width + height*height) * self.progress)
                
            # Draw circle
            pygame.draw.circle(
                overlay, 
                (0, 0, 0, 0),  # Transparent
                (width // 2, height // 2), 
                radius
            )
            
            surface.blit(overlay, (0, 0))
            
        elif self.transition_type == "pixelate":
            # Pixelate effect (simplified)
            # This is a simple implementation that gets progressively blockier
            pixel_size = int(max(1, 20 * self.progress)) if self.direction == "out" else int(max(1, 20 * (1.0 - self.progress)))
            
            if pixel_size > 1:
                # Create a smaller surface
                small_width = max(1, width // pixel_size)
                small_height = max(1, height // pixel_size)
                small_surface = pygame.Surface((small_width, small_height))
                
                # Copy the screen to the smaller surface
                pygame.transform.scale(surface, (small_width, small_height), small_surface)
                
                # Scale back up to the screen size
                pygame.transform.scale(small_surface, (width, height), surface)


class CameraShake:
    """
    Handles camera shake effects for impacts and explosions.
    """
    
    def __init__(self):
        """Initialize the camera shake system."""
        self.active = False
        self.duration = 0.0
        self.intensity = 0.0
        self.timer = 0.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.trauma = 0.0  # Trauma-based shake (0.0 to 1.0)
        self.trauma_decay = 2.0  # How quickly trauma decays
        
    def add_trauma(self, amount: float):
        """
        Add trauma to the camera shake system.
        
        Args:
            amount: Amount of trauma to add (0.0 to 1.0)
        """
        self.trauma = min(1.0, self.trauma + amount)
        self.active = self.trauma > 0.0
        
    def start(self, duration: float, intensity: float):
        """
        Start a camera shake effect.
        
        Args:
            duration: Duration of the shake in seconds
            intensity: Intensity of the shake in pixels
        """
        self.active = True
        self.duration = max(0.1, duration)  # Minimum duration of 0.1 seconds
        self.intensity = max(1.0, intensity)  # Minimum intensity of 1.0 pixels
        self.timer = 0.0
        
    def update(self, dt: float) -> Tuple[float, float]:
        """
        Update the camera shake effect.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            Tuple of (offset_x, offset_y) to apply to the camera
        """
        # Reset offsets
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # Update trauma-based shake
        if self.trauma > 0.0:
            # Decay trauma over time
            self.trauma = max(0.0, self.trauma - self.trauma_decay * dt)
            
            # Calculate shake amount based on trauma
            shake_amount = self.trauma * self.trauma  # Square for more responsive shake
            
            # Generate perlin-like noise for smoother shake
            time_scale = 10.0
            self.offset_x = shake_amount * 20.0 * (
                math.sin(self.timer * time_scale) + 
                0.5 * math.sin(self.timer * time_scale * 2.3)
            )
            self.offset_y = shake_amount * 20.0 * (
                math.cos(self.timer * time_scale * 0.9) + 
                0.5 * math.cos(self.timer * time_scale * 2.1)
            )
            
            # Update timer
            self.timer += dt
            
            # Check if trauma is effectively zero
            if self.trauma < 0.01:
                self.trauma = 0.0
                self.active = False
                
        # Update timed shake
        elif self.active:
            # Update timer
            self.timer += dt
            
            # Check if shake is complete
            if self.timer >= self.duration:
                self.active = False
                return (0.0, 0.0)
                
            # Calculate shake progress
            progress = self.timer / self.duration
            
            # Calculate shake intensity (decreases over time)
            current_intensity = self.intensity * (1.0 - progress)
            
            # Calculate random offsets
            self.offset_x = random.uniform(-1.0, 1.0) * current_intensity
            self.offset_y = random.uniform(-1.0, 1.0) * current_intensity
            
        return (self.offset_x, self.offset_y)


class FlashEffect:
    """
    Handles flash effects for impacts and collisions.
    """
    
    def __init__(self):
        """Initialize the flash effect system."""
        self.active = False
        self.duration = 0.0
        self.color = (255, 255, 255)  # White by default
        self.timer = 0.0
        self.alpha = 0
        
    def start(self, duration: float, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Start a flash effect.
        
        Args:
            duration: Duration of the flash in seconds
            color: Color of the flash
        """
        self.active = True
        self.duration = max(0.05, duration)  # Minimum duration of 0.05 seconds
        self.color = color
        self.timer = 0.0
        self.alpha = 255
        
    def update(self, dt: float) -> bool:
        """
        Update the flash effect.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            True if the flash is active, False otherwise
        """
        if not self.active:
            return False
            
        # Update timer
        self.timer += dt
        
        # Check if flash is complete
        if self.timer >= self.duration:
            self.active = False
            self.alpha = 0
            return False
            
        # Calculate alpha (fades out over time)
        self.alpha = int(255 * (1.0 - (self.timer / self.duration)))
        
        return True
        
    def render(self, surface: pygame.Surface):
        """
        Render the flash effect.
        
        Args:
            surface: Surface to render on
        """
        if not self.active or self.alpha <= 0:
            return
            
        # Create overlay surface with alpha
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*self.color, self.alpha))
        
        # Blit overlay to surface
        surface.blit(overlay, (0, 0))


class EffectsManager:
    """
    Manages all visual effects for the game.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """Get the singleton instance of the EffectsManager."""
        if EffectsManager._instance is None:
            EffectsManager._instance = EffectsManager()
        return EffectsManager._instance
    
    def __init__(self):
        """Initialize the effects manager."""
        self.particle_system = ParticleSystem()
        self.screen_transition = ScreenTransition()
        self.camera_shake = CameraShake()
        self.flash_effect = FlashEffect()
        
    def update(self, dt: float):
        """
        Update all effects.
        
        Args:
            dt: Time delta in seconds
        """
        # Update particle system
        self.particle_system.update(dt)
        
        # Update screen transition
        self.screen_transition.update(dt)
        
        # Update camera shake
        self.camera_shake.update(dt)
        
        # Update flash effect
        self.flash_effect.update(dt)
        
    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """
        Render all effects.
        
        Args:
            surface: Surface to render on
            camera_offset: Camera offset for rendering
        """
        # Render particles
        self.particle_system.render(surface, camera_offset)
        
        # Render flash effect
        self.flash_effect.render(surface)
        
        # Render screen transition (always on top)
        self.screen_transition.render(surface)
        
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int] = (255, 100, 50),
                        size: str = "medium", shake: bool = True, flash: bool = True):
        """
        Create an explosion effect at the specified position.
        
        Args:
            x: X position of the explosion center
            y: Y position of the explosion center
            color: Base color of the particles
            size: Size of the explosion ("small", "medium", "large")
            shake: Whether to add camera shake
            flash: Whether to add a flash effect
        """
        # Determine explosion parameters based on size
        if size == "small":
            particle_count = 30
            particle_size = 3.0
            particle_speed = 150.0
            particle_lifetime = 0.8
            shake_intensity = 5.0
            shake_duration = 0.2
            flash_duration = 0.1
        elif size == "large":
            particle_count = 100
            particle_size = 8.0
            particle_speed = 300.0
            particle_lifetime = 1.5
            shake_intensity = 15.0
            shake_duration = 0.5
            flash_duration = 0.2
        else:  # medium
            particle_count = 50
            particle_size = 5.0
            particle_speed = 200.0
            particle_lifetime = 1.0
            shake_intensity = 10.0
            shake_duration = 0.3
            flash_duration = 0.15
            
        # Create particles
        self.particle_system.create_explosion(
            x, y, color, 
            particle_count, 
            particle_size, 
            particle_speed, 
            particle_lifetime
        )
        
        # Add camera shake
        if shake:
            self.camera_shake.add_trauma(shake_duration)
            
        # Add flash effect
        if flash:
            flash_color = (color[0], color[1], color[2])
            self.flash_effect.start(flash_duration, flash_color)
            
    def create_splash(self, x: float, y: float, color: Tuple[int, int, int] = (50, 100, 255),
                     size: str = "medium"):
        """
        Create a splash effect at the specified position.
        
        Args:
            x: X position of the splash center
            y: Y position of the splash center
            color: Base color of the particles
            size: Size of the splash ("small", "medium", "large")
        """
        # Determine splash parameters based on size
        if size == "small":
            particle_count = 20
            particle_size = 2.0
            particle_speed = 100.0
            particle_lifetime = 0.6
        elif size == "large":
            particle_count = 50
            particle_size = 5.0
            particle_speed = 200.0
            particle_lifetime = 1.0
        else:  # medium
            particle_count = 30
            particle_size = 3.0
            particle_speed = 150.0
            particle_lifetime = 0.8
            
        # Create particles
        self.particle_system.create_splash(
            x, y, color, 
            particle_count, 
            particle_size, 
            particle_speed, 
            particle_lifetime
        )
        
    def create_player_movement_trail(self, x: float, y: float, direction: Tuple[float, float],
                                    color: Tuple[int, int, int] = (50, 150, 255)):
        """
        Create a trail effect for player movement.
        
        Args:
            x: X position of the trail start
            y: Y position of the trail start
            direction: Direction vector for the trail
            color: Base color of the particles
        """
        # Create trail particles
        self.particle_system.create_trail(
            x, y, color, 
            count=3, 
            size=2.0, 
            speed=30.0, 
            lifetime=0.4,
            direction=direction
        )
        
        # Create bubble trail
        self.particle_system.create_bubble_trail(
            x, y, 
            count=1, 
            size=2.0, 
            speed=20.0, 
            lifetime=1.0
        )
        
    def start_screen_transition(self, transition_type: str, direction: str, duration: float = 1.0,
                              color: Tuple[int, int, int] = (0, 0, 0),
                              callback: Optional[Callable] = None,
                              next_state: Optional[str] = None):
        """
        Start a screen transition.
        
        Args:
            transition_type: Type of transition ("fade", "wipe", "circle", "pixelate")
            direction: Direction of transition ("in" or "out")
            duration: Duration of the transition in seconds
            color: Color to use for the transition
            callback: Function to call when the transition completes
            next_state: Name of the next state to transition to (if any)
        """
        self.screen_transition.start(
            transition_type,
            direction,
            duration,
            color,
            callback,
            next_state
        )
        
    def add_camera_shake(self, amount: float):
        """
        Add trauma to the camera shake system.
        
        Args:
            amount: Amount of trauma to add (0.0 to 1.0)
        """
        self.camera_shake.add_trauma(amount)
        
    def start_camera_shake(self, duration: float, intensity: float):
        """
        Start a camera shake effect.
        
        Args:
            duration: Duration of the shake in seconds
            intensity: Intensity of the shake in pixels
        """
        self.camera_shake.start(duration, intensity)
        
    def start_flash(self, duration: float, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Start a flash effect.
        
        Args:
            duration: Duration of the flash in seconds
            color: Color of the flash
        """
        self.flash_effect.start(duration, color)
        
    def get_camera_offset(self) -> Tuple[float, float]:
        """
        Get the current camera offset from shake effects.
        
        Returns:
            Tuple of (offset_x, offset_y)
        """
        return (self.camera_shake.offset_x, self.camera_shake.offset_y)
        
    def clear_particles(self):
        """Clear all particles."""
        self.particle_system.clear()
        
    def is_transition_active(self) -> bool:
        """
        Check if a screen transition is currently active.
        
        Returns:
            True if a transition is active, False otherwise
        """
        return self.screen_transition.active