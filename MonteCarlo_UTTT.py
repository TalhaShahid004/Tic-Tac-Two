import customtkinter as ctk
import random
import math
from copy import deepcopy

# ultimate tic tac toe

# I will use a 2d array for the game logic
# Initialise an empty board
game_state = [[None for i in range(9)] for j in range(9)]
# print(game_state)


def printGameState(grid=game_state):
    print("Ultimate Tic Tac Toe Board:")

    print("-----------------------------")
    for i in range(0, 9, 3):
        for j in range(3):
            for k in range(i, i+3):
                print("|", end=" ")
                for l in range(3):
                    if grid[k][3*j+l] == None:
                        print(" ", end=" ")
                    else:
                        print(grid[k][3*j+l], end=" ")
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


LargeGridweights = [
    1.4, 1, 1.4,
    1 , 1.75, 1,
    1.4, 1, 1.4,
]

SmallGridWeights = [
    0.2,   0.17, 0.2, 
    0.17, 0.22, 0.17, 
    0.2,   0.17, 0.2
]

# Define the Node class for MCTS
class Node:
    """
        Represents a node in the Monte Carlo Tree Search (MCTS) algorithm.

        Attributes:
            board (list): The game board representing the state of the game.
            parent (Node): The parent node of this node. None if it's the root node.
            children (list): The list of child nodes of this node.
            next_small_grid (tuple): The coordinates of the small grid where the next move can be played legally.
            wins (int): The number of simulated games won from this node.
            visits (int): The number of times this node has been visited during simulations.
    """
    def __init__(self, board, player, parent=None, next_small_grid=None, move=None):
        """
        Initialize a node with the given game board, parent node, and next small grid.

        Args:
            board (list): The game board representing the state of the game.
            parent (Node, optional): The parent node of this node. Defaults to None.
            next_small_grid (tuple, optional): The coordinates of the small grid where the next move can be played legally. Defaults to None.
        """
        self.board = board
        self.parent = parent
        self.children = {}
        self.next_small_grid = next_small_grid
        self.move = move
        self.player = player
        self.wins = 0
        self.visits = 0



# Function to perform MCTS and return the best move
def mcts(player, gameState, iterations, next_small_grid):
    game = deepcopy(gameState)
    root = Node(game, player, None, next_small_grid, None)
    make_children(player, root)
    for i in range(iterations):
        #print(f"iteration: i")
        node = root
        current_state = deepcopy(game)
        # Selection phase
        node = select_best_child(node)
        current_state[node.move[0]][node.move[1]] = player
        #print(f"move= {node.move}")
        player = "O" if player == "X" else "X"
        # Simulation and backprop
        simulate_random_playout(node, current_state, player)
    # Select the best move based on the most visited child
    best_child = max(root.children.values(), key=lambda child: child.visits)
    return best_child.move

def make_children(player, node):
    #print(f"Moves after node {node.move} with player {player}:")
    if node.next_small_grid is None:
        # If the next grid wasn't playable, find the first available small grid
        for i in range(9):
            if check_small_grid_win(node.board[i]) is None:
                node.next_small_grid = i
                break

    if node.next_small_grid is not None:
        for i in range(9):
            if node.board[node.next_small_grid][i] is None:
                board_copy = [row[:] for row in node.board]
                board_copy[node.next_small_grid][i] = player
                next_small = i if check_small_grid_win(board_copy[i]) is None else None
                move = [node.next_small_grid, i]
                child = Node(board_copy, node.player, node, next_small, move)
                #print(f"row, col = {node.next_small_grid}, {i}, next small = {next_small}")
                node.children[node.next_small_grid, i] = child
    else:
        # If all small grids are won, allow moves in any available position
        for i in range(9):
            for j in range(9):
                if node.board[i][j] is None:
                    board_copy = [row[:] for row in node.board]
                    board_copy[i][j] = player
                    move = [i, j]
                    child = Node(board_copy, node.player, node, None, move)
                    node.children[i,j]=child


# Function to backpropagate the result of a playout
def backpropagate(node, winner):
    while node is not None:
        node.visits += 1
        if winner == node.player:
            node.wins += 1
        node = node.parent


