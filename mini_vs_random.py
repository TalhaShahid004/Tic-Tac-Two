import random
import customtkinter as ctk
import math
import random
from copy import deepcopy

# ultimate tic tac toe

# I will use a 2d array for the game logic
# Initialise an empty board
game_state = [[None for i in range(9)] for j in range(9)]

large_grid_state = [None for i in range(9)] # None means no one has won


# print(game_state)


def printGameState():
    # Clear the console
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

def Only_check_small_grid_win(selected_grid):
    for i in range(3):
        # check for a row win
        if game_state[selected_grid][3*i] == game_state[selected_grid][3*i+1] == game_state[selected_grid][3*i+2] != None:
            
            # return the winner
            return game_state[selected_grid][3*i]
        
        # check for a column win
        if game_state[selected_grid][i] == game_state[selected_grid][i+3] == game_state[selected_grid][i+6] != None:
            
            # return the winner
            return game_state[selected_grid][i]
        
    # check for a diagonal win
    if game_state[selected_grid][0] == game_state[selected_grid][4] == game_state[selected_grid][8] != None:

        # return the winner
        return game_state[selected_grid][0]
    
    if game_state[selected_grid][2] == game_state[selected_grid][4] == game_state[selected_grid][6] != None:

        # return the winner
        return game_state[selected_grid][2]
    
    # check for a tie
    count = 0
    for i in range(9):
        if game_state[selected_grid][i] != None:
            count += 1
    
    if count == 9:
        # update the large grid state to indicate a tie
        return "tie"
    
    # if no one has won and there is no tie
    return None

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

def check_small_grid_win(selected_grid):
    for i in range(3):
        # check for a row win
        if selected_grid[3 * i] == selected_grid[3 * i + 1] == selected_grid[3 * i + 2] != None:
            # return the winner
            return selected_grid[3 * i]

        # check for a column win
        if selected_grid[i] == selected_grid[i + 3] == selected_grid[i + 6] != None:
            # return the winner
            return selected_grid[i]

    # check for a diagonal win
    if selected_grid[0] == selected_grid[4] == selected_grid[8] != None:
        # return the winner
        return selected_grid[0]
    if selected_grid[2] == selected_grid[4] == selected_grid[6] != None:
        # return the winner
        return selected_grid[2]

    # check for a tie
    count = 0
    for i in range(9):
        if selected_grid[i] != None:
            count += 1
    if count == 9:
        return "tie"

    # if no one has won and there is no tie
    return None

for i in range(9):
    check_small_grid_win_state(i)

def Only_check_large_grid_win_state():
    fakeboard = []
    for i in range(9):
        fakeboard.append(Only_check_small_grid_win(i))
    
    for i in range(0, 9, 3):
        if fakeboard[i] == fakeboard[i+1] == fakeboard[i+2] != None:
            return fakeboard[i]
    
    # check for a column win
    for i in range(3):
        if fakeboard[i] == fakeboard[i+3] == fakeboard[i+6] != None:
            return fakeboard[i]
    
    # check for a diagonal win
    if fakeboard[0] == fakeboard[4] == fakeboard[8] != None:
        return fakeboard[0]
    
    if fakeboard[2] == fakeboard[4] == fakeboard[6] != None:
        return fakeboard[2]
    
    # check for a tie
    count = 0
    for i in range(9):
        if fakeboard[i] != None:
            count += 1
    
    if count == 9:
        return "tie"
    
    # if no one has won and there is no tie
    return None

def game_won(board):
    large_grid_states = [None] * 9

    # Check for a win in each small grid
    for i in range(9):
        small_grid = board[i]
        winner = check_small_grid_win(small_grid)
        large_grid_states[i] = winner

    # Check for a win in the large grid
    large_grid_winner = check_small_grid_win(large_grid_states)
    if large_grid_winner:
        return large_grid_winner

    # Check for a tie
    if all(cell is not None for grid in board for cell in grid):
        return "tie"

    # If no winner and not a tie
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


