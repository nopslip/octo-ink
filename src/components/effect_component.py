"""
Effect Component for the Octopus Ink Slime game.
Handles visual effects like ink splatters, ship sinking animations, and explosions.
"""

import pygame
import random
from typing import Dict, List, Tuple, Optional
from src.components.component import Component


class EffectManager:
    """
    Manages visual effects in the game.
    Implements the singleton pattern for global access.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """
        Get the singleton instance of the EffectManager.
        
        Returns:
            The EffectManager instance
        """
        if EffectManager._instance is None:
            EffectManager._instance = EffectManager()
        return EffectManager._instance
    
    def __init__(self):
        """Initialize the effect manager."""
        self.effects = []
        self.effect_templates = {
            # Ink splatter effects for different colors
            "splatter_dark_blue": {
                "animation": "animations/splatter_dark_blue.png",
                "frames": 8,
                "duration": 0.8
            },
            "splatter_purple": {
                "animation": "animations/splatter_purple.png",
                "frames": 8,
                "duration": 0.8
            },
            "splatter_green": {
                "animation": "animations/splatter_green.png",
                "frames": 8,
                "duration": 0.8
            },
            "splatter_red": {
                "animation": "animations/splatter_red.png",
                "frames": 8,
                "duration": 0.8
            },
            "splatter_rainbow": {
                "animation": "animations/splatter_rainbow.png",
                "frames": 12,
                "duration": 1.2,
                "particles": {
                    "count": 20,
                    "colors": [(255, 0, 0), (255, 165, 0), (255, 255, 0), 
                               (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)],
                    "speed": 100,
                    "lifetime": 1.5
                }
            },
            
            # Ship sinking effects
            "ship_sinking_small": {
                "animation": "animations/ship_sinking_small.png",
                "frames": 12,
                "duration": 2.0,
                "screen_shake": {
                    "intensity": 5,
                    "duration": 0.5
                },
                "particles": {
                    "count": 15,
                    "colors": [(150, 150, 255), (100, 100, 200)],
                    "speed": 80,
                    "lifetime": 1.0
                }
            },
            "ship_sinking_medium": {
                "animation": "animations/ship_sinking_medium.png",
                "frames": 15,
                "duration": 2.5,
                "screen_shake": {
                    "intensity": 8,
                    "duration": 0.7
                },
                "particles": {
                    "count": 25,
                    "colors": [(150, 150, 255), (100, 100, 200)],
                    "speed": 100,
                    "lifetime": 1.2
                }
            },
            "ship_sinking_large": {
                "animation": "animations/ship_sinking_large.png",
                "frames": 18,
                "duration": 3.0,
                "screen_shake": {
                    "intensity": 12,
                    "duration": 1.0
                },
                "particles": {
                    "count": 40,
                    "colors": [(150, 150, 255), (100, 100, 200)],
                    "speed": 120,
                    "lifetime": 1.5
                }
            },
            
            # Captain effects
            "head_explosion": {
                "animation": "animations/head_explosion.png",
                "frames": 12,
                "duration": 1.0,
                "screen_shake": {
                    "intensity": 10,
                    "duration": 0.3
                },
                "particles": {
                    "count": 30,
                    "colors": [(255, 0, 0), (200, 0, 0)],
                    "speed": 150,
                    "lifetime": 0.8
                }
            },
            
            # Explosion effects
            "small_explosion": {
                "animation": "animations/small_explosion.png",
                "frames": 8,
                "duration": 0.6,
                "screen_shake": {
                    "intensity": 3,
                    "duration": 0.2
                },
                "particles": {
                    "count": 10,
                    "colors": [(255, 200, 0), (255, 100, 0)],
                    "speed": 80,
                    "lifetime": 0.5
                }
            },
            "medium_explosion": {
                "animation": "animations/medium_explosion.png",
                "frames": 10,
                "duration": 0.8,
                "screen_shake": {
                    "intensity": 6,
                    "duration": 0.4
                },
                "particles": {
                    "count": 20,
                    "colors": [(255, 200, 0), (255, 100, 0)],
                    "speed": 100,
                    "lifetime": 0.7
                }
            },
            "large_explosion": {
                "animation": "animations/large_explosion.png",
                "frames": 12,
                "duration": 1.0,
                "screen_shake": {
                    "intensity": 10,
                    "duration": 0.6
                },
                "particles": {
                    "count": 30,
                    "colors": [(255, 200, 0), (255, 100, 0)],
                    "speed": 120,
                    "lifetime": 1.0
                }
            }
        }
        
        # Cache for loaded effect images
        self.effect_images = {}
        
        # Particle system reference
        self.particle_system = None
        
        # Camera manager reference for screen shake
        self.camera_manager = None
    
    def set_particle_system(self, particle_system):
        """
        Set the particle system reference.
        
        Args:
            particle_system: The particle system instance
        """
        self.particle_system = particle_system
    
    def set_camera_manager(self, camera_manager):
        """
        Set the camera manager reference.
        
        Args:
            camera_manager: The camera manager instance
        """
        self.camera_manager = camera_manager
    
    def load_effect_images(self, asset_manager):
        """
        Load all effect images using the asset manager.
        
        Args:
            asset_manager: The asset manager instance
        """
        for effect_type, template in self.effect_templates.items():
            animation_path = template["animation"]
            if animation_path not in self.effect_images:
                self.effect_images[animation_path] = asset_manager.load_image(animation_path)
    
    def create_effect(self, effect_type: str, position: Tuple[float, float]):
        """
        Create a new visual effect.
        
        Args:
            effect_type: Type of effect to create
            position: Position (x, y) to create the effect at
        """
        if effect_type in self.effect_templates:
            template = self.effect_templates[effect_type]
            effect = {
                "type": effect_type,
                "position": position,
                "animation": template["animation"],
                "frames": template["frames"],
                "current_frame": 0,
                "frame_time": template["duration"] / template["frames"],
                "timer": 0,
                "completed": False
            }
            self.effects.append(effect)
            
            # Handle special effects
            if "particles" in template and self.particle_system:
                particle_config = template["particles"]
                self.particle_system.create_particles(
                    position,
                    particle_config["count"],
                    particle_config["colors"],
                    particle_config["speed"],
                    particle_config["lifetime"]
                )
            
            if "screen_shake" in template and self.camera_manager:
                shake_config = template["screen_shake"]
                self.camera_manager.apply_shake(
                    shake_config["intensity"],
                    shake_config["duration"]
                )
            
            # Play corresponding sound effect
            from src.engine.audio_manager import AudioManager
            audio_manager = AudioManager.get_instance()
            
            # Map effect types to sound effects
            sound_mappings = {
                "splatter_dark_blue": "ink_splat",
                "splatter_purple": "ink_splat",
                "splatter_green": "ink_splat",
                "splatter_red": "ink_splat",
                "splatter_rainbow": "ink_splat_special",
                "ship_sinking_small": "ship_sink",
                "ship_sinking_medium": "ship_sink",
                "ship_sinking_large": "ship_sink",
                "head_explosion": "head_explosion",
                "small_explosion": "explosion",
                "medium_explosion": "explosion",
                "large_explosion": "explosion"
            }
            
            if effect_type in sound_mappings:
                audio_manager.play_sound(sound_mappings[effect_type])
    
    def update(self, dt: float):
        """
        Update all active effects.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update all active effects
        for effect in self.effects:
            effect["timer"] += dt
            if effect["timer"] >= effect["frame_time"]:
                effect["timer"] -= effect["frame_time"]
                effect["current_frame"] += 1
                if effect["current_frame"] >= effect["frames"]:
                    effect["completed"] = True
        
        # Remove completed effects
        self.effects = [e for e in self.effects if not e["completed"]]
    
    def render(self, surface: pygame.Surface):
        """
        Render all active effects.
        
        Args:
            surface: Pygame surface to render to
        """
        # Render all active effects
        for effect in self.effects:
            # Skip if the image isn't loaded
            if effect["animation"] not in self.effect_images:
                continue
                
            # Get the image
            image = self.effect_images[effect["animation"]]
            
            # Calculate source rect based on current frame
            frame_width = image.get_width() / effect["frames"]
            frame_height = image.get_height()
            src_rect = pygame.Rect(
                effect["current_frame"] * frame_width, 0,
                frame_width, frame_height
            )
            
            # Calculate destination rect
            dest_rect = pygame.Rect(
                effect["position"][0] - frame_width / 2,
                effect["position"][1] - frame_height / 2,
                frame_width, frame_height
            )
            
            # Draw the effect
            surface.blit(image, dest_rect, src_rect)


