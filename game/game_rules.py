def check_win(board, row, col):
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
        count = 1 
        
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
    
    if is_board_full(board):
        return 'draw'
    
    return 'in_progress'


def get_valid_moves_with_heuristics(board, distance=2):
    size = board.size
    valid_moves = set()
    for row in range(size):
        for col in range(size):
            if board.get_cell(row, col) != 0:
                for dr in range(-distance, distance + 1):
                    for dc in range(-distance, distance + 1):
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < size and 0 <= nc < size and board.get_cell(nr, nc) == 0:
                            valid_moves.add((nr, nc))

    # Fallback: first move or isolated stones
    if not valid_moves:
        center = size // 2
        return [(center, center)]

    return list(valid_moves)


class GameRules:
    pass