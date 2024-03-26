from customtkinter import *
from tkinter import messagebox


class TicTacToeButton(CTkButton):
    def __init__(self, master, on_click): # constructor
        super().__init__(master, text="", width=50, height=50, corner_radius=1) # super constructor for CTkButton
        self.configure(command=on_click)

    def mark(self, text, color): # method for coloring and marking the button and being written on
        self.configure(text=text, fg_color=color, text_color="#FFFFFF")


class TicTacToeGrid(CTkFrame): 
    def __init__(self, master, large_row, large_col, on_button_click): # main window constructor
        super().__init__(master)
        self.buttons = [] # list of all buttons available
        self.on_button_click = on_button_click # assigning local variable to field for button click method
        self.large_row = large_row # large row is the total number of rows in the Large tictactoe board (3)
        self.large_col = large_col # large row is the total number of cols in the Large tictactoe board (3)

        for r in range(3):
            self.grid_rowconfigure(r, weight=1) # customtkinter method to assigning a slot to put the button in, weight is the size of the gap
            self.grid_columnconfigure(r, weight=1)

            for c in range(3):
                button = TicTacToeButton(self, lambda b=r, a=c: self.on_button_click(b, a, self.large_row, self.large_col)) 
                button.grid(row=r, column=c, sticky="nsew")
                self.buttons.append(button)

    def check_win(self):
        grid = [button.cget("text") for button in self.buttons]
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

    def mark_win(self, winner):
        fg = "blue" if winner == 'X' else "red"
        for i, button in enumerate(self.buttons):
            if i == 4:
                button.mark(winner, fg)
            else:
                button.mark("", fg)


class LargeGrid(CTkFrame):
    def __init__(self, master, on_button_click):
        super().__init__(master, fg_color="transparent")
        self.grid_frames = []
        self.wins = [[0, 0, 0], 
                     [0, 0, 0], 
                     [0, 0, 0]]

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

            for j in range(3):
                outer_frame = CTkFrame(self)
                outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

                grid_frame = TicTacToeGrid(outer_frame, i, j, on_button_click)
                grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
                self.grid_frames.append(outer_frame)

    def check_win(self):
        for i in range(3):
            if self.wins[i][0] == self.wins[i][1] == self.wins[i][2] != 0:
                return self.wins[i][0]
            if self.wins[0][i] == self.wins[1][i] == self.wins[2][i] != 0:
                return self.wins[0][i]
        if self.wins[0][0] == self.wins[1][1] == self.wins[2][2] != 0:
            return self.wins[0][0]
        if self.wins[0][2] == self.wins[1][1] == self.wins[2][0] != 0:
            return self.wins[0][2]
        return None

    def update_outline(self, next_row, next_col):
        for i in range(9):
            row, col = i // 3, i % 3
            if next_row is None or next_col is None:
                if self.wins[row][col] == 0:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    self.grid_frames[i].configure(fg_color="transparent")
            elif self.wins[next_row][next_col] != 0:
                if self.wins[row][col] == 0:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    self.grid_frames[i].configure(fg_color="transparent")
            else:
                if row == next_row and col == next_col:
                    self.grid_frames[i].configure(fg_color="yellow")
                else:
                    self.grid_frames[i].configure(fg_color="transparent")


class GameManager:
    def __init__(self):
        self.turn = 0
        self.nextLargeGridRow = None
        self.nextLargeGridColumn = None

    def check_button_used(self, button, large_row, large_col, large_grid):
        if button.cget("text") != "":
            return False

        if large_grid.wins[large_row][large_col] != 0:
            return False

        return True

    def check_button_large_grid(self, large_row, large_col, large_grid):
        if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
            return True

        if large_grid.wins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
            return large_grid.wins[large_row][large_col] == 0

        return large_row == self.nextLargeGridRow and large_col == self.nextLargeGridColumn

    def change_button_text(self, button):
        if self.turn % 2 == 0:
            button.mark("X", "#4B7BE5")
        else:
            button.mark("O", "#F08080")

    def check_small_grid_win(self, large_row, large_col, large_grid):
        grid_frame = large_grid.grid_frames[large_row * 3 + large_col].winfo_children()[0]
        winner = grid_frame.check_win()

        if winner:
            grid_frame.mark_win(winner)
            large_grid.wins[large_row][large_col] = winner

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"Player {winner} wins!")

    def update_turn_label(self, label):
        if self.turn % 2 == 0:
            label.configure(text="Player X's turn")
        else:
            label.configure(text="Player O's turn")

    def on_button_click(self, small_row, small_col, large_row, large_col, button, large_grid, turn_label):
        if not self.check_button_used(button, large_row, large_col, large_grid) or not self.check_button_large_grid(large_row, large_col, large_grid):
            return

        self.change_button_text(button)
        self.turn += 1

        self.nextLargeGridRow = small_row
        self.nextLargeGridColumn = small_col

        self.check_small_grid_win(large_row, large_col, large_grid)
        winner = large_grid.check_win()
        if winner:
            self.show_winner(winner)
            return

        large_grid.update_outline(self.nextLargeGridRow, self.nextLargeGridColumn)
        self.update_turn_label(turn_label)


class UltimateTicTacToe(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Tic Tac Toe")
        self.minsize(400, 400)
        self.resizable(False, False)

        self.game_manager = GameManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.turn_label = CTkLabel(self, text="Player X's turn", font=("Arial", 16))
        self.turn_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.large_grid = LargeGrid(self, self.on_button_click)
        self.large_grid.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.large_grid.update_outline(None, None)

    def on_button_click(self, small_row, small_col, large_row, large_col):
        button = self.large_grid.grid_frames[large_row * 3 + large_col].winfo_children()[0].buttons[small_row * 3 + small_col]
        self.game_manager.on_button_click(small_row, small_col, large_row, large_col, button, self.large_grid, self.turn_label)


if __name__ == "__main__":
    set_appearance_mode("dark")
    app = UltimateTicTacToe()
    app.mainloop()