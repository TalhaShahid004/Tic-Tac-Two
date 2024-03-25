import random

class node:
    def __init__(self):
        self.value = 0
        self.occupied = "-"

    def occupy(self, player):
        self.occupied = player

    def assign_score(self, score):
        self.value = score

class tictactoe:
    value = 0
    won = ""
    grid = []
    winning_combinations = []

    def __init__(self):
        self.grid = [node() for i in range(9)]
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

    def move(self, square_num, player):
        self.grid[square_num].occupy(player)

    def assign_score(self, score):
        self.value = score

    def check_winner(self):
        for combo in self.winning_combinations:
            symbols = [self.grid[i].occupied for i in combo]
            if symbols.count("X") == 3:
                self.won = "X"
            elif symbols.count("O") == 3:
                self.won = "O"

    def display(self):
        for i in range(3):
            for j in range(3):
                print(self.grid[i*3 + j].occupied, end=", ")
            print()
        print()

    def displayRow(self, i):
        for j in range(3):
            print(self.grid[i * 3 + j].occupied, end=", ")


def exploreTicTacToes(tictactoe):
    player_1 = "X"
    player_2 = "O"
    tictactoe.display()

    while tictactoe.won == "" and not all(node.occupied != "-" for node in tictactoe.grid):
        i = random.randint(0, 8)
        while tictactoe.grid[i].occupied != "-":
            i = random.randint(0, 8)

        tictactoe.move(i, player_1)
        tictactoe.display()
        tictactoe.check_winner()
        if tictactoe.won != "":
            print(f"Player {tictactoe.won} wins!")
            return

        i = random.randint(0, 8)
        while tictactoe.grid[i].occupied != "-":
            i = random.randint(0, 8)

        tictactoe.move(i, player_2)
        tictactoe.display()
        tictactoe.check_winner()
        if tictactoe.won != "":
            print(f"Player {tictactoe.won} wins!")
            return

    print("It's a tie!")



class UltimateTicTacToes:
    value = 0
    won = ""
    active_board = -1
    def __init__(self):
        self.grid = [tictactoe() for i in range(9)]
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

    def move(self, grid_num, square_num, player):
        self.grid[grid_num].move(square_num, player)
        self.grid[grid_num].check_winner()
        self.check_winner()
        self.active_board = square_num if self.grid[square_num].won == "" else -1

    def checkIfWon(self, i):
        return self.grid[i].won != ""

    def checkIfGridLegal(self, i):
        if not self.checkIfWon(i) and (self.active_board == -1 or self.active_board == i):
            return True
        return False

    def assign_score(self, score):
        self.value = score

    def check_winner(self):
        for combo in self.winning_combinations:
            symbols = [self.grid[i].won for i in combo]
            if symbols.count("X") == 3:
                self.won = "X"
                return
            elif symbols.count("O") == 3:
                self.won = "O"
                return

    def display(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.grid[i*3 + j].displayRow(k)
                    print("   ", end="")
                print()
            print()
        print()


def exploreUTTT(UTTT):
    player_1 = "X"
    player_2 = "O"
    active_player = player_1
    UTTT.display()

    while UTTT.won == "" and not all(UTTT.checkIfWon(i) for i in range(len(UTTT.grid))):
        if UTTT.active_board != -1:
            grid_select = UTTT.active_board
        else: #if grid active_board is -1 meaning we can make a move anywhere
            grid_select = random.randint(0, 8)
            while not UTTT.checkIfGridLegal(grid_select):
                grid_select = random.randint(0, 8)

        square = random.randint(0, 8)
        while UTTT.grid[grid_select].grid[square].occupied != "-":
            square = random.randint(0, 8)

        UTTT.grid[grid_select].move(square, active_player)
        UTTT.grid[grid_select].check_winner()
        UTTT.display()
        UTTT.check_winner()

        if UTTT.won != "":
            print(f"Player {UTTT.won} wins!")
            return

        active_player = player_2 if active_player == player_1 else player_1

    print("It's a tie")



def main():
    uttt = UltimateTicTacToes()
    exploreUTTT(uttt)


if __name__ == '__main__':
    main()
