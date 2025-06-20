"""Test script to verify player implementation."""

import pygame
import sys
from src.engine.game_engine import GameEngine

def main():
    """Run a test of the player implementation."""
    # Initialize the game engine
    engine = GameEngine()
    engine.initialize(width=1024, height=768, title="Octopus Ink Slime - Player Test")
    
    # Add some test enemies to shoot at
    engine.entity_factory.create_ship(200, 200, "small")
    engine.entity_factory.create_ship(600, 200, "medium")
    engine.entity_factory.create_ship(400, 400, "large")
    
    print("\n=== PLAYER CONTROLS TEST ===")
    print("Arrow Keys / WASD: Move the octopus")
    print("Spacebar: Hold to fire ink continuously")
    print("ESC: Quit")
    print("\nThe octopus has 10 arms that fire sequentially.")
    print("Green arm tips = ready to fire")
    print("Red arm tips = on cooldown")
    print("\nTry shooting at the ships to see them sink!")
    
    # Run the game
    engine.run()

if __name__ == "__main__":
    main()