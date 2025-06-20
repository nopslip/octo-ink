"""Animation Component for managing sprite animations."""

from typing import Dict, List, Optional
from src.components.component import Component


class AnimationComponent(Component):
    """Component that manages sprite animations."""
    
    def __init__(self):
        """Initialize the AnimationComponent."""
        super().__init__("animation")
        
        # Animation data
        self.animations: Dict[str, List[int]] = {}  # name -> list of frame indices
        self.frame_durations: Dict[str, float] = {}  # name -> duration per frame
        
        # Current animation state
        self.current_animation: Optional[str] = None
        self.current_frame: int = 0
        self.frame_timer: float = 0.0
        self.is_playing: bool = True
        self.loop: bool = True
        
        # Animation callbacks
        self.on_animation_complete = None
        
    def update(self, dt: float) -> None:
        """Update animation state.
        
        Args:
            dt: Delta time in seconds since the last update
        """
        if not self.is_playing or not self.current_animation:
            return
            
        # Update frame timer
        self.frame_timer += dt
        
        # Check if we need to advance to next frame
        frame_duration = self.frame_durations.get(self.current_animation, 0.1)
        if self.frame_timer >= frame_duration:
            self.frame_timer -= frame_duration
            self._advance_frame()
            
    def _advance_frame(self) -> None:
        """Advance to the next frame in the current animation."""
        if not self.current_animation:
            return
            
        frames = self.animations.get(self.current_animation, [])
        if not frames:
            return
            
        self.current_frame += 1
        
        # Check if animation is complete
        if self.current_frame >= len(frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.current_frame = len(frames) - 1
                self.is_playing = False
                
                # Trigger callback
                if self.on_animation_complete:
                    self.on_animation_complete(self.current_animation)
                    
    def play(self, animation_name: str, loop: bool = True) -> None:
        """Play a specific animation.
        
        Args:
            animation_name: Name of the animation to play
            loop: Whether to loop the animation
        """
        if animation_name == self.current_animation and self.is_playing:
            return  # Already playing this animation
            
        self.current_animation = animation_name
        self.current_frame = 0
        self.frame_timer = 0.0
        self.is_playing = True
        self.loop = loop
        
    def stop(self) -> None:
        """Stop the current animation."""
        self.is_playing = False
        
    def pause(self) -> None:
        """Pause the current animation."""
        self.is_playing = False
        
    def resume(self) -> None:
        """Resume the current animation."""
        self.is_playing = True
        
    def add_animation(self, name: str, frames: List[int], 
                     frame_duration: float = 0.1) -> None:
        """Add a new animation.
        
        Args:
            name: Name of the animation
            frames: List of frame indices
            frame_duration: Duration of each frame in seconds
        """
        self.animations[name] = frames
        self.frame_durations[name] = frame_duration
        
    def get_current_frame_index(self) -> int:
        """Get the current frame index for the render component.
        
        Returns:
            The current frame index
        """
        if not self.current_animation:
            return 0
            
        frames = self.animations.get(self.current_animation, [])
        if not frames or self.current_frame >= len(frames):
            return 0
            
        return frames[self.current_frame]