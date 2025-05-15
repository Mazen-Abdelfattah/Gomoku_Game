def order_moves(board, moves, player):
    """
    Order moves for better alpha-beta pruning efficiency.
        
    Returns:
        list: Ordered list of (row, col) tuples
    """
    opponent = 3 - player  # 1 -> 2, 2 -> 1
    
    # Assign a score to each move
    move_scores = []
    for row, col in moves:
        score = score_move(board, row, col, player, opponent)
        move_scores.append((score, row, col))
    
    # Sort moves by score (higher score first)
    move_scores.sort(reverse=True)
    
    # Return ordered moves
    return [(row, col) for _, row, col in move_scores]


def score_move(board, row, col, player, opponent):
    """
    Score a move based on patterns it creates/blocks.
    
    Args:
        board: The current board state
        row (int): Row of the move
        col (int): Column of the move
        player (int): The player making the move
        opponent (int): The opponent player
        
    Returns:
        float: Score for the move (higher is better)
    """
    score = 0
    
    # Check in all 8 directions
    directions = [
        (0, 1),   # Right
        (1, 1),   # Down-Right
        (1, 0),   # Down
        (1, -1),  # Down-Left
        (0, -1),  # Left
        (-1, -1), # Up-Left
        (-1, 0),  # Up
        (-1, 1)   # Up-Right
    ]
    
    # Score for creating patterns
    for dr, dc in directions:
        # Place stone temporarily
        
        # board.grid[row][col] = player
        board.set_cell(row, col, player)
        
        # Check patterns for player
        pattern_score = check_pattern_score(board, row, col, dr, dc, player)
        score += pattern_score
        
        # Undo temporary placement
        board.set_cell(row, col, 0)
    
    # Score for blocking opponent's patterns
    for dr, dc in directions:
        # Place opponent's stone temporarily
        
        # board.grid[row][col] = opponent
        board.set_cell(row, col, opponent)
        
        # Check patterns for opponent
        pattern_score = check_pattern_score(board, row, col, dr, dc, opponent)
        score += pattern_score * 0.9  # Blocking is slightly less valuable than creating
        
        # Undo temporary placement
        board.set_cell(row, col, 0)
        
    # Bonus for center and near-center positions
    center = board.size // 2
    distance_from_center = abs(row - center) + abs(col - center)
    center_score = max(0, 5 - distance_from_center) * 2
    score += center_score
    
    return score


def check_pattern_score(board, row, col, dr, dc, player):
    """
    Check for patterns in a specific direction.
    
    Args:
        board: The current board state
        row (int): Row of the move
        col (int): Column of the move
        dr (int): Row direction (-1, 0, or 1)
        dc (int): Column direction (-1, 0, or 1)
        player (int): The player to check patterns for
        
    Returns:
        float: Score based on the patterns found
    """
    # Initialize pattern counts
    open_four = 0   # ●●●●_
    four = 0        # ●●●●
    open_three = 0  # _●●●_
    three = 0       # ●●●
    open_two = 0    # _●●_
    two = 0         # ●●
    
    # Check forward and backward to find patterns
    segment = []
    for i in range(-4, 5):  # Check 9 positions (4 on each side plus the move position)
        r, c = row + i*dr, col + i*dc
        if 0 <= r < board.size and 0 <= c < board.size:
            segment.append(board.get_cell(r, c))
        else:
            segment.append(-1)  # Out of bounds
    
    # Find patterns in the segment
    if len(segment) >= 5:
        # Check for open four: _●●●●_
        if contains_pattern(segment, [0, player, player, player, player, 0], player):
            open_four += 1
        
        # Check for four: ●●●●_ or _●●●●
        if (contains_pattern(segment, [player, player, player, player, 0], player) or
            contains_pattern(segment, [0, player, player, player, player], player)):
            four += 1
        
        # Check for open three: _●●●_
        if contains_pattern(segment, [0, player, player, player, 0], player):
            open_three += 1
        
        # Check for three: ●●●_ or _●●●
        if (contains_pattern(segment, [player, player, player, 0], player) or
            contains_pattern(segment, [0, player, player, player], player)):
            three += 1
        
        # Check for open two: _●●_
        if contains_pattern(segment, [0, player, player, 0], player):
            open_two += 1
        
        # Check for two: ●●_ or _●●
        if (contains_pattern(segment, [player, player, 0], player) or
            contains_pattern(segment, [0, player, player], player)):
            two += 1
    
    # Calculate score based on patterns found
    score = (
        open_four * 1000 +
        four * 100 +
        open_three * 50 +
        three * 10 +
        open_two * 5 +
        two * 1
    )
    
    return score


def contains_pattern(segment, pattern, player):
    """
    Check if a segment contains a specific pattern.
    
    Args:
        segment (list): The segment to check
        pattern (list): The pattern to look for
        player (int): The player's stone type
        
    Returns:
        bool: True if the pattern is found, False otherwise
    """
    for i in range(len(segment) - len(pattern) + 1):
        match = True
        for j in range(len(pattern)):
            if pattern[j] != -1 and segment[i+j] != pattern[j]:
                match = False
                break
        if match:
            return True
    
    return False