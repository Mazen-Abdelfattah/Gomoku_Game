import tkinter as tk
from tkinter import messagebox, ttk
from game.board import Board
from game.game_rules import check_win, is_board_full
from game.player import AIPlayer, HumanPlayer
from ai.minmax import minimax
from ai.alphabeta import alpha_beta
import time

CELL_SIZE = 40


class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku")

        # --- Game Options ---
        self.setup_frame = tk.Frame(root)
        self.setup_frame.pack(pady=10)

        # Game mode
        tk.Label(self.setup_frame, text="Game Mode:").grid(row=0, column=0)
        self.game_mode = ttk.Combobox(self.setup_frame, values=["Human vs AI", "AI vs AI"])
        self.game_mode.current(0)
        self.game_mode.grid(row=0, column=1)

        # Board size
        tk.Label(self.setup_frame, text="Board Size (9-19):").grid(row=1, column=0)
        self.board_size_var = tk.IntVar(value=15)
        tk.Entry(self.setup_frame, textvariable=self.board_size_var, width=5).grid(row=1, column=1)

        # AI algorithm
        tk.Label(self.setup_frame, text="AI Algorithm:").grid(row=2, column=0)
        self.algorithm_var = ttk.Combobox(self.setup_frame, values=["alphabeta", "minimax"])
        self.algorithm_var.current(0)
        self.algorithm_var.grid(row=2, column=1)

        # AI Depth
        tk.Label(self.setup_frame, text="AI Depth:").grid(row=3, column=0)
        self.depth_var = tk.IntVar(value=3)
        tk.Entry(self.setup_frame, textvariable=self.depth_var, width=5).grid(row=3, column=1)

        # Move Limit (for AI vs AI)
        tk.Label(self.setup_frame, text="Move Limit (AI vs AI):").grid(row=4, column=0)
        self.move_limit_var = tk.StringVar(value="")
        tk.Entry(self.setup_frame, textvariable=self.move_limit_var, width=5).grid(row=4, column=1)

        # Start button
        tk.Button(self.setup_frame, text="Start Game", command=self.start_game).grid(row=5, column=0, columnspan=2,
                                                                                     pady=10)

        # Canvas & Status
        self.canvas = None
        self.status = None

    def start_game(self):
        try:
            size = int(self.board_size_var.get())
            if not (9 <= size <= 19):
                raise ValueError("Board size out of range.")
        except:
            messagebox.showerror("Error", "Board size must be an integer between 9 and 19.")
            return

        self.board_size = size
        self.board = Board(size=self.board_size)

        algo = self.algorithm_var.get()
        depth = int(self.depth_var.get())
        algorithm_fn = alpha_beta if algo == "alphabeta" else minimax

        self.canvas = tk.Canvas(self.root, width=self.board_size * CELL_SIZE, height=self.board_size * CELL_SIZE)
        self.canvas.pack()
        self.status = tk.Label(self.root, text="Game started.")
        self.status.pack()

        self.draw_board()

        mode = self.game_mode.get()
        if mode == "Human vs AI":
            self.ai = AIPlayer(-1, algorithm=algorithm_fn, depth=depth)
            self.current_player = 1  # human
            self.canvas.bind("<Button-1>", self.handle_click_human_vs_ai)
            self.status.config(text="Your turn (X)")
        else:
            self.ai1 = AIPlayer(1, algorithm=minimax, depth=depth)
            self.ai2 = AIPlayer(-1, algorithm=algorithm_fn, depth=depth)
            self.current_player = self.ai1
            self.ai_vs_ai(move_limit=self.move_limit_var.get())

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                symbol = self.board.get_cell(i, j)
                if symbol == 1:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
                elif symbol == -1:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")

    def handle_click_human_vs_ai(self, event):
        if self.current_player != 1:
            return
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if self.board.get_cell(row, col) == 0:
            self.board.place_piece(row, col, 1)
            self.draw_board()

            if check_win(self.board, row, col):
                self.status.config(text="You won!")
                messagebox.showinfo("Game Over", "You won!")
                return

            if is_board_full(self.board):
                self.status.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                return

            self.current_player = -1
            self.status.config(text="AI is thinking...")
            self.root.after(100, self.ai_move)

    def ai_move(self):
        row, col = self.ai.get_move(self.board)
        self.board.place_piece(row, col, -1)
        self.draw_board()

        if check_win(self.board, row, col):
            self.status.config(text="AI won!")
            messagebox.showinfo("Game Over", "AI won!")
            return

        if is_board_full(self.board):
            self.status.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.status.config(text="Your turn (X)")
        self.current_player = 1

    def ai_vs_ai(self, move_limit=None):
        try:
            move_limit = int(move_limit) if move_limit else None
        except:
            move_limit = None

        self.ai_move_count = 0
        self.ai_max_moves = move_limit
        self.ai_turn()

    def ai_turn(self):
        if self.ai_max_moves is not None and self.ai_move_count >= self.ai_max_moves:
            self.status.config(text="Move limit reached. Draw.")
            messagebox.showinfo("Game Over", "Move limit reached. Draw.")
            return

        row, col = self.current_player.get_move(self.board)
        self.board.place_piece(row, col, self.current_player.symbol)
        self.draw_board()

        if check_win(self.board, row, col):
            winner = "Minimax AI" if self.current_player.symbol == 1 else "Alpha-Beta AI"
            self.status.config(text=f"{winner} won!")
            messagebox.showinfo("Game Over", f"{winner} won!")
            return

        if is_board_full(self.board):
            self.status.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.current_player = self.ai1 if self.current_player == self.ai2 else self.ai2
        self.ai_move_count += 1
        self.status.config(text=f"{'Minimax' if self.current_player.symbol == 1 else 'Alpha-Beta'} is thinking...")
        self.root.after(500, self.ai_turn)


if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()
