import requests
import pygame
import random
import string

TILE_COLOR = (255, 204, 153)
BACKGROUND = (0, 153, 0)


class Screen():

    def __init__(self, title, width, height):
        self.screenWidth = width
        self.screenHeight = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def add_icon(self, image):
        self.icon = pygame.image.load(image)
        pygame.display.set_icon(self.icon)


class ScrabbleScreen(Screen):

    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        self.TILESIZE = 32
        self.BOARD_POS = (15, 15)
        self.RACK_POS = (500, 15)
        self.font = pygame.font.SysFont('', 32)
        self.buttonImage = pygame.transform.scale(pygame.image.load("images/button.png"), (200, 50))
        self.tileImg = pygame.image.load("images/tile.png")
        self.board = []
        #self.getData()
        self.makeBoard()



    #creates a box surrounding the tile currently hovered over
    def boardSurf(self):
        self.board_surf = pygame.Surface( ( self.TILESIZE*15, self.TILESIZE * 15 ) )
        for y in range(0, 15):
            for x in range(0, 15):
                rect = pygame.Rect(x*self.TILESIZE, y*self.TILESIZE, self.TILESIZE, self.TILESIZE)
                pygame.draw.rect(self.board_surf, TILE_COLOR, rect)
                pygame.draw.rect(self.board_surf, BACKGROUND, rect, 2)

    '''
    #creates the board for the player
    def makeBoard(self):
        self.board = []
        for y in range(0, 15):
            self.board.append([])
            for x in range(0, 15):
                self.board[y].append(None)
        for x in range(0, 15):
            self.board[1][x] = ('black', random.choice(string.ascii_letters))
        for x in range(0, 15):
            self.board[6][x] = ('black', random.choice(string.ascii_letters))
    '''

    def makeBoard(self):
        get_board = requests.get('http://46.101.199.68:3000/getdata').text
        #print(get_board)
        self.board = []
        get_board = eval(get_board)
        for y in range(0, 15):
            self.board.append([])
            for x in range(0, 15):
                self.board[y].append(None)
        for i, row in enumerate(get_board):
            for j, cell in enumerate(get_board[row]):
                #self.newLetter(i, j, cell)
                self.board[i][j] = ('black', get_board[row][j])



    #creates the players rack of scrabble tiles
    def makeRack(self):
        self.rack = []
        for y in range(0, 7):
            self.rack.append(None)
        for x in range(0, 7):
            self.rack[x] = ('black', random.choice(string.ascii_letters))
        set_rack = requests.get('http://46.101.199.68:3000/setrack?player=1&rack={}'.format(self.rack)).text
        print(set_rack)

    # cuts off the rack into squares to match the background colour
    # creates the colour for the rack
    def RackSurf(self):
        self.rack_surf = pygame.Surface( ( self.TILESIZE*2 , (self.TILESIZE)*14 ) )
        for y in range(0, 7):
            rect = pygame.Rect(0, y*(2*self.TILESIZE), 2*self.TILESIZE, 2*self.TILESIZE)
            pygame.draw.rect(self.rack_surf, pygame.Color("blue"), rect)
            pygame.draw.rect(self.rack_surf, BACKGROUND, rect, 2)
        return self

    # gets the players mouse position on the board
    def getMousePosBoard(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.BOARD_POS
        x, y = [int(v // self.TILESIZE) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0: return (self.board[y][x], x, y)
        except IndexError: pass
        return None, None, None

    # gets the players mouse position on the rack
    def getMousePosRack(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.RACK_POS
        x, y = [int(v // (self.TILESIZE*2)) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0 : return (self.rack[y], x, y)
        except IndexError: pass
        return None, None, None

    # draws the pieces on the board and on the players rack
    def draw_pieces(self, selected_piece):
        sx, sy = None, None
        if selected_piece:
            piece, sx, sy = selected_piece
        for y in range(0, 15):
            for x in range(0, 15):
                piece = self.board[y][x]
                if piece:
                    selected = x == sx and y == sy
                    color, type = piece
                    s1 = self.font.render(type[0], True, pygame.Color(color))
                    s2 = self.font.render(type[0], True, pygame.Color('darkgrey'))
                    pos = pygame.Rect(self.BOARD_POS[0] + x * self.TILESIZE+1, self.BOARD_POS[1] + y * self.TILESIZE + 1, self.TILESIZE, self.TILESIZE)
                    self.screen.blit(self.tileImg, (self.BOARD_POS[0] + x * self.TILESIZE, self.BOARD_POS[1] + y * self.TILESIZE))
                    self.screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                    self.screen.blit(s1, s1.get_rect(center=pos.center))
        for y in range(0, 7):
            piece = self.rack[y]
            if piece:
                color, type = piece
                s1 = self.font.render(type[0], True, pygame.Color('red' if selected else color))
                s2 = self.font.render(type[0], True, pygame.Color('darkgrey'))
                pos = pygame.Rect(self.RACK_POS[0] , self.RACK_POS[1] + y *(2* self.TILESIZE) + 1, 2*self.TILESIZE,2* self.TILESIZE)
                self.screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                self.screen.blit(s1, s1.get_rect(center=pos.center))

    #Highlights the rack squares
    def draw_rack_selector(self):
        piece, _, mouseY = self.getMousePosRack()
        if piece != None:
            rect = (self.RACK_POS[0] , self.RACK_POS[1] + mouseY * (2 *self.TILESIZE), 2*self.TILESIZE, 2*self.TILESIZE)
            pygame.draw.rect(self.screen, (255, 255, 0, 50), rect, 2)
        return self

    # Highlights the board squares
    def draw_board_selector(self):
        piece, mouseX, mouseY = self.getMousePosBoard()
        if piece != None:
            rect = (self.BOARD_POS[0] + mouseX * self.TILESIZE, self.BOARD_POS[1] + mouseY * self.TILESIZE, self.TILESIZE, self.TILESIZE)
            pygame.draw.rect(self.screen, (255, 0, 0, 50), rect, 2)
        return self
    # For drawing a line from the rack to the board
    def draw_drag(self, selected_piece):
        if selected_piece:
            piece, x, y = self.getMousePosBoard()
            if x != None:
                if self.board[y][x] != None or self.board[y][x] != '#':
                    rect = (self.BOARD_POS[0] + x * self.TILESIZE, self.BOARD_POS[1] + y * self.TILESIZE, self.TILESIZE, self.TILESIZE)
                    pygame.draw.rect(self.screen, (255, 0, 0, 50), rect, 2)
                else:
                    rect = (self.BOARD_POS[0] + x * self.TILESIZE, self.BOARD_POS[1] + y * self.TILESIZE, self.TILESIZE, self.TILESIZE)
                    pygame.draw.rect(self.screen, (0, 255, 0, 50), rect, 2)

                color, type = selected_piece[0]
                s1 = self.font.render(type[0], True, pygame.Color(color))
                s2 = self.font.render(type[0], True, pygame.Color('darkgrey'))
                pos = pygame.Vector2(pygame.mouse.get_pos())
                self.screen.blit(s2, s2.get_rect(center=pos + (1, 1)))
                self.screen.blit(s1, s1.get_rect(center=pos))
                selected_rect = pygame.Rect(self.RACK_POS[0] + selected_piece[1] * self.TILESIZE*2, self.RACK_POS[1] + selected_piece[2] * self.TILESIZE*2, self.TILESIZE*2, self.TILESIZE*2)
                pygame.draw.line(self.screen, pygame.Color('red'), selected_rect.center, pos)
            return (x, y)
        return None

    # Creates a New Rack for the player
    def newRack(self):
        for y in range(0,7):
            self.rack[y] =  ('black', random.choice(string.ascii_letters))

    # Shuffles The players current Rack
    def shuffleRack(self):
        random.shuffle(self.rack)

    def undoMove(self, piece, originalPos):
        self.rack[originalPos] = piece

    # This is used to create buttons for the players use
    def drawButton(self, x, y, text, mousePos):
        mouseX, mouseY = mousePos
        self.screen.blit(self.buttonImage, (x, y))
        self.screen.blit(self.font.render(text , True , (255, 255, 255)) , (x+10,y+15))
        return (x, y)

    def mainLoop(self):
        #Load Assets
        self.makeBoard()
        self.boardSurf()
        self.makeRack()
        self.RackSurf()
        selected_piece = None
        drop_pos = None
        #Main Loop
        while True:
            piece, mouseX, mouseY = self.getMousePosRack()
            #Commented out because it was throwing an error - Brendan
            #mouse = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece != None or piece != '#':
                        selected_piece = piece, mouseX, mouseY
                    '''Throwing up a load of errors here, so I commented it out - Brendan
                    if endTurnButton[0] <= mouse[0] <= endTurnButton[0]+140 and endTurnButton[1] <= mouse[1] <= endTurnButton[1]+40:
                        self.newRack()
                    if shuffleButton[0] <= mouse[0] <= shuffleButton[0]+140 and shuffleButton[1] <= mouse[1] <= shuffleButton[1]+40:
                        self.shuffleRack()
                    if undoButton[0] <= mouse[0] <= undoButton[0]+140 and undoButton[1] <= mouse[1] <= undoButton[1]+40:
                        print("FCK")
                        '''

                if e.type == pygame.MOUSEBUTTONUP:
                    if drop_pos and selected_piece:
                        if self.board[drop_pos[1]][drop_pos[0]] == None:
                            piece, old_x, old_y = selected_piece
                            self.rack[old_y] = 0
                            new_x, new_y = drop_pos
                            self.board[new_y][new_x] = piece
                    selected_piece = None
                    drop_pos = None

            self.screen.fill(BACKGROUND)
            self.screen.blit(self.board_surf, self.BOARD_POS)
            self.screen.blit(self.rack_surf, self.RACK_POS)
            self.draw_rack_selector()
            self.draw_board_selector()
            self.draw_pieces(selected_piece)
            drop_pos = self.draw_drag(selected_piece)
            '''load of errors thrown up here, so I commented it out - Brendan
            endTurnButton = self.drawButton(500, 500, "End Turn", mouse)
            shuffleButton = self.drawButton(500, 550, "Shuffle", mouse)
            undoButton = self.drawButton(500, 600, "Undo", mouse)
            '''
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    s = ScrabbleScreen("Scrabble Game", 640, 640).mainLoop()
