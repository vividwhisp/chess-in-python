import pygame
from const  import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.current_turn = "white"
        self.sounds = {
            "move": pygame.mixer.Sound("assets/sounds/move.wav"),
            "capture": pygame.mixer.Sound("assets/sounds/capture.wav"),
        }

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def next_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

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




                
