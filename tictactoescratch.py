
from tkinter import messagebox
from customtkinter import *

# Button class

class Button(CTkButton):
    #default constructor
    def __init__(self, master, on_click):
        super().__init__(master, text="", width=50, height=50, corner_radius=1)  # dimensions
        # adds the on_click method to the button
        self.configure(command=on_click)

    def mark(self, text, color):  # method for coloring and marking the button and being written on
        self.configure(text=text, fg_color=color, text_color="#FFFFFF")


# Small 3x3 Grid class
class smallGrid(CTkFrame):
    # default constructor
    def __init__(self, master, large_row, large_col, on_button_click):
        # calls the constructor of the parent class
        super().__init__(master)

        # create a variable that shows if the small grid is won or not
        self.won = False
        self.buttons = []
        self.on_button_click = on_button_click
        self.large_row = large_row
        self.large_col = large_col

        for r in range(3):
            self.grid_rowconfigure(r, weight=1) # customtkinter method to assigning a slot to put the button in, weight is the size of the gap
            self.grid_columnconfigure(r, weight=1)

            for c in range(3):
                # create a button with lambda function to pass the row and column of the button
                button = Button(self, lambda b=r, a=c: self.on_button_click(b, a, self.large_row, self.large_col))
                button.grid(row=r, column=c, sticky="nsew")
                self.buttons.append(button)

    def check_small_grid_win(self):
        # set grid as a list of the text of the buttons
        grid = [button.cget("text") for button in self.buttons]
        # Check if there is a win condition

        for i in range(0, 9, 3):
            # Check rows
            # If the elements at indices i, i+1, and i+2 are the same (excluding empty cells),
            # there is a win condition in that row
            if grid[i] == grid[i + 1] == grid[i + 2] != "":
                self.won = True
                return grid[i]

        for i in range(3):
            # Check columns
            # If the elements at indices i, i+3, and i+6 are the same (excluding empty cells),
            # there is a win condition in that column
            if grid[i] == grid[i + 3] == grid[i + 6] != "":
                self.won = True
                return grid[i]

        # Check diagonal from top-left to bottom-right
        # If the elements at indices 0, 4, and 8 are the same (excluding empty cells),
        # there is a win condition in that diagonal
        if grid[0] == grid[4] == grid[8] != "":
            self.won = True
            return grid[0]

        # Check diagonal from top-right to bottom-left
        # If the elements at indices 2, 4, and 6 are the same (excluding empty cells),
        # there is a win condition in that diagonal
        if grid[2] == grid[4] == grid[6] != "":
            self.won = True
            return grid[2]

        # If no win condition is found, return None
        return None

    # Method to mark the small grid as won
    def mark_small_grid_win(self, winner):
        fg = "blue" if winner == 'X' else "red"
        for i, button in enumerate(self.buttons):
            if i == 4:
                button.mark(winner, fg)
            else:
                button.mark("", fg)

    def get_small_grid_won(self):
        return self.won


