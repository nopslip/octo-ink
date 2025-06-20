"""
Asset caching system for efficient resource management.
This system ensures assets are loaded only once and reused throughout the game.
"""

import os
import pygame
from typing import Dict, Any, Optional, Tuple, List, Union


class AssetCache:
    """
    Asset caching system for efficient resource management.
    
    This class provides a centralized cache for game assets such as images,
    sounds, fonts, and animations. It ensures that assets are loaded only once
    and reused throughout the game, improving performance and reducing memory usage.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """Get the singleton instance of the AssetCache."""
        if AssetCache._instance is None:
            AssetCache._instance = AssetCache()
        return AssetCache._instance
    
    def __init__(self):
        """Initialize the asset cache."""
        # Image cache: filename -> Surface
        self.images: Dict[str, pygame.Surface] = {}
        
        # Sound cache: filename -> Sound
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        # Font cache: (filename, size) -> Font
        self.fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        
        # Animation cache: filename -> List[Surface]
        self.animations: Dict[str, List[pygame.Surface]] = {}
        
        # Sprite sheet cache: filename -> Dict[str, Surface]
        self.sprite_sheets: Dict[str, Dict[str, pygame.Surface]] = {}
        
        # Base paths for asset types
        self.base_paths = {
            "images": "assets/images",
            "sounds": "assets/sounds",
            "fonts": "assets/fonts",
            "animations": "assets/animations",
            "sprite_sheets": "assets/sprite_sheets"
        }
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        
    def get_image(self, filename: str, colorkey: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
        """
        Get an image from the cache, loading it if necessary.
        
        Args:
            filename: Path to the image file (relative to the images directory)
            colorkey: Color to use as transparency (optional)
            
        Returns:
            The loaded image as a pygame Surface
        """
        # Check if the image is already in the cache
        if filename in self.images:
            self.cache_hits += 1
            return self.images[filename]
            
        # Image not in cache, load it
        self.cache_misses += 1
        
        # Construct full path
        full_path = os.path.join(self.base_paths["images"], filename)
        
        try:
            # Load the image
            image = pygame.image.load(full_path).convert_alpha()
            
            # Apply colorkey if specified
            if colorkey is not None:
                image.set_colorkey(colorkey)
                
            # Add to cache
            self.images[filename] = image
            
            return image
        except pygame.error as e:
            print(f"Error loading image {full_path}: {e}")
            
            # Return a placeholder image
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            return placeholder
            
    def get_sound(self, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        Get a sound from the cache, loading it if necessary.
        
        Args:
            filename: Path to the sound file (relative to the sounds directory)
            
        Returns:
            The loaded sound, or None if loading failed
        """
        # Check if the sound is already in the cache
        if filename in self.sounds:
            self.cache_hits += 1
            return self.sounds[filename]
            
        # Sound not in cache, load it
        self.cache_misses += 1
        
        # Construct full path
        full_path = os.path.join(self.base_paths["sounds"], filename)
        
        try:
            # Load the sound
            sound = pygame.mixer.Sound(full_path)
            
            # Add to cache
            self.sounds[filename] = sound
            
            return sound
        except pygame.error as e:
            print(f"Error loading sound {full_path}: {e}")
            return None
            
    def get_font(self, filename: str, size: int) -> pygame.font.Font:
        """
        Get a font from the cache, loading it if necessary.
        
        Args:
            filename: Path to the font file (relative to the fonts directory),
                     or None to use the default font
            size: Font size in points
            
        Returns:
            The loaded font
        """
        # Create cache key
        cache_key = (filename, size)
        
        # Check if the font is already in the cache
        if cache_key in self.fonts:
            self.cache_hits += 1
            return self.fonts[cache_key]
            
        # Font not in cache, load it
        self.cache_misses += 1
        
        try:
            # Load the font
            if filename is None:
                # Use default font
                font = pygame.font.Font(None, size)
            else:
                # Construct full path
                full_path = os.path.join(self.base_paths["fonts"], filename)
                font = pygame.font.Font(full_path, size)
                
            # Add to cache
            self.fonts[cache_key] = font
            
            return font
        except pygame.error as e:
            print(f"Error loading font {filename} (size {size}): {e}")
            
            # Return default font as fallback
            default_font = pygame.font.Font(None, size)
            self.fonts[cache_key] = default_font
            return default_font
            
    def get_animation_frames(self, filename: str, frame_count: int, 
                            frame_width: Optional[int] = None, 
                            colorkey: Optional[Tuple[int, int, int]] = None) -> List[pygame.Surface]:
        """
        Get animation frames from the cache, loading them if necessary.
        
        Args:
            filename: Path to the animation sprite sheet (relative to the animations directory)
            frame_count: Number of frames in the animation
            frame_width: Width of each frame (if None, calculated from image width / frame_count)
            colorkey: Color to use as transparency (optional)
            
        Returns:
            List of animation frames as pygame Surfaces
        """
        # Create cache key
        cache_key = f"{filename}_{frame_count}"
        
        # Check if the animation is already in the cache
        if cache_key in self.animations:
            self.cache_hits += 1
            return self.animations[cache_key]
            
        # Animation not in cache, load it
        self.cache_misses += 1
        
        # Construct full path
        full_path = os.path.join(self.base_paths["animations"], filename)
        
        try:
            # Load the sprite sheet
            sprite_sheet = pygame.image.load(full_path).convert_alpha()
            
            # Apply colorkey if specified
            if colorkey is not None:
                sprite_sheet.set_colorkey(colorkey)
                
            # Calculate frame dimensions
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()
            
            if frame_width is None:
                frame_width = sheet_width // frame_count
                
            frame_height = sheet_height
            
            # Extract frames
            frames = []
            for i in range(frame_count):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), 
                          (i * frame_width, 0, frame_width, frame_height))
                frames.append(frame)
                
            # Add to cache
            self.animations[cache_key] = frames
            
            return frames
        except pygame.error as e:
            print(f"Error loading animation {full_path}: {e}")
            
            # Return placeholder frames
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            return [placeholder] * frame_count
            
    def get_sprite_sheet(self, filename: str, sprite_map: Dict[str, Tuple[int, int, int, int]],
                        colorkey: Optional[Tuple[int, int, int]] = None) -> Dict[str, pygame.Surface]:
        """
        Get sprites from a sprite sheet, loading them if necessary.
        
        Args:
            filename: Path to the sprite sheet (relative to the sprite_sheets directory)
            sprite_map: Dictionary mapping sprite names to their rectangles (x, y, width, height)
            colorkey: Color to use as transparency (optional)
            
        Returns:
            Dictionary mapping sprite names to their pygame Surfaces
        """
        # Check if the sprite sheet is already in the cache
        if filename in self.sprite_sheets:
            self.cache_hits += 1
            return self.sprite_sheets[filename]
            
        # Sprite sheet not in cache, load it
        self.cache_misses += 1
        
        # Construct full path
        full_path = os.path.join(self.base_paths["sprite_sheets"], filename)
        
        try:
            # Load the sprite sheet
            sheet = pygame.image.load(full_path).convert_alpha()
            
            # Apply colorkey if specified
            if colorkey is not None:
                sheet.set_colorkey(colorkey)
                
            # Extract sprites
            sprites = {}
            for name, rect in sprite_map.items():
                x, y, width, height = rect
                sprite = pygame.Surface((width, height), pygame.SRCALPHA)
                sprite.blit(sheet, (0, 0), (x, y, width, height))
                sprites[name] = sprite
                
            # Add to cache
            self.sprite_sheets[filename] = sprites
            
            return sprites
        except pygame.error as e:
            print(f"Error loading sprite sheet {full_path}: {e}")
            
            # Return empty dictionary
            return {}
            
    def preload_assets(self, asset_list: Dict[str, List[str]]):
        """
        Preload a list of assets to ensure they're in the cache.
        
        Args:
            asset_list: Dictionary mapping asset types to lists of filenames
        """
        # Preload images
        if "images" in asset_list:
            for filename in asset_list["images"]:
                self.get_image(filename)
                
        # Preload sounds
        if "sounds" in asset_list:
            for filename in asset_list["sounds"]:
                self.get_sound(filename)
                
        # Preload fonts
        if "fonts" in asset_list:
            for font_info in asset_list["fonts"]:
                if isinstance(font_info, tuple) and len(font_info) == 2:
                    filename, size = font_info
                    self.get_font(filename, size)
                    
        # Preload animations
        if "animations" in asset_list:
            for anim_info in asset_list["animations"]:
                if isinstance(anim_info, tuple) and len(anim_info) >= 2:
                    filename, frame_count = anim_info[:2]
                    frame_width = anim_info[2] if len(anim_info) > 2 else None
                    self.get_animation_frames(filename, frame_count, frame_width)
                    
    def clear_cache(self, asset_type: Optional[str] = None):
        """
        Clear the asset cache.
        
        Args:
            asset_type: Type of assets to clear ("images", "sounds", "fonts", "animations", "sprite_sheets"),
                       or None to clear all
        """
        if asset_type is None or asset_type == "images":
            self.images.clear()
            
        if asset_type is None or asset_type == "sounds":
            self.sounds.clear()
            
        if asset_type is None or asset_type == "fonts":
            self.fonts.clear()
            
        if asset_type is None or asset_type == "animations":
            self.animations.clear()
            
        if asset_type is None or asset_type == "sprite_sheets":
            self.sprite_sheets.clear()
            
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the asset cache.
        
        Returns:
            Dictionary with cache statistics
        """
        total_hits_misses = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_hits_misses) if total_hits_misses > 0 else 0
        
        return {
            "images": len(self.images),
            "sounds": len(self.sounds),
            "fonts": len(self.fonts),
            "animations": len(self.animations),
            "sprite_sheets": len(self.sprite_sheets),
            "total_assets": (
                len(self.images) + 
                len(self.sounds) + 
                len(self.fonts) + 
                len(self.animations) + 
                len(self.sprite_sheets)
            ),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate
        }