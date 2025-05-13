def check_win(board, row, col):
    """
    Check if the most recent move at (row, col) has created a winning position
    
    Args:
        board: The game board
        row: Row of the last move
        col: Column of the last move
        
    Returns:
        bool: True if the move resulted in a win, False otherwise
    """
    player = board.get_cell(row, col)
    if player == 0:
        return False
    
    # Define the four directions to check: horizontal, vertical, diagonal, anti-diagonal
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)], # Diagonal
        [(1, -1), (-1, 1)]  # Anti-diagonal
    ]
    
    # Check each direction
    for direction_pair in directions:
        count = 1  # Count the piece at (row, col)
        
        # Check in both directions of the pair
        for dx, dy in direction_pair:
            # Count consecutive pieces in this direction
            for step in range(1, 5):  # We need 5 in a row to win
                r, c = row + dx * step, col + dy * step
                if 0 <= r < board.size and 0 <= c < board.size and board.get_cell(r, c) == player:
                    count += 1
                else:
                    break
            
            if count >= 5:
                return True  # Player has at least 5 in a row
        
        if count >= 5:
            return True  # Player has at least 5 in a row
    
    return False

def is_board_full(board):
    """
    Check if the board is full (draw condition)
    
    Args:
        board: The game board
        
    Returns:
        bool: True if the board is full, False otherwise
    """
    return board.is_full()

def get_game_state(board):
    """
    Get the current state of the game
    
    Args:
        board: The game board
        
    Returns:
        str: 'player1_win', 'player2_win', 'draw', or 'in_progress'
    """
    # Check if the last move resulted in a win
    if board.last_move:
        row, col, player = board.last_move
        if check_win(board, row, col):
            return 'player1_win' if player == 1 else 'player2_win'
    
    # Check for draw
    if is_board_full(board):
        return 'draw'
    
    # Game is still in progress
    return 'in_progress'

def get_valid_moves_with_heuristics(board, proximity=2):
    """
    Get valid moves with heuristic optimization (prioritizing moves near existing pieces)
    
    Args:
        board: The game board
        proximity: How many cells away from existing pieces to consider
        
    Returns:
        list: List of valid (row, col) positions
    """
    # If this is one of the first moves, consider center and surrounding positions
    if len(board.move_history) < 2:
        center = board.size // 2
        offset = 3  # Consider a 7x7 area around the center for first moves
        moves = []
        for r in range(max(0, center - offset), min(board.size, center + offset + 1)):
            for c in range(max(0, center - offset), min(board.size, center + offset + 1)):
                if board.is_valid_move(r, c):
                    moves.append((r, c))
        return moves
    
    # After the first few moves, only consider moves near existing pieces
    return board.get_restricted_valid_moves(proximity)
