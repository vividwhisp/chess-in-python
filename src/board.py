from const import *
from square import Square
from piece import *

class Board:
    def __init__(self):
        self.squares = []
        self.en_passant_square = None

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)

    def _add_pieces(self,color):
        row_pawn , row_other = (6,7) if color == 'white' else (1,0)
         #Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn,col, Pawn(color))
        
        #Knights 

        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        #Bishops

        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        #Rooks

        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        #Queen 

        self.squares[row_other][3] = Square(row_other,3,Queen(color))

        #King 

        self.squares[row_other][4] = Square(row_other,4,King(color))
    
    def try_move(self,start_row,start_col,target_row,target_col):
        # bounds
        if (
            start_row < 0
            or start_row >= ROWS
            or start_col < 0
            or start_col >= COLS
            or target_row < 0
            or target_row >= ROWS
            or target_col < 0
            or target_col >= COLS
        ):
            return False, False

        # same square
        if start_row == target_row and start_col == target_col:
            return False, False

        piece = self.squares[start_row][start_col].piece
        if not piece:
            return False, False

        target_square = self.squares[target_row][target_col]
        if target_square.has_piece() and target_square.piece.color == piece.color:
            return False, False

        if not self.is_valid_move(piece, start_row, start_col, target_row, target_col):
            return False, False

        if self._would_leave_king_in_check(
            piece, start_row, start_col, target_row, target_col
        ):
            return False, False

        is_en_passant = self._is_en_passant_capture(
            piece, start_row, start_col, target_row, target_col
        )
        is_castling = piece.name == "king" and abs(target_col - start_col) == 2
        capture = target_square.has_piece() or is_en_passant

        if is_en_passant:
            captured_row = start_row
            captured_col = target_col
            self.squares[captured_row][captured_col].piece = None

        target_square.piece = piece
        self.squares[start_row][start_col].piece = None

        if is_castling:
            self._move_castling_rook(start_row, start_col, target_col)

        piece.moved = True

        if piece.name == "pawn" and abs(target_row - start_row) == 2:
            self.en_passant_square = ((start_row + target_row) // 2, start_col)
        else:
            self.en_passant_square = None

        if piece.name == "pawn":
            self._promote_pawn_if_needed(target_row, target_col)

        return True, capture

    def is_valid_move(self, piece, start_row, start_col, target_row, target_col):
        dr = target_row - start_row
        dc = target_col - start_col

        # Pawn
        if piece.name == 'pawn':
            direction = piece.dir
            start_row_for_pawn = 6 if piece.color == 'white' else 1

            # forward move (no capture)
            if dc == 0:
                if dr == direction and not self.squares[target_row][target_col].has_piece():
                    return True
                if (
                    start_row == start_row_for_pawn
                    and dr == 2 * direction
                    and not self.squares[start_row + direction][start_col].has_piece()
                    and not self.squares[target_row][target_col].has_piece()
                ):
                    return True

            # diagonal capture
            if abs(dc) == 1 and dr == direction:
                if self.squares[target_row][target_col].has_piece():
                    return True
                if self._is_en_passant_capture(
                    piece, start_row, start_col, target_row, target_col
                ):
                    return True

            return False

        # Knight
        if piece.name == 'knight':
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]

        # King
        if piece.name == 'king':
            if abs(dc) == 2 and dr == 0:
                return self._can_castle(piece, start_row, start_col, target_col)
            return max(abs(dr), abs(dc)) == 1

        # Rook
        if piece.name == 'rook':
            if dr == 0 or dc == 0:
                return self.is_path_clear(start_row, start_col, target_row, target_col)
            return False

        # Bishop
        if piece.name == 'bishop':
            if abs(dr) == abs(dc):
                return self.is_path_clear(start_row, start_col, target_row, target_col)
            return False

        # Queen
        if piece.name == 'queen':
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                return self.is_path_clear(start_row, start_col, target_row, target_col)
            return False

        return False

    def is_path_clear(self, start_row, start_col, target_row, target_col):
        dr = target_row - start_row
        dc = target_col - start_col

        step_row = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_col = 0 if dc == 0 else (1 if dc > 0 else -1)

        current_row = start_row + step_row
        current_col = start_col + step_col

        while current_row != target_row or current_col != target_col:
            if self.squares[current_row][current_col].has_piece():
                return False
            current_row += step_row
            current_col += step_col

        return True

    def is_in_check(self, color):
        king_pos = self._find_king(color)
        if not king_pos:
            return False
        enemy_color = "black" if color == "white" else "white"
        return self.is_square_attacked(king_pos[0], king_pos[1], enemy_color)

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        return not self.has_any_legal_move(color)

    def has_any_legal_move(self, color):
        for start_row in range(ROWS):
            for start_col in range(COLS):
                square = self.squares[start_row][start_col]
                if not square.has_piece():
                    continue

                piece = square.piece
                if piece.color != color:
                    continue

                for target_row in range(ROWS):
                    for target_col in range(COLS):
                        if start_row == target_row and start_col == target_col:
                            continue

                        target_square = self.squares[target_row][target_col]
                        if (
                            target_square.has_piece()
                            and target_square.piece.color == color
                        ):
                            continue

                        if not self.is_valid_move(
                            piece, start_row, start_col, target_row, target_col
                        ):
                            continue

                        if self._would_leave_king_in_check(
                            piece, start_row, start_col, target_row, target_col
                        ):
                            continue

                        return True
        return False

    def is_square_attacked(self, row, col, by_color):
        for r in range(ROWS):
            for c in range(COLS):
                square = self.squares[r][c]
                if not square.has_piece():
                    continue
                piece = square.piece
                if piece.color != by_color:
                    continue
                if self._can_piece_attack_square(piece, r, c, row, col):
                    return True
        return False

    def _is_en_passant_capture(self, piece, start_row, start_col, target_row, target_col):
        if piece.name != "pawn":
            return False
        if self.en_passant_square is None:
            return False
        if (target_row, target_col) != self.en_passant_square:
            return False
        if abs(target_col - start_col) != 1:
            return False
        if target_row - start_row != piece.dir:
            return False
        adjacent_square = self.squares[start_row][target_col]
        if not adjacent_square.has_piece():
            return False
        adjacent_piece = adjacent_square.piece
        return adjacent_piece.name == "pawn" and adjacent_piece.color != piece.color

    def _can_castle(self, king, row, start_col, target_col):
        if king.moved:
            return False
        if target_col not in (2, 6):
            return False

        rook_col = 7 if target_col == 6 else 0
        rook_square = self.squares[row][rook_col]
        if not rook_square.has_piece():
            return False

        rook = rook_square.piece
        if rook.name != "rook" or rook.color != king.color or rook.moved:
            return False

        step = 1 if rook_col > start_col else -1
        col = start_col + step
        while col != rook_col:
            if self.squares[row][col].has_piece():
                return False
            col += step

        enemy_color = "black" if king.color == "white" else "white"
        if self.is_square_attacked(row, start_col, enemy_color):
            return False
        if self.is_square_attacked(row, start_col + step, enemy_color):
            return False
        if self.is_square_attacked(row, target_col, enemy_color):
            return False

        return True

    def _move_castling_rook(self, row, start_col, target_col):
        if target_col == 6:
            rook_start_col = 7
            rook_target_col = 5
        else:
            rook_start_col = 0
            rook_target_col = 3

        rook = self.squares[row][rook_start_col].piece
        self.squares[row][rook_start_col].piece = None
        self.squares[row][rook_target_col].piece = rook
        if rook:
            rook.moved = True

    def _promote_pawn_if_needed(self, row, col):
        square = self.squares[row][col]
        if not square.has_piece():
            return
        piece = square.piece
        if piece.name != "pawn":
            return
        if row not in (0, 7):
            return
        promoted_piece = Queen(piece.color)
        promoted_piece.moved = True
        square.piece = promoted_piece

    def _find_king(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if not square.has_piece():
                    continue
                piece = square.piece
                if piece.color == color and piece.name == "king":
                    return row, col
        return None

    def _can_piece_attack_square(
        self, piece, start_row, start_col, target_row, target_col
    ):
        dr = target_row - start_row
        dc = target_col - start_col

        if piece.name == "pawn":
            return dr == piece.dir and abs(dc) == 1
        if piece.name == "knight":
            return (abs(dr), abs(dc)) in ((2, 1), (1, 2))
        if piece.name == "king":
            return max(abs(dr), abs(dc)) == 1
        if piece.name == "rook":
            return (dr == 0 or dc == 0) and self.is_path_clear(
                start_row, start_col, target_row, target_col
            )
        if piece.name == "bishop":
            return abs(dr) == abs(dc) and self.is_path_clear(
                start_row, start_col, target_row, target_col
            )
        if piece.name == "queen":
            return (dr == 0 or dc == 0 or abs(dr) == abs(dc)) and self.is_path_clear(
                start_row, start_col, target_row, target_col
            )
        return False

    def _would_leave_king_in_check(
        self, piece, start_row, start_col, target_row, target_col
    ):
        start_square = self.squares[start_row][start_col]
        target_square = self.squares[target_row][target_col]

        old_start_piece = start_square.piece
        old_target_piece = target_square.piece
        old_piece_moved = piece.moved
        old_en_passant = self.en_passant_square

        is_en_passant = self._is_en_passant_capture(
            piece, start_row, start_col, target_row, target_col
        )
        captured_ep_square = None
        captured_ep_piece = None

        is_castling = piece.name == "king" and abs(target_col - start_col) == 2
        rook_state = None

        if is_en_passant:
            captured_ep_square = self.squares[start_row][target_col]
            captured_ep_piece = captured_ep_square.piece
            captured_ep_square.piece = None

        start_square.piece = None
        target_square.piece = piece
        piece.moved = True

        if is_castling:
            if target_col == 6:
                rook_start_col, rook_target_col = 7, 5
            else:
                rook_start_col, rook_target_col = 0, 3
            rook_start_square = self.squares[start_row][rook_start_col]
            rook_target_square = self.squares[start_row][rook_target_col]
            rook_piece = rook_start_square.piece
            rook_state = (
                rook_start_square,
                rook_target_square,
                rook_piece,
                rook_piece.moved if rook_piece else None,
            )
            rook_start_square.piece = None
            rook_target_square.piece = rook_piece
            if rook_piece:
                rook_piece.moved = True

        in_check = self.is_in_check(piece.color)

        if rook_state:
            rook_start_square, rook_target_square, rook_piece, rook_moved = rook_state
            rook_start_square.piece = rook_piece
            rook_target_square.piece = None
            if rook_piece:
                rook_piece.moved = rook_moved

        start_square.piece = old_start_piece
        target_square.piece = old_target_piece
        piece.moved = old_piece_moved
        self.en_passant_square = old_en_passant

        if is_en_passant and captured_ep_square is not None:
            captured_ep_square.piece = captured_ep_piece

        return in_check


