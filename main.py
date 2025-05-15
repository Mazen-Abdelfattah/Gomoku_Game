# main.py - Entry point for the Gomoku game

import time
from game.board import Board
from game.game_rules import check_win, is_board_full
from game.player import HumanPlayer, AIPlayer
from ai.minmax import minimax
from ai.alphabeta import alpha_beta
from ai.evaluation import evaluate_board
from ui.console_ui import display_board, get_human_move

def human_vs_ai_game(board_size=15, ai_algorithm="alphabeta", ai_depth=3):
    """
    Run a Human vs AI game
    
    Args:
        board_size: Size of the board (default: 15x15)
        ai_algorithm: AI algorithm to use ("minimax" or "alphabeta")
        ai_depth: Maximum search depth for the AI
    """
    # Initialize board
    board = Board(size=board_size)
    
    # Create players
    human_player = HumanPlayer(1)  # Human plays as X (1)
    
    # Choose AI algorithm
    if ai_algorithm.lower() == "minimax":
        ai_player = AIPlayer(-1, algorithm=minimax, depth=ai_depth)
    else:
        ai_player = AIPlayer(-1, algorithm=alpha_beta, depth=ai_depth)
    
    # Main game loop
    current_player = human_player  # Human goes first
    
    while True:
        
        # Get current player's move
        if current_player == human_player:
            print(f"\nYour turn (X)")
            row, col = get_human_move(board)
        else:
            print(f"\nAI is thinking...")
            start_time = time.time()
            row, col = current_player.get_move(board)
            end_time = time.time()
            print(f"AI placed at ({row + 1}, {col + 1}) in {end_time - start_time:.2f} seconds")
        
        # Make the move
        board.place_piece(row, col, current_player.symbol)
        display_board(board)  # Show the board after each move
        
        # Check for win
        if check_win(board, row, col):
            winner = "You" if current_player == human_player else "AI"
            print(f"\n{winner} won the game!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("\nGame ended in a draw!")
            break
        
        # Switch player
        current_player = ai_player if current_player == human_player else human_player


def ai_vs_ai_game(board_size=15, ai1_depth=3, ai2_depth=3, max_moves=None):
    """
    Run an AI vs AI game (Minimax vs Alpha-Beta)
    
    Args:
        board_size: Size of the board (default: 15x15)
        ai1_depth: Maximum search depth for Minimax
        ai2_depth: Maximum search depth for Alpha-Beta
        max_moves: Maximum number of moves (to prevent endless games)
    """
    # Initialize board
    board = Board(size=board_size)
    
    # Create AI players
    minimax_player = AIPlayer(1, algorithm=minimax, depth=ai1_depth)
    alphabeta_player = AIPlayer(-1, algorithm=alpha_beta, depth=ai2_depth)
    
    # Stats tracking
    minimax_times = []
    alphabeta_times = []
    move_count = 0
    
    # Main game loop
    current_player = minimax_player  # Minimax goes first
    
    while True:
        
        # Get current player's move
        start_time = time.time()
        
        if current_player == minimax_player:
            print(f"\nMinimax AI is thinking...")
            row, col = current_player.get_move(board)
            end_time = time.time()
            elapsed = end_time - start_time
            minimax_times.append(elapsed)
            print(f"Minimax AI placed at ({row}, {col}) in {elapsed:.2f} seconds")
        else:
            print(f"\nAlpha-Beta AI is thinking...")
            row, col = current_player.get_move(board)
            end_time = time.time()
            elapsed = end_time - start_time
            alphabeta_times.append(elapsed)
            print(f"Alpha-Beta AI placed at ({row}, {col}) in {elapsed:.2f} seconds")
        
        # Make the move
        board.place_piece(row, col, current_player.symbol)
        display_board(board)  # Show the board after each move
        move_count += 1
        
        # Check for win
        if check_win(board, row, col):
            winner = "Minimax AI" if current_player == minimax_player else "Alpha-Beta AI"
            print(f"\n{winner} won the game!")
            break
        
        # Check for draw or move limit
        if is_board_full(board) or (max_moves and move_count >= max_moves):
            print("\nGame ended in a draw!" if is_board_full(board) else "\nGame ended due to move limit!")
            break
        
        # Switch player
        current_player = alphabeta_player if current_player == minimax_player else minimax_player
    
    # Display performance statistics
    if minimax_times:
        avg_minimax_time = sum(minimax_times) / len(minimax_times)
        print(f"\nMinimax average time per move: {avg_minimax_time:.4f} seconds")
    
    if alphabeta_times:
        avg_alphabeta_time = sum(alphabeta_times) / len(alphabeta_times)
        print(f"Alpha-Beta average time per move: {avg_alphabeta_time:.4f} seconds")
    
    if minimax_times and alphabeta_times:
        speedup = sum(minimax_times) / sum(alphabeta_times)
        print(f"Alpha-Beta speedup factor: {speedup:.2f}x")


def main():
    """Main program entry point"""
    print("Welcome to Gomoku (Five in a Row)!")
    print("="*40)
    
    # Game setup
    while True:
        print("\nSelect game mode:")
        print("1. Human vs AI")
        print("2. AI vs AI (Minimax vs Alpha-Beta)")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            # Human vs AI game
            print("\nHuman vs AI Game Setup")
            print("-" * 30)
            
            # Board size selection
            while True:
                try:
                    board_size = int(input("Enter board size (9-19, default 15): ") or 15)
                    if 9 <= board_size <= 19:
                        break
                    else:
                        print("Board size must be between 9 and 19.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # AI algorithm selection
            algorithm = input("Select AI algorithm (minimax/alphabeta, default alphabeta): ").lower() or "alphabeta"
            if algorithm not in ["minimax", "alphabeta"]:
                algorithm = "alphabeta"
                print("Using default: Alpha-Beta pruning")
            
            # AI depth selection
            while True:
                try:
                    depth = int(input(f"Enter AI search depth (1-5, default 3): ") or 3)
                    if 1 <= depth <= 5:
                        break
                    else:
                        print("Depth must be between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Start the game
            human_vs_ai_game(board_size=board_size, ai_algorithm=algorithm, ai_depth=depth)
            
        elif choice == "2":
            # AI vs AI game
            print("\nAI vs AI Game Setup")
            print("-" * 30)
            
            # Board size selection
            while True:
                try:
                    board_size = int(input("Enter board size (9-19, default 15): ") or 15)
                    if 9 <= board_size <= 19:
                        break
                    else:
                        print("Board size must be between 9 and 19.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Minimax depth selection
            while True:
                try:
                    minimax_depth = int(input("Enter Minimax search depth (1-4, default 3): ") or 3)
                    if 1 <= minimax_depth <= 4:
                        break
                    else:
                        print("Depth must be between 1 and 4.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Alpha-Beta depth selection
            while True:
                try:
                    alphabeta_depth = int(input("Enter Alpha-Beta search depth (1-5, default 3): ") or 3)
                    if 1 <= alphabeta_depth <= 5:
                        break
                    else:
                        print("Depth must be between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Move limit selection
            while True:
                try:
                    move_limit = input("Enter maximum number of moves (default 100, press Enter for no limit): ")
                    if move_limit == "":
                        move_limit = None
                        break
                    else:
                        move_limit = int(move_limit)
                        if move_limit > 0:
                            break
                        else:
                            print("Move limit must be a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Start the game
            ai_vs_ai_game(
                board_size=board_size, 
                ai1_depth=minimax_depth, 
                ai2_depth=alphabeta_depth,
                max_moves=move_limit
            )
            
        elif choice == "3":
            print("\nThank you for playing Gomoku!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
