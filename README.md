# Chess in Python (Pygame)

A desktop chess game built with Python and Pygame.  
Current implementation includes core rules, special moves, turn handling, check/checkmate detection, promotion choice UI, and game-over actions.

## Features
- Drag-and-drop piece movement
- Turn-based play (`white` then `black`)
- Legal move validation for all pieces
- Special moves:
- Castling
- En passant
- Pawn promotion with UI choice (`Queen`, `Rook`, `Bishop`, `Knight`)
- Check and checkmate detection
- Checkmate overlay with:
- `Play Again`
- `Quit`
- Move and capture sounds
- Cached piece images for smoother dragging/rendering

## Controls
- Left click on your piece to pick it up
- Drag to a target square and release to move
- On promotion, click the piece you want
- On checkmate, click:
- `Play Again` to reset the board
- `Quit` to close the app

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
- `src/main.py`: Entry point, event loop, overlays (promotion/game-over), input handling
- `src/game.py`: Game state, turn state, sound handling, reset/status updates
- `src/board.py`: Board model, move legality, special rules, check/checkmate logic
- `src/piece.py`: Piece classes and texture/image setup
- `src/dragger.py`: Drag behavior and dragged-piece rendering
- `src/square.py`: Square container model
- `assets/images/`: Piece sprite assets
- `assets/sounds/`: Move and capture audio assets

## Current Rule Coverage
- Normal legal moves for pawn, rook, knight, bishop, queen, king
- Castling with path and attack checks
- En passant capture
- Promotion flow with explicit piece selection
- Self-check prevention (illegal if your king would remain in check)
- Check and checkmate detection

## Known Limitations
- Stalemate is not implemented yet
- Draw rules are not implemented yet:
- Threefold repetition
- Fifty-move rule
- Insufficient material
- Promotion UI uses text buttons (no piece icons yet)

## Suggested Next Steps
- Add stalemate and draw rule detection
- Add legal move highlighting for selected pieces
- Show check/checkmate status in on-board HUD (not only console)
- Add move history and undo
- Add tests for board logic and special move edge cases
