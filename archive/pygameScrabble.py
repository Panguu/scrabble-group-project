import pygame as pg


color = (255, 0, 0)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 180)
RED   = (255,   0,   0)

# A winow class which is run when program is called
class Window():
    def __init__(self, title, width, height):
        self.windowWidth = width
        self.windowHeight = height
        pg.display.set_caption(title)


    # A simple setIcon function that is used to set the icon of the pygame window
    def setIcon(self, iconName):
        self.icon = pg.image.load(iconName)
        pg.display.set_icon(self.icon)

class GameWindow(Window):
    def __init__(self, title="Simple Program", width=640, height=640):
        super().__init__(title, width, height)

    #This starts the window after set up has started
    def start(self):
        #Load Assets
        self.font_obj = pg.font.Font('freesansbold.ttf', 32)
        rack = self.loadRack()
        self.window = pg.display.set_mode((self.windowWidth, self.windowHeight))
        self.makeBoard()
        #Run MainLoop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.PlayerRack(rack)
            self.player_input()
            pg.display.update()

    def newLetter(self, row, col, letter):
        text_surface_obj = self.font_obj.render(letter, True, GREEN, BLUE)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = ((self.windowWidth/15)*int(row), (self.windowHeight/16)*int(col))
        self.window.blit(text_surface_obj, text_rect_obj)

    def player_input(self):
        row, col, letter = input().split()
        self.newLetter(row, col, letter)
        print(row, col, letter)

    def makeBoard(self):
        self.cells = []
        for i in range(15):
            row = []
            for j in range(15):
                pg.draw.rect(self.window, color, pg.Rect((self.windowWidth/15) *i,(self.windowHeight/16)  *j, (self.windowWidth/15), (self.windowHeight/16)), 2)
                #row.append(cell_data)
        self.cells.append(row)
        self.tiles = []

    def loadRack(self):
        rectHeight = self.windowHeight // 16
        rackX = 0
        rackY = self.windowHeight - rectHeight
        return pg.Rect(rackX, rackY, self.windowWidth, rectHeight)

    def PlayerRack(self, rack):
        pg.draw.rect(self.window, (0, 0, 255), rack)

if __name__ == "__main__":
    pg.init()
    w = GameWindow(title="Scrabble")
    w.setIcon("images/icon.png")
    w.start()
