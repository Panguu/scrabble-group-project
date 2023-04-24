#import sys
import requests
import pygame
import random
import time
import string
import threading as td

TILE_COLOR = (255, 204, 153)
BACKGROUND = (0, 153, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (128, 0, 0)

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
    def __init__(self, title, width, height, serverip="http://localhost:3000", username="anonymous", playernumber=0, max_players=1):
        super().__init__(title, width, height)
        self.TILESIZE = 32
        self.BOARD_POS = (15, 15)
        self.RACK_POS = (500, 15)
        self.font = pygame.font.SysFont('', 32)
        self.buttonImage = pygame.transform.scale(pygame.image.load("images/button.png"), (160, 50))
        self.tileImg = pygame.image.load("images/tile.png")
        self.board = []
        self.rack = []
        self.rack_surf = pygame.Surface( ( self.TILESIZE*2 , (self.TILESIZE)*14 ) )
        self.board_surf = pygame.Surface( ( self.TILESIZE*15, self.TILESIZE * 15 ) )
        self.serverip = serverip
        self.currentTurn = int(requests.get("{}/getturn".format(self.serverip)).text)
        self.name = username
        self.playerNumber = playernumber
        print("Player Number: " + str(self.playerNumber))
        self.maxplayers = max_players
        self.matched_words = []
        self.score = 0
        self.makeBoard()



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
    def checkWords(self):
        print("checkWords")
        output = []
        vertical_output = []
        with open("newDict.txt", "r") as dict:
            listWords = dict.read().split()
            while True:
                if self.killThread:
                    break
                if self.checkDict:

                    for x in self.board:
                        output.append([z for z in x])

                    for n in self.board:
                        vertical_output.append([z for z in n])
                        vertical = list(zip(*vertical_output)) # using zip to get vertial letters


                    for idx, row in enumerate(output):
                        for word in listWords:
                            if word in "".join(row):
                                self.score += len(word)
                                print(row, " == ", word)

                        word = "".join(row)
                        print(word)
                        for dic_word in listWords: # checks horizontally
                            if dic_word[:-1] == word:
                                print("Valid word in horizontal row: " + word.strip('-'))

                                print(str(idx), word.index(word.strip('-')))
                                self.score += len(dic_word)
                                idy = word.index(word.strip('-'))
                                if idx%idy == 0 or idy%idx == 0:
                                    self.score = self.score * 2


                    for idx, column in enumerate(vertical): ## not sure if we need this?
                        for word in listWords:
                            if word == column:
                                print(column, "==",word)

                        word = "".join(column)

                        for dic_word in listWords:
                            if dic_word in word:
                                print("Valid word in vertical column")
                                self.score += len(dic_word)


    #creates a box surrounding the tile currently hovered over
    def surf(self, dict, surf_spot, color=TILE_COLOR, tileMultiplyer=1, pos=(0,0)):
        for y in range(0, pos[1]):
            for x in range(0, pos[0]):
                rect = pygame.Rect(x*self.TILESIZE, tileMultiplyer*(y*self.TILESIZE), tileMultiplyer*self.TILESIZE, tileMultiplyer*self.TILESIZE)
                pygame.draw.rect(surf_spot, color, rect)
                pygame.draw.rect(surf_spot, BACKGROUND, rect, 2)
        return self


    def makeBoard(self):
        get_board = requests.get('{}/getdata'.format(self.serverip)).text
        self.board = []
        get_board = eval(get_board)
        for y in range(0, 15):
            self.board.append([])
            for x in range(0, 15):
                self.board[y].append('-')
        for i, row in enumerate(get_board):
            for j, cell in enumerate(get_board[row]):
                self.board[i][j] = get_board[row][j]



    #creates the players rack of scrabble tiles
    def makeRack(self):
        self.rack = []
        for y in range(0, 7):
            self.rack.append(None)
        for x in range(0, 7):
            self.rack[x] = random.choice(string.ascii_letters.upper())
        set_rack = requests.get('{}/setrack?player={}&rack={}'.format(self.serverip, self.playerNumber, [x for x in self.rack])).text
    # gets the mouse pos on the board
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
            if x >= 0 and y >= 0 : return (self.rack[y], 0, y)
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
                    s1 = self.font.render(piece, True, pygame.Color('black'))
                    #if x == y or x == y/2 or x/2 == y or x == y*2:
                    if x != 0 and y != 0:
                        if x%y == 0 or y%x == 0:
                            s2 = self.font.render(piece, True, pygame.Color('red'))
                        else:
                            s2 = self.font.render(piece, True, pygame.Color('darkgrey'))
                    else:
                        s2 = self.font.render(piece, True, pygame.Color('darkgrey'))
                    pos = pygame.Rect(self.BOARD_POS[0] + x * self.TILESIZE+1, self.BOARD_POS[1] + y * self.TILESIZE + 1, self.TILESIZE, self.TILESIZE)
                    self.screen.blit(self.tileImg, (self.BOARD_POS[0] + x * self.TILESIZE, self.BOARD_POS[1] + y * self.TILESIZE))
                    self.screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                    self.screen.blit(s1, s1.get_rect(center=pos.center))
        for y in range(0, 7):
            piece = self.rack[y]
            if piece:
                s1 = self.font.render(piece, True, pygame.Color('black'))
                s2 = self.font.render(piece, True, pygame.Color('darkgrey'))
                pos = pygame.Rect(self.RACK_POS[0] , self.RACK_POS[1] + y *(2* self.TILESIZE) + 1, 2*self.TILESIZE,2* self.TILESIZE)
                self.screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                self.screen.blit(s1, s1.get_rect(center=pos.center))

    '''
    draw rack selector and draw boad selector draws the outline when hovered over the tile
    can be combined later into one function
    '''
    #Highlights the squares on the board
    def draw_selector(self, pos,items, tileMultiplyer=1, color=(255, 255, 0, 50)):
        piece, mouseX, mouseY = items
        if piece != None:
            rect = (pos[0] + (mouseX * (tileMultiplyer * self.TILESIZE)) , pos[1] + mouseY * (tileMultiplyer *self.TILESIZE), tileMultiplyer*self.TILESIZE, tileMultiplyer*self.TILESIZE)
            pygame.draw.rect(self.screen, color, rect, 2)
        return self

    # For drawing a line from the rack to the board
    def draw_drag(self, selected_piece):
        if selected_piece:
            piece, x, y = self.getMousePosBoard()
            if x != None:
                if self.board[y][x] != None or self.board[y][x] != '-':
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

                type = selected_piece
                s1 = self.font.render(type[0], True, pygame.Color('black'))
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
            if self.rack[y] == None or self.rack[y] == 0:
                self.rack[y] = random.choice(string.ascii_letters.upper())
                set_rack = requests.get('{}/setrack?player={}&rack={}'.format(self.serverip, self.playerNumber, [x for x in self.rack])).text


    # Shuffles The players current Rack
    def shuffleRack(self):
        random.shuffle(self.rack)

    def endTurn(self):
        self.currentTurn = int(self.currentTurn) + 1
        if self.currentTurn > self.maxplayers:
            self.currentTurn = 1
        set_turn = requests.get('{}/setturn?turn={}'.format(self.serverip, self.currentTurn)).text
        print(set_turn)

    # This is used to create buttons for the players use
    def drawButton(self, x, y, text, mousePos):
        mouseX, mouseY = mousePos
        self.screen.blit(self.buttonImage, (x, y))
        self.screen.blit(self.font.render(text , True , (255, 255, 255)) , (x+10,y+15))
        return (x, y)

    def checkTurn(self):
        while True:
            if self.killThread:
                break
            if self.runCheck:
                time.sleep(5)
                result = requests.get("{}/getturn".format(self.serverip)).text
                print("WORK")
                print(result)
                self.currentTurn = int(result)
                self.makeBoard()

    def mainLoop(self):
        playertext = self.font.render('Player: '+ str(self.playerNumber), True, green, blue)
        playertextRect = playertext.get_rect()
        # thread to check if its the players turn
        self.killThread = False
        self.runCheck = True
        checkTurnThread = td.Thread(target=self.checkTurn, args=())
        checkTurnThread.start()
        # thread to check the word in the dictionary
        self.checkDict = False
        checkDict = td.Thread(target=self.checkWords, args=())
        checkDict.start()

        # set the center of the rectangular object.
        #textRect.center = (100, 550)
        playertextRect.center = (100, 550)
        #Load Assets
        #board surf highlights the squares currently hovered over
        self.surf(self.board, self.board_surf, pos=(15,15))
        self.surf(self.rack, self.rack_surf, pygame.Color("blue"), 2, (1,7))
        self.makeRack()
        selected_piece = None
        drop_pos = None
        #Main Loop
        while True:
                #print([None for None in mouse])
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.killThread = True
                        return

                    if self.currentTurn == self.playerNumber:
                        self.runCheck = False
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if piece != None:
                                selected_piece = piece, mouseX, mouseY
                                checkButton = self.drawButton(0, 600, "Check Words", mouse)
                                shuffleButton = self.drawButton(160, 600, "Shuffle", mouse)
                                resetBoardButton = self.drawButton(320, 600, "Reset Board", mouse)
                                endTurnButton = self.drawButton(480, 600, "End Turn", mouse)
                            #Throwing up a load of errors here, so I commented it out - Brendan
                            if endTurnButton[0] <= mouse[0] <= endTurnButton[0]+140 and endTurnButton[1] <= mouse[1] <= endTurnButton[1]+40:
                                #self.newRack()
                                if int(self.currentTurn == self.playerNumber):
                                    self.endTurn()
                                    self.newRack()
                                    self.runCheck = True
                            if shuffleButton[0] <= mouse[0] <= shuffleButton[0]+140 and shuffleButton[1] <= mouse[1] <= shuffleButton[1]+40:
                                self.shuffleRack()
                            if checkButton[0] <= mouse[0] <= checkButton[0]+140 and checkButton[1] <= mouse[1] < checkButton[1]+40:
                                self.checkDict=True
                            if resetBoardButton[0] <= mouse[0] <= resetBoardButton[0]+140 and resetBoardButton[1] <= mouse[1] < resetBoardButton[1]+40:
                                result = requests.get("{}/reset".format(self.serverip)).text
                                self.makeBoard()
                                print('result')


                        if e.type == pygame.MOUSEBUTTONUP and int(self.currentTurn) == int(self.playerNumber):
                            if drop_pos and selected_piece:
                                piece, old_x, old_y = selected_piece
                                new_x, new_y = drop_pos
                                if new_x != None:
                                    try:
                                        if self.board[new_y][new_x] == None or self.board[new_y][new_x] == "-":
                                            my_request = "{}/settile?x={}&y={}&char={}&turn={}&player={}".format(self.serverip, new_x, new_y, piece, self.currentTurn, self.playerNumber)
                                            print(my_request)
                                            set_tile = requests.get(my_request).text
                                            print(set_tile) #This line is necessary, but doesn't do anything - please don't delete
                                            self.checkDict = True
                                            self.rack[old_y] = 0
                                            self.board[new_y][new_x] = piece
                                    except:
                                        print("error")
                                selected_piece = None
                                drop_pos = None
                        else:
                            self.runCheck = True
                pygame.display.set_caption("Turn: " + str(self.currentTurn) + ", username: " + str(self.name) + ", score: " + str(self.score))
                piece, mouseX, mouseY = self.getMousePosRack()
                mouse = pygame.mouse.get_pos()


                self.screen.fill(BACKGROUND)
                self.screen.blit(playertext, playertextRect)
                self.screen.blit(self.board_surf, self.BOARD_POS)
                self.screen.blit(self.rack_surf, self.RACK_POS)
                self.draw_pieces(selected_piece)
                self.draw_selector(self.RACK_POS,self.getMousePosRack(), 2)
                self.draw_selector(self.BOARD_POS, self.getMousePosBoard(), 1, pygame.Color('red'))
                checkButton = self.drawButton(0, 600, "Check Words", mouse)
                shuffleButton = self.drawButton(160, 600, "Shuffle", mouse)
                resetBoardButton = self.drawButton(320, 600, "Reset Board", mouse)
                endTurnButton = self.drawButton(480, 600, "End Turn", mouse)
                drop_pos = self.draw_drag(selected_piece)
                self.checkDict=False
                pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    print("Welcome to scrabble - Please place first tile in center")
    name = input("Enter your username: ")
    ip = input("Enter server ip \n1. http://46.101.199.68\n2. Default\n3. Enter manually here: \n")
    port = input("Enter server port\n1. 3000\n2. Default\n3. Enter manually here: \n")
    playernumber = int(input("Enter player number: "))
    max_players_int = int(input("Enter max number of players in game: "))
    #port = input("Enter server port: (leave blank for default)")
    #ip_port = "http://{}:{}".format(ip, port)
    ip_port = "{}:{}".format(ip, port)
    if ip == "1":
        s = ScrabbleScreen("Scrabble Game", 640, 640, serverip="http://46.101.199.68:3000", username=name, playernumber=playernumber, max_players=max_players_int).mainLoop()
    elif ip == "2":
        s = ScrabbleScreen("Scrabble Game", 640, 640, username=name, playernumber=playernumber, max_players=max_players_int).mainLoop()
    else:
        s = ScrabbleScreen("Scrabble Game", 640, 640, serverip=ip_port, username=name, playernumber=playernumber, max_players=max_players_int).mainLoop()
    '''
    if len(sys.argv) >1:
        print(sys.argv[1])
        s = ScrabbleScreen("Scrabble Game", 640, 640, sys.argv[1], username=name).mainLoop()
    else:
        print(sys.argv)
        s = ScrabbleScreen("Scrabble Game", 640, 640, username=name).mainLoop()
    '''