def minimize(player, board, depth, alpha, beta, next_large_grid):
    won_or_tie = check_large_grid_win_state()
    if won_or_tie == "X":
        return -1, None
    elif won_or_tie == "O":
        return 1, None
    elif won_or_tie == "tie":
        return 0, None

    if depth == 0:
        return evaluation(player, board, next_large_grid), None

    minEval = float("inf")
    best_move = None

    if next_large_grid == None:
        available_grids = [i for i in range(9) if board[i] == None and large_grid_state[i] == None]
    else:
        available_grids = [next_large_grid] if large_grid_state[next_large_grid] == None else [i for i in range(9) if board[i] == None and large_grid_state[i] == None]

    for i in available_grids:
        for j in range(9):
            if game_state[i][j] == None:
                game_state[i][j] = player
                eval, _ = maximize("X", board, depth - 1, alpha, beta, j)
                game_state[i][j] = None
                if eval < minEval:
                    minEval = eval
                    best_move = (i, j)
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
        if beta <= alpha:
            break
    return minEval, best_move

def maximize(player, board, depth, alpha, beta, next_large_grid):
    won_or_tie = check_large_grid_win_state()
    if won_or_tie == "X":
        return -1, None
    elif won_or_tie == "O":
        return 1, None
    elif won_or_tie == "tie":
        return 0, None

    if depth == 0:
        return evaluation(player, board, next_large_grid), None

    maxEval = float("-inf")
    best_move = None

    if next_large_grid == None:
        available_grids = [i for i in range(9) if board[i] == None and large_grid_state[i] == None]
    else:
        available_grids = [next_large_grid] if large_grid_state[next_large_grid] == None else [i for i in range(9) if board[i] == None and large_grid_state[i] == None]

    for i in available_grids:
        for j in range(9):
            if game_state[i][j] == None:
                game_state[i][j] = player
                eval, _ = minimize("O", board, depth - 1, alpha, beta, j)
                game_state[i][j] = None
                if eval > maxEval:
                    maxEval = eval
                    best_move = (i, j)
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
        if beta <= alpha:
            break
    return maxEval, best_move

def minimax(player, board, depth, alpha, beta, next_large_grid):
    # if the game is over, return the score
    eval, best_move = maximize(player,board,depth,alpha,beta,next_large_grid)
    return eval, best_move

LargeGridweights = [
    1.4, 1, 1.4,
    1 , 1.75, 1,
    1.4, 1, 1.4,
]

SmallGridWeights = [
    1,   0.9, 1, 
    0.9, 1.5, 0.9, 
    1,   0.9, 1
]



def evaluation(player, board, nextgrid):
    score = 0
    # Evaluate small grid blocks
    for i in range(9):
        small_grid = game_state[i]
        score += evaluate_small_grid_win(player, small_grid, i, 3)
        score += evaluate_blocking_win(player, small_grid, 2, SmallGridWeights)
        score -= evaluate_small_grid_loss(player, small_grid, 3)
        score += evaluate_grid_two_row(player, small_grid, 1)
        score -= evaluate_avoid_opp_block(player, small_grid, 2)
        score *= LargeGridweights[i]
    
    #score -= evaluate_opponent_adv(player, 3, nextgrid)
    score -= evaluate_large_grid_loss(player, board, 5)
    # Evaluate large grid win
    score += evaluate_large_grid_win(player, board, 5)
    score -= evaluate_avoid_opp_block(player, board, 3)
    # Evaluate large grid block
    score += evaluate_grid_two_row(player, small_grid, 2)
    score += evaluate_blocking_win(player, board, 2, LargeGridweights)
    #if score<0:
    #    print("low score")
    return score

def evaluate_opponent_adv(player, decrement, nextgrid):
    score = 0
    state = Only_check_small_grid_win(nextgrid)
    if state!=None and player == "X":
        score += decrement
    return score

def evaluate_small_grid_loss(player, board, decrement):
    score = 0
    opponent = 'O' if player == 'X' else 'X'
    
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == opponent:
            score += decrement

    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == opponent:
            score += decrement

    # Check diagonals
    if board[0] == board[4] == board[8] == opponent:
        score += decrement

    if board[2] == board[4] == board[6] == opponent:
        score += decrement

    return score

