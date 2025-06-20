"""
Audio Manager for the Octopus Ink Slime game.
Handles loading and playing sound effects and music.
"""

import pygame
import os
from typing import Dict, List, Optional, Tuple


class AudioManager:
    """Manages sound effects and background music for the game."""
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """
        Get the singleton instance of the AudioManager.
        
        Returns:
            The AudioManager instance
        """
        if AudioManager._instance is None:
            AudioManager._instance = AudioManager()
        return AudioManager._instance
    
    def __init__(self):
        """Initialize the audio manager."""
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Sound effects dictionary
        self.sound_effects: Dict[str, pygame.mixer.Sound] = {}
        
        # Music tracks dictionary
        self.music_tracks: Dict[str, str] = {}
        
        # Volume settings
        self.sound_volume = 0.7
        self.music_volume = 0.5
        
        # Current music track
        self.current_music = None
        
        # Sound categories for group volume control
        self.sound_categories: Dict[str, List[str]] = {
            "player": [],
            "enemy": [],
            "ui": [],
            "environment": []
        }
        
        # Category volume multipliers
        self.category_volumes: Dict[str, float] = {
            "player": 1.0,
            "enemy": 1.0,
            "ui": 1.0,
            "environment": 1.0
        }
        
        # Mute state
        self.muted = False
        self.previous_volumes = (self.sound_volume, self.music_volume)
    
    def load_sound(self, sound_id: str, file_path: str, category: str = None) -> bool:
        """
        Load a sound effect.
        
        Args:
            sound_id: Unique identifier for the sound
            file_path: Path to the sound file
            category: Optional category for group volume control
            
        Returns:
            True if the sound was loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                print(f"Warning: Sound file not found: {file_path}")
                return False
                
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(self.sound_volume)
            self.sound_effects[sound_id] = sound
            
            # Add to category if specified
            if category and category in self.sound_categories:
                self.sound_categories[category].append(sound_id)
                
            return True
        except Exception as e:
            print(f"Error loading sound {sound_id} from {file_path}: {e}")
            return False
    
    def load_music(self, music_id: str, file_path: str) -> bool:
        """
        Register a music track.
        
        Args:
            music_id: Unique identifier for the music track
            file_path: Path to the music file
            
        Returns:
            True if the music was registered successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                print(f"Warning: Music file not found: {file_path}")
                return False
                
            self.music_tracks[music_id] = file_path
            return True
        except Exception as e:
            print(f"Error registering music {music_id} from {file_path}: {e}")
            return False
    
    def play_sound(self, sound_id: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> bool:
        """
        Play a sound effect.
        
        Args:
            sound_id: ID of the sound to play
            loops: Number of times to repeat the sound (-1 for infinite)
            maxtime: Maximum play time in milliseconds
            fade_ms: Fade-in time in milliseconds
            
        Returns:
            True if the sound was played successfully, False otherwise
        """
        if self.muted:
            return False
            
        if sound_id not in self.sound_effects:
            print(f"Warning: Sound {sound_id} not loaded")
            return False
            
        try:
            # Get the sound and play it
            sound = self.sound_effects[sound_id]
            
            # Calculate effective volume based on category
            effective_volume = self.sound_volume
            for category, sounds in self.sound_categories.items():
                if sound_id in sounds:
                    effective_volume *= self.category_volumes[category]
                    break
            
            sound.set_volume(effective_volume)
            sound.play(loops, maxtime, fade_ms)
            return True
        except Exception as e:
            print(f"Error playing sound {sound_id}: {e}")
            return False
    
    def stop_sound(self, sound_id: str) -> bool:
        """
        Stop a playing sound effect.
        
        Args:
            sound_id: ID of the sound to stop
            
        Returns:
            True if the sound was stopped successfully, False otherwise
        """
        if sound_id not in self.sound_effects:
            return False
            
        try:
            self.sound_effects[sound_id].stop()
            return True
        except Exception as e:
            print(f"Error stopping sound {sound_id}: {e}")
            return False
    
    def play_music(self, music_id: str, loops: int = -1, fade_ms: int = 1000) -> bool:
        """
        Play a music track.
        
        Args:
            music_id: ID of the music track to play
            loops: Number of times to repeat the music (-1 for infinite)
            fade_ms: Fade-in time in milliseconds
            
        Returns:
            True if the music was played successfully, False otherwise
        """
        if self.muted:
            return False
            
        if music_id not in self.music_tracks:
            print(f"Warning: Music track {music_id} not loaded")
            return False
            
        try:
            # Stop any currently playing music
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fade_ms)
            
            # Load and play the new music
            pygame.mixer.music.load(self.music_tracks[music_id])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            
            self.current_music = music_id
            return True
        except Exception as e:
            print(f"Error playing music {music_id}: {e}")
            return False
    
    def stop_music(self, fade_ms: int = 1000) -> bool:
        """
        Stop the currently playing music.
        
        Args:
            fade_ms: Fade-out time in milliseconds
            
        Returns:
            True if the music was stopped successfully, False otherwise
        """
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fade_ms)
                self.current_music = None
            return True
        except Exception as e:
            print(f"Error stopping music: {e}")
            return False
    
    def pause_music(self):
        """Pause the currently playing music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the currently paused music."""
        pygame.mixer.music.unpause()
    
    def set_sound_volume(self, volume: float):
        """
        Set the global sound effect volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        
        # Update all loaded sound effects
        for sound in self.sound_effects.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float):
        """
        Set the music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_category_volume(self, category: str, volume: float):
        """
        Set the volume multiplier for a sound category.
        
        Args:
            category: The sound category
            volume: Volume multiplier (0.0 to 1.0)
        """
        if category in self.category_volumes:
            self.category_volumes[category] = max(0.0, min(1.0, volume))
            
            # Update all sounds in this category
            for sound_id in self.sound_categories.get(category, []):
                if sound_id in self.sound_effects:
                    self.sound_effects[sound_id].set_volume(
                        self.sound_volume * self.category_volumes[category]
                    )
    
    def mute(self):
        """Mute all audio."""
        if not self.muted:
            self.previous_volumes = (self.sound_volume, self.music_volume)
            self.set_sound_volume(0.0)
            self.set_music_volume(0.0)
            self.muted = True
    
    def unmute(self):
        """Unmute all audio."""
        if self.muted:
            self.set_sound_volume(self.previous_volumes[0])
            self.set_music_volume(self.previous_volumes[1])
            self.muted = False
    
    def toggle_mute(self):
        """Toggle mute state."""
        if self.muted:
            self.unmute()
        else:
            self.mute()
    
    def load_default_sounds(self):
        """Load default game sounds."""
        # Player sounds
        self.load_sound("player_shoot", "assets/sounds/ink_shoot.wav", "player")
        self.load_sound("player_hit", "assets/sounds/player_hit.wav", "player")
        
        # Enemy sounds
        self.load_sound("ship_hit", "assets/sounds/ship_hit.wav", "enemy")
        self.load_sound("ship_sink", "assets/sounds/ship_sink.wav", "enemy")
        self.load_sound("captain_panic", "assets/sounds/captain_panic.wav", "enemy")
        self.load_sound("head_explosion", "assets/sounds/head_explosion.wav", "enemy")
        
        # UI sounds
        self.load_sound("button_click", "assets/sounds/button_click.wav", "ui")
        self.load_sound("menu_select", "assets/sounds/menu_select.wav", "ui")
        self.load_sound("level_complete", "assets/sounds/level_complete.wav", "ui")
        self.load_sound("game_over", "assets/sounds/game_over.wav", "ui")
        self.load_sound("high_score", "assets/sounds/high_score.wav", "ui")
        self.load_sound("menu_open", "assets/sounds/menu_open.wav", "ui")
        
        # Environment sounds
        self.load_sound("splash", "assets/sounds/splash.wav", "environment")
        self.load_sound("bubble", "assets/sounds/bubble.wav", "environment")
        self.load_sound("ink_splat", "assets/sounds/ink_splat.wav", "environment")
        self.load_sound("ink_splat_special", "assets/sounds/ink_splat_special.wav", "environment")
        self.load_sound("explosion", "assets/sounds/explosion.wav", "environment")
        
        # Music tracks
        self.load_music("main_menu", "assets/sounds/main_menu_music.mp3")
        self.load_music("gameplay", "assets/sounds/gameplay_music.mp3")
        self.load_music("boss_battle", "assets/sounds/boss_battle_music.mp3")
        self.load_music("game_over", "assets/sounds/game_over_music.mp3")