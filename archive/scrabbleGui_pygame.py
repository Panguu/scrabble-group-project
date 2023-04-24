import pygame
import requests

pygame.init()

color = (255, 0, 0)
font_obj = pygame.font.Font('freesansbold.ttf', 32)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 180)
RED   = (255,   0,   0)

class Game():

    def __init__(self):
        self.surface = pygame.display.set_mode((1500, 1500))
        pygame.display.set_caption("Scrabble")
        self.player_input()

    def makeGui(self):
        self.cells = []
        for i in range(15):
            row = []
            for j in range(15):
                pygame.draw.rect(self.surface, color, pygame.Rect(100*i, 100*j, 100, 100), 2)
                #row.append(cell_data)
        self.cells.append(row)
        self.tiles = []

    def printLetters(self):
        get_board = requests.get('http://46.101.199.68:3000/getdata').text
        print(get_board)
        get_board = eval(get_board)
        for i,row in enumerate(get_board):
            for j, cell in enumerate(get_board[row]):
                self.newLetter(i, j, cell)

    def player_input(self):
        for _ in range(20):
            row, col, letter = input().split()
            self.newLetter(row, col, letter)

    def mainloop(self):
        while True:
            self.makeGui()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    def newLetter(self, row, col, letter):
        text_surface_obj = font_obj.render('Hello World!', True, GREEN, BLUE)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (100*row, 100*col)
        self.surface.blit(text_surface_obj, text_rect_obj)


if __name__ == "__main__":
    s = Game()
    s.mainloop()
