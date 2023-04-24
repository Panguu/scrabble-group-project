#import sys
import requests
import pygame
import random
import string

TILE_COLOR = (255, 204, 153)
BACKGROUND = (0, 153, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (128, 0, 0)
#font = pygame.font.Font('freesansbold.ttf', 32)


'''
Screen Class if a class to create a window
it takes in  a given title, width, height
has function add_icon to add a icon to the window, takes in the filename of image
'''
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
    '''
    init is a sub class of Screen
    has some predefined values such as
    TILESIZE which determins the size of the tiles on the board
    BOARD_POS is the starting x and y cords of the top left hand side of the board
    RACK_POS is the starting x and y cords of the rack
    font is the font used in pygame currently set to the current font used by the system
    buttonImage is the image used for buttons
    tileImg is the image used for a placed tile
    board and rack are empty lists which will contain the info of the pieces placed into the rack/board
    '''

    def __init__(self, title, width, height, serverip="http://localhost:3000", username="anonymous", playernumber=0):
        super().__init__(title, width, height)
        self.TILESIZE = 32
        self.BOARD_POS = (15, 15)
        self.RACK_POS = (500, 15)
        self.font = pygame.font.SysFont('', 32)
        self.buttonImage = pygame.transform.scale(pygame.image.load("images/button.png"), (200, 50))
        self.tileImg = pygame.image.load("images/tile.png")
        self.board = []
        self.rack = []
        self.rack_surf = pygame.Surface( ( self.TILESIZE*2 , (self.TILESIZE)*14 ) )
        self.board_surf = pygame.Surface( ( self.TILESIZE*15, self.TILESIZE * 15 ) )
        #self.currentTurn = []
        #self.serverip = "http://46.101.199.68:3000"
        self.serverip = serverip
        self.currentTurn = int(requests.get("{}/getturn".format(self.serverip)).text)
        self.name = username
        #if len(sys.argv) > 2:
        #    self.playerNumber = sys.argv[2]
        #else:
        #    self.playerNumber = 1
        self.playerNumber = playernumber
        print("Player Number: " + str(self.playerNumber))
        self.maxplayers = 1
        self.matched_words = []
        self.score = 0
        #self.getData()
        self.makeBoard()



    def checkWords(self):
        print("checkWords")
        output = []
        vertical_output = []

        for x in self.board:
            output.append([z[1] for z in x])

        for n in self.board:
            vertical_output.append([z[1] for z in n])
            vertical = list(zip(*vertical_output)) # using zip to get vertial letters

        '''
        print("Horizontal")
        print("________________________________________________")
        for i, x in enumerate(output):
           print(i, "\t", x)

        print("Vertical")
        print("________________________________________________")
        for i, x in enumerate(vertical):
            print(i, "\t",x)
        '''

        for idx, row in enumerate(output):
            for word in open("words.txt"):
                if word == row:
                    print(row, " == ", word)

            word = "".join(row).upper()
            print(word)

            for dic_word in open("words.txt"): # checks horizontally
                if dic_word.lower()[:-1] in word.lower():
                    print("Valid word in horizontal row: " + word.strip('#'))
                    #print(row.index(word))
                    print(str(idx), word.index(word.strip('#')))
                    self.score += len(dic_word)
                    idy = word.index(word.strip('#'))
                    if idx%idy == 0 or idy%idx == 0:
                        self.score = self.score * 2


        for idx, column in enumerate(vertical): ## not sure if we need this?
            for word in open("words.txt"):
                if word == column:
                    print(column, "==",word)

            word = "".join(column).upper()

            for dic_word in open("words.txt"):
                if dic_word.lower() in word.lower():
                    print("Valid word in vertical column")
                    self.score += len(dic_word)


    #creates a box surrounding the tile currently hovered over
    def boardSurf(self):
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
        get_board = requests.get('{}/getdata'.format(self.serverip)).text
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
        set_rack = requests.get('{}/setrack?player={}&rack={}'.format(self.serverip, self.playerNumber, [x[1] for x in self.rack])).text
        #set_rack = requests.get('{}/setrack?player=1&rack={}'.format(self.serverip, self.rack)).text
        set_rack # this line is needed, but doesn't do anything -please don't delete
        #print(set_rack)
        #print([x[1] for x in self.rack])
        #set_rack = requests.get('http://localhost:3000/setrack?player=1&rack={}'.format(self.rack)).text
        #print(set_rack)

    # cuts off the rack into squares to match the background colour
    # creates the colour for the rack
    def RackSurf(self, dict):
        for y in range(len(dict)):
            rect = pygame.Rect(0, y*(2*self.TILESIZE), 2*self.TILESIZE, 2*self.TILESIZE)
            pygame.draw.rect(self.rack_surf, pygame.Color("blue"), rect)
            pygame.draw.rect(self.rack_surf, BACKGROUND, rect, 2)
        return self

    '''
    get mouse pos board and get mouse pos rack can be optimized
    these can become one function later
    '''
    # gets the players mouse position on the board
    def getMousePosBoard(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self.BOARD_POS
        x, y = [int(v // self.TILESIZE) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                #print(self.board[y][x])
                return (self.board[y][x], x, y)
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
                    #if x == y or x == y/2 or x/2 == y or x == y*2:
                    if x != 0 and y != 0:
                        if x%y == 0 or y%x == 0:
                            s2 = self.font.render(type[0], True, pygame.Color('red'))
                        else:
                            s2 = self.font.render(type[0], True, pygame.Color('darkgrey'))
                    else:
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

    '''
    draw rack selector and draw boad selector draws the outline when hovered over the tile
    can be combined later into one function
    '''
    #Highlights the rack squares
    def draw_rack_selector(self):
        piece, mouseX, mouseY = self.getMousePosRack()
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
                    if int(self.currentTurn) == 1:
                        #if (x+y) == 15 and min(x,y) == 7 or (x+y == 16 and min(x,y) == 8) or (x+y == 14 and max(x,y == 7)):
                        if [x,y] == [7,7] or [x,y] == [7,8] or [x,y] == [8,7] or [x,y] == [8,8]:
                            print("Centre")
                        else:
                            print(y, x)
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

    def endTurn(self):
        #self.currentTurn = []
        #if int(self.currentTurn) == int(self.playerNumber):
        self.currentTurn = int(self.currentTurn) + 1
        if self.currentTurn > self.maxplayers:
            self.currentTurn = 1
        #print(self.currentTurn)
        set_turn = requests.get('{}/setturn?turn={}'.format(self.serverip, self.currentTurn)).text
        #print(set_turn)
        #self.currentTurn = int(requests.get('{}/getturn'.format(self.serverip)).text)
        #self.board = requests.get('http://localhost:3000/getdata')

    def undoMove(self, piece, originalPos):
        #self.rack.append(self.currentTurn[-1][0])
        #self.currentTurn.remove(-1)
        pass

    # This is used to create buttons for the players use
    def drawButton(self, x, y, text, mousePos):
        mouseX, mouseY = mousePos
        self.screen.blit(self.buttonImage, (x, y))
        self.screen.blit(self.font.render(text , True , (255, 255, 255)) , (x+10,y+15))
        return (x, y)

    def mainLoop(self):
        #text = self.font.render('Turn: '+self.currentTurn[int(self.playerNumber)], True, green, blue)
        #text = self.font.render('Turn: '+ str(self.currentTurn), True, green, blue)
        playertext = self.font.render('Player: '+ str(self.playerNumber), True, green, blue)
        # create a rectangular object for the
        # text surface object
        #textRect = text.get_rect()
        playertextRect = playertext.get_rect()


        # set the center of the rectangular object.
        #textRect.center = (100, 550)
        playertextRect.center = (100, 600)
        #Load Assets
        self.boardSurf()
        self.makeRack()
        self.RackSurf(self.rack)
        selected_piece = None
        drop_pos = None
        #Main Loop
        while True:
            pygame.display.set_caption("Turn: " + str(self.currentTurn) + ", username: " + str(self.name) + ", score: " + str(self.score))
            piece, mouseX, mouseY = self.getMousePosRack()
            #Commented out because it was throwing an error - Brendan
            mouse = pygame.mouse.get_pos()
            str(mouse).upper()
            #print([None for None in mouse])
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece != None:# or piece != '#':
                        selected_piece = piece, mouseX, mouseY
                    endTurnButton = self.drawButton(500, 500, "End Turn", mouse)
                    shuffleButton = self.drawButton(500, 550, "Shuffle", mouse)
                    undoButton = self.drawButton(500, 600, "Undo", mouse)
                    checkButton = self.drawButton(500, 450, "Check Words", mouse)
                    checkTurnButton = self.drawButton(300, 600, "Check if Turn", mouse)
                    #Throwing up a load of errors here, so I commented it out - Brendan
                    if endTurnButton[0] <= mouse[0] <= endTurnButton[0]+140 and endTurnButton[1] <= mouse[1] <= endTurnButton[1]+40:
                        #self.newRack()
                        if int(self.currentTurn == self.playerNumber):
                            self.endTurn()
                    if shuffleButton[0] <= mouse[0] <= shuffleButton[0]+140 and shuffleButton[1] <= mouse[1] <= shuffleButton[1]+40:
                        self.shuffleRack()
                    if undoButton[0] <= mouse[0] <= undoButton[0]+140 and undoButton[1] <= mouse[1] <= undoButton[1]+40:
                        self.endTurn()
                    if checkButton[0] <= mouse[0] <= checkButton[0]+140 and checkButton[1] <= mouse[1] < checkButton[1]+40:
                        self.checkWords()
                    if checkTurnButton[0] <= mouse[0] <= checkTurnButton[0]+140 and checkTurnButton[1] <= mouse[1] < checkTurnButton[1]+40:
                        result = requests.get("{}/getturn".format(self.serverip)).text
                        print("WORK")
                        print(result)
                        self.currentTurn = int(result)
                        self.makeBoard()

                        #http://localhost:3000/getturn").text)
                        #get_turn = requests.get("http://localhost:3000/getturn").text
                        #print(get_turn)

                if e.type == pygame.MOUSEBUTTONUP and int(self.currentTurn) == int(self.playerNumber):
                    if drop_pos and selected_piece:
                        piece, old_x, old_y = selected_piece
                        new_x, new_y = drop_pos
                        if new_x != None:
                            my_request = "{}/settile?x={}&y={}&char={}&turn={}&player={}".format(self.serverip, new_x, new_y, piece[1], self.currentTurn, self.playerNumber)
                            print(my_request)
                            set_tile = requests.get(my_request).text
                            print(set_tile) #This line is necessary, but doesn't do anything - please don't delete
                            try:
                                if self.board[drop_pos[1]][drop_pos[0]] == None or self.board[drop_pos[1]][drop_pos[0]][1] == '#':
                                    #self.currentTurn.append([selected_piece, drop_pos])
                                    self.rack[old_y] = 0
                                    self.board[new_y][new_x] = piece
                            except:
                                print("error")
                                pass
                            self.checkWords()
                            selected_piece = None
                    drop_pos = None

            self.screen.fill(BACKGROUND)
            self.screen.blit(self.board_surf, self.BOARD_POS)
            self.screen.blit(self.rack_surf, self.RACK_POS)
            #self.screen.blit(text, textRect)
            self.screen.blit(playertext, playertextRect)
            self.draw_rack_selector()
            self.draw_board_selector()
            self.draw_pieces(selected_piece)
            endTurnButton = self.drawButton(500, 500, "End Turn", mouse)
            shuffleButton = self.drawButton(500, 550, "Shuffle", mouse)
            undoButton = self.drawButton(500, 600, "Undo", mouse)
            checkButton = self.drawButton(500, 450, "Check Words", mouse)
            checkTurnButton = self.drawButton(300, 600, "Check if Turn", mouse)
            #print(selected_piece)
            drop_pos = self.draw_drag(selected_piece)
            #self.checkWords()
            #self.checkWords()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    print("Welcome to scrabble - Please place first tile in center")
    name = input("Enter your username: ")
    ip = input("Enter server ip \n1. http://46.101.199.68\n2. Default\n3. Enter manually here: \n")
    port = input("Enter server port\n1. 3000\n2. Default\n3. Enter manually here: \n")
    playernumber = int(input("Enter player number: "))
    #port = input("Enter server port: (leave blank for default)")
    #ip_port = "http://{}:{}".format(ip, port)
    ip_port = "{}:{}".format(ip, port)
    if ip == "1":
        s = ScrabbleScreen("Scrabble Game", 640, 640, serverip="http://46.101.199.68:3000", username=name, playernumber=playernumber).mainLoop()
    elif ip == "2":
        s = ScrabbleScreen("Scrabble Game", 640, 640, username=name, playernumber=playernumber).mainLoop()
    else:
        s = ScrabbleScreen("Scrabble Game", 640, 640, serverip=ip_port, username=name, playernumber=playernumber).mainLoop()
    '''
    if len(sys.argv) >1:
        print(sys.argv[1])
        s = ScrabbleScreen("Scrabble Game", 640, 640, sys.argv[1], username=name).mainLoop()
    else:
        print(sys.argv)
        s = ScrabbleScreen("Scrabble Game", 640, 640, username=name).mainLoop()
    '''