def evaluate_blocking_win(player, grid, increment, weights):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for i in range(0, 9, 3):
        if grid[i] == grid[i+1] == opponent and grid[i+2] == player:
            score += increment
            score *= weights[i + 2]
        elif grid[i] == grid[i+2] == opponent and grid[i+1] == player:
            score += increment
            score *= weights[i + 1]

        elif grid[i+1] == grid[i+2] == opponent and grid[i] == player:
            score += increment
            score *= weights[i]


    # Check columns
    for i in range(3):
        if grid[i] == grid[i+3] == opponent and grid[i+6] == player:
            score += increment
            score *= weights[i + 6]

        elif grid[i] == grid[i+6] == opponent and grid[i+3] == player:
            score += increment
            score *= weights[i + 3]

        elif grid[i+3] == grid[i+6] == opponent and grid[i] == player:
            score += increment
            score *= weights[i ]


    # Check diagonals
    if grid[0] == grid[4] == opponent and grid[8] == player:
        score += increment
        score *= weights[8]

    elif grid[0] == grid[8] == opponent and grid[4] == player:    
        score *= weights[4]
        score += increment
    
    elif grid[4] == grid[8] == opponent and grid[0] == player:
        score += increment
        score *= weights[0]


    if grid[2] == grid[4] == opponent and grid[6] == player:
        score += increment
        score *= weights[6]
    elif grid[2] == grid[6] == opponent and grid[4] == player:
        score += increment
        score *= weights[4]
    elif grid[4] == grid[6] == opponent and grid[2] == player:
        score += increment
        score *= weights[2]
    
    return score

# this function checks if placing a move in a small grid will result in a win
def evaluate_small_grid_win(player, small_grid, gridnum , increment):
    score = 0

    # Check rows
    for i in range(0, 9, 3):
        if small_grid[i] == small_grid[i+1] == small_grid[i+2] == player:
            score += increment
            score*=LargeGridweights[gridnum]
            return score
        

    # Check columns
    for i in range(3):
        if small_grid[i] == small_grid[i+3] == small_grid[i+6] == player:
            score += increment
            score*=LargeGridweights[gridnum]
            return score

    # Check diagonals
    if small_grid[0] == small_grid[gridnum] == small_grid[8] == player:
        score += increment
        score*=LargeGridweights[gridnum]
        return score

    if small_grid[2] == small_grid[gridnum] == small_grid[6] == player:
        score += increment
        score*=LargeGridweights[gridnum]
        return score

    return score

# this evaluation will check if the board has been won by the AI player
def evaluate_large_grid_win(player, board, increment):
    score = 0
    opponent = 'O' if player == 'X' else 'X'
    
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == opponent:
            score += increment

    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == opponent:
            score += increment

    # Check diagonals
    if board[0] == board[4] == board[8] == opponent:
        score += increment

    if board[2] == board[4] == board[6] == opponent:
        score += increment

    return score

def evaluate_large_grid_loss(player, board, decrement):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == opponent:
            score += decrement

    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == opponent:
            score += decrement

    # Check diagonals
    if board[0] == board[4] == board[8] == opponent:
        score += decrement

    if board[2] == board[4] == board[6] == opponent:
        score += decrement

    return score


def evaluate_grid_two_row(player, grid, increment):
    score = 0
    for i in range(0, 9, 3):
        if grid[i] == grid[i+1] == player and grid[i+2] == None:
            score += increment
        elif grid[i] == grid[i+2] == player and grid[i+1] == None:
            score += increment

        elif grid[i+1] == grid[i+2] == player and grid[i] == None:
            score += increment


    # Check columns
    for i in range(3):
        if grid[i] == grid[i+3] == player and grid[i+6] == None:
            score += increment

        elif grid[i] == grid[i+6] == player and grid[i+3] == None:
            score += increment

        elif grid[i+3] == grid[i+6] == player and grid[i] == None:
            score += increment


    # Check diagonals
    if grid[0] == grid[4] == player and grid[8] == None:
        score += increment

    elif grid[0] == grid[8] == player and grid[4] == None:    
        score += increment
    
    elif grid[4] == grid[8] == player and grid[0] == None:
        score += increment

    if grid[2] == grid[4] == player and grid[6] == None:
        score += increment
    elif grid[2] == grid[6] == player and grid[4] == None:
        score += increment
    elif grid[4] == grid[6] == player and grid[2] == None:
        score += increment
    
    return score


