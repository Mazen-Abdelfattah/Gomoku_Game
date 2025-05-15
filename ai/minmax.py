from game.game_rules import check_win, get_valid_moves_with_heuristics

def minimax(board, depth, alpha, beta, maximizing_player, eval_fn, player_symbol, max_moves=10):
    """
    Optimized Minimax with Alpha-Beta pruning and heuristic move limiting for Gomoku.

    Args:
        board: Current board state.
        depth: Depth limit for the search.
        alpha: Alpha value for pruning.
        beta: Beta value for pruning.
        maximizing_player: True if maximizing player's turn, False otherwise.
        eval_fn: Evaluation function to score board states.
        player_symbol: Symbol of the current player (1 or -1).
        max_moves: Limit the number of heuristic-based moves to explore per turn.

    Returns:
        Tuple: (best_score, best_move)
    """
    if board.last_move:
        last_row, last_col, _ = board.last_move
        if check_win(board, last_row, last_col):
            if board.get_cell(last_row, last_col) == player_symbol:
                return 1000000, None  # Win
            else:
                return -1000000, None  # Loss

    if depth == 0 or board.is_full():
        return eval_fn(board, player_symbol), None

    valid_moves = get_valid_moves_with_heuristics(board)

    # Sort moves by proximity to last move (helps pruning efficiency)
    if board.last_move:
        last_row, last_col, _ = board.last_move
        valid_moves.sort(key=lambda move: abs(move[0] - last_row) + abs(move[1] - last_col))

    # Limit moves to top-N heuristically chosen
    valid_moves = valid_moves[:max_moves]

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for row, col in valid_moves:
            board.place_piece(row, col, player_symbol)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, eval_fn, player_symbol, max_moves)
            board.undo_last_move()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (row, col)

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff

        return max_eval, best_move

    else:
        min_eval = float('inf')
        opponent = -player_symbol
        for row, col in valid_moves:
            board.place_piece(row, col, opponent)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, eval_fn, player_symbol, max_moves)
            board.undo_last_move()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (row, col)

            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff

        return min_eval, best_move
