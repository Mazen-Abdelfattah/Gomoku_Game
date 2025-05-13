def display_board(board):
    """
    Display the Gomoku board in the console.
    Args:
        board (list of list): 2D list representing the board. 
                              0=empty, 1=player1 (X), 2=player2 (O)
    """
    size = len(board)
    # Print column headers
    print("   " + " ".join(f"{i+1:2}" for i in range(size)))
    for idx, row in enumerate(board):
        # Print row number
        row_str = f"{idx+1:2} "
        for cell in row:
            if cell == 1:
                row_str += " X"
            elif cell == 2:
                row_str += " O"
            else:
                row_str += " ."
        print(row_str)

def get_human_move(board):
    """
    Prompt the human player to enter a move.
    Args:
        board (list of list): Current board state.
    Returns:
        tuple: (row, col) as zero-based indices.
    """
    size = 15  # Assuming a standard Gomoku board size, but it should be -> len(board) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    while True:
        try:
            move = input(f"Enter your move as 'row col' (1-{size} 1-{size}): ")
            row_str, col_str = move.strip().split()
            row, col = int(row_str) - 1, int(col_str) - 1
            # if not (0 <= row < size and 0 <= col < size):
            #     print("Move out of bounds. Try again.")
            #     continue
            # if board[row][col] != 0:
            #     print("Cell already occupied. Try again.")
            #     continue
            return row, col
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by space.")

