def display_board(board):
    size = board.size
    print("   " + " ".join(f"{i+1:2}" for i in range(size)))
    for idx in range(size):
        row_str = f"{idx+1:2} "
        for jdx in range(size):
            cell = board.get_cell(idx, jdx)
            if cell == 1:
                row_str += " X"
            elif cell == -1:
                row_str += " O"
            else:
                row_str += " ."
        print(row_str)

def get_human_move(board):
    size = board.size
    while True:
        try:
            move = input(f"Enter your move as 'row col' (1-{size} 1-{size}): ")
            parts = move.strip().split()
            if len(parts) != 2:
                print("Invalid input format. Please enter two numbers separated by space.")
                continue
            row_str, col_str = parts
            row, col = int(row_str) - 1, int(col_str) - 1
            if not (0 <= row < size and 0 <= col < size):
                print("Move out of bounds. Try again.")
                continue
            if board.get_cell(row, col) != 0:
                print("Cell already occupied. Try again.")
                continue
            return row, col
        except ValueError:
            print("Invalid input format. Please enter two valid numbers separated by space.")