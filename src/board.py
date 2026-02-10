from const import *
from square import Square
from piece import *

class Board:
    def __init__(self):
        self.squares = []

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

        capture = target_square.has_piece()
        target_square.piece = piece
        self.squares[start_row][start_col].piece = None
        piece.moved = True
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

            return False

        # Knight
        if piece.name == 'knight':
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]

        # King
        if piece.name == 'king':
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





b = Board()
b._create()


