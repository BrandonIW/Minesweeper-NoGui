# Step1: Initialize the board and generate the bombs                                                       - Done
# Step2: Show the user the board and ask where to dig                                                      - Done
# Step3: If the location is a bomb, show game over                                                         - Done
# Step4: If the location if not a bomb, dig recursively until each square is at least next a bomb          - Done
# Step5: Repeat steps 2-4 until there are no bombs left. Then we win                                       - Done
# Step6: Each square must have an associated value indicating number of adjacent bombs upon initialization - Done
# Step7: Allow the user to select how many bombs and how large the playing board                           - Done
# Step8: Play again button?                                                                                - Done
# Step9: When lose, show how many squares remaining or smth                                                - Done
# Step10: Remove random print statements                                                                   - Done

# Bugs
# - Destroy first window upon new instance of game
# - Input validation with non-numeric numbers

#[
#[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9)],
#[(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9)]
#[(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9)]
#[(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9)]
#[(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),(4,9)]
#[(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9)]
#[(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9)]
#[(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9)]
#[(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9)]
#[(9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9)]
#]

from random import randint
from itertools import product
from itertools import count
from tkinter import Tk, Button, messagebox
from threading import Thread
import re

class Minesweeper:

    continue_game = True

    easy = re.compile(r'([0-9])\W([0-9])')
    intermediate = re.compile(r'(1[0-5]|[0-9])\W(1[0-5]|[0-9])')
    hard = re.compile(r'(1[0-9]|[0-9])\W(1[0-9]|[0-9])')

    difficulty ={
        10: "easy",
        15: "intermediate",
        20: "hard"
    }

    def __init__(self,dim_size,num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.dug = set()                                    # The set will house tuples of coordinates basically. Each coordinate
                                                            # represents where we've already dug
        self.board = self.make_new_board()                  # We create our board with bombs
        self.assign_values_to_board()                       # Assign values to the board_with_values
        self.show_board()                                   # Show the player the board
        self.difficulty = Minesweeper.difficulty.get(self.dim_size)

    def make_new_board(self):
        # This initializes our board. It is just a list of lists. It looks like [[None, None, ..., None],[None, None, ..., None]...etc.]
        # Then it plants the bombs. We should end with a list of [[None, None, *, None, None, *],[None,None,* ...etc]]

        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            location = randint(0,(self.dim_size**2) - 1)         # Each location on the board has their own specific value. If we're doing a 10x10 it's 0-99
            row = location // self.dim_size                      # If we want the row coordinate, we take our location, i.e. 36 for example, and floor divide by 10 (no remainder).
                                                                 # This gets us our row i.e. 36 / 10 = 3. Row 3
            column = location % self.dim_size                    # For the column coordinate, we need the remainder. i.e. 36 % 10 = 6. So row=3, column=6

            if board[row][column] == "*":                        # This means we've already planted a bomb there, so we ignore that and keep going
                continue

            board[row][column] = "*"                             # Plants a bomb
            bombs_planted += 1
        return board


    def assign_values_to_board(self):
        ### Once the board is initialized by make_new_board, we should assign each non-bomb [row][column] pair a number
        ### that tells us how many bombs are in all adjacent positions to it. In other words,
        ### for each position inside of self.board that is not a "*", assign a value to that position that is equal
        ### to the number of "*" adjacent to it.

        # For each row,column in product(<dimension size>) i.e. [0,1,2,3,4,5,6,7,8,9] if dim_size is 10 (This results in (0,0)(0,1)(0,2)...etc.,(9,9))
        # If that that board position at self.board[row][column] is a mine, recreate the mine. If it's not a mine, run function to calculate adjacent mines

        self.board_with_values = [self.calculate_adjacent_mines(row,column) if self.board[row][column] != "*" else "*" for row,column in product(range(self.dim_size),repeat=2)]

        ### Nice way to create a list of lists of a specific length
        self.board_with_values = [self.board_with_values[i:i + self.dim_size] for i in range(0, len(self.board_with_values), self.dim_size)]

        #board = [[calculate_adjacent_mines(idex,idex2) if square != "*" else "*" for idex2,square in enumerate(row)] for idex,row in enumerate(board)] <-- This also works

    def calculate_adjacent_mines(self,row,column):
        # Let's say I pass in row/column of [2,3]. So I need an iterable of:
        # [[1,2][1,3][1,4][2,4][2,2][3,2][3,3][3,4]]
        # So we can pass in every instance of board[row][column]. With this, we need to take each instance of board[row][column]
        # and check and see if there's a "*" in
        # - 1 column larger
        # - 1 column less
        # - 1 row larger
        # - 1 row less
        # - 1 row and 1 column larger
        # - 1 row and 1 column less
        # - 1 row larger and 1 column less
        # - 1 row less and 1 column larger

        total_mines = count(0)                        # Our total number of mines that we will return


        # For each row,column in our adjacent_coords, check and see if it's a mine. If so, increment.
        for row2,col2 in self.find_adjacent_coords(row,column):
            if self.board[row2][col2] == "*":
                next(total_mines)
            continue

        # Return final value indicating all adjacent mines
        return next(total_mines)


### Probably the most useful code here. Returns a list of all adjacent coordinates to the coordinates passed in. Does not go beyond
### perimiter of the grid

    def find_adjacent_coords(self,row,column):

        rows = [row,(row+1),(row-1)]                  # [1,2,3]. Take our passed in row, and create an iterable of one row above, and below
        columns = [column, (column+1),(column-1)]     # [2,3,4]. Take our passed in column and create an iterable of one column above and below

        adjacent_coords = list(product(rows,columns)) # [(2, 3), (2, 4), (2, 2), (3, 3), (3, 4), (3, 2), (1, 3), (1, 4), (1, 2)]
        adjacent_coords.remove((row,column))          # [(2, 4), (2, 2), (3, 3), (3, 4), (3, 2), (1, 3), (1, 4), (1, 2)]

        # Then we need to cut out any adjacent_coords that are beyond the permiter of the playing board. We return these coordinates
        return [coords for coords in adjacent_coords if (coords[0] > -1 and coords[0] < self.dim_size) and (coords[1] > -1 and coords[1] < self.dim_size)]


    def show_board(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]  # Create a new blank board with just None's, with the dimensions of the board

        # For each possible position on the board, if [row][column] has already been dug we want to show the numerical value associated with it, i.e. the numbers of bombs
        # around it. This is because we've already dug it. If it HASN'T been dug yet, then of course we can't show that value

        for row in range(self.dim_size):
            for column in range(self.dim_size):
                if f"{row},{column}" in self.dug:
                    visible_board[row][column] = str(self.board[row][column])
                else:
                    visible_board[row][column] = ' '

                string_rep = ''

        # String formatting
        widths = []
        for idex in range(self.dim_size):
            columns = map(lambda x: x[idex], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idex,column in enumerate(indices):
            format = '%-' + str(widths[idex]) + "s"
            cells.append(format % (column))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idex, column in enumerate(row):
                format = '%-' + str(widths[idex]) + "s"
                cells.append(format % (column))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-"*str_len + "\n" + string_rep + "-"*str_len

        print(string_rep)

### Main code for gameplay. While Board.continue_game is True, take coordinates from the user, add to existing set,
### and run the dig function.

    def main(self):

        while Minesweeper.continue_game:
            if len(self.dug) == (self.dim_size**2) - self.num_bombs:   # Check to see if length of all guessed coordinates equal
                self.play_again_win()                                  # num of squares minus num of bombs. If so, we win

            coordinates = input("Enter your row and column: ") # Get coordinates from player
            easy_regex = Minesweeper.easy.search(coordinates)
            int_regex = Minesweeper.intermediate.search(coordinates)
            hard_regex = Minesweeper.hard.search(coordinates)

            try:
                if self.difficulty == "easy":
                    self.dug.add(easy_regex.group(1) + ',' + easy_regex.group(2))
                    if self.dig(int(easy_regex.group(1)),int(easy_regex.group(2))):
                        Minesweeper.continue_game = False

                elif self.difficulty == "intermediate":
                    self.dug.add(int_regex.group(1) + ',' + int_regex.group(2))
                    if self.dig(int(int_regex.group(1)),int(int_regex.group(2))):
                        Minesweeper.continue_game = False

                elif self.difficulty == "hard":
                    self.dug.add(hard_regex.group(1) + ',' + hard_regex.group(2))
                    if self.dig(int(hard_regex.group(1)),int(hard_regex.group(2))):
                        Minesweeper.continue_game = False

            except AttributeError:
                print(f"Value must be numeric between 0 and {self.dim_size}")

            self.show_board()

        self.play_again_loss()


### First we simply check to see if the provided coordinates is a bomb. If so, we lose.
### Otherwise, set board[row][column] to our associated value which shows the number of adjacent bombs
### We only recursively dig IF that value is 0

    def dig(self,row,column):

        if self.board[row][column] == "*":
            return True

        self.board[row][column] = self.board_with_values[row][column]        #If the dig is not a bomb, get it's associated value

        if self.board[row][column] > 0:                                      #If the dig has a bomb surrounding it. Just return False
            return False

        if self.board[row][column] == 0:                                     #If the value is a 0 (no neighbouring bombs) we want to recusively dig
            for (adjrow,adjcolumn) in self.find_adjacent_coords(row,column): #We must add the coordinates to self.dug as we recursively dig, else we get in an infinite loop
                if f"{adjrow},{adjcolumn}" not in self.dug:
                    self.dug.add(str(adjrow) + "," + str(adjcolumn))
                    self.dig(adjrow,adjcolumn)


    def play_again_win(self):
        if messagebox.askyesno(title="Minesweeper", message=f"You win"):
            Minesweeper.continue_game = True
            MainMenu()

        else:
            print("You've exited the game")
            quit()


    def play_again_loss(self):
        if messagebox.askyesno(title="Minesweeper", message=f"You lost. There were {((self.dim_size**2) - self.num_bombs) - len(self.dug)} squares left \n\nPlay again?"):
            Minesweeper.continue_game = True
            MainMenu()

        else:
            print("You've exited the game")
            quit()


class MainMenu:
    def __init__(self):
        window = Tk()
        window.title("Minesweeper")
        window.geometry("300x85")
        window.config(background="white")


        dict = {
            "Easy": [10,15],
            "Medium": [15,40],
            "Hard": [20,99]
        }
        easy_button = Button(window,
                             text = "Easy",
                             command = lambda: [self.play_game(dict.get("Easy")[0],dict.get("Easy")[1])],
                             font = ("New Times Roman", 10),
                             fg = "white",
                             bg = "black").pack(fill="x")

        intermediate_button = Button(window,
                                     text = "Intermediate",
                                     command = lambda: [self.play_game(dict.get("Medium")[0],dict.get("Medium")[1])],
                                     font = ("New Times Roman", 10),
                                     fg = "white",
                                     bg = "black").pack(fill="x")

        hard_button = Button(window,
                             text = "Hard",
                             command = lambda: [self.play_game(dict.get("Hard")[0],dict.get("Hard")[1])],
                             font = ("New Times Roman", 10),
                             fg = "white",
                             bg = "black").pack(fill="x")


        window.mainloop()


    def play_game(self,dimensions,mines):
        game = Minesweeper(dimensions,mines)
        Thread(target=game.main).start()



if __name__ =='__main__':
    MainMenu()





