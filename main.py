#!/usr/bin/env python3
"""
Octopus Ink Slime Game
Main entry point for the game.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.engine.game_engine import GameEngine
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE


def main():
    """Main function to run the game."""
    # Create game engine instance
    engine = GameEngine()
    
    try:
        # Initialize the game
        engine.initialize(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
        
        # Run the game
        engine.run()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Clean up
        engine.quit()


if __name__ == "__main__":
    main()