# Function to simulate a random playout from a node with both players making random moves
def simulate_random_playout(node, gameState, player):
    #print("Simulation started")
    current_state = deepcopy(gameState)
    child = node
    make_children(player, child)
    while game_won(current_state) is None:
        maxmove = -2
        move = None
        # Choosing best child
        for moves in child.children.keys():
            if LargeGridweights[moves[0]] + SmallGridWeights[moves[1]] > maxmove:
                move = moves
                maxmove = LargeGridweights[moves[0]] + SmallGridWeights[moves[1]]
        child = child.children.get(move)
        #move, child = random.choice(list(child.children.items()))  # Access move and child tuple
        #print(move)
        current_state[move[0]][move[1]] = player
        player = "O" if player == "X" else "X"  # Alternate players
        #printGameState(current_state)
        if game_won(current_state) is not None:
            break
        make_children(player, child)
    winner = game_won(current_state)
    #print(f"Winner: {winner}")
    backpropagate(child, winner)
    #Sprint("game finished")
    return winner


# Function to select the best child node using UCB1 formula
def select_best_child(node):
    best_child = None
    best_score = -float('inf')
    for child in node.children.values():
        if child.visits == 0:
            return child
        score = child.wins / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits)
        if score > best_score:
            best_child = child
            best_score = score
    return best_child




# def evaluation(player, board, next_large_grid):
  
#     score = 0

#     # Prioritize sending the opponent to an already won grid
#     score += prioritise_sending_to_already_won_grid(player, board, next_large_grid)

#     # Prioritize winning the large grid
#     score += prioritise_large_grid_win(player, board)

#     # Block the opponent from winning the large grid
#     score += block_large_grid_win(player, board)

#     # Prioritize winning the small grids
#     for i in range(9):
#         score += prioritise_small_grid_wins(player, game_state[i]) * SmallGridWeights[i]

#     # Block the opponent from winning the small grids
#     for i in range(9):
#         score += block_small_grid_win(player, game_state[i]) * SmallGridWeights[i]

#     # Prioritize adjacent moves in the large grid
#     score += prioritise_adjacent_moves_large_grid(player, board) * LargeGridweights[4]

#     # Prioritize adjacent moves in the small grids
#     for i in range(9):
#         score += prioritise_adjacent_moves_small_grid(player, game_state[i]) * SmallGridWeights[i]

#     return score


# def block_large_grid_win(player, large_grid):
#     # we want to block the player from winning the large grid
#     # if there is a move that blocks the player, add a score of 800

#     score = 0

#     # large_grid is a 9 element array
    
#     # row win check
#     for i in range(0, 9, 3):
#         if large_grid[i] == large_grid[i+1] == player and large_grid[i+2] == None:
#             score += 3000
#         if large_grid[i] == large_grid[i+2] == player and large_grid[i+1] == None:
#             score += 3000
#         if large_grid[i+1] == large_grid[i+2] == player and large_grid[i] == None:
#             score += 3000

#     # column win check
#     for i in range(3):
#         if large_grid[i] == large_grid[i+3] == player and large_grid[i+6] == None:
#             score += 3000
#         if large_grid[i] == large_grid[i+6] == player and large_grid[i+3] == None:
#             score += 3000
#         if large_grid[i+3] == large_grid[i+6] == player and large_grid[i] == None:
#             score += 3000

#     # diagonal win check
#     if large_grid[0] == large_grid[4] == player and large_grid[8] == None:
#         score += 3000
#     if large_grid[0] == large_grid[8] == player and large_grid[4] == None:
#         score += 3000
#     if large_grid[4] == large_grid[8] == player and large_grid[0] == None:
#         score += 3000
#     if large_grid[2] == large_grid[4] == player and large_grid[6] == None:
#         score += 3000
#     if large_grid[2] == large_grid[6] == player and large_grid[4] == None:
#         score += 3000
#     if large_grid[4] == large_grid[6] == player and large_grid[2] == None:
#         score += 3000



#     return score

# # this is overall win 
# def prioritise_large_grid_win(player, large_grid):
#     # we want to help the player win in the large grid
#     # if there is a move that helps the player win, add a score of 10000

#     score = 0

#     # large_grid is a 9 element array

#     # row win check
#     for i in range(0, 9, 3):
#         if large_grid[i] == large_grid[i+1] == player and large_grid[i+2] == None:
#             score += 10000
#         if large_grid[i] == large_grid[i+2] == player and large_grid[i+1] == None:
#             score += 10000
#         if large_grid[i+1] == large_grid[i+2] == player and large_grid[i] == None:
#             score += 10000

#     # column win check
#     for i in range(3):
#         if large_grid[i] == large_grid[i+3] == player and large_grid[i+6] == None:
#             score += 10000
#         if large_grid[i] == large_grid[i+6] == player and large_grid[i+3] == None:
#             score += 10000
#         if large_grid[i+3] == large_grid[i+6] == player and large_grid[i] == None:
#             score += 10000

