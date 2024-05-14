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



class Node:
    """
    Represents a node in the Monte Carlo Tree Search (MCTS) algorithm.

    Attributes:
        board (list): The game board representing the state of the game at this node.
        parent (Node): The parent node of this node. None if it's the root node.
        children (dict): Dictionary containing child nodes as values and their corresponding moves as keys.
        next_small_grid (tuple): The coordinates of the small grid where the next move can be played legally.
        move (tuple): The coordinates of the move that led to this node.
        player (str): The player whose the one supposed to be winning, MCTS with 'O' would only have nodes with player as 'O'.
        wins (int): The number of simulated games won from this node.
        visits (int): The number of times this node has been visited during simulations.
    """
    def __init__(self, board, player, parent=None, next_small_grid=None, move=None):
        """
        Initialize a node with the given game board, player, parent node, and next small grid.

        Args:
            board (list): The game board representing the state of the game.
            player (str): The player who is supposed to be winning.
            parent (Node, optional): The parent node of this node. Defaults to None.
            next_small_grid (tuple, optional): The coordinates of the small grid where the next move can be played legally. Defaults to None.
            move (tuple, optional): The coordinates of the move that led to this node. Defaults to None.
        """
        self.board = board
        self.parent = parent
        self.children = {}
        self.next_small_grid = next_small_grid
        self.move = move
        self.player = player
        self.wins = 0
        self.visits = 0


def mcts(player, gameState, iterations, next_small_grid):
    """
        Performs Monte Carlo Tree Search (MCTS) to find the best move for the given player.

        Args:
            player (str): The player ('X' or 'O') for whom the move is being determined.
            gameState (list): The current state of the game represented as a 9x9 grid.
            iterations (int): The number of iterations to run MCTS.
            next_small_grid (tuple): The coordinates of the small grid where the next move can be played legally.

        Returns:
            tuple: The coordinates of the best move determined by MCTS.
        """
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
        player = "O" if player == "X" else "X"
        # Simulation and backprop
        simulate_random_playout(node, current_state, player)
    # Select the best move based on the most visited child, can also change this to wins/visits ratio
    best_child = max(root.children.values(), key=lambda child: child.visits)
    return best_child.move

def make_children(player, node):
    """
        Expands the children of the given node based on the legal moves available in the game state.

        Args:
            player (str): The player ('X' or 'O') making the move.
            node (Node): The node for which children are to be created.
    """
    if node.next_small_grid is None:
        # If the next grid wasn't playable, find the first available small grid
        for i in range(9):
            if check_small_grid_win(node.board[i]) is None:
                node.next_small_grid = i
                break

    if node.next_small_grid is not None:
        # If there's a next small grid available
        for i in range(9):
            if node.board[node.next_small_grid][i] is None:
                # If the position is available in the next small grid, create a child node
                board_copy = [row[:] for row in node.board]
                board_copy[node.next_small_grid][i] = player
                # Determine the next small grid for the child node
                next_small = i if check_small_grid_win(board_copy[i]) is None else None
                move = (node.next_small_grid, i)
                child = Node(board_copy, player, node, next_small, move)
                node.children[(node.next_small_grid, i)] = child
    else:
        # If all small grids are won, allow moves in any available position
        for i in range(9):
            for j in range(9):
                # If the position is available, create a child node
                if node.board[i][j] is None:
                    board_copy = [row[:] for row in node.board]
                    board_copy[i][j] = player
                    move = [i, j]
                    child = Node(board_copy, node.player, node, None, move)
                    node.children[i,j]=child


def backpropagate(node, winner):
    """
        Backpropagates the result of a playout from the given node.

        Args:
            node (Node): The node from which to start backpropagation.
            winner (str): The winner of the simulated game ('X', 'O', or 'tie').
    """
    # Start from the given node and propagate the result upwards
    while node is not None:
        # Increment the number of visits to the node
        node.visits += 1
        # Increment the number of wins if the winner matches the node's player
        if winner == node.player:
            node.wins += 1
        # Move to the parent node for further backpropagation
        node = node.parent


def simulate_random_playout(node, gameState, player):
    """
        Simulates a random playout from the given node with both players making random moves.

        Args:
            node (Node): The node from which to start the random playout.
            gameState (list): The current state of the game.
            player (str): The player whose turn it is to make a move.

        Returns:
            str: The winner of the simulated game ('X', 'O', or 'tie').
    """
    #print("Simulation started")
    current_state = deepcopy(gameState) # Create a deep copy of the game state
    child = node # Start the playout from the given node
    make_children(player, child) # Generate children for the starting node
    # Continue the playout until a player wins or the game ends in a tie
    while game_won(current_state) is None:
        """ This part of code doesnt pick on random but on which child node has the greatest weight on its move
        maxmove = -2
        move = None
        # Choosing best child
        for moves in child.children.keys():
            if LargeGridweights[moves[0]] + SmallGridWeights[moves[1]] > maxmove:
                move = moves
                maxmove = LargeGridweights[moves[0]] + SmallGridWeights[moves[1]]
        child = child.children.get(move)"""
        # Choose a random move from the available child nodes
        move, child = random.choice(list(child.children.items()))

        # Update the game state with the selected move
        current_state[move[0]][move[1]] = player

        # Alternate players for the next move
        player = "O" if player == "X" else "X"

        # Generate children for the next player's turn
        make_children(player, child)
        #printGameState(current_state)
        if game_won(current_state) is not None:
            break
        make_children(player, child)
    winner = game_won(current_state)
    #print(f"Winner: {winner}")
    backpropagate(child, winner)
    #Sprint("game finished")
    return winner


def select_best_child(node):
    """
        Selects the best child node using the Upper Confidence Bound (UCB1) formula.

        Args:
            node (Node): The parent node from which to select the best child.

        Returns:
            Node: The best child node according to the UCB1 formula.
    """
    best_child = None
    best_score = -float('inf')
    for child in node.children.values():
        # If a child node has not been visited, return it immediately
        if child.visits == 0:
            return child

        # Calculate the UCB1 score for the child node
        score = child.wins / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits)

        # Update the best child and best score if the current child has a higher score
        if score > best_score:
            best_child = child
            best_score = score
    return best_child

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
        