# Large 3x3 Grid class
class LargeGrid(CTkFrame):
    def __init__(self,master, on_button_click):
        super().__init__(master, fg_color="transparent")
        self.grid_frames = []
        # create a variable that shows if the large grid is won or not
        self.wins = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]

        # create a 3x3 grid of small grids
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

            for j in range(3):
                outer_frame = CTkFrame(self)
                outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

                grid_frame = smallGrid(outer_frame, i, j, on_button_click)
                grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
                self.grid_frames.append(outer_frame)

    def check_large_grid_win(self):
        for i in range(3):
            # Check rows
            # If the elements in the i-th row (self.wins[i][0], self.wins[i][1], self.wins[i][2])
            # are the same and not equal to 0, there is a win condition in that row
            if self.wins[i][0] == self.wins[i][1] == self.wins[i][2] != 0:
                return self.wins[i][0]

            # Check columns
            # If the elements in the i-th column (self.wins[0][i], self.wins[1][i], self.wins[2][i])
            # are the same and not equal to 0, there is a win condition in that column
            if self.wins[0][i] == self.wins[1][i] == self.wins[2][i] != 0:
                return self.wins[0][i]

        # Check diagonal from top-left to bottom-right
        # If the elements in the diagonal (self.wins[0][0], self.wins[1][1], self.wins[2][2])
        # are the same and not equal to 0, there is a win condition in that diagonal
        if self.wins[0][0] == self.wins[1][1] == self.wins[2][2] != 0:
            return self.wins[0][0]

        # Check diagonal from top-right to bottom-left
        # If the elements in the diagonal (self.wins[0][2], self.wins[1][1], self.wins[2][0])
        # are the same and not equal to 0, there is a win condition in that diagonal
        if self.wins[0][2] == self.wins[1][1] == self.wins[2][0] != 0:
            return self.wins[0][2]

        # If no win condition is found, return None
        return None

    # marks open cells and yellow
    def update_outline(self, next_row, next_col):
        # Iterate over each small grid in the large grid
        for i in range(9):
            # Calculate the row and column of the current small grid
            row, col = i // 3, i % 3

            # Check if the next move is not specified (i.e., next_row and next_col are None)
            if next_row is None or next_col is None:
                # If the current small grid is not won, highlight it in yellow
                if self.wins[row][col] == 0:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    # If the current small grid is already won, make it transparent
                    self.grid_frames[i].configure(fg_color="transparent")

            # Check if the next move is in a small grid that is already won
            elif self.wins[next_row][next_col] != 0:
                # If the current small grid is not won, highlight it in yellow
                if self.wins[row][col] == 0:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    # If the current small grid is already won, make it transparent
                    self.grid_frames[i].configure(fg_color="transparent")

            # If the next move is in a valid small grid
            else:
                # If the current small grid matches the next move's row and column, highlight it in yellow
                if row == next_row and col == next_col:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    # If the current small grid does not match the next move, make it transparent
                    self.grid_frames[i].configure(fg_color="transparent")





# Game logic class
class GameManager:
    def __init__(self):
        self.turn = 0
        self.nextLargeGridRow = None
        self.nextLargeGridCol = None

    # check if the button is already used
    def check_button_used(self, button, large_row, large_col, large_grid):
        if button.cget("text") != "":
            return False

        if large_grid.wins[large_row][large_col] != 0:
            return False

        return True

    # check if the button is in the correct grid
    def check_button_large_grid(self, large_row, large_col, large_grid):
        if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
            return True

        if large_grid.wins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
            return large_grid.wins[large_row][large_col] == 0

        return large_row == self.nextLargeGridRow and large_col == self.nextLargeGridColumn

    # method to change the button text
    def change_button_text(self, button):
        if self.turn % 2 == 0:
            button.mark("X", "#4B7BE5")
        else:
            button.mark("O", "#F08080")

    # method to check if there is a win on the small grid
    def check_small_grid_win(self, large_row, large_col, large_grid):
        # Get the small grid that the button belongs to
        grid_frame = large_grid.grid_frames[large_row * 3 + large_col].winfo_children()[0]

        # Check if there is a win condition in the small grid
        winner = grid_frame.check_small_grid_win()

        # If there is a win condition, mark the small grid as won
        if winner:
            grid_frame.mark_small_grid_win(winner)
            large_grid.wins[large_row][large_col] = winner

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"Player {winner} wins!")

    def update_turn_label(self, label):
        if self.turn % 2 == 0:
            label.configure(text="Player X's turn")
        else:
            label.configure(text="Player O's turn")


    def on_button_click(self, small_row, small_col, large_row, large_col, button, large_grid, turn_label):
        if not self.check_button_used(button, large_row, large_col, large_grid) or not self.check_button_large_grid(
                large_row, large_col, large_grid):
            return

        self.change_button_text(button)
        self.turn += 1

        self.nextLargeGridRow = small_row
        self.nextLargeGridColumn = small_col

        self.check_small_grid_win(large_row, large_col, large_grid)
        winner = large_grid.check_large_grid_win()
        if winner:
            self.show_winner(winner)
            return

        large_grid.update_outline(self.nextLargeGridRow, self.nextLargeGridColumn)
        self.update_turn_label(turn_label)

    # method to get the state space of the game
    def get_state_space(self, large_grid):
        state_space = {
            'turn': 'X' if self.turn % 2 == 0 else 'O',
            'next_large_grid': (self.nextLargeGridRow, self.nextLargeGridColumn),  
            'small_grids': [],
            'large_grid': large_grid.wins
        }

        for i in range(9):
            small_grid = large_grid.grid_frames[i].winfo_children()[0]
            buttons_state = [button.cget("text") for button in small_grid.buttons]
            state_space['small_grids'].append(buttons_state)

        return state_space
    
