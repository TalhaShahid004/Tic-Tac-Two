# ultimate tic tac toe

# I will use a 2d array for the game logic
# Initialise an empty board
game_state = [[None for i in range(9)] for j in range(9)]
print(game_state)

def printGameState():
    print("Ultimate Tic Tac Toe Board:")

    print("-----------------------------")
    
    for i in range(0, 9, 3):
        for j in range(3):
            for k in range(i, i+3):
                print("|", end=" ")
                for l in range(3):
                    if game_state[k][3*j+l] == None:
                        print(" ", end=" ")
                    else:
                        print(game_state[k][3*j+l], end=" ")
                print("|", end=" ")
            print()
        print("-----------------------------")

# can return X, 0, tie or None
def check_small_grid_win_state(selected_grid):
    # check for a win in the selected small grid
    # if there is, return the winner (X or O)
    # if there is no win, return None


    for i in range(3):
        # check for a row win
        if game_state[selected_grid][i] == game_state[selected_grid][i+1] == game_state[selected_grid][i+2]:
            # update the large grid state
            large_grid_state[selected_grid] = game_state[selected_grid][i]
           
            # return the winner
            return game_state[selected_grid][i]
        
        # check for a column win
        if game_state[selected_grid][i] == game_state[selected_grid][i+3] == game_state[selected_grid][i+6]:
            # update the large grid state
            large_grid_state[selected_grid] = game_state[selected_grid][i]
           
            # return the winner
            return game_state[selected_grid][i]
        

    for i in range(0, 3, 2):
        # check for a diagonal win
        if game_state[selected_grid][i] == game_state[selected_grid][4] == game_state[selected_grid][8-i]:
            # update the large grid state
            large_grid_state[selected_grid] = game_state[selected_grid][i]

            # return the winner
            return game_state[selected_grid][i]

    # check for a tie
    for i in range(9):
        count = 0
        if game_state[selected_grid][i] != None:
            count += 1
    
        if count == 9:
            return "tie"
    
    # if no one has won and there is no tie
    return None

def check_large_grid_win_state():
    # check for a row win
    for i in range(3):
        if large_grid_state[i] == large_grid_state[i+1] == large_grid_state[i+2]:
            player_won_or_tie = large_grid_state[i]
            won_or_tie = True
            next_large_grid = None
            return large_grid_state[i]
    
    # check for a column win
    for i in range(3):
        if large_grid_state[i] == large_grid_state[i+3] == large_grid_state[i+6]:
            player_won_or_tie = large_grid_state[i]
            won_or_tie = True
            next_large_grid = None
            return large_grid_state[i]
        
    # check for a diagonal win
    if large_grid_state[0] == large_grid_state[4] == large_grid_state[8]:
        player_won_or_tie = large_grid_state[0]
        won_or_tie = True
        next_large_grid = None
        return large_grid_state[0]
    
    if large_grid_state[2] == large_grid_state[4] == large_grid_state[6]:
        player_won_or_tie = large_grid_state[2]
        won_or_tie = True
        next_large_grid = None 
        return large_grid_state[2]
    
    # check for a tie
    for i in range(9):
        count = 0
        if large_grid_state[i] != None:
            count += 1
        
        if count == 9:
            won_or_tie = True
            return "tie"
        
    # if no one has won and there is no tie
    return None

def get_large_grid_input(exclude_grids=None):
    while True:
        # input validation for large grid row
        while True:
            largeGridRow = input("What is your large grid row? (1-3) ")
            if largeGridRow.isdigit() and 1 <= int(largeGridRow) <= 3:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")
        
        # input validation for large grid column
        while True:
            largeGridColumn = input("What is your large grid column? (1-3) ")
            if largeGridColumn.isdigit() and 1 <= int(largeGridColumn) <= 3:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")   
        
        # map the large grid row and column to an index 0-8
        selected_grid = 3 * (int(largeGridRow) - 1) + (int(largeGridColumn) - 1)
        
        # if the grid is not won and not excluded
        if large_grid_state[selected_grid] == None and (exclude_grids is None or selected_grid not in exclude_grids):
            return selected_grid
        else:
            print("The selected large grid is already won or not available. Please choose another one.")


def get_small_grid_input(selected_grid):
    while True:
        # input validation for move's row
        while True:
            rowMove = input("What is your move's row? (1-3) ")
            if rowMove.isdigit() and 1 <= int(rowMove) <= 3:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")   

        # input validation for move's column
        while True:
            columnMove = input("What is your move's column? (1-3) ")
            if columnMove.isdigit() and 1 <= int(columnMove) <= 3:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")   
        
        # map the move's row and column to an index 0-8
        small_grid_index = 3 * (int(rowMove) - 1) + (int(columnMove) - 1)
        
        # check if the spot is not already played
        if game_state[selected_grid][small_grid_index] == None:
            return small_grid_index
        else:
            print("That spot is already played. Please choose another one.")

# 0 1 2
# 3 4 5
# 6 7 8

# game logic

# userinput
won_or_tie = False
player_won_or_tie = None
next_large_grid = None  
large_grid_state = [None for i in range(9)] # None means no one has won
turn = 0

# sample output check 
# game_state[0][0] = "X"
# game_state[0][1] = "X"
# game_state[0][2] = "X"

# game_state[1][0] = "X"
# game_state[1][3] = "X"
# game_state[1][6] = "X"

# game_state[2][0] = "X"
# game_state[2][4] = "X"
# game_state[2][8] = "X"

printGameState()

human1 = "X"
human2 = "O"

# sample large grid check
# large_grid_state[0] = "X"


# game logic

# userinput
won_or_tie = False
player_won_or_tie = None
next_large_grid = None  
large_grid_state = [None for i in range(9)] # None means no one has won
turn = 0

printGameState()

human1 = "X"
human2 = "O"

while not won_or_tie:
    if turn % 2 == 0:
        print("Player 1's turn (X)")
        player = human1
    else:
        print("Player 2's turn (O)")
        player = human2
    
    if next_large_grid is None or large_grid_state[next_large_grid] is not None:
        selected_grid = get_large_grid_input()
    else:
        selected_grid = next_large_grid
    
    small_grid_index = get_small_grid_input(selected_grid)
    game_state[selected_grid][small_grid_index] = player
    
    small_grid_winner = check_small_grid_win_state(selected_grid)
    
    if small_grid_winner is not None:
        print(f"Player {player} has won the small grid at position {selected_grid}!")
    
    large_grid_winner = check_large_grid_win_state()
    
    if large_grid_winner is not None:
        won_or_tie = True
        player_won_or_tie = large_grid_winner
    
    next_large_grid = small_grid_index
    
    if large_grid_state[next_large_grid] is not None:
        print("The next large grid is already won. Please choose any non-won grid.")
        next_large_grid = None
    
    turn += 1
    printGameState()


if player_won_or_tie == "tie":
    print("The game ended in a tie!")
else:
    print(f"Player {player_won_or_tie} has won the game!")