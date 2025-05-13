# Heuristic functions to evaluate board positions
# Pattern recognition for threats (open/closed sequences)

def evaluate_board(board, player):
    """
    Evaluate the board state from the perspective of the given player.
    
    Args:
        board: The current board state
        player (int): The player number (1 or 2)
        
    Returns:
        float: A score indicating how good the board is for the player
                (higher is better for the player)
    """
    opponent = 3 - player  # 1 -> 2, 2 -> 1
    
    # Score for player's patterns
    player_score = evaluate_patterns(board, player)
    
    # Score for opponent's patterns (negative because opponent's advantage is bad for player)
    opponent_score = evaluate_patterns(board, opponent)
    
    # Return the difference
    return player_score - opponent_score


def evaluate_patterns(board, player):
    """
    Evaluate the board by looking for various patterns of stones.
    
    Args:
        board: The current board state
        player (int): The player number (1 or 2)
        
    Returns:
        float: A score based on stone patterns
    """
    score = 0
    
    # The directions to check: horizontal, vertical, diagonal, anti-diagonal
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal
        (1, -1)   # Anti-diagonal
    ]
    
    # Check all positions on the board
    for row in range(board.size):
        for col in range(board.size):
            # For each position, check in all directions
            for dr, dc in directions:
                # Skip if we don't have enough space in this direction
                if (row + 4*dr >= board.size or 
                    row + 4*dr < 0 or 
                    col + 4*dc >= board.size or 
                    col + 4*dc < 0):
                    continue
                
                # Extract the 5-stone segment
                segment = [board.board[row + i*dr][col + i*dc] for i in range(5)]
                
                # Calculate the pattern score for this segment
                score += evaluate_segment(segment, player)
    
    return score


def evaluate_segment(segment, player):
    """
    Evaluate a segment of 5 consecutive positions.
    
    Args:
        segment (list): List of 5 consecutive board positions
        player (int): The player number (1 or 2)
        
    Returns:
        float: Score based on the pattern found
    """
    opponent = 3 - player
    
    # Count player and opponent stones in the segment
    player_count = segment.count(player)
    opponent_count = segment.count(opponent)
    empty_count = segment.count(0)
    
    # If there are both player and opponent stones, no potential for 5 in a row
    if player_count > 0 and opponent_count > 0:
        return 0
    
    # If there are only player stones and empty spaces
    if player_count > 0 and empty_count > 0:
        # Score based on the number of player stones (exponential scoring)
        if player_count == 4:   # 4 in a row, one move away from winning
            return 1000
        elif player_count == 3: # 3 in a row
            return 100
        elif player_count == 2: # 2 in a row
            return 10
        elif player_count == 1: # 1 stone
            return 1
    
    # If there are only opponent stones and empty spaces
    if opponent_count > 0 and empty_count > 0:
        # We'll score defensively but slightly lower than offensive scores
        if opponent_count == 4:   # Block opponent's 4 in a row
            return 900
        elif opponent_count == 3: # Block opponent's 3 in a row
            return 90
        elif opponent_count == 2: # Block opponent's 2 in a row
            return 9
        elif opponent_count == 1: # Block opponent's 1 stone
            return 0
    
    # Empty segment
    return 0