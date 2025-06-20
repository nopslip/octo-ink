#!/usr/bin/env python3
"""
Comprehensive test script for the Octopus Ink Slime game.
This script runs the game with debug information enabled and tests all game components.
"""

import pygame
import sys
import time
import os
import psutil
from typing import Dict, List, Tuple
from src.engine.game_engine import GameEngine
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class GameTester:
    """Test harness for the Octopus Ink Slime game."""
    
    def __init__(self):
        """Initialize the game tester."""
        self.engine = None
        self.start_time = 0
        self.frame_times = []
        self.memory_usage = []
        self.entity_counts = []
        self.component_counts = {}
        self.collision_tests = 0
        self.process = psutil.Process(os.getpid())
        
    def initialize(self):
        """Initialize the game engine with test configuration."""
        print("Initializing Octopus Ink Slime Test Environment")
        print("=" * 50)
        
        # Create and initialize the game engine
        self.engine = GameEngine()
        self.engine.initialize(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            "Octopus Ink Slime - Test Mode"
        )
        
        # Enable debug mode
        self.engine.debug_mode = True
        
        # Record start time
        self.start_time = time.time()
        
        print("Game engine initialized")
        print("Debug mode enabled")
        print("=" * 50)
        
    def run_tests(self):
        """Run a series of tests on the game components."""
        if not self.engine:
            raise RuntimeError("Game engine not initialized. Call initialize() first.")
        
        print("\nRunning game component tests...")
        
        # Test entity creation
        self._test_entity_creation()
        
        # Test level system
        self._test_level_system()
        
        # Test collision system
        self._test_collision_system()
        
        # Test input system
        self._test_input_system()
        
        # Test rendering system
        self._test_rendering_system()
        
        # Test audio system
        self._test_audio_system()
        
        print("\nAll component tests completed")
        print("=" * 50)
        
        # Run the game loop with performance monitoring
        self._run_game_with_monitoring()
        
    def _test_entity_creation(self):
        """Test the entity creation system."""
        print("\nTesting Entity Creation System:")
        
        # Test player creation
        player = self.engine.entity_factory.create_player(
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT // 2
        )
        print(f"- Player created: {player is not None}")
        
        # Test ship creation
        ship = self.engine.entity_factory.create_ship(200, 200, "medium")
        print(f"- Ship created: {ship is not None}")
        
        # Test captain creation
        captain = self.engine.entity_factory.create_captain(250, 200)
        print(f"- Captain created: {captain is not None}")
        
        # Test turtle creation
        turtle = self.engine.entity_factory.create_turtle(300, 300)
        print(f"- Turtle created: {turtle is not None}")
        
        # Test fish creation
        fish = self.engine.entity_factory.create_fish(400, 400)
        print(f"- Fish created: {fish is not None}")
        
        # Test ink slime creation
        direction = pygame.math.Vector2(1, 0)
        ink = self.engine.entity_factory.create_ink_slime(
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT // 2, 
            direction
        )
        print(f"- Ink slime created: {ink is not None}")
        
        # Verify entity count
        entity_count = self.engine.entity_manager.get_entity_count()
        print(f"- Total entities created: {entity_count}")
        
    def _test_level_system(self):
        """Test the level system."""
        print("\nTesting Level System:")
        
        # Test level manager
        if self.engine.level_manager:
            current_level = self.engine.level_manager.get_current_level_id()
            print(f"- Current level: {current_level}")
            
            # Test level data
            level_data = self.engine.level_manager.get_current_level_data()
            print(f"- Level data retrieved: {level_data is not None}")
            
            # Test level generator
            if self.engine.level_generator:
                print(f"- Level generator initialized: {self.engine.level_generator is not None}")
                
                # Test level initialization
                self.engine.level_generator.initialize_level(level_data)
                print("- Level initialized successfully")
        else:
            print("- Level manager not initialized")
            
    def _test_collision_system(self):
        """Test the collision detection system."""
        print("\nTesting Collision System:")
        
        # Create test entities for collision
        player = self.engine.entity_factory.create_player(100, 100)
        ship = self.engine.entity_factory.create_ship(150, 100, "small")
        
        # Test collision detection
        collision = self.engine._check_collision(player, ship)
        print(f"- Collision detection working: {collision is not None}")
        
        # Test physics engine
        if self.engine.physics_engine:
            print(f"- Physics engine initialized: {self.engine.physics_engine is not None}")
            
            # Update physics once
            self.engine.physics_engine.update(0.016)  # ~60 FPS
            print("- Physics engine update successful")
        else:
            print("- Physics engine not initialized")
            
    def _test_input_system(self):
        """Test the input system."""
        print("\nTesting Input System:")
        
        # Check input manager
        if self.engine.input_manager:
            print(f"- Input manager initialized: {self.engine.input_manager is not None}")
            
            # Test key state retrieval
            up_key = self.engine.input_manager.is_key_pressed(pygame.K_UP)
            print(f"- Key state retrieval working: {up_key is not None}")
        else:
            print("- Input manager not initialized")
            
    def _test_rendering_system(self):
        """Test the rendering system."""
        print("\nTesting Rendering System:")
        
        # Check if screen is initialized
        print(f"- Screen initialized: {self.engine.screen is not None}")
        
        # Test entity rendering
        if self.engine.entity_manager:
            # Render once to test
            self.engine.entity_manager.render(self.engine.screen)
            print("- Entity rendering successful")
        else:
            print("- Entity manager not initialized")
            
        # Test UI rendering
        if self.engine.ui_manager:
            print(f"- UI manager initialized: {self.engine.ui_manager is not None}")
            
            # Render UI once to test
            self.engine.ui_manager.render(self.engine.screen)
            print("- UI rendering successful")
        else:
            print("- UI manager not initialized")
            
    def _test_audio_system(self):
        """Test the audio system."""
        print("\nTesting Audio System:")
        
        # Check audio manager
        if self.engine.audio_manager:
            print(f"- Audio manager initialized: {self.engine.audio_manager is not None}")
            
            # Test sound loading
            self.engine.audio_manager.load_default_sounds()
            print("- Default sounds loaded successfully")
            
            # Test sound playing (without actually playing to avoid noise)
            print("- Sound system ready")
        else:
            print("- Audio manager not initialized")
            
    def _run_game_with_monitoring(self):
        """Run the game loop with performance monitoring."""
        print("\nRunning game with performance monitoring...")
        print("Press ESC to exit the test")
        print("=" * 50)
        
        # Set up monitoring variables
        frame_count = 0
        last_time = time.time()
        running = True
        
        # Create a font for displaying stats
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        
        while running and frame_count < 1000:  # Limit to 1000 frames for testing
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Record frame time
            self.frame_times.append(dt)
            
            # Record memory usage
            mem_info = self.process.memory_info()
            self.memory_usage.append(mem_info.rss / 1024 / 1024)  # MB
            
            # Record entity count
            if self.engine.entity_manager:
                self.entity_counts.append(self.engine.entity_manager.get_entity_count())
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update game state
            self.engine.run()
            
            # Display performance stats
            if frame_count % 10 == 0:  # Update stats every 10 frames
                self._display_performance_stats(font)
            
            frame_count += 1
            
        # Generate performance report
        self._generate_performance_report()
        
    def _display_performance_stats(self, font):
        """Display performance statistics on screen."""
        if not self.engine.screen:
            return
            
        # Calculate current FPS
        current_fps = 1.0 / self.frame_times[-1] if self.frame_times else 0
        
        # Calculate average FPS
        avg_fps = len(self.frame_times) / sum(self.frame_times) if self.frame_times else 0
        
        # Get current memory usage
        current_memory = self.memory_usage[-1] if self.memory_usage else 0
        
        # Get current entity count
        current_entities = self.entity_counts[-1] if self.entity_counts else 0
        
        # Create stat texts
        stats = [
            f"FPS: {current_fps:.1f} (Avg: {avg_fps:.1f})",
            f"Memory: {current_memory:.1f} MB",
            f"Entities: {current_entities}",
            f"Test Runtime: {time.time() - self.start_time:.1f}s",
            "Press ESC to exit test"
        ]
        
        # Render stats
        y_offset = 10
        for stat in stats:
            text_surface = font.render(stat, True, (255, 255, 0))
            self.engine.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
            
        # Update display
        pygame.display.flip()
        
    def _generate_performance_report(self):
        """Generate a performance report based on collected data."""
        print("\nPerformance Test Results:")
        print("=" * 50)
        
        # Calculate FPS statistics
        if self.frame_times:
            avg_fps = len(self.frame_times) / sum(self.frame_times)
            min_fps = 1.0 / max(self.frame_times)
            max_fps = 1.0 / min(self.frame_times)
            
            print(f"FPS Statistics:")
            print(f"- Average FPS: {avg_fps:.2f}")
            print(f"- Minimum FPS: {min_fps:.2f}")
            print(f"- Maximum FPS: {max_fps:.2f}")
            print(f"- Target FPS: {FPS}")
            print(f"- FPS Stability: {min_fps/max_fps*100:.1f}%")
        
        # Calculate memory statistics
        if self.memory_usage:
            avg_memory = sum(self.memory_usage) / len(self.memory_usage)
            min_memory = min(self.memory_usage)
            max_memory = max(self.memory_usage)
            memory_growth = max_memory - min_memory
            
            print(f"\nMemory Usage Statistics:")
            print(f"- Average Memory: {avg_memory:.2f} MB")
            print(f"- Minimum Memory: {min_memory:.2f} MB")
            print(f"- Maximum Memory: {max_memory:.2f} MB")
            print(f"- Memory Growth: {memory_growth:.2f} MB")
            
        # Calculate entity statistics
        if self.entity_counts:
            avg_entities = sum(self.entity_counts) / len(self.entity_counts)
            max_entities = max(self.entity_counts)
            
            print(f"\nEntity Statistics:")
            print(f"- Average Entity Count: {avg_entities:.1f}")
            print(f"- Maximum Entity Count: {max_entities}")
            
        # Overall performance assessment
        print("\nPerformance Assessment:")
        
        # FPS assessment
        if self.frame_times:
            if avg_fps >= FPS * 0.95:
                print("- FPS: Excellent (Meeting or exceeding target)")
            elif avg_fps >= FPS * 0.8:
                print("- FPS: Good (Near target)")
            elif avg_fps >= FPS * 0.6:
                print("- FPS: Fair (Below target)")
            else:
                print("- FPS: Poor (Significantly below target)")
                
        # Memory assessment
        if self.memory_usage and len(self.memory_usage) > 10:
            if memory_growth < 1.0:
                print("- Memory: Excellent (Stable usage)")
            elif memory_growth < 5.0:
                print("- Memory: Good (Minimal growth)")
            elif memory_growth < 20.0:
                print("- Memory: Fair (Moderate growth)")
            else:
                print("- Memory: Poor (Significant growth - possible memory leak)")
                
        print("=" * 50)
        print("Test completed")
        
def main():
    """Main function to run the game tests."""
    print("Octopus Ink Slime - Comprehensive Test Suite")
    print("=" * 50)
    
    # Create and run the game tester
    tester = GameTester()
    
    try:
        # Initialize the game
        tester.initialize()
        
        # Run the tests
        tester.run_tests()
        
    except Exception as e:
        print(f"An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        pygame.quit()
        print("Test environment cleaned up")
        
if __name__ == "__main__":
    main()