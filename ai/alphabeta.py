from game.game_rules import check_win, get_valid_moves_with_heuristics
from ai.move_ordering import order_moves

def alpha_beta(board, depth, alpha, beta, maximizing_player, eval_fn, player_symbol):
    """
    Alpha-Beta pruning algorithm for Gomoku
    
    Args:
        board: The current board state
        depth: Maximum search depth
        alpha: Alpha value
        beta: Beta value
        maximizing_player: True if maximizing player's turn, False otherwise
        eval_fn: Function to evaluate board states
        player_symbol: Symbol of the player using this algorithm (1 or -1)
        
    Returns:
        best_score: The score of the best move
        best_move: The best move (row, col)
    """
    # Check for terminal states
    if board.last_move:
        last_row, last_col, _ = board.last_move
        if check_win(board, last_row, last_col):
            if board.get_cell(last_row, last_col) == player_symbol:
                return 100000, None  # Player won
            else:
                return -100000, None  # Opponent won
    
    # If maximum depth reached or board is full
    if depth == 0 or board.is_full():
        return eval_fn(board, player_symbol), None
    
    # Get and order valid moves
    valid_moves = get_valid_moves_with_heuristics(board)
    valid_moves = order_moves(board, valid_moves, player_symbol if maximizing_player else -player_symbol)
    
    if maximizing_player:
        best_score = float('-inf')
        best_move = None
        
        # Try each valid move
        for move in valid_moves:
            row, col = move
            
            # Make the move
            board.place_piece(row, col, player_symbol)
            
            # Recursively evaluate the position
            score, _ = alpha_beta(board, depth - 1, alpha, beta, False, eval_fn, player_symbol)
            
            # Undo the move
            board.undo_last_move()
            
            # Update best score and move
            if score > best_score:
                best_score = score
                best_move = move
            
            # Alpha-Beta pruning
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cutoff
        
        return best_score, best_move
    
    else:  # Minimizing player
        best_score = float('inf')
        best_move = None
        opponent_symbol = -player_symbol
        
        # Try each valid move
        for move in valid_moves:
            row, col = move
            
            # Make the move
            board.place_piece(row, col, opponent_symbol)
            
            # Recursively evaluate the position
            score, _ = alpha_beta(board, depth - 1, alpha, beta, True, eval_fn, player_symbol)
            
            # Undo the move
            board.undo_last_move()
            
            # Update best score and move
            if score < best_score:
                best_score = score
                best_move = move
            
            # Alpha-Beta pruning
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cutoff
        
        return best_score, best_move
