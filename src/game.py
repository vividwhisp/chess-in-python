import pygame
from const  import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.current_turn = "white"
        self.game_over = False
        self.winner = None
        self.game_over_message = ""
        self.position_counts = {}
        self.sounds = {
            "move": pygame.mixer.Sound("assets/sounds/move.wav"),
            "capture": pygame.mixer.Sound("assets/sounds/capture.wav"),
        }
        self._record_current_position()

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def next_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def update_status_after_move(self):
        if self.board.is_checkmate(self.current_turn):
            self.game_over = True
            self.winner = "white" if self.current_turn == "black" else "black"
            self.game_over_message = f"Checkmate! {self.winner} wins"
            print(self.game_over_message)
            return
        if self.board.is_stalemate(self.current_turn):
            self.game_over = True
            self.winner = None
            self.game_over_message = "Stalemate! Draw"
            print(self.game_over_message)
            return
        if self.board.is_insufficient_material():
            self.game_over = True
            self.winner = None
            self.game_over_message = "Insufficient material! Draw"
            print(self.game_over_message)
            return
        if self._record_current_position() >= 3:
            self.game_over = True
            self.winner = None
            self.game_over_message = "Threefold repetition! Draw"
            print(self.game_over_message)
            return
        if self.board.is_in_check(self.current_turn):
            print(f"Check: {self.current_turn} king is under attack.")

    def reset(self):
        self.board = Board()
        self.dragger = Dragger()
        self.current_turn = "white"
        self.game_over = False
        self.winner = None
        self.game_over_message = ""
        self.position_counts = {}
        self._record_current_position()

    def _record_current_position(self):
        key = self.board.get_position_key(self.current_turn)
        new_count = self.position_counts.get(key, 0) + 1
        self.position_counts[key] = new_count
        return new_count

    def showbg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col ) % 2 == 0:
                    color = (234,235,200)
                else:
                    color = (119,154,88)
                rect = (col * SQUARE_SIZE,row * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)

                pygame.draw.rect(surface,color,rect)
    def show_pieces(self, surface):
        for row in range(ROWS):
         for col in range(COLS):
            square = self.board.squares[row][col]

            if square.has_piece():
                piece = square.piece  
                if piece is not self.dragger.piece:
                    img = piece.image

                    img_center = (
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    )

                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)




                
