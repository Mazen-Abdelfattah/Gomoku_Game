"""
Tests for the GameRules class.
"""

import unittest
from game.board import Board
from game.game_rules import GameRules


class TestGameRules(unittest.TestCase):
    """Test suite for the GameRules class."""
    
    def setUp(self):
        """Set up a new board for each test."""
        self.board = Board(size=15)
        self.rules = GameRules()
    
    def test_horizontal_win(self):
        """Test horizontal win condition."""
        # Place 5 stones in a horizontal row for player 1
        for col in range(5):
            self.board.place_stone(3, col, 1)
        
        # Check win
        self.assertTrue(self.rules.check_win(self.board, 3, 4, 1))
        self.assertEqual(self.rules.get_game_state(self.board), 'player1_win')
    
    def test_vertical_win(self):
        """Test vertical win condition."""
        # Place 5 stones in a vertical row for player 2
        for row in range(5):
            self.board.place_stone(row, 3, 2)
        
        # Check win
        self.assertTrue(self.rules.check_win(self.board, 4, 3, 2))
        self.assertEqual(self.rules.get_game_state(self.board), 'player2_win')
    
    def test_diagonal_win(self):
        """Test diagonal win condition."""
        # Place 5 stones in a diagonal for player 1
        for i in range(5):
            self.board.place_stone(i, i, 1)
        
        # Check win
        self.assertTrue(self.rules.check_win(self.board, 4, 4, 1))
        self.assertEqual(self.rules.get_game_state(self.board), 'player1_win')
    
    def test_antidiagonal_win(self):
        """Test anti-diagonal win condition."""
        # Place 5 stones in an anti-diagonal for player 2
        for i in range(5):
            self.board.place_stone(i, 4-i, 2)
        
        # Check win
        self.assertTrue(self.rules.check_win(self.board, 4, 0, 2))
        self.assertEqual(self.rules.get_game_state(self.board), 'player2_win')
    
    def test_no_win(self):
        """Test no win condition."""
        # Place 4 stones in a row (not enough to win)
        for col in range(4):
            self.board.place_stone(3, col, 1)
        
        # Check no win
        self.assertFalse(self.rules.check_win(self.board, 3, 3, 1))
        self.assertEqual(self.rules.get_game_state(self.board), 'ongoing')
    
    def test_draw(self):
        """Test draw condition."""
        # Create a custom board that's almost full
        self.board = Board(size=3)
        
        # Fill the board without creating a win
        # First two rows
        for row in range(2):
            for col in range(3):
                player = (row + col) % 2 + 1
                self.board.place_stone(row, col, player)
        
        # Last row (except last cell)
        self.board.place_stone(2, 0, 1)
        self.board.place_stone(2, 1, 2)
        
        # Game still ongoing
        self.assertEqual(self.rules.get_game_state(self.board), 'ongoing')
        
        # Fill the last cell
        self.board.place_stone(2, 2, 1)
        
        # Now it should be a draw
        self.assertTrue(self.rules.check_draw(self.board))
        self.assertEqual(self.rules.get_game_state(self.board), 'draw')
    
    def test_complex_game_state(self):
        """Test more complex game states."""
        # Create a game where both players have 4 in a row
        for col in range(4):
            self.board.place_stone(3, col, 1)  # Player 1
            self.board.place_stone(5, col, 2)  # Player 2
        
        # No win yet
        self.assertEqual(self.rules.get_game_state(self.board), 'ongoing')
        
        # Player 1 completes 5 in a row
        self.board.place_stone(3, 4, 1)
        
        # Player 1 should win
        self.assertEqual(self.rules.get_game_state(self.board), 'player1_win')


if __name__ == "__main__":
    unittest.main()