def evaluate_avoid_opp_block(player, grid, increment):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for i in range(0, 9, 3):
        if grid[i] == grid[i+1] == opponent and grid[i+2] == player:
            score += increment
        elif grid[i] == grid[i+2] == opponent and grid[i+1] == player:
            score += increment

        elif grid[i+1] == grid[i+2] == opponent and grid[i] == player:
            score += increment


    # Check columns
    for i in range(3):
        if grid[i] == grid[i+3] == opponent and grid[i+6] == player:
            score += increment

        elif grid[i] == grid[i+6] == opponent and grid[i+3] == player:
            score += increment

        elif grid[i+3] == grid[i+6] == opponent and grid[i] == player:
            score += increment


    # Check diagonals
    if grid[0] == grid[4] == opponent and grid[8] == player:
        score += increment

    elif grid[0] == grid[8] == opponent and grid[4] == player:    
        score += increment
    
    elif grid[4] == grid[8] == opponent and grid[0] == player:
        score += increment

    if grid[2] == grid[4] == opponent and grid[6] == player:
        score += increment
    elif grid[2] == grid[6] == opponent and grid[4] == player:
        score += increment
    elif grid[4] == grid[6] == opponent and grid[2] == player:
        score += increment
    
    return score

# game logic

# userinput


# printGameState()

human1 = "X"
human2 = "O"

def get_ai_move(player, depth, next_large_grid, AI):
    if AI == "mini":
        _, move = minimax(player, large_grid_state, depth, float("-inf"), float("inf"), next_large_grid)
        # print("mini")
    if move is None:
        # If no valid move is found, search for any available move
        for i in range(9):
            if large_grid_state[i] == None:
                for j in range(9):
                    if game_state[i][j] == None:
                        return i, j
    return move

# using custom tkinter, i want to build a gui for the game
# i have the game state in the variable game_state as a 2d array
# i will use the game_state to update the gui after each button click
# the playable large grids will be outlined in yellow, 
# the playable grid is found in the next_large_grid variable
# If a large grid has been won, then change the background colours of the buttons to a darker shade of the winning player
# if there is a tie, then change the background colour of the buttons to grey
# for human moves 'O', we use dark blue, for AI moves 'X', we use red. 
# the default colour is blue for the buttons


class SmallGrid(ctk.CTkFrame):
    def __init__(self, master, large_row, large_col, on_button_click):
        super().__init__(master)
        self.buttons = []
        self.large_row = large_row
        self.large_col = large_col
        
        for r in range(3):
            self.grid_rowconfigure(r, weight=1)
            self.grid_columnconfigure(r, weight=1)
            for c in range(3):
                button = ctk.CTkButton(self, text="", width=50, height=50, corner_radius=1)
                button.grid(row=r, column=c, sticky="nsew")
                self.buttons.append(button)
                
minimaxdepth = 4
mcts_int = 500
minimax_wins = 0
random_wins = 0
ties = 0
total_moves = 0
num_games = 5
won_or_tie = False
player_won_or_tie = None
next_large_grid = None
turn = 0
game_moves = 0


if minimaxdepth % 2==1:
    if minimaxdepth > 6:
        minimaxdepth -= 1
    else:
        minimaxdepth += 1
    
def reset_game():
    global game_state, large_grid_state
    game_state = [[None for i in range(9)] for j in range(9)]
    large_grid_state = [None for i in range(9)]

