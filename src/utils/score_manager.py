"""
Score Manager for the Octopus Ink Slime game.
Handles tracking, saving, and loading scores.
"""

import os
import json
from typing import List, Dict, Tuple, Optional


class ScoreManager:
    """
    Manages game scores, high scores, and score multipliers.
    Implements the singleton pattern for global access.
    """
    
    _instance = None
    
    @staticmethod
    def get_instance():
        """
        Get the singleton instance of the ScoreManager.
        
        Returns:
            The ScoreManager instance
        """
        if ScoreManager._instance is None:
            ScoreManager._instance = ScoreManager()
        return ScoreManager._instance
    
    def __init__(self):
        """Initialize the score manager."""
        # Current game score
        self.current_score = 0
        
        # High scores list (name, score, level)
        self.high_scores = []
        
        # Score history for the current game
        self.score_history = []
        
        # Score multipliers
        self.base_multiplier = 1.0
        self.combo_multiplier = 1.0
        self.level_multipliers = {
            1: 1.0,    # Level 1: Normal scoring
            2: 1.2,    # Level 2: 20% bonus
            3: 1.5,    # Level 3: 50% bonus
            4: 1.8,    # Level 4: 80% bonus
            5: 2.0     # Level 5: Double scoring
        }
        
        # Combo system
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 2.0  # Seconds before combo resets
        
        # Current level
        self.current_level = 1
        
        # Load high scores
        self.load_high_scores()
    
    def reset(self):
        """Reset the score manager for a new game."""
        self.current_score = 0
        self.score_history = []
        self.base_multiplier = 1.0
        self.combo_multiplier = 1.0
        self.combo_count = 0
        self.combo_timer = 0
        self.current_level = 1
    
    def add_points(self, points: int, record_history: bool = True):
        """
        Add points to the current score.
        
        Args:
            points: Base points to add
            record_history: Whether to record this score in history
        """
        # Calculate effective multiplier
        effective_multiplier = (
            self.base_multiplier * 
            self.combo_multiplier * 
            self.level_multipliers.get(self.current_level, 1.0)
        )
        
        # Calculate actual points with multiplier
        actual_points = int(points * effective_multiplier)
        
        # Add to current score
        self.current_score += actual_points
        
        # Increment combo
        self.combo_count += 1
        self.combo_timer = 0
        
        # Update combo multiplier (max 3.0x)
        self.combo_multiplier = min(3.0, 1.0 + (self.combo_count * 0.1))
        
        # Record in history if enabled
        if record_history:
            self.score_history.append({
                "points": actual_points,
                "base_points": points,
                "multiplier": effective_multiplier,
                "combo": self.combo_count,
                "level": self.current_level
            })
    
    def update(self, dt: float):
        """
        Update the score manager.
        
        Args:
            dt: Time delta in seconds since last update
        """
        # Update combo timer
        if self.combo_count > 0:
            self.combo_timer += dt
            if self.combo_timer >= self.combo_timeout:
                # Reset combo
                self.combo_count = 0
                self.combo_multiplier = 1.0
    
    def set_level(self, level: int):
        """
        Set the current level.
        
        Args:
            level: New level number
        """
        self.current_level = level
    
    def get_current_score(self) -> int:
        """
        Get the current score.
        
        Returns:
            Current score
        """
        return self.current_score
    
    def get_high_scores(self, count: int = 10) -> List[Dict]:
        """
        Get the top high scores.
        
        Args:
            count: Number of high scores to return
            
        Returns:
            List of high score entries
        """
        return self.high_scores[:count]
    
    def get_current_multiplier(self) -> float:
        """
        Get the current effective multiplier.
        
        Returns:
            Current effective multiplier
        """
        return (
            self.base_multiplier * 
            self.combo_multiplier * 
            self.level_multipliers.get(self.current_level, 1.0)
        )
    
    def get_combo_count(self) -> int:
        """
        Get the current combo count.
        
        Returns:
            Current combo count
        """
        return self.combo_count
    
    def check_high_score(self) -> bool:
        """
        Check if the current score is a high score.
        
        Returns:
            True if the current score is a high score
        """
        if not self.high_scores:
            return True
            
        return self.current_score > self.high_scores[-1]["score"] if len(self.high_scores) >= 10 else True
    
    def add_high_score(self, name: str) -> int:
        """
        Add the current score to high scores.
        
        Args:
            name: Player name
            
        Returns:
            Position in high scores (0-based)
        """
        high_score = {
            "name": name,
            "score": self.current_score,
            "level": self.current_level,
            "date": self._get_current_date()
        }
        
        # Add to high scores
        self.high_scores.append(high_score)
        
        # Sort high scores
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Trim to top 10
        if len(self.high_scores) > 10:
            self.high_scores = self.high_scores[:10]
        
        # Save high scores
        self.save_high_scores()
        
        # Return position
        return self.high_scores.index(high_score)
    
    def load_high_scores(self):
        """Load high scores from file."""
        try:
            if os.path.exists("high_scores.json"):
                with open("high_scores.json", "r") as f:
                    self.high_scores = json.load(f)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []
    
    def save_high_scores(self):
        """Save high scores to file."""
        try:
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def _get_current_date(self) -> str:
        """
        Get the current date as a string.
        
        Returns:
            Current date string
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_score_breakdown(self) -> Dict:
        """
        Get a breakdown of the current score.
        
        Returns:
            Dictionary with score breakdown
        """
        # Count score sources
        sources = {}
        for entry in self.score_history:
            source = entry.get("source", "unknown")
            if source not in sources:
                sources[source] = 0
            sources[source] += entry["points"]
        
        return {
            "total": self.current_score,
            "sources": sources,
            "highest_combo": max([entry["combo"] for entry in self.score_history]) if self.score_history else 0,
            "highest_multiplier": max([entry["multiplier"] for entry in self.score_history]) if self.score_history else 1.0
        }