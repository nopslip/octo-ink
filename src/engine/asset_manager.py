"""Asset manager for loading and managing game assets."""

import os
import pygame
from typing import Dict, Optional, Tuple


class AssetManager:
    """
    Manages loading and caching of game assets.
    
    Handles loading and storing images, sounds, fonts, and other assets
    to avoid redundant loading and improve performance.
    """
    
    def __init__(self):
        """Initialize the asset manager."""
        # Asset storage
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, Dict[int, pygame.font.Font]] = {}
        self.animations: Dict[str, Dict[str, list]] = {}
        
        # Base paths
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        self.image_path = os.path.join(self.base_path, "images")
        self.sound_path = os.path.join(self.base_path, "sounds")
        self.font_path = os.path.join(self.base_path, "fonts")
        
        # Ensure asset directories exist
        os.makedirs(self.image_path, exist_ok=True)
        os.makedirs(self.sound_path, exist_ok=True)
        os.makedirs(self.font_path, exist_ok=True)
        
    def load_image(self, name: str, file_path: Optional[str] = None, 
                  colorkey: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
        """
        Load an image asset.
        
        Args:
            name: Identifier for the image
            file_path: Path to the image file (relative to assets/images/)
                       If None, uses name as the file path
            colorkey: Color to use as transparency (if any)
            
        Returns:
            Loaded image surface
        """
        # Check if already loaded
        if name in self.images:
            return self.images[name]
            
        # Determine file path
        if file_path is None:
            file_path = name
            
        # Ensure file has extension
        if not any(file_path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']):
            file_path += '.png'  # Default to PNG
            
        # Load the image
        full_path = os.path.join(self.image_path, file_path)
        try:
            image = pygame.image.load(full_path).convert_alpha()
            
            # Apply colorkey if specified
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
                
            # Store and return
            self.images[name] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {full_path}: {e}")
            # Return a placeholder image (small purple square)
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Purple
            self.images[name] = placeholder
            return placeholder
            
    def load_sound(self, name: str, file_path: Optional[str] = None) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound asset.
        
        Args:
            name: Identifier for the sound
            file_path: Path to the sound file (relative to assets/sounds/)
                       If None, uses name as the file path
                       
        Returns:
            Loaded sound object or None if loading failed
        """
        # Check if already loaded
        if name in self.sounds:
            return self.sounds[name]
            
        # Determine file path
        if file_path is None:
            file_path = name
            
        # Ensure file has extension
        if not any(file_path.endswith(ext) for ext in ['.wav', '.ogg', '.mp3']):
            file_path += '.wav'  # Default to WAV
            
        # Load the sound
        full_path = os.path.join(self.sound_path, file_path)
        try:
            sound = pygame.mixer.Sound(full_path)
            self.sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {full_path}: {e}")
            return None
            
    def load_font(self, name: str, size: int, file_path: Optional[str] = None) -> pygame.font.Font:
        """
        Load a font asset.
        
        Args:
            name: Identifier for the font
            size: Font size in points
            file_path: Path to the font file (relative to assets/fonts/)
                       If None, uses name as the file path
                       
        Returns:
            Loaded font object
        """
        # Check if already loaded at this size
        if name in self.fonts and size in self.fonts[name]:
            return self.fonts[name][size]
            
        # Initialize font dict if needed
        if name not in self.fonts:
            self.fonts[name] = {}
            
        # Determine file path
        if file_path is None:
            file_path = name
            
        # Ensure file has extension
        if not any(file_path.endswith(ext) for ext in ['.ttf', '.otf']):
            file_path += '.ttf'  # Default to TTF
            
        # Load the font
        full_path = os.path.join(self.font_path, file_path)
        try:
            # Try to load custom font
            font = pygame.font.Font(full_path, size)
        except pygame.error as e:
            print(f"Error loading font {full_path}: {e}")
            # Fall back to default font
            font = pygame.font.Font(None, size)
            
        # Store and return
        self.fonts[name][size] = font
        return font
        
    def load_animation(self, name: str, sprite_sheet: str, frame_width: int, 
                      frame_height: int, frame_count: int, colorkey: Optional[Tuple[int, int, int]] = None) -> list:
        """
        Load an animation from a sprite sheet.
        
        Args:
            name: Identifier for the animation
            sprite_sheet: Name of the sprite sheet image
            frame_width: Width of each frame in pixels
            frame_height: Height of each frame in pixels
            frame_count: Number of frames in the animation
            colorkey: Color to use as transparency (if any)
            
        Returns:
            List of animation frames (surfaces)
        """
        # Check if already loaded
        if name in self.animations:
            return self.animations[name]
            
        # Load the sprite sheet
        sheet = self.load_image(sprite_sheet, colorkey=colorkey)
        
        # Extract frames
        frames = []
        for i in range(frame_count):
            x = i * frame_width
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, 0, frame_width, frame_height))
            frames.append(frame)
            
        # Store and return
        self.animations[name] = frames
        return frames
        
    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """
        Get a previously loaded image.
        
        Args:
            name: Identifier for the image
            
        Returns:
            Image surface or None if not found
        """
        return self.images.get(name)
        
    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """
        Get a previously loaded sound.
        
        Args:
            name: Identifier for the sound
            
        Returns:
            Sound object or None if not found
        """
        return self.sounds.get(name)
        
    def get_font(self, name: str, size: int) -> Optional[pygame.font.Font]:
        """
        Get a previously loaded font.
        
        Args:
            name: Identifier for the font
            size: Font size in points
            
        Returns:
            Font object or None if not found
        """
        if name in self.fonts and size in self.fonts[name]:
            return self.fonts[name][size]
        return None
        
    def get_animation(self, name: str) -> Optional[list]:
        """
        Get a previously loaded animation.
        
        Args:
            name: Identifier for the animation
            
        Returns:
            List of animation frames or None if not found
        """
        return self.animations.get(name)
        
    def preload_assets(self) -> None:
        """Preload commonly used assets to avoid loading delays during gameplay."""
        # Preload player images
        self.load_image("octopus", "player/octopus.png")
        
        # Preload enemy images
        self.load_image("ship_small", "enemies/ship_small.png")
        self.load_image("ship_medium", "enemies/ship_medium.png")
        self.load_image("ship_large", "enemies/ship_large.png")
        self.load_image("captain", "enemies/captain.png")
        self.load_image("turtle", "enemies/turtle.png")
        self.load_image("fish", "enemies/fish.png")
        
        # Preload projectile images
        self.load_image("ink_blue", "projectiles/ink_blue.png")
        self.load_image("ink_purple", "projectiles/ink_purple.png")
        self.load_image("ink_green", "projectiles/ink_green.png")
        self.load_image("ink_red", "projectiles/ink_red.png")
        self.load_image("ink_rainbow", "projectiles/ink_rainbow.png")
        
        # Preload sound effects
        self.load_sound("shoot", "effects/shoot.wav")
        self.load_sound("hit", "effects/hit.wav")
        self.load_sound("sink", "effects/sink.wav")
        
        # Preload fonts
        self.load_font("main", 24)
        self.load_font("title", 48)