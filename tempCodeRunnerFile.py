import customtkinter as ctk

# ultimate tic tac toe

# I will use a 2d array for the game logic
# Initialise an empty board
game_state = [[None for i in range(9)] for j in range(9)]
print(game_state)

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

class UltimateTicTacToeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Tic Tac Toe")
        self.geometry("400x400")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.cells = []
        for i in range(9):
            self.frame.grid_rowconfigure(i // 3, weight=1)
            self.frame.grid_columnconfigure(i % 3, weight=1)
            cell_frame = ctk.CTkFrame(self.frame)
            cell_frame.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")
            cell_frame.grid_rowconfigure(0, weight=1)
            cell_frame.grid_columnconfigure(0, weight=1)
            cell = []
            for j in range(9):
                cell_frame.grid_rowconfigure(j // 3, weight=1)
                cell_frame.grid_columnconfigure(j % 3, weight=1)
                button = ctk.CTkButton(cell_frame, text="", font=("Arial", 20), command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=j // 3, column=j % 3, padx=2, pady=2, sticky="nsew")
                cell.append(button)
            self.cells.append(cell)

        self.update_gui()
        if turn % 2 != 0:
            self.ai_move()

    def button_click(self, row, col):
        global turn, next_large_grid
        if turn % 2 == 0:  # Player 1's turn
            if next_large_grid == None or next_large_grid == row:
                selected_grid = row
                selected_small_grid = col
                if game_state[selected_grid][selected_small_grid] == None:
                    game_state[selected_grid][selected_small_grid] = "X"
                    self.update_gui()
                    small_grid_winner = check_small_grid_win_state(selected_grid)
                    if small_grid_winner != None:
                        print(f"Player {small_grid_winner} has won the small grid!")
                        next_large_grid = selected_small_grid
                    else:
                        next_large_grid = selected_small_grid
                    if large_grid_state[next_large_grid] != None:
                        next_large_grid = None
                    player_won_or_tie = check_large_grid_win_state()
                    if player_won_or_tie != None:
                        self.game_over(player_won_or_tie)
                    else:
                        turn += 1
                        self.ai_move()

    def ai_move(self):
        global turn, next_large_grid
        print("AI Player's turn (O)")
        selected_grid, selected_small_grid = get_ai_move("O", 10, next_large_grid)
        game_state[selected_grid][selected_small_grid] = "O"
        self.update_gui()
        small_grid_winner = check_small_grid_win_state(selected_grid)
        if small_grid_winner != None:
            print(f"Player {small_grid_winner} has won the small grid!")
            next_large_grid = selected_small_grid
        else:
            next_large_grid = selected_small_grid
        if large_grid_state[next_large_grid] != None:
            next_large_grid = None
        player_won_or_tie = check_large_grid_win_state()
        if player_won_or_tie != None:
            self.game_over(player_won_or_tie)
        else:
            turn += 1

    def game_over(self, winner):
        if winner == "tie":
            message = "The game ended in a tie!"
        else:
            message = f"Player {winner} has won the game!"
        ctk.CTkMessagebox(self, title="Game Over", message=message)

    def update_gui(self):
        for i in range(9):
            for j in range(9):
                if game_state[i][j] == "X":
                    self.cells[i][j].configure(text="X", text_color="blue")
                elif game_state[i][j] == "O":
                    self.cells[i][j].configure(text="O", text_color="red")
                else:
                    self.cells[i][j].configure(text="")

# game logic

# userinput
won_or_tie = False
player_won_or_tie = None
next_large_grid = None
large_grid_state = [None for i in range(9)]  # None means no one has won
turn = 0

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

if __name__ == "__main__":
    app = UltimateTicTacToeGUI()
    app.mainloop()