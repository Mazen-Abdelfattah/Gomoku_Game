class Player:
    """
    Abstract base class for players
    """
    def __init__(self, symbol):
        """
        Initialize a player
        
        Args:
            symbol: Player's symbol (1 for player 1, -1 for player 2)
        """
        self.symbol = symbol
    
    def get_move(self, board):
        """
        Get the player's move
        
        Args:
            board: The game board
            
        Returns:
            tuple: (row, col) position to place the piece
        """
        raise NotImplementedError("Subclasses must implement get_move()")


class HumanPlayer(Player):
    """
    Human player that makes moves based on user input
    """
    def get_move(self, board):
        """
        Get the human player's move from input
        
        Args:
            board: The game board
            
        Returns:
            tuple: (row, col) position to place the piece
        """
        # This is just a placeholder, the actual implementation is in console_ui.py
        # The implementation is separated to maintain a clean separation of UI and logic
        pass


class AIPlayer(Player):
    """
    AI player that makes moves using a search algorithm
    """
    def __init__(self, symbol, algorithm, depth=3, eval_fn=None):
        """
        Initialize an AI player
        
        Args:
            symbol: Player's symbol (1 for player 1, -1 for player 2)
            algorithm: Search algorithm to use (minimax or alpha-beta)
            depth: Maximum search depth
            eval_fn: Board evaluation function
        """
        super().__init__(symbol)
        self.algorithm = algorithm
        self.depth = depth
        from ai.evaluation import evaluate_board
        self.eval_fn = eval_fn or evaluate_board
    
    def get_move(self, board):
        """
        Get the AI player's move by running the search algorithm
        
        Args:
            board: The game board
            
        Returns:
            tuple: (row, col) position to place the piece
        """
        from game.game_rules import get_valid_moves_with_heuristics
        
        # For the first move on an empty board, just place in the center
        if not board.move_history:
            center = board.size // 2
            return center, center
        
        # Run the search algorithm
        if self.algorithm.__name__ == 'minimax':
            _, move = self.algorithm(board, self.depth, self.symbol == 1, self.eval_fn, self.symbol)
        else:  # alpha-beta
            _, move = self.algorithm(board, self.depth, float('-inf'), float('inf'), 
                                    self.symbol == 1, self.eval_fn, self.symbol)
        
        return move