class EffectComponent(Component):
    """Component for entities that can create visual effects."""
    
    def __init__(self):
        """Initialize the effect component."""
        super().__init__("effect")
        self.active_effects = []
        self.effect_manager = EffectManager.get_instance()
    
    def create_effect(self, effect_type: str, offset: Tuple[float, float] = (0, 0)):
        """
        Create a visual effect at the entity's position.
        
        Args:
            effect_type: Type of effect to create
            offset: Optional offset from the entity's position
        """
        transform = self.entity.get_component("transform")
        if transform:
            position = (
                transform.position.x + offset[0],
                transform.position.y + offset[1]
            )
            self.effect_manager.create_effect(effect_type, position)
    
    def create_random_effect(self, effect_types: List[str], 
                            offset_range: Tuple[float, float, float, float] = (-10, 10, -10, 10)):
        """
        Create a random effect from a list of possible effects.
        
        Args:
            effect_types: List of possible effect types to choose from
            offset_range: Range for random offset (min_x, max_x, min_y, max_y)
        """
        if not effect_types:
            return
            
        effect_type = random.choice(effect_types)
        offset = (
            random.uniform(offset_range[0], offset_range[1]),
            random.uniform(offset_range[2], offset_range[3])
        )
        self.create_effect(effect_type, offset)
    
    def create_effect_sequence(self, effect_type: str, count: int, 
                              interval: float, offset_range: Tuple[float, float, float, float] = (-10, 10, -10, 10)):
        """
        Schedule a sequence of effects to be created over time.
        
        Args:
            effect_type: Type of effect to create
            count: Number of effects to create
            interval: Time interval between effects in seconds
            offset_range: Range for random offset (min_x, max_x, min_y, max_y)
        """
        self.active_effects.append({
            "type": effect_type,
            "count": count,
            "remaining": count,
            "interval": interval,
            "timer": 0,
            "offset_range": offset_range
        })
    
    def update(self, dt: float):
        """
        Update the effect component.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update effect sequences
        for effect in self.active_effects:
            if effect["remaining"] > 0:
                effect["timer"] += dt
                if effect["timer"] >= effect["interval"]:
                    effect["timer"] -= effect["interval"]
                    effect["remaining"] -= 1
                    
                    # Create the effect with random offset
                    offset = (
                        random.uniform(effect["offset_range"][0], effect["offset_range"][1]),
                        random.uniform(effect["offset_range"][2], effect["offset_range"][3])
                    )
                    self.create_effect(effect["type"], offset)
        
        # Remove completed effect sequences
        self.active_effects = [e for e in self.active_effects if e["remaining"] > 0]