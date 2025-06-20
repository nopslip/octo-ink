"""Test script for the enemy and obstacle implementation."""

import pygame
from src.engine.game_engine import GameEngine


def main():
    """Run the enemy system test."""
    print("Starting Octopus Ink Slime - Enemy System Test")
    print("=" * 50)
    print("Controls:")
    print("- Arrow Keys: Move octopus")
    print("- Space: Shoot ink")
    print("- ESC: Quit")
    print("=" * 50)
    print("\nEnemy Behaviors:")
    print("- Ships: Move horizontally across screen")
    print("- Captains: Ride on ships, panic when ship sinks")
    print("- Turtles: Block shots with shields")
    print("- Fish: Wander around as bonus targets")
    print("=" * 50)
    
    # Create and initialize the game engine
    engine = GameEngine()
    engine.initialize(800, 600, "Octopus Ink Slime - Enemy System Test")
    
    # Run the game
    engine.run()
    
    # Clean up
    engine.quit()


if __name__ == "__main__":
    main()