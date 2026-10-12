import unittest
from unittest.mock import MagicMock
import pygame
import os

# Import the PongGame class from your specific file name
from pypong import PongGame, WIDTH 

class TestPyPong(unittest.TestCase):
    def setUp(self):
        """Initialize the game instance before each test."""
        # Use 'dummy' driver so tests can run without a monitor (headless)
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        self.game = PongGame()

    def tearDown(self):
        """Clean up after each test."""
        pygame.quit()

    def test_initial_state(self):
        """Test 1: Verify that PyPong starts in the MENU state with default values."""
        self.assertEqual(self.game.state, "MENU")
        self.assertEqual(self.game.player_score, 0)
        self.assertEqual(self.game.ai_score, 0)
        self.assertEqual(self.game.win_score, 10)

    def test_menu_navigation_logic(self):
        """Test 2: Verify that menu selection logic updates the internal state correctly."""
        # Simulate pressing 'DOWN' on the menu to select "Win Score"
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_DOWN
        
        self.game.handle_menu_input(mock_event)
        # The menu index should have moved from 0 to 1
        self.assertEqual(self.game.menu_index, 1)
        
        # Simulate pressing 'RETURN' on "Win Score"
        mock_event.key = pygame.K_RETURN
        self.game.handle_menu_input(mock_event)
        
        # The win score should have incremented from 10 to 15 per your logic
        self.assertEqual(self.game.win_score, 15)
        self.assertIn("Win Score: 15", self.game.menu_options[1])

    def test_scoring_and_game_over(self):
        """Test 3: Verify that scoring correctly triggers the GAME_OVER state in PyPong."""
        # Set game to PLAYING state manually to bypass menu
        self.game.state = "PLAYING"
        self.game.player_score = 9 # One point away from winning
        self.game.win_score = 10
        
        # Simulate the ball going past the AI (right side)
        # We manipulate the ball position to trigger the scoring logic in update()
        self.game.ball_x = WIDTH + 5 
        self.game.ball_dx = 5
        
        # Run one update cycle
        self.game.update()
        
        # Check if player score incremented and state changed to GAME_OVER
        self.assertEqual(self.game.player_score, 10)
        self.assertEqual(self.game.state, "GAME_OVER")

if __name__ == "__main__":
    unittest.main()
