class Player:
    """
    Abstract base class for players
    """
    def __init__(self, symbol):
        """
            symbol: Player's symbol (1 for player 1, -1 for player 2)
        """
        self.symbol = symbol
    
    def get_move(self, board):
        raise NotImplementedError("Subclasses must implement get_move()")


class HumanPlayer(Player):
    def get_move(self, board):
        # This is just a placeholder, the actual implementation is in console_ui.py
        # The implementation is separated to maintain a clean separation of UI and logic
        pass


class AIPlayer(Player):
    def __init__(self, symbol, algorithm, depth=3, eval_fn=None):
        super().__init__(symbol)
        self.algorithm = algorithm
        self.depth = depth
        from ai.evaluation import evaluate_board
        self.eval_fn = eval_fn or evaluate_board
    
    def get_move(self, board):
        from game.game_rules import get_valid_moves_with_heuristics
        
        # For the first move on an empty board, just place in the center
        if not board.move_history:
            center = board.size // 2
            return center, center
        
        # Run the search algorithm
        if self.algorithm.__name__ == 'minimax':
            _, move = self.algorithm(board, self.depth, float('-inf'), float('inf'), self.symbol == 1, self.eval_fn,
                                    self.symbol)
        else:  # alpha-beta
            _, move = self.algorithm(board, self.depth, float('-inf'), float('inf'), 
                                    self.symbol == 1, self.eval_fn, self.symbol)
        
        return move
