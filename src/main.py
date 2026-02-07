import pygame
import sys
from const import *
from game import Game


class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('CHESS GAME')
        self.game = Game()


    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True: 
            game.showbg(screen)
            game.show_pieces(screen)
        
            for event in pygame.event.get():
                    #Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         dragger.update_mouse(event.pos)

                         clicked_row = dragger.mouseY // SQUARE_SIZE
                         clicked_col = dragger.mouseY // SQUARE_SIZE



                         if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)


                    
                    elif event.type == pygame.MOUSEMOTION:
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                                dragger.update_blit(screen)
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                         dragger.undrag_piece()

                    elif event == pygame.QUIT:
                        pygame.quit()
                        sys.exit()



            pygame.display.update()

        
        
        
main = Main()
main.mainloop() 