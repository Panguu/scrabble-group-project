import requests

import tkinter as tk


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Scrabble")

        self.main_grid = tk.Frame(
        self, bg="blue", bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(0))
        self.makeGui()
        self.printLetters()
        self.player_input()
        self.mainloop()

    def printLetters(self):
        get_board = requests.get('http://46.101.199.68:3000/getdata').text
        print(get_board)
        get_board = eval(get_board)
        for i,row in enumerate(get_board):
            for j, cell in enumerate(get_board[row]):
                self.newLetter(i, j, cell)

    def sendCharacterToServer(self, row, col, letter):
        data_send = 'http://46.101.199.68:3000/settile?x={0}&y={1}&char={2}&turn=2&player=1'.format(col, row, letter)
        print(data_send)
        requests.get('http://46.101.199.68:3000/settile?x={0}&y={1}&char={2}&turn=2&player=1'.format(col, row, letter))


    def makeGui(self):
        self.cells = []
        for i in range(15):
            row = []
            for j in range(15):
                cell_frame = tk.Frame(self.main_grid, bg="white", width=20, height=20)
                cell_frame.grid(row=i, column=j, padx=1, pady = 1)
                cell_data = {"frame":cell_frame}
                row.append(cell_data)
        self.cells.append(row)

    def newLetter(self, row, col, letter):
        cell_number = tk.Label(self.main_grid, bg="white", fg="black", text=letter)
        cell_number.grid(row=int(row), column=int(col))

    def player_input(self):
        for _ in range(20):
            row, col, letter = input().split()

            self.newLetter(row, col, letter)
            self.sendCharacterToServer(row, col, letter)




if __name__ == "__main__":
    s = Game()
