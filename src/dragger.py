import pygame
from const import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos 

    def update_blit(self, surface):
    # load texture
        texture = self.piece.texture
        img = pygame.image.load(texture)

        # follow mouse
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)

        # draw
        surface.blit(img, self.piece.texture_rect)

        
    
    def save_initial(self,pos):
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_col = pos[0] // SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.piece.set_texture(size=128)  # set ONCE
        self.dragging = True

    
    def undrag_piece (self):
        self.piece = None
        self.dragging = False