def gui():
    global minimax_wins, random_wins, ties, total_moves, won_or_tie, player_won_or_tie, next_large_grid, turn, game_moves

    for game_num in range(1, num_games + 1):
        reset_game()
        won_or_tie = False
        player_won_or_tie = None
        next_large_grid = None
        turn = 0
        game_moves = 0  # Initialize game_moves to 0 for each game

        app = ctk.CTk()
        app.title(f"Ultimate Tic Tac Toe - Game {game_num}")
        app.minsize(400, 400)
        app.resizable(False, False)

        grid_frames = []

        # Create player title
        turn_label = ctk.CTkLabel(app, text="Minimax's turn", font=("Arial", 16))
        turn_label.pack(pady=(10, 0))

        # Create a 3x3 grid of small grids
        main_frame = ctk.CTkFrame(app)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        for i in range(3):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
            for j in range(3):
                outer_frame = ctk.CTkFrame(main_frame)
                outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
                grid_frame = SmallGrid(outer_frame, i, j, None)
                grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
                grid_frames.append(outer_frame)

        def check_game_over():
            global minimax_wins, random_wins, ties, total_moves, won_or_tie, player_won_or_tie

            if won_or_tie:
                if player_won_or_tie == "tie":
                    ties += 1
                elif player_won_or_tie == "X":
                    minimax_wins += 1
                else:
                    random_wins += 1
                total_moves += game_moves
                app.after(2000, app.destroy)  # Close the window after 2 seconds

        def update_gui():
            for i in range(9):
                for j in range(9):
                    cell_value = game_state[i][j]
                    small_row = j // 3
                    small_col = j % 3
                    button_index = small_row * 3 + small_col
                    button = grid_frames[i].winfo_children()[0].buttons[button_index]

                    if cell_value == 'X':
                        button.configure(text='X', fg_color="#4B7BE5")
                    elif cell_value == 'O':
                        button.configure(text='O', fg_color="#F08080")
                    else:
                        button.configure(text='', fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

            # Highlight playable large grids
            for i in range(9):
                if next_large_grid is None or next_large_grid == i:
                    if large_grid_state[i] is None:
                        grid_frames[i].configure(border_width=2, border_color="yellow")
                    else:
                        grid_frames[i].configure(border_width=0)
                else:
                    grid_frames[i].configure(border_width=0)

            # Update large grid state colors
            for i in range(9):
                if large_grid_state[i] == 'X':
                    for button in grid_frames[i].winfo_children()[0].buttons:
                        button.configure(fg_color="blue")
                elif large_grid_state[i] == 'O':
                    for button in grid_frames[i].winfo_children()[0].buttons:
                        button.configure(fg_color="red")
                elif large_grid_state[i] == 'tie':
                    for button in grid_frames[i].winfo_children()[0].buttons:
                        button.configure(fg_color="gray")

        def play_game():
            global won_or_tie, player_won_or_tie, next_large_grid, turn, game_moves

            if not won_or_tie:
                if turn % 2 == 0:
                    # Minimax player's turn
                    depth = minimaxdepth
                    player = "X"
                    grid = next_large_grid
                    selected_grid, selected_small_grid = get_ai_move(player, depth, grid, "mini")
                    game_state[selected_grid][selected_small_grid] = "X"

                    small_grid_winner = check_small_grid_win_state(selected_grid)

                    if small_grid_winner is not None:
                        print(f"{small_grid_winner} has won the small grid!")
                        next_large_grid = selected_small_grid
                    else:
                        next_large_grid = selected_small_grid

                    if large_grid_state[next_large_grid] is not None:
                        next_large_grid = None

                    player_won_or_tie = check_large_grid_win_state()
                    if player_won_or_tie is not None:
                        won_or_tie = True

                    if won_or_tie:
                        check_game_over()

                    turn += 1
                    turn_label.configure(text="Random Agent's turn")
                    game_moves += 1  # Increment game_moves for each move
                    update_gui()

                elif turn % 2 != 0:
                    # Random agent's turn
                    player = "O"
                    available_moves = []
                    if next_large_grid is None:
                        for i in range(9):
                            if large_grid_state[i] is None:
                                for j in range(9):
                                    if game_state[i][j] is None:
                                        available_moves.append((i, j))
                    else:
                        for j in range(9):
                            if game_state[next_large_grid][j] is None:
                                available_moves.append((next_large_grid, j))

                    if available_moves:
                        selected_grid, selected_small_grid = random.choice(available_moves)
                        game_state[selected_grid][selected_small_grid] = "O"

                        small_grid_winner = check_small_grid_win_state(selected_grid)

                        if small_grid_winner is not None:
                            print(f"{small_grid_winner} has won the small grid!")
                            next_large_grid = selected_small_grid
                        else:
                            next_large_grid = selected_small_grid

                        if large_grid_state[next_large_grid] is not None:
                            next_large_grid = None

                        player_won_or_tie = check_large_grid_win_state()
                        if player_won_or_tie is not None:
                            won_or_tie = True

                        if won_or_tie:
                            check_game_over()

    

                        turn += 1
                        turn_label.configure(text="Minimax's turn")
                        game_moves += 1  # Increment game_moves for each move
                        update_gui()

            if not won_or_tie:
                app.after(10, play_game)  # Schedule the next move after a 500ms delay
                
        update_gui()
        app.after(50, play_game)  # Start the game loop
        app.mainloop()

    print(f"Minimax wins: {minimax_wins}")
    print(f"Random wins: {random_wins}")
    print(f"Ties: {ties}")
    print(f"Average moves per game: {total_moves / num_games}")

gui()