from board import Board
from piece import Pawn, Knight, Bishop, Rook, Queen, King

PIECE_CLASS = {
    "pawn" : Pawn,
    "knight" : Knight,
    "bishop" : Bishop,
    "rook" : Rook,
    "queen" : Queen,
    "king" : King,
}

def get_all_legal_moves(board,color):
    moves = []

    for sr in range(8):
        for sc in range(8):
            square = board.squares[sr][sc]
            if not square.has_piece():
                continue
            piece = square.piece

            if piece.color != color:
                continue

            for tr in range(8):
                for tc in range(8):
                    if sr==tr and sc == tc:
                        continue

                    target = board.squares[tr][tc]

                    if target.has_piece() and target.piece.color == color:
                        continue
                    if not board.is_valid_move(piece, sr, sc, tr, tc):
                        continue

                    if board._would_leave_king_in_check(piece, sr, sc, tr, tc):
                        continue

                    moves.append((sr, sc, tr, tc))
            
            return moves
        
def clone_board(board):
    new_board = Board()

    #clear auto-setup pieces
    for r in range(8):
        for c in range(8):
            new_board.squares[r][c].piece = None

    #copy pieces

    for r in range(8):
        for c in range(8):
            sq = board.squares[r][c]

            if not sq.has_piece():
                continue

            p = sq.piece
            np = PIECE_CLASS[p.name](p.color)
            np.moved = p.moved
            new_board.sqaures[r][c].piece = np

        new_board.en_passant_square = board.en_passant_square
        new_board.pending_promotion = board.pending_promotion

        return new_board
    
def apply_move(board,move):
    sr, sc, tr, tc = move
    new_board = clone_board(board)
    moved, _ = new_board.try_move(sr, sc, tr, tc)

    if moved and new_board.has_pending_promotion():
        new_board.promote_pawn("queen")
    return new_board
    
def evaluate(board,ai_color):
    score = 0.0
    for r in range(8):
        for c in range(8):
            sq = board.squares[r][c]
            if sq.has_piece():
                score += sq.piece.value #white positive, Black Negative
    return score if ai_color == "white" else -score
