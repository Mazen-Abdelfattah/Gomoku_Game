class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.last_move = None
        self.move_history = []
    
    def place_piece(self, row, col, player):
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        self.last_move = (row, col, player)
        self.move_history.append((row, col, player))
        return True
    
    def is_valid_move(self, row, col):
        # Check if position is within board bounds
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        
        # Check if position is already occupied
        return self.board[row][col] == 0
    
    def get_valid_moves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves
    
    def get_restricted_valid_moves(self, proximity=2):
        """
        Get valid moves that are close to existing pieces
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
        if not self.move_history:
            return False
        
        last_row, last_col, _ = self.move_history.pop()
        self.board[last_row][last_col] = 0
        
        self.last_move = self.move_history[-1] if self.move_history else None
        return True
    
    def is_full(self):
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
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = value
            return True
        return False


