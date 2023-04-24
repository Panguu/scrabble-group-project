
letter_score = {
    "a":1,
    "e":1,
    "i":1,
    "o":1,
    "n":1,
    "r":1,
    "t":1,
    "l":1,
    "s":1,
    "u":1,
    "d":2,
    "g":2,
    "b":3,
    "c":3,
    "m":3,
    "p":3,
    "f":4,
    "h":4,
    "v":4,
    "w":4,
    "y":4,
    "k":5,
    "j":8,
    "x":8,
    "q":10,
    "z":10
}


class Player():
    def __init__(self, Player_no):
        self.player_no = Player_no
        #Sets the player score to zero for the start of the game
        self.score = 0
        #creates an empyt rack for the players tiles
        self.rack = []

    def add_score(self, word=[]):
        for i in word.lower():
            self.score += letter_score[i]
        return self


if __name__ == "__main__":
    p = Player(1)
    p.add_score("")
    print(p.score)
