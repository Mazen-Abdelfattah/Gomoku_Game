"""
Tests for the Board class.
"""

import unittest
from game.board import Board


class TestBoard(unittest.TestCase):
    """Test suite for the Board class."""
    
    def setUp(self):
        """Set up a new board for each test."""
        self.board = Board(size=15)
    
    def test_board_initialization(self):
        """Test board initialization."""
        self.assertEqual(self.board.size, 15)
        self.assertEqual(len(self.board.grid), 15)
        self.assertEqual(len(self.board.grid[0]), 15)
        self.assertEqual(self.board.grid[0][0], 0)
        self.assertEqual(len(self.board.history), 0)
        self.assertIsNone(self.board.last_move)
    
    def test_place_stone(self):
        """Test placing a stone on the board."""
        # Place stone at (3, 4) for player 1
        self.assertTrue(self.board.place_stone(3, 4, 1))
        self.assertEqual(self.board.grid[3][4], 1)
        self.assertEqual(self.board.last_move, (3, 4))
        self.assertEqual(len(self.board.history), 1)
        self.assertEqual(self.board.history[0], (3, 4, 1))
        
        # Place stone at (5, 6) for player 2
        self.assertTrue(self.board.place_stone(5, 6, 2))
        self.assertEqual(self.board.grid[5][6], 2)
        self.assertEqual(self.board.last_move, (5, 6))
        self.assertEqual(len(self.board.history), 2)
        self.assertEqual(self.board.history[1], (5, 6, 2))
    
    def test_invalid_moves(self):
        """Test invalid moves."""
        # Place stone at (3, 4)
        self.board.place_stone(3, 4, 1)
        
        # Try to place on the same spot
        self.assertFalse(self.board.place_stone(3, 4, 2))
        
        # Try to place outside the board
        self.assertFalse(self.board.place_stone(-1, 0, 1))
        self.assertFalse(self.board.place_stone(0, -1, 1))
        self.assertFalse(self.board.place_stone(15, 0, 1))
        self.assertFalse(self.board.place_stone(0, 15, 1))
    
    def test_undo_move(self):
        """Test undoing a move."""
        # Place two stones
        self.board.place_stone(3, 4, 1)
        self.board.place_stone(5, 6, 2)
        
        # Undo the last move
        self.board.undo_move()
        self.assertEqual(self.board.grid[5][6], 0)
        self.assertEqual(self.board.last_move, (3, 4))
        self.assertEqual(len(self.board.history), 1)
        
        # Undo the first move
        self.board.undo_move()
        self.assertEqual(self.board.grid[3][4], 0)
        self.assertIsNone(self.board.last_move)
        self.assertEqual(len(self.board.history), 0)
        
        # Try to undo with no history
        self.assertIsNone(self.board.undo_move())
    
    def test_is_valid_move(self):
        """Test checking if a move is valid."""
        # Test valid moves
        self.assertTrue(self.board.is_valid_move(0, 0))
        self.assertTrue(self.board.is_valid_move(7, 7))
        self.assertTrue(self.board.is_valid_move(14, 14))
        
        # Place a stone
        self.board.place_stone(7, 7, 1)
        
        # Test invalid moves
        self.assertFalse(self.board.is_valid_move(7, 7))  # Occupied
        self.assertFalse(self.board.is_valid_move(-1, 0))  # Out of bounds
        self.assertFalse(self.board.is_valid_move(0, -1))  # Out of bounds
        self.assertFalse(self.board.is_valid_move(15, 0))  # Out of bounds
        self.assertFalse(self.board.is_valid_move(0, 15))  # Out of bounds
    
    def test_get_valid_moves(self):
        """Test getting valid moves."""
        # An empty board should have 15x15 = 225 valid moves
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(len(valid_moves), 15 * 15)
        
        # Place a stone and check again
        self.board.place_stone(7, 7, 1)
        valid_moves = self.board.get_valid_moves()
        self.assertEqual(len(valid_moves), 15 * 15 - 1)
        self.assertNotIn((7, 7), valid_moves)
    
    def test_is_full(self):
        """Test checking if the board is full."""
        # New board should not be full
        self.assertFalse(self.board.is_full())
        
        # Fill the board
        for row in range(15):
            for col in range(15):
                self.board.place_stone(row, col, 1)
        
        # Board should now be full
        self.assertTrue(self.board.is_full())
    
    def test_get_stone(self):
        """Test getting a stone at a specific position."""
        # Empty position
        self.assertEqual(self.board.get_stone(0, 0), 0)
        
        # Place stones and check
        self.board.place_stone(3, 4, 1)
        self.assertEqual(self.board.get_stone(3, 4), 1)
        
        self.board.place_stone(5, 6, 2)
        self.assertEqual(self.board.get_stone(5, 6), 2)
        
        # Out of bounds
        self.assertIsNone(self.board.get_stone(-1, 0))
        self.assertIsNone(self.board.get_stone(0, -1))
        self.assertIsNone(self.board.get_stone(15, 0))
        self.assertIsNone(self.board.get_stone(0, 15))


if __name__ == "__main__":
    unittest.main()