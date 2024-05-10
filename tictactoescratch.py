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
    for i in range(3):
        # check for a row win
        if game_state[selected_grid][3*i] == game_state[selected_grid][3*i+1] == game_state[selected_grid][3*i+2] != None:
            # update the large grid state
            large_grid_state[selected_grid] = game_state[selected_grid][3*i]
           
            # return the winner
            return game_state[selected_grid][3*i]
        
        # check for a column win
        if game_state[selected_grid][i] == game_state[selected_grid][i+3] == game_state[selected_grid][i+6] != None:
            # update the large grid state
            large_grid_state[selected_grid] = game_state[selected_grid][i]
           
            # return the winner
            return game_state[selected_grid][i]
        
    # check for a diagonal win
    if game_state[selected_grid][0] == game_state[selected_grid][4] == game_state[selected_grid][8] != None:
        # update the large grid state
        large_grid_state[selected_grid] = game_state[selected_grid][0]

        # return the winner
        return game_state[selected_grid][0]
    
    if game_state[selected_grid][2] == game_state[selected_grid][4] == game_state[selected_grid][6] != None:
        # update the large grid state
        large_grid_state[selected_grid] = game_state[selected_grid][2]

        # return the winner
        return game_state[selected_grid][2]
    
    # check for a tie
    count = 0
    for i in range(9):
        if game_state[selected_grid][i] != None:
            count += 1
    
    if count == 9:
        # update the large grid state to indicate a tie
        large_grid_state[selected_grid] = "tie"
        return "tie"
    
    # if no one has won and there is no tie
    return None

def check_large_grid_win_state():
    # check for a row win
    for i in range(0, 9, 3):
        if large_grid_state[i] == large_grid_state[i+1] == large_grid_state[i+2] != None:
            return large_grid_state[i]
    
    # check for a column win
    for i in range(3):
        if large_grid_state[i] == large_grid_state[i+3] == large_grid_state[i+6] != None:
            return large_grid_state[i]
        
    # check for a diagonal win
    if large_grid_state[0] == large_grid_state[4] == large_grid_state[8] != None:
        return large_grid_state[0]
    
    if large_grid_state[2] == large_grid_state[4] == large_grid_state[6] != None:
        return large_grid_state[2]
    
    # check for a tie
    count = 0
    for i in range(9):
        if large_grid_state[i] != None:
            count += 1
        
    if count == 9:
        return "tie"
        
    # if no one has won and there is no tie
    return None

def get_large_grid_input():
    
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
        
        # if the grid is not won hence it is available
        if large_grid_state[selected_grid] == None:
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

# takes in the player/turn, the board, depth, and alpha and beta values
def minimax(player, board, depth, alpha, beta, next_large_grid):
    # if the game is over, return the score
    won_or_tie_minimax = check_large_grid_win_state()
    if won_or_tie_minimax == "X":
        return 1, None
    elif won_or_tie_minimax == "O":
        return -1, None
    elif won_or_tie_minimax == "tie":
        return 0, None

    # if the depth is 0, return the score
    if depth == 0:
        return evaluation(player, board), None

    # if it is the player's turn
    if player == "X":
        # we want to maximize the score
        maxEval = float("-inf")
        best_move = None
        
        # if next_large_grid is None, consider all available large grids
        if next_large_grid == None:
            available_grids = [i for i in range(9) if board[i] == None and large_grid_state[i] == None]
        else:
            available_grids = [next_large_grid] if large_grid_state[next_large_grid] == None else []
        
        for i in available_grids:
            for j in range(9):
                if game_state[i][j] == None:
                    game_state[i][j] = player
                    eval, _ = minimax("O", board, depth - 1, alpha, beta, j)
                    game_state[i][j] = None
                    if eval > maxEval:
                        maxEval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        # we want to minimize the score
        minEval = float("inf")
        best_move = None
        
        # if next_large_grid is None, consider all available large grids
        if next_large_grid == None:
            available_grids = [i for i in range(9) if board[i] == None and large_grid_state[i] == None]
        else:
            available_grids = [next_large_grid] if large_grid_state[next_large_grid] == None else []
        
        for i in available_grids:
            for j in range(9):
                if game_state[i][j] == None:
                    game_state[i][j] = player
                    eval, _ = minimax("X", board, depth - 1, alpha, beta, j)
                    game_state[i][j] = None
                    if eval < minEval:
                        minEval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return minEval, best_move



