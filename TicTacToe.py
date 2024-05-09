import random
import time

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
        try:
            self.grid[square_num].occupy(player)
        except TypeError:
            print("type error")
            raise Exception("Rare condition of Crashing where the end is reached without ending the game")

    def assign_score(self, score):
        self.value = score    

    def evaluate_func(self):
         # Winning conditions
        if self.won == "X":
            return 1
        elif self.won == "O":
            return -1
        elif self.is_draw():
            return 0

        # Heuristic evaluation
        score = 0
        x_count = self.count("X")
        o_count = self.count("O")
            # Favor local boards with more X's and fewer O's
        score += (x_count - o_count) / (x_count + o_count + 1)
        return score

    def is_draw(self):
        for n in self.grid:
            if (n.occupied == "-"):
                return False
        return True
    
    def count(self, player):
        count = 0
        for i in self.grid:
            if i.occupied == player :
                count+=1
        return count

    def check_winner(self):
        for combo in self.winning_combinations:
            symbols = [self.grid[i].occupied for i in combo]
            if symbols.count("X") == 3:
                return "X"
            elif symbols.count("O") == 3:
                return "O"
        return ""
    
    def set_won(self, player):
        self.won = player

    def display(self):
        for i in range(3):
            for j in range(3):
                print(self.grid[i*3 + j].occupied, end=", ")
            print()
        print()

    def displayRow(self, i):
        for j in range(3):
            print(self.grid[i * 3 + j].occupied, end=", ")


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
        self.check_winner() #checking if game is won
        self.active_board = square_num if self.grid[square_num].won == "" else -1

    def checkIfWon(self, i):
        return self.grid[i].won != ""

    def checkIfGridLegal(self, i): # a board is legal to move into if it has not been won
        if (not self.checkIfWon(i)): #and (self.active_board == -1 or self.active_board == i):
            return True
        return False

    def assign_score(self, score):
        self.value = score

    def check_winner(self):
        tictactoe = convert_to_tictactoe(self)
        self.won = tictactoe.check_winner()

    def display(self):
        print("________________________________")
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.grid[i * 3 + k].displayRow(j)
                    print("   ", end="")
                print()
            print()
        print()



def exploreUTTT(UTTT):
    player_1 = "X"
    player_2 = "O"
    active_player = player_1
    UTTT.display()
    player = ["X","0"]
    depth = 2   
    while UTTT.won == "" and not all(UTTT.checkIfWon(i) for i in range(len(UTTT.grid))):

        #### this part is playing the actual game
         # selecting the grid to play on ( needs logic later )
        if UTTT.active_board != -1:
            grid_select = UTTT.active_board
        else: #if grid active_board is -1 meaning we can make a move anywhere ( need to make this selecting the best possible grid )
            newgrid = convert_to_tictactoe(UTTT)
            _, grid_select = minimax_tictactoe(player, newgrid, depth)

        
        board = UTTT.grid[grid_select] # using the tictactoe board given by grid_select
        _, square = minimax_tictactoe(player, board, depth)

        UTTT.grid[grid_select].move(square, active_player) # doing the actual move
        UTTT.grid[grid_select].won = UTTT.grid[grid_select].check_winner() # check if the current tictactoe board is won
        if UTTT.checkIfGridLegal(square):
            UTTT.active_board = square # this selects the next grid to play on
        else:
            UTTT.active_board = -1
        UTTT.display() 
        UTTT.check_winner() # check if the overal board is won

        #Adding delay for output here
        time.sleep(0)

        if UTTT.won != "": # finishing the game if won
            print(f"Player {UTTT.won} wins!")
            return

        active_player = player_2 if active_player == player_1 else player_1
        swap(player)

    print("It's a tie")

def convert_to_tictactoe(UTTT): # this function is ONLY used for making the UTTT board into a normal tictactoe board so we can play on it
    newtictactoe = tictactoe()
    for i in range(9):
        newtictactoe.grid[i].occupy(UTTT.grid[i].won)
        if newtictactoe.grid[i].occupied == "":
            newtictactoe.grid[i].occupy("-")
    return newtictactoe

def minimax_tictactoe(player, board, depth):
    best_score, best_move = maximize_tictactoe(player, board, -float('inf'), float('inf'), depth)
    return best_score, best_move

def maximize_tictactoe(player, board, alpha, beta, depth):
    won = board.check_winner()
    if won == player[0]: # if the current playing player is winning then return 1 (default X)
        return 1, None
    elif won == player[1]: # if its his opponent return 0 (default O)
        return -1, None
    elif depth == 0: # if leaf has been reached
        return board.evaluate_func(), None
    
    best_move = None
    new_score = -float('inf')
    for r in range(9):
        if board.grid[r].occupied == "-":
            board.grid[r].occupy(player[0])
            score,_ = minimize_tictactoe(player, board, alpha, beta, depth - 1)
            if new_score < score: #applying min
                new_score = score
                best_move = r
            alpha = max(new_score, alpha)
            board.grid[r].occupy("-")
            if alpha>=beta:
                break
    return new_score, best_move

def minimize_tictactoe(player, board, alpha, beta, depth):
    board.check_winner()
    if board.won == player[1]: # if the current playing player is winning then return 1
        return 1, None
    elif board.won == player[0]: # if its his opponent return 0
        return -1, None
    elif depth == 0: # if leaf has been reached
        return board.evaluate_func(), None
    
    best_move = None
    new_score = float('inf')
    for r in range(9):
        if board.grid[r].occupied == "-":
            board.grid[r].occupy(player[1])
            score,_ = maximize_tictactoe(player, board, alpha, beta, depth - 1)
            if new_score < score: #applying min
                new_score = score
                best_move = r
            alpha = max(new_score, alpha)
            board.grid[r].occupy("-")
            if alpha>=beta:
                break
    return new_score, best_move

def swap(arr):
    n = arr[0]
    arr[0] = arr[1]
    arr[1] = n

def main():
    uttt = UltimateTicTacToes()
    exploreUTTT(uttt)


if __name__ == '__main__':
    main() # good luck
