"""Level manager for the Octopus Ink Slime game.

This module handles level progression, transitions, and tracking
the player's progress through the game.
"""

from typing import Dict, Any, Optional, Callable
from src.levels.level_data import LevelData


class LevelManager:
    """Manages level progression and state in the game.
    
    The LevelManager keeps track of the current level, loads level
    configurations, and handles transitions between levels.
    """
    
    def __init__(self):
        """Initialize the LevelManager."""
        # Current level tracking
        self.current_level_id: int = 1
        self.current_level_data: Dict[str, Any] = {}
        
        # Level progress tracking
        self.level_completed: bool = False
        self.level_score: int = 0
        self.level_time_remaining: float = 0
        self.level_progress: float = 0.0  # 0.0 to 1.0
        
        # Callbacks
        self.on_level_complete_callback: Optional[Callable] = None
        self.on_level_failed_callback: Optional[Callable] = None
        
        # Load initial level data
        self._load_current_level()
        
    def _load_current_level(self) -> None:
        """Load the data for the current level."""
        self.current_level_data = LevelData.get_level_data(self.current_level_id)
        self.level_completed = False
        self.level_score = 0
        self.level_time_remaining = self.current_level_data["time_limit"]
        self.level_progress = 0.0
        
    def start_level(self) -> Dict[str, Any]:
        """Start the current level.
        
        Returns:
            The configuration data for the current level
        """
        self._load_current_level()
        return self.current_level_data
        
    def update(self, dt: float, current_score: int) -> None:
        """Update the level manager.
        
        Args:
            dt: Delta time in seconds since the last update
            current_score: The current score for this level
        """
        # Update level timer
        if self.level_time_remaining > 0:
            self.level_time_remaining -= dt
            
        # Update level score
        self.level_score = current_score
        
        # Check for level completion
        score_target = self.current_level_data["score_target"]
        self.level_progress = min(1.0, self.level_score / score_target)
        
        # Check if level is completed
        if not self.level_completed and self.level_score >= score_target:
            self.level_completed = True
            if self.on_level_complete_callback:
                self.on_level_complete_callback(self.current_level_id, self.level_score)
                
        # Check if level failed (time ran out)
        if not self.level_completed and self.level_time_remaining <= 0:
            if self.on_level_failed_callback:
                self.on_level_failed_callback(self.current_level_id, self.level_score)
                
    def advance_to_next_level(self) -> bool:
        """Advance to the next level.
        
        Returns:
            True if successfully advanced to next level, False if at max level
        """
        if self.current_level_id < LevelData.get_level_count():
            self.current_level_id += 1
            self._load_current_level()
            return True
        return False
        
    def restart_current_level(self) -> None:
        """Restart the current level."""
        self._load_current_level()
        
    def set_level(self, level_id: int) -> None:
        """Set the current level to a specific level ID.
        
        Args:
            level_id: The level ID to set (1-based)
            
        Raises:
            ValueError: If the level_id is invalid
        """
        if level_id < 1 or level_id > LevelData.get_level_count():
            raise ValueError(f"Invalid level ID: {level_id}. Must be between 1 and {LevelData.get_level_count()}")
            
        self.current_level_id = level_id
        self._load_current_level()
        
    def get_current_level_id(self) -> int:
        """Get the current level ID.
        
        Returns:
            The current level ID (1-based)
        """
        return self.current_level_id
        
    def get_current_level_data(self) -> Dict[str, Any]:
        """Get the configuration data for the current level.
        
        Returns:
            A dictionary containing the current level configuration
        """
        return self.current_level_data
        
    def get_level_progress(self) -> float:
        """Get the current level progress.
        
        Returns:
            The level progress as a value between 0.0 and 1.0
        """
        return self.level_progress
        
    def get_level_time_remaining(self) -> float:
        """Get the time remaining for the current level.
        
        Returns:
            The time remaining in seconds
        """
        return max(0.0, self.level_time_remaining)
        
    def is_level_completed(self) -> bool:
        """Check if the current level is completed.
        
        Returns:
            True if the level is completed
        """
        return self.level_completed
        
    def get_level_completion_stats(self) -> Dict[str, Any]:
        """Get statistics for the completed level.
        
        Returns:
            A dictionary containing level completion statistics
        """
        time_used = self.current_level_data["time_limit"] - self.level_time_remaining
        
        return {
            "level_id": self.current_level_id,
            "level_name": self.current_level_data["name"],
            "score": self.level_score,
            "target_score": self.current_level_data["score_target"],
            "time_used": time_used,
            "time_limit": self.current_level_data["time_limit"],
            "is_completed": self.level_completed,
            "next_level_id": min(self.current_level_id + 1, LevelData.get_level_count()),
            "next_level_name": LevelData.get_level_data(
                min(self.current_level_id + 1, LevelData.get_level_count())
            )["name"] if self.current_level_id < LevelData.get_level_count() else "Game Complete"
        }
        
    def set_on_level_complete_callback(self, callback: Callable) -> None:
        """Set the callback function for level completion.
        
        Args:
            callback: Function to call when level is completed
        """
        self.on_level_complete_callback = callback
        
    def set_on_level_failed_callback(self, callback: Callable) -> None:
        """Set the callback function for level failure.
        
        Args:
            callback: Function to call when level is failed
        """
        self.on_level_failed_callback = callback
        
    def get_current_ink_color(self) -> str:
        """Get the ink color for the current level.
        
        Returns:
            The ink color string for the current level
        """
        return self.current_level_data["ink_color"]
        
    def get_level_count(self) -> int:
        """Get the total number of levels in the game.
        
        Returns:
            The total number of levels
        """
        return LevelData.get_level_count()