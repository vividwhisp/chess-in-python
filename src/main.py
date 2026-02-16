import pygame
import sys
from const import *
from game import Game


class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF)
        pygame.display.set_caption('CHESS GAME')
        self.game = Game()
        self.title_font = pygame.font.SysFont("arial", 46, bold=True)
        self.button_font = pygame.font.SysFont("arial", 30, bold=True)
        self.info_font = pygame.font.SysFont("arial", 24)
        self.play_again_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 20, 260, 56)
        self.quit_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 90, 260, 56)

    def draw_game_over_overlay(self):
        screen = self.screen
        game = self.game
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 140, 440, 320)
        pygame.draw.rect(screen, (245, 245, 245), panel_rect, border_radius=12)
        pygame.draw.rect(screen, (35, 35, 35), panel_rect, width=2, border_radius=12)

        winner_text = f"Checkmate! {game.winner.capitalize()} wins"
        text_surface = self.title_font.render(winner_text, True, (20, 20, 20))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
        screen.blit(text_surface, text_rect)

        info_surface = self.info_font.render("Choose an option:", True, (60, 60, 60))
        info_rect = info_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(info_surface, info_rect)

        pygame.draw.rect(screen, (42, 125, 67), self.play_again_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 45, 45), self.quit_rect, border_radius=8)

        play_text = self.button_font.render("Play Again", True, (255, 255, 255))
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))
        screen.blit(play_text, play_text.get_rect(center=self.play_again_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_rect.center))


    def mainloop(self):
        game = self.game
        screen = self.screen

        while True: 
            dragger = game.dragger
            board = game.board
            game.showbg(screen)
            game.show_pieces(screen)
            if dragger.dragging:
                dragger.update_blit(screen)
            if game.game_over:
                self.draw_game_over_overlay()
        
            for event in pygame.event.get():
                    #Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         if game.game_over:
                            if self.play_again_rect.collidepoint(event.pos):
                                game.reset()
                            elif self.quit_rect.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()
                            continue
                         dragger.update_mouse(event.pos)

                         clicked_row = dragger.mouseY // SQUARE_SIZE
                         clicked_col = dragger.mouseX // SQUARE_SIZE



                         if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.current_turn:
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)


                    
                    elif event.type == pygame.MOUSEMOTION:
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                         if dragger.dragging:
                             dragger.update_mouse(event.pos)
                             released_row = dragger.mouseY // SQUARE_SIZE
                             released_col = dragger.mouseX // SQUARE_SIZE
                             moved, captured = board.try_move(
                                 dragger.initial_row,
                                 dragger.initial_col,
                                 released_row,
                                 released_col,
                             )
                             if moved:
                                 game.play_sound("capture" if captured else "move")
                                 game.next_turn()
                                 game.update_status_after_move()
                             dragger.undrag_piece()

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()



            pygame.display.update()

        
        
        
main = Main()
main.mainloop() 
