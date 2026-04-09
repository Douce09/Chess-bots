# Chess-bots

A graphical chess game implemented in Python using Tkinter.

## Features

- Complete chess board with all pieces
- Graphical user interface with clickable squares
- Basic movement and capture rules for all pieces
- Turn-based gameplay (white and black)
- Unicode chess piece symbols
- Game ends when a king is captured
- **Black player automatically makes random legal moves**

## Requirements

- Python 3.6 or higher with Tkinter (usually included)

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/) or using your package manager.

   On Windows, you can install via Microsoft Store or winget:
   ```
   winget install Python.Python.3.11
   ```

2. Ensure Python is in your PATH.

## Running the Game

Run the chess game with:
```
python Chess.py
```
or
```
py Chess.py
```

## How to Play

- The board is displayed graphically with alternating light and dark squares.
- Pieces are shown using Unicode chess symbols.
- **White is the human player. Click on a piece to select it (highlighted in red), then click on the destination square to move the piece.**
- **Black moves automatically with a random legal move after each of your moves.**
- Invalid moves will show an error message.
- The current player's turn is displayed below the board.

## Limitations

- No castling, en passant, or pawn promotion implemented yet.
- No check or checkmate detection (game ends only on king capture).
- Basic validation only; does not prevent moves that put own king in check. 
