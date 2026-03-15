# Chess in Python (Pygame)

A desktop chess game built with Python and Pygame. Play locally in two-player mode or against a basic AI. The game enforces legal moves, handles special rules, and includes UI feedback for game states.

## Highlights
- Two modes: `PVP` (two players, one machine) and `vs AI` (Human as White vs AI as Black)
- Drag-and-drop movement with full legality checks
- Special moves: castling and en passant
- Promotion UI with selectable piece (`Queen`, `Rook`, `Bishop`, `Knight`)
- Check, checkmate, and draw detection
- Move/capture sound effects
- Game-over overlay with `Play Again` and `Quit`
- On-screen mode banner and quick toggle

## Controls
- Left click and drag a piece to move
- Press `M` to toggle between `PVP` and `vs AI` (this resets the game)
- On promotion, click the piece to promote into
- On game over, click `Play Again` to reset or `Quit` to exit

## Requirements
- Python 3.10+
- `pygame`

## Installation
```bash
pip install pygame
```

## Run
From the project root:
```bash
python src/main.py
```

## AI Configuration
Defaults in `src/main.py`:
- `self.game_mode = "ai"`
- `self.ai_color = "black"`
- `self.human_color = "white"`
- `self.ai_depth = 2`

Increase `self.ai_depth` for stronger but slower AI.

## Project Structure
- `src/main.py`: app entry point, event loop, overlays, mode switching, AI turn execution
- `src/game.py`: game/session state, sounds, draw/checkmate status updates
- `src/board.py`: board model, move legality, special rules, draw/check helpers
- `src/ai.py`: minimax + alpha-beta pruning and board evaluation
- `src/piece.py`: piece classes and texture loading
- `src/dragger.py`: drag interaction handling
- `src/square.py`: square model
- `assets/images/`: piece sprites
- `assets/sounds/`: move/capture audio

## Rule Coverage
Implemented:
- Standard movement rules for all pieces
- Self-check prevention
- Castling
- En passant
- Promotion with choice UI
- Check/checkmate
- Stalemate
- Insufficient material
- Threefold repetition

Not implemented yet:
- Fifty-move rule

## Tips and Notes
- Mode toggle (`M`) resets the game state.
- AI currently plays Black by default.
- If audio is not available, verify your system audio device and `assets/sounds/` files.

## Next Improvements
- Add fifty-move rule detection
- Add legal-move highlighting for selected pieces
- Add move history and undo
- Add tests for board logic and AI search behavior
- a Full fledge game