def evaluation(player, board):
    score = 0

    # Check for wins in each small grid
    for i in range(9):
        if board[i] != None:
            small_grid_score = evaluate_small_grid(player, game_state[i])
            score += small_grid_score
        

    # Check for wins in the large grid
    large_grid_score = evaluate_large_grid(player, board)
    score += large_grid_score * 10  # Giving higher weight to large grid wins

    return score

def evaluate_small_grid(player, small_grid):
    score = 0

    # Check rows
    for i in range(0, 9, 3):
        if small_grid[i] == small_grid[i+1] == small_grid[i+2] == player:
            score += 1
        elif small_grid[i] == small_grid[i+1] == small_grid[i+2] != None and small_grid[i] != player:
            score -= 1

    # Check columns
    for i in range(3):
        if small_grid[i] == small_grid[i+3] == small_grid[i+6] == player:
            score += 1
        elif small_grid[i] == small_grid[i+3] == small_grid[i+6] != None and small_grid[i] != player:
            score -= 1

    # Check diagonals
    if small_grid[0] == small_grid[4] == small_grid[8] == player:
        score += 1
    elif small_grid[0] == small_grid[4] == small_grid[8] != None and small_grid[0] != player:
        score -= 1

    if small_grid[2] == small_grid[4] == small_grid[6] == player:
        score += 1
    elif small_grid[2] == small_grid[4] == small_grid[6] != None and small_grid[2] != player:
        score -= 1

    return score

def evaluate_large_grid(player, board):
    score = 0

    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            score += 1
        elif board[i] == board[i+1] == board[i+2] != None and board[i] != player:
            score -= 1

    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            score += 1
        elif board[i] == board[i+3] == board[i+6] != None and board[i] != player:
            score -= 1

    # Check diagonals
    if board[0] == board[4] == board[8] == player:
        score += 1
    elif board[0] == board[4] == board[8] != None and board[0] != player:
        score -= 1

    if board[2] == board[4] == board[6] == player:
        score += 1
    elif board[2] == board[4] == board[6] != None and board[2] != player:
        score -= 1

    return score

# 0 1 2
# 3 4 5
# 6 7 8

# game logic

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

def get_ai_move(player, depth, next_large_grid):
    _, move = minimax(player, large_grid_state, depth, float("-inf"), float("inf"), next_large_grid)
    if move is None:
        # If no valid move is found, search for any available move
        for i in range(9):
            if large_grid_state[i] == None:
                for j in range(9):
                    if game_state[i][j] == None:
                        return i, j
    return move

while not won_or_tie:
    # determines the player turn
    if turn % 2 == 0:
        print("Player 1's turn (X)")
        # print the next large grid
        print(f"Next large grid: {next_large_grid}")
        
        print(large_grid_state)
        player = human1
        
        # get the large grid input
        if next_large_grid == None:
            selected_grid = get_large_grid_input()
        else:
            selected_grid = next_large_grid

        # get the small grid input
        selected_small_grid = get_small_grid_input(selected_grid)
    else:
        print("AI Player's turn (O)")
        print(large_grid_state)
        player = human2
        
        # get the AI's move
        selected_grid, selected_small_grid = get_ai_move(player, 10, next_large_grid)  # depth adjustable
    
    # update the game state
    game_state[selected_grid][selected_small_grid] = player

    # check if the small grid has been won
    small_grid_winner = check_small_grid_win_state(selected_grid)

    # if the small grid has been won
    if small_grid_winner != None:
        printGameState()
        print(f"Player {small_grid_winner} has won the small grid!")
        next_large_grid = selected_small_grid
    else:
        next_large_grid = selected_small_grid

    # if the next large grid is already won
    if large_grid_state[next_large_grid] != None:
        next_large_grid = None
        
    # check if the large grid has been won
    player_won_or_tie = check_large_grid_win_state()
    if player_won_or_tie != None:
        won_or_tie = True
        break

    turn += 1
    printGameState()



if player_won_or_tie == "tie":
    print("The game ended in a tie!")
else:
    print(f"Player {player_won_or_tie} has won the game!")