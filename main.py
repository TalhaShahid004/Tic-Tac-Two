from customtkinter import *
from tkinter import messagebox


class UltimateTicTacToe(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Tic Tac Toe")
        self.minsize(400, 400)
        self.resizable(False, False)  # Make the window non-resizable

        self.turn = 0
        self.buttons = []  # Store button instances

        self.largeGridWins = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]  # Store the wins of the large grid
        
        self.large_grid_frames = []  # Store the frames of the large grid

        # Store the next large grid row and column based on the current turn
        self.nextLargeGridRow = None
        self.nextLargeGridColumn = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Create a label to display the current turn
        self.turn_label = CTkLabel(self, text="Player X's turn", font=("Arial", 16))
        self.turn_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        # loop through the large 3x3 grid rows
        for i in range(3):
            self.main_frame.grid_rowconfigure(i, weight=1)
            self.main_frame.grid_columnconfigure(i, weight=1)

            # loop through the large 3x3 grid columns
            for j in range(3):
                outer_frame = CTkFrame(self.main_frame)
                outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

                grid_frame = CTkFrame(outer_frame)
                grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
                self.large_grid_frames.append(outer_frame)  # Store the outer frame in the list

                # loop through the small 3x3 grid rows
                for r in range(3):
                    grid_frame.grid_rowconfigure(r, weight=1)
                    grid_frame.grid_columnconfigure(r, weight=1)

                    # loop through the small 3x3 grid columns
                    for c in range(3):
                        button = CTkButton(grid_frame, text="", width=50, height=50, corner_radius=1)
                        button.grid(row=r, column=c, sticky="nsew")
                        self.buttons.append((button, r, c, i, j))  # store buttons in array

        # add function to all buttons
        for button, small_row, small_col, large_row, large_col in self.buttons:
            button.configure(
                command=lambda b=button, sr=small_row, sc=small_col, lr=large_row, lc=large_col: self.button_clicked(b,
                                                                                                                     sr,
                                                                                                                     sc,
                                                                                                                     lr,
                                                                                                                     lc))

        self.update_large_grid_outline()  # Set the initial outline

    # Update the turn label text
    def update_turn_label(self):
        if self.turn % 2 == 0:
            self.turn_label.configure(text="Player X's turn")
        else:
            self.turn_label.configure(text="Player O's turn")

    # master function to handle button click
    def button_clicked(self, button, small_row, small_col, large_row, large_col):
        # check if the button has already been set and if the move is valid
        if not self.check_button_used(button, large_row, large_col) or not self.check_button_large_grid(large_row,
                                                                                                        large_col):
            return

        self.change_button_text(button)
        self.turn += 1

        self.nextLargeGridRow = small_row
        self.nextLargeGridColumn = small_col

        self.check_small_grid_win(large_row, large_col)
        self.check_large_grid_win()

        self.update_large_grid_outline()  # Update the outline of available large grids
        self.update_turn_label()  # Update the turn label
    # used for player ticker (X or O)
    def change_button_text(self, button):
        if self.turn % 2 == 0:
            button.configure(text="X", fg_color = "blue")
        else:
            button.configure(text="O", fg_color = "red")

    # check if the button is already used
    def check_button_used(self, button, large_row, large_col):
        # Check if the button is already set
        if button.cget("text") != "":
            return False

        # Check if the small grid is already won
        if self.largeGridWins[large_row][large_col] != 0:
            return False

        return True

    # check if the move is valid based on the next large grid coordinates
    def check_button_large_grid(self, large_row, large_col):
        if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
            return True

        # Check if the next large grid is already won
        if self.largeGridWins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
            # If the next large grid is won, allow the player to place their piece in any non-won grid
            return self.largeGridWins[large_row][large_col] == 0

        return large_row == self.nextLargeGridRow and large_col == self.nextLargeGridColumn

    # check if a small grid is won
    def check_small_grid_win(self, large_row, large_col):
        small_grid = [button.cget("text") for button, _, _, lr, lc in self.buttons if
                      lr == large_row and lc == large_col]
        winner = self.check_win(small_grid)
        
        if winner == 'X': #will be used later
            fg = "blue"
        else:
            fg = "red"
            
        if winner:
            self.largeGridWins[large_row][large_col] = winner

    # check if the large grid is won
    def check_large_grid_win(self):
        winner = self.check_win(self.largeGridWins)
        if winner:
            self.show_winner(winner)

    # check for a win in a grid
    def check_win(self, grid):
        if isinstance(grid[0], list):
            # grid is a 2D list (large grid)
            for i in range(3):
                if grid[i][0] == grid[i][1] == grid[i][2] != 0:
                    return grid[i][0]
                if grid[0][i] == grid[1][i] == grid[2][i] != 0:
                    return grid[0][i]
            if grid[0][0] == grid[1][1] == grid[2][2] != 0:
                return grid[0][0]
            if grid[0][2] == grid[1][1] == grid[2][0] != 0:
                return grid[0][2]
        else:
            # grid is a 1D list (small grid)
            for i in range(0, 9, 3):
                if grid[i] == grid[i + 1] == grid[i + 2] != "":
                    return grid[i]
            for i in range(3):
                if grid[i] == grid[i + 3] == grid[i + 6] != "":
                    return grid[i]
            if grid[0] == grid[4] == grid[8] != "":
                return grid[0]
            if grid[2] == grid[4] == grid[6] != "":
                return grid[2]
        return None

    # show the winner
    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        self.quit()

    def update_large_grid_outline(self):
        for i in range(9):
            row, col = i // 3, i % 3
            if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
                if self.largeGridWins[row][col] == 0:
                    self.large_grid_frames[i].configure(fg_color="yellow")
                else:
                    self.large_grid_frames[i].configure(fg_color="transparent")
            elif self.largeGridWins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
                if self.largeGridWins[row][col] == 0:
                    self.large_grid_frames[i].configure(fg_color="yellow")
                else:
                    self.large_grid_frames[i].configure(fg_color="transparent")
            else:
                if row == self.nextLargeGridRow and col == self.nextLargeGridColumn:
                    self.large_grid_frames[i].configure(fg_color="yellow")
                else:
                    self.large_grid_frames[i].configure(fg_color="transparent")



if __name__ == "__main__":
    set_appearance_mode("dark")
    app = UltimateTicTacToe()
    app.mainloop()
