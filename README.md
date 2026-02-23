# Chess in Python (Pygame)

A desktop chess game built with Python and Pygame.
The current implementation is **Human (White) vs AI (Black)**, with core chess rules, promotion UI, and game-over overlays.

## Features
- Drag-and-drop piece movement
- Turn-based play with automatic AI response
- Minimax AI with alpha-beta pruning (`src/ai.py`)
- Legal move validation for all pieces
- Special moves: castling and en passant
- Pawn promotion with UI choice (`Queen`, `Rook`, `Bishop`, `Knight`) and piece icons
- Check, checkmate, and stalemate detection
- Game-over overlay with `Play Again` and `Quit`
- Move and capture sounds
- Cached piece images for smoother rendering

## Game Mode
- You play as **White**
- AI plays as **Black**
- AI defaults to depth `2`

To tweak AI settings, update these values in `src/main.py`:
- `self.ai_color = "black"`
- `self.ai_depth = 2`

## Controls
- Left click your piece to pick it up
- Drag to a target square and release to move
- On promotion, click the piece you want
- On game over, click `Play Again` to reset
- On game over, click `Quit` to close the app

## Requirements
- Python 3.10+
- Pygame

## Setup
```bash
pip install pygame
```

## Run
From the project root:
```bash
python src/main.py
```

## Project Structure
- `src/main.py`: Entry point, event loop, overlays, player input, AI turn handling
- `src/game.py`: Game state, turn state, sound playback, reset/status updates
- `src/board.py`: Board model, legality checks, special rules, check/checkmate/stalemate logic
- `src/ai.py`: Move generation, board cloning, evaluation, minimax search
- `src/piece.py`: Piece classes and texture/image setup
- `src/dragger.py`: Drag behavior and dragged-piece rendering
- `src/square.py`: Square data model
- `assets/images/`: Piece sprite assets
- `assets/sounds/`: Move and capture audio assets

## Rule Coverage
- Normal legal moves for pawn, rook, knight, bishop, queen, king
- Castling with path and attack checks
- En passant capture
- Promotion flow with explicit piece selection and icons
- Self-check prevention (illegal if your king remains in check)
- Check, checkmate, and stalemate detection and Insufficient Material Draw

## Known Limitations
- Draw rules beyond stalemate are not implemented yet:
  - Threefold repetition
  - Fifty-move rule

## Suggested Next Steps
- Add draw-rule detection (threefold, fifty-move, insufficient material)
- Add legal move highlighting for selected pieces
- Show check/checkmate/stalemate status in an on-board HUD
- Add move history and undo
- Add tests for board logic and AI behavior