class AIAgent:
    def __init__(self, player):
        self.max_depth = 1  # can be changed
        self.player = player

    # this is the function that will actually be called
    def get_next_move(self, state_space):
        # call minimax function
        _, move = self.minimax(state_space, self.max_depth, float('-inf'), float('inf'), self.player)
        return move

    def minimax(self, state_space, depth, alpha, beta, player):
        # terminal conditions
        # if the game is over, ie x or o wins or tie, return the score
        if self.is_game_over(state_space):
            return self.evaluate_state_space(state_space, player), None
        # if the depth is 0, return the score
        if depth == 0:
            return self.evaluate_state_space(state_space, player), None

        # if the current player is maximizing
        # ai player logic
        if player == self.player:
            best_score = float('-inf')
            best_move = None
            for move in self.generate_possible_moves(state_space, player):
                new_state_space = self.make_move(state_space, move, player)
                score, _ = self.minimax(new_state_space, depth - 1, alpha, beta, 'O' if player == 'X' else 'X')
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            # if the current player is minimizing
            # human player logic
            best_score = float('inf')
            best_move = None
            for move in self.generate_possible_moves(state_space, player):
                new_state_space = self.make_move(state_space, move, player)
                score, _ = self.minimax(new_state_space, depth - 1, alpha, beta, 'X' if player == 'O' else 'O')
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

        


        
    def generate_possible_moves(self, state_space, player):
        possible_moves = []

        next_large_grid_row, next_large_grid_col = state_space['next_large_grid']
        if next_large_grid_row is None or next_large_grid_col is None:
            # whole large grid is open for playing
            for large_row in range(3):
                for large_col in range(3):
                    # make sure the large grid isnt won
                    if state_space['large_grid'][large_row][large_col] == 0:
                        for small_row in range(3):
                            for small_col in range(3):
                                if state_space['small_grids'][large_row * 3 + large_col][small_row * 3 + small_col] == '':
                                    possible_moves.append((large_row, large_col, small_row, small_col))
        else:
            # if the next large grid is specified, only that one can be played
            for small_row in range(3):
                for small_col in range(3):
                    if state_space['small_grids'][next_large_grid_row * 3 + next_large_grid_col][small_row * 3 + small_col] == '':
                        possible_moves.append((next_large_grid_row, next_large_grid_col, small_row, small_col))

        return possible_moves

    # method to actually make the move
    def make_move(self, state_space, move, player):
        new_state_space = state_space.copy()
        # get the moves details
        large_row, large_col, small_row, small_col = move

        # update the state space
        new_state_space['small_grids'][large_row * 3 + large_col][small_row * 3 + small_col] = player

        # update the next large grid
        new_state_space['next_large_grid'] = (small_row, small_col)

        # update the turn
        new_state_space['turn'] = 'O' if player == 'X' else 'X'

        return new_state_space
    
    def is_game_over(self, state_space):
        # Check if the game is over based on the current state space
        # Return True if the game is over, False otherwise

        # Check if the large grid is won as a tic tac toe board
        for i in range(3):
            # Check rows
            if state_space['large_grid'][i][0] == state_space['large_grid'][i][1] == state_space['large_grid'][i][2] != 0:
                return True

            # Check columns
            if state_space['large_grid'][0][i] == state_space['large_grid'][1][i] == state_space['large_grid'][2][i] != 0:
                return True
        
        # Check diagonal from top-left to bottom-right
        if state_space['large_grid'][0][0] == state_space['large_grid'][1][1] == state_space['large_grid'][2][2] != 0:
            return True
        
        # Check diagonal from top-right to bottom-left
        if state_space['large_grid'][0][2] == state_space['large_grid'][1][1] == state_space['large_grid'][2][0] != 0:
            return True
        
            


        return False

    def evaluate_state_space(self, state_space, player):
        score = 0

        # Evaluate the small grids
        for large_row in range(3):
            for large_col in range(3):
                small_grid = state_space['small_grids'][large_row * 3 + large_col]

                # Check for winning conditions in the small grid
                for i in range(3):
                    # Check rows
                    if small_grid[i * 3] == small_grid[i * 3 + 1] == small_grid[i * 3 + 2]:
                        if small_grid[i * 3] == player:
                            score += 10
                        elif small_grid[i * 3] != '':
                            score -= 10

                    # Check columns
                    if small_grid[i] == small_grid[i + 3] == small_grid[i + 6]:
                        if small_grid[i] == player:
                            score += 10
                        elif small_grid[i] != '':
                            score -= 10

                # Check diagonal from top-left to bottom-right
                if small_grid[0] == small_grid[4] == small_grid[8]:
                    if small_grid[0] == player:
                        score += 10
                    elif small_grid[0] != '':
                        score -= 10

                # Check diagonal from top-right to bottom-left
                if small_grid[2] == small_grid[4] == small_grid[6]:
                    if small_grid[2] == player:
                        score += 10
                    elif small_grid[2] != '':
                        score -= 10

        # Evaluate the large grid
        for i in range(3):
            # Check rows
            if state_space['large_grid'][i][0] == state_space['large_grid'][i][1] == state_space['large_grid'][i][2]:
                if state_space['large_grid'][i][0] == player:
                    score += 100
                elif state_space['large_grid'][i][0] != 0:
                    score -= 100

            # Check columns
            if state_space['large_grid'][0][i] == state_space['large_grid'][1][i] == state_space['large_grid'][2][i]:
                if state_space['large_grid'][0][i] == player:
                    score += 100
                elif state_space['large_grid'][0][i] != 0:
                    score -= 100

        # Check diagonal from top-left to bottom-right
        if state_space['large_grid'][0][0] == state_space['large_grid'][1][1] == state_space['large_grid'][2][2]:
            if state_space['large_grid'][0][0] == player:
                score += 100
            elif state_space['large_grid'][0][0] != 0:
                score -= 100

        # Check diagonal from top-right to bottom-left
        if state_space['large_grid'][0][2] == state_space['large_grid'][1][1] == state_space['large_grid'][2][0]:
            if state_space['large_grid'][0][2] == player:
                score += 100
            elif state_space['large_grid'][0][2] != 0:
                score -= 100

        return score

