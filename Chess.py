import tkinter as tk
from tkinter import messagebox
import random

class ChessBoard:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 'white'
        self.move_history = []
        self.selected_square = None
        self.game_over = False
        self.winner = None

    def initialize_board(self):
        # 8x8 board, rows 0-7, columns 0-7
        board = [['' for _ in range(8)] for _ in range(8)]

        # Place pawns
        for col in range(8):
            board[1][col] = 'pawn_black'
            board[6][col] = 'pawn_white'

        # Place other pieces
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(8):
            board[0][col] = pieces[col] + '_black'
            board[7][col] = pieces[col] + '_white'

        return board

    def get_piece_symbol(self, piece):
        if piece == '':
            return ''
        piece_type, color = piece.split('_')
        symbols = {
            'pawn': {'white': '♙', 'black': '♟'},
            'rook': {'white': '♖', 'black': '♜'},
            'knight': {'white': '♘', 'black': '♞'},
            'bishop': {'white': '♗', 'black': '♝'},
            'queen': {'white': '♕', 'black': '♛'},
            'king': {'white': '♔', 'black': '♚'}
        }
        return symbols[piece_type][color]

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece == '':
            return False
        color = piece.split('_')[1]
        if color != self.current_turn:
            return False

        # Basic checks: not moving to same square, not capturing own piece
        if (start_row, start_col) == (end_row, end_col):
            return False
        target = self.board[end_row][end_col]
        if target != '' and target.split('_')[1] == color:
            return False

        piece_type = piece.split('_')[0]

        # Implement movement rules for each piece
        if piece_type == 'pawn':
            return self.is_valid_pawn_move(start_row, start_col, end_row, end_col, color)
        elif piece_type == 'rook':
            return self.is_valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'knight':
            return self.is_valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'bishop':
            return self.is_valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'queen':
            return self.is_valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece_type == 'king':
            return self.is_valid_king_move(start_row, start_col, end_row, end_col)

        return False

    def is_valid_pawn_move(self, start_row, start_col, end_row, end_col, color):
        direction = -1 if color == 'white' else 1
        start_row_pawn = 6 if color == 'white' else 1

        # Forward move
        if start_col == end_col:
            if end_row == start_row + direction:
                return self.board[end_row][end_col] == ''
            elif end_row == start_row + 2 * direction and start_row == start_row_pawn:
                return self.board[end_row][end_col] == '' and self.board[start_row + direction][start_col] == ''
        # Capture
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return self.board[end_row][end_col] != '' and self.board[end_row][end_col].split('_')[1] != color

        return False

    def is_valid_rook_move(self, start_row, start_col, end_row, end_col):
        if start_row != end_row and start_col != end_col:
            return False
        # Check path is clear
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.board[start_row][col] != '':
                    return False
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self.board[row][start_col] != '':
                    return False
        return True

    def is_valid_knight_move(self, start_row, start_col, end_row, end_col):
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        # Check path is clear
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        while row != end_row:
            if self.board[row][col] != '':
                return False
            row += row_step
            col += col_step
        return True

    def is_valid_queen_move(self, start_row, start_col, end_row, end_col):
        return self.is_valid_rook_move(start_row, start_col, end_row, end_col) or self.is_valid_bishop_move(start_row, start_col, end_row, end_col)

    def is_valid_king_move(self, start_row, start_col, end_row, end_col):
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    def make_move(self, start_row, start_col, end_row, end_col):
        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            return False
        captured = self.board[end_row][end_col]
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ''
        self.move_history.append((start_row, start_col, end_row, end_col, piece))
        if captured and captured.split('_')[0] == 'king':
            self.game_over = True
            self.winner = self.current_turn
        else:
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        return True

    def get_legal_moves(self, color):
        """Returns all legal moves for a given color as a list of tuples (start_row, start_col, end_row, end_col)"""
        legal_moves = []
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board[start_row][start_col]
                if piece == '' or piece.split('_')[1] != color:
                    continue
                for end_row in range(8):
                    for end_col in range(8):
                        if self.is_valid_move(start_row, start_col, end_row, end_col):
                            legal_moves.append((start_row, start_col, end_row, end_col))
        return legal_moves

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = ChessBoard()
        self.square_size = 60
        self.canvas = tk.Canvas(root, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_square_click)
        self.status_label = tk.Label(root, text=f"{self.board.current_turn.capitalize()}'s turn")
        self.status_label.pack()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]  # Light and dark squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board.board[row][col]
                if piece:
                    symbol = self.board.get_piece_symbol(piece)
                    self.canvas.create_text(x1 + self.square_size//2, y1 + self.square_size//2, text=symbol, font=("Arial", 30))
        # Highlight selected square
        if self.board.selected_square:
            row, col = self.board.selected_square
            x1 = col * self.square_size
            y1 = row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def on_square_click(self, event):
        if self.board.game_over:
            return
        col = event.x // self.square_size
        row = event.y // self.square_size
        if self.board.selected_square is None:
            # Select piece
            if self.board.board[row][col] != '':
                self.board.selected_square = (row, col)
                self.draw_board()
        else:
            # Move to square
            start_row, start_col = self.board.selected_square
            if self.board.make_move(start_row, start_col, row, col):
                if self.board.game_over:
                    messagebox.showinfo("Game Over", f"{self.board.winner.capitalize()} wins!")
                    self.status_label.config(text="Game Over")
                else:
                    self.status_label.config(text=f"{self.board.current_turn.capitalize()}'s turn")
                    # Schedule black to move after a delay
                    if self.board.current_turn == 'black':
                        self.root.after(500, self.make_random_black_move)
            else:
                messagebox.showerror("Invalid Move", "That move is not allowed.")
            self.board.selected_square = None
            self.draw_board()

    def make_random_black_move(self):
        """Make a random legal move for the black player"""
        if self.board.game_over or self.board.current_turn != 'black':
            return
        
        legal_moves = self.board.get_legal_moves('black')
        if legal_moves:
            start_row, start_col, end_row, end_col = random.choice(legal_moves)
            if self.board.make_move(start_row, start_col, end_row, end_col):
                self.draw_board()
                if self.board.game_over:
                    messagebox.showinfo("Game Over", f"{self.board.winner.capitalize()} wins!")
                    self.status_label.config(text="Game Over")
                else:
                    self.status_label.config(text=f"{self.board.current_turn.capitalize()}'s turn")

def main():
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()