#     # diagonal win check
#     if large_grid[0] == large_grid[4] == player and large_grid[8] == None:
#         score += 10000
#     if large_grid[0] == large_grid[8] == player and large_grid[4] == None:
#         score += 10000
#     if large_grid[4] == large_grid[8] == player and large_grid[0] == None:
#         score += 10000
#     if large_grid[2] == large_grid[4] == player and large_grid[6] == None:
#         score += 10000
#     if large_grid[2] == large_grid[6] == player and large_grid[4] == None:
#         score += 10000
#     if large_grid[4] == large_grid[6] == player and large_grid[2] == None:
#         score += 10000

#     return score

# def block_small_grid_win(player, small_grid):
#     # we want to block the player from winning the small grid
#     # if there is a move that blocks the player, add a score of 800

#     score = 0

#     # small_grid is a 9 element array
    
#     # row win check
#     for i in range(0, 9, 3):
#         if small_grid[i] == small_grid[i+1] == player and small_grid[i+2] == None:
#             score += 80
#         if small_grid[i] == small_grid[i+2] == player and small_grid[i+1] == None:
#             score += 80
#         if small_grid[i+1] == small_grid[i+2] == player and small_grid[i] == None:
#             score += 80

#     # column win check
#     for i in range(3):
#         if small_grid[i] == small_grid[i+3] == player and small_grid[i+6] == None:
#             score += 80
#         if small_grid[i] == small_grid[i+6] == player and small_grid[i+3] == None:
#             score += 80
#         if small_grid[i+3] == small_grid[i+6] == player and small_grid[i] == None:
#             score += 80

#     # diagonal win check
#     if small_grid[0] == small_grid[4] == player and small_grid[8] == None:
#         score += 80
#     if small_grid[0] == small_grid[8] == player and small_grid[4] == None:
#         score += 80
#     if small_grid[4] == small_grid[8] == player and small_grid[0] == None:
#         score += 80
#     if small_grid[2] == small_grid[4] == player and small_grid[6] == None:
#         score += 80
#     if small_grid[2] == small_grid[6] == player and small_grid[4] == None:
#         score += 80
#     if small_grid[4] == small_grid[6] == player and small_grid[2] == None:
#         score += 80

#     return score

# def prioritise_small_grid_wins(player, small_grid):
#     # we want to help the player win in the small grid
#     # if there is a move that helps the player win, add a score of 100

#     score = 0

#     # small_grid is a 9 element array

#     # row win check
#     for i in range(0, 9, 3):
#         if small_grid[i] == small_grid[i+1] == player and small_grid[i+2] == None:
#             score += 100
#         if small_grid[i] == small_grid[i+2] == player and small_grid[i+1] == None:
#             score += 100
#         if small_grid[i+1] == small_grid[i+2] == player and small_grid[i] == None:
#             score += 100

#     # column win check
#     for i in range(3):
#         if small_grid[i] == small_grid[i+3] == player and small_grid[i+6] == None:
#             score += 100
#         if small_grid[i] == small_grid[i+6] == player and small_grid[i+3] == None:
#             score += 100
#         if small_grid[i+3] == small_grid[i+6] == player and small_grid[i] == None:
#             score += 100

#     # diagonal win check
#     if small_grid[0] == small_grid[4] == player and small_grid[8] == None:
#         score += 100
#     if small_grid[0] == small_grid[8] == player and small_grid[4] == None:
#         score += 100
#     if small_grid[4] == small_grid[8] == player and small_grid[0] == None:
#         score += 100
#     if small_grid[2] == small_grid[4] == player and small_grid[6] == None:
#         score += 100
#     if small_grid[2] == small_grid[6] == player and small_grid[4] == None:
#         score += 100
#     if small_grid[4] == small_grid[6] == player and small_grid[2] == None:
#         score += 100

#     return score


# def prioritise_sending_to_already_won_grid(player, large_grid, next_large_grid):
#     score = 0

#     if next_large_grid is not None:
#         score += 50

#     return score

# def prioritise_adjacent_moves_large_grid(player, large_grid):
#     score = 0
    
#     # Check rows
#     for i in range(0, 9, 3):
#         if large_grid[i] == player and large_grid[i+1] == None:
#             score += 100
#         if large_grid[i+1] == player and large_grid[i+2] == None:
#             score += 100
    
#     # Check columns
#     for i in range(3):
#         if large_grid[i] == player and large_grid[i+3] == None:
#             score += 100
#         if large_grid[i+3] == player and large_grid[i+6] == None:
#             score += 100
    
#     # Check diagonals
#     if large_grid[0] == player and large_grid[4] == None:
#         score += 100
#     if large_grid[4] == player and large_grid[8] == None:
#         score += 100
#     if large_grid[2] == player and large_grid[4] == None:
#         score += 100
#     if large_grid[4] == player and large_grid[6] == None:
#         score += 100
    
#     return score

# def prioritise_adjacent_moves_small_grid(player, small_grid):
#     score = 0
    
#     # Check rows
#     for i in range(0, 9, 3):
#         if small_grid[i] == player and small_grid[i+1] == None:
#             score += 10
#         if small_grid[i+1] == player and small_grid[i+2] == None:
#             score += 10
    
#     # Check columns
#     for i in range(3):
#         if small_grid[i] == player and small_grid[i+3] == None:
#             score += 10
#         if small_grid[i+3] == player and small_grid[i+6] == None:
#             score += 10
    
#     # Check diagonals
#     if small_grid[0] == player and small_grid[4] == None:
#         score += 10
#     if small_grid[4] == player and small_grid[8] == None:
#         score += 10
#     if small_grid[2] == player and small_grid[4] == None:
#         score += 10
#     if small_grid[4] == player and small_grid[6] == None:
#         score += 10
    
#     return score

# game logic

# userinput
won_or_tie = False
player_won_or_tie = None
next_large_grid = None  
large_grid_state = [None for i in range(9)] # None means no one has won
turn = 0

# printGameState()

human1 = "X"
human2 = "O"

def get_ai_move(player, iterations, next_large_grid):
    move = mcts(player, game_state, iterations, next_large_grid)
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
                button = ctk.CTkButton(self, text="", width=50, height=50, corner_radius=1,
                                       command=lambda b=r, a=c: on_button_click(b, a, self.large_row, self.large_col))
                button.grid(row=r, column=c, sticky="nsew")
                self.buttons.append(button)

def gui():
    global turn, next_large_grid, won_or_tie, player_won_or_tie

    turn = 0
    next_large_grid = None
    won_or_tie = False
    player_won_or_tie = None
    if turn % 2 == 0:
        player = human1
    else:
        player = human2

    app = ctk.CTk()
    app.title("Ultimate Tic Tac Toe")
    app.minsize(400, 400)
    app.resizable(False, False)
    
    grid_frames = []
    
    # Create player title
    turn_label = ctk.CTkLabel(app, text="Player " + player + "'s turn", font=("Arial", 16))
    turn_label.pack(pady=(20, 0))
    
    def on_button_click(row, col, large_row, large_col):
        global turn, next_large_grid, won_or_tie, player_won_or_tie

        if won_or_tie:
            return

        selected_grid = large_row * 3 + large_col
        selected_small_grid = row * 3 + col

        if next_large_grid is not None and selected_grid != next_large_grid:
            return

        if game_state[selected_grid][selected_small_grid] is not None:
            return

        player = human1 if turn % 2 == 0 else human2
        game_state[selected_grid][selected_small_grid] = player

        small_grid_winner = check_small_grid_win_state(selected_grid)

        if small_grid_winner is not None:
            print(f"Player {small_grid_winner} has won the small grid!")
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
        update_gui()

        if not won_or_tie and turn % 2 != 0:
            # AI player's turn
            iterations = 1000
            player = human2
            grid = next_large_grid
            selected_grid, selected_small_grid = get_ai_move(player, iterations, grid)
            game_state[selected_grid][selected_small_grid] = human2

            small_grid_winner = check_small_grid_win_state(selected_grid)

            if small_grid_winner is not None:
                print(f"Player {small_grid_winner} has won the small grid!")
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
            update_gui()

    # Create a 3x3 grid of small grids
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    for i in range(3):
        main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(i, weight=1)
        for j in range(3):
            outer_frame = ctk.CTkFrame(main_frame)
            outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
            grid_frame = SmallGrid(outer_frame, i, j, on_button_click)
            grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
            grid_frames.append(outer_frame)

    def check_game_over():
        global won_or_tie, player_won_or_tie

        if won_or_tie:
            if player_won_or_tie == "tie":
                show_winner_popup("tie")
            else:
                show_winner_popup(player_won_or_tie)

    def show_winner_popup(winner):
        popup = ctk.CTkToplevel(app)
        popup.title("Game Over")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.transient(app)  # Make the popup window appear on top of the main window
        popup.grab_set()  # Disable interaction with the main window until the popup is closed

        if winner == "tie":
            message = "The game ended in a tie!"
        else:
            message = f"Player {winner} has won the game!"

        label = ctk.CTkLabel(popup, text=message, font=("Arial", 16))
        label.pack(expand=True)

        button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        button.pack(pady=10)
        
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
    
    update_gui()
    
    app.mainloop()



gui()
        