# UI and Game class
class UltimateTicTacToe(CTk):
    def __init__(self, ai_player=None):
        super().__init__()
        self.title("Ultimate Tic Tac Toe")
        self.minsize(400, 400)
        self.resizable(False, False)

        self.game_manager = GameManager()
        self.ai_player = ai_player

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.turn_label = CTkLabel(self, text="Player X's turn", font=("Arial", 16))
        self.turn_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.large_grid = LargeGrid(self, self.on_button_click)
        self.large_grid.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.large_grid.update_outline(None, None)

    def on_button_click(self, small_row, small_col, large_row, large_col):
        button = self.large_grid.grid_frames[large_row * 3 + large_col].winfo_children()[0].buttons[
            small_row * 3 + small_col]
        self.game_manager.on_button_click(small_row, small_col, large_row, large_col, button, self.large_grid,
                                          self.turn_label)

        # Access the state space after each button click
        state_space = self.game_manager.get_state_space(self.large_grid)
        print("Current State Space:")
        print(state_space)

        # Check if it's the AI player's turn
        if self.ai_player is not None and self.game_manager.turn % 2 == (1 if self.ai_player.player == 'O' else 0):
            # Get the AI agent's move
            ai_move = self.ai_player.get_next_move(state_space)

            # Perform the AI agent's move
            if ai_move is not None:
                large_row, large_col, small_row, small_col = ai_move
                button = self.large_grid.grid_frames[large_row * 3 + large_col].winfo_children()[0].buttons[
                    small_row * 3 + small_col]
                self.game_manager.on_button_click(small_row, small_col, large_row, large_col, button, self.large_grid,
                                                  self.turn_label)

if __name__ == "__main__":
    set_appearance_mode("dark")
    ai_player = AIAgent('O')  # Create an instance of the AIAgent, specifying the player ('X' or 'O')
    app = UltimateTicTacToe(ai_player=ai_player)
    app.mainloop()
