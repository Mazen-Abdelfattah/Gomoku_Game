class Board:
    """
    Represents the Gomoku game board
    """
    
    def __init__(self, size=15):
        """
        Initialize the game board
        
        Args:
            size: Size of the board (default: 15x15)
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.last_move = None
        self.move_history = []
    
    def place_piece(self, row, col, player):
        """
        Place a piece on the board
        
        Args:
            row: Row index
            col: Column index
            player: Player symbol (1 for player 1, -1 for player 2)
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        self.last_move = (row, col, player)
        self.move_history.append((row, col, player))
        return True
    
    def is_valid_move(self, row, col):
        """
        Check if a move is valid
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        # Check if position is within board bounds
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        
        # Check if position is already occupied
        return self.board[row][col] == 0
    
    def get_valid_moves(self):
        """
        Get all valid moves on the board
        
        Returns:
            list: List of valid (row, col) positions
        """
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves
    
    def get_restricted_valid_moves(self, proximity=2):
        """
        Get valid moves that are close to existing pieces
        
        Args:
            proximity: How many cells away from existing pieces to consider
            
        Returns:
            list: List of valid (row, col) positions near existing pieces
        """
        candidates = set()
        
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:  # Occupied cell
                    # Add nearby empty cells as candidates
                    for dr in range(-proximity, proximity + 1):
                        for dc in range(-proximity, proximity + 1):
                            nr, nc = row + dr, col + dc
                            if (0 <= nr < self.size and 0 <= nc < self.size and 
                                    self.board[nr][nc] == 0):
                                candidates.add((nr, nc))
        
        return list(candidates) if candidates else self.get_valid_moves()
    
    def get_cell(self, row, col):
        """
        Get the value of a cell on the board
        
        Args:-
            row: Row index
            col: Column index
            
        Returns:
            int: Cell value (0 for empty, 1 for player 1, -1 for player 2)
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return None
    
    def get_board_copy(self):
        """
        Get a copy of the current board state
        
        Returns:
            list: 2D list representing the board
        """
        return [row[:] for row in self.board]
    
    def undo_last_move(self):
        """
        Undo the last move made on the board
        
        Returns:
            bool: True if a move was undone, False if no moves to undo
        """
        if not self.move_history:
            return False
        
        last_row, last_col, _ = self.move_history.pop()
        self.board[last_row][last_col] = 0
        
        self.last_move = self.move_history[-1] if self.move_history else None
        return True
    
    def is_full(self):
        """
        Check if the board is full
        
        Returns:
            bool: True if the board is full, False otherwise
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return False
        return True
    
    def clear(self):
        """
        Clear the board to its initial state
        """
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None
        self.move_history = []
        
        
    def set_cell(self, row, col, value): 
        """
        Set the value of a cell on the board

        Args:
            row: Row index
            col: Column index
            value: Value to set (0 for empty, 1 for player 1, -1 for player 2)

        Returns:
            bool: True if the cell was set, False if out of bounds
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = value
            return True
        return False


