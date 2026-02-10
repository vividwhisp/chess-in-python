# Chess in Python (Pygame)

A simple chess game built with Python and Pygame. The focus is on core mechanics: board rendering, drag-and-drop piece movement, basic legal move rules, and move/capture sounds.

## Features
- Drag-and-drop pieces
- Legal move validation for all pieces
- Capture and move sounds
- Clean board rendering with cached piece images

## Controls
- Mouse down on a piece to pick it up
- Drag to a target square
- Release to attempt the move

## Requirements
- Python 3.10+
- Pygame

## Setup
Install dependencies:
```bash
pip install pygame
```

## Run
From the project root:
```bash
python src/main.py
```

## Project Structure
- `src/main.py` Entry point and event loop
- `src/game.py` Game orchestration and sounds
- `src/board.py` Board state and move logic
- `src/piece.py` Piece definitions
- `src/dragger.py` Dragging behavior
- `assets/images/` Piece sprites
- `assets/sounds/` Move and capture sounds

## Notes
- Move rules are implemented, but check/checkmate, castling, and en passant are not yet included.
- Piece images are cached to reduce flicker and improve performance.

## Roadmap
- Add turn system (white/black)
- Implement check and checkmate detection
- Add castling and en passant
- Highlight legal moves

