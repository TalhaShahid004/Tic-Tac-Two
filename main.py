from customtkinter import *
from tkinter import messagebox


class TicTacToeGrid(CTkFrame):
    def __init__(self, master, large_row, large_col, on_button_click):
        super().__init__(master)
        self.buttons = []
        self.on_button_click = on_button_click
        self.large_row = large_row
        self.large_col = large_col

        for r in range(3):
            self.grid_rowconfigure(r, weight=1)
            self.grid_columnconfigure(r, weight=1)

            for c in range(3):
                button = CTkButton(self, text="", width=50, height=50, corner_radius=1)
                button.grid(row=r, column=c, sticky="nsew")
                button.configure(command=lambda b=button, sr=r, sc=c: self.on_button_click(b, sr, sc, self.large_row, self.large_col))
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
                button.configure(text=winner, fg_color=fg)
            else:
                button.configure(text="", fg_color=fg)


class UltimateTicTacToe(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Tic Tac Toe")
        self.minsize(400, 400)
        self.resizable(False, False)

        self.turn = 0
        self.large_grid_wins = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.large_grid_frames = []
        self.nextLargeGridRow = None
        self.nextLargeGridColumn = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.turn_label = CTkLabel(self, text="Player X's turn", font=("Arial", 16))
        self.turn_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        for i in range(3):
            self.main_frame.grid_rowconfigure(i, weight=1)
            self.main_frame.grid_columnconfigure(i, weight=1)

            for j in range(3):
                outer_frame = CTkFrame(self.main_frame)
                outer_frame.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

                grid_frame = TicTacToeGrid(outer_frame, i, j, self.on_button_click)
                grid_frame.pack(expand=True, fill="both", padx=3, pady=3)
                self.large_grid_frames.append(outer_frame)

        self.update_large_grid_outline()

    def on_button_click(self, button, small_row, small_col, large_row, large_col):
        if not self.check_button_used(button, large_row, large_col) or not self.check_button_large_grid(large_row, large_col):
            return

        self.change_button_text(button)
        self.turn += 1

        self.nextLargeGridRow = small_row
        self.nextLargeGridColumn = small_col

        self.check_small_grid_win(large_row, large_col)
        self.check_large_grid_win()

        self.update_large_grid_outline()
        self.update_turn_label()

    def check_button_used(self, button, large_row, large_col):
        if button.cget("text") != "":
            return False

        if self.large_grid_wins[large_row][large_col] != 0:
            return False

        return True

    def change_button_text(self, button):
        if self.turn % 2 == 0:
            button.configure(text="X", fg_color="#4B7BE5", text_color="#FFFFFF")
        else:
            button.configure(text="O", fg_color="#F08080", text_color="#FFFFFF")

    def check_button_large_grid(self, large_row, large_col):
        if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
            return True

        if self.large_grid_wins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
            return self.large_grid_wins[large_row][large_col] == 0

        return large_row == self.nextLargeGridRow and large_col == self.nextLargeGridColumn

    def check_small_grid_win(self, large_row, large_col):
        grid_frame = self.main_frame.grid_slaves(row=large_row, column=large_col)[0].winfo_children()[0]
        winner = grid_frame.check_win()

        if winner:
            grid_frame.mark_win(winner)
            self.large_grid_wins[large_row][large_col] = winner

    def check_large_grid_win(self):
        winner = self.check_win(self.large_grid_wins)
        if winner:
            self.show_winner(winner)

    def check_win(self, grid):
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != 0:
                return grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] != 0:
                return grid[0][i]
        if grid[0][0] == grid[1][1] == grid[2][2] != 0:
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != 0:
            return grid[0][2]
        return None

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        self.quit()

    def update_turn_label(self):
        if self.turn % 2 == 0:
            self.turn_label.configure(text="Player X's turn")
        else:
            self.turn_label.configure(text="Player O's turn")

    def update_large_grid_outline(self):
        for i in range(9):
            row, col = i // 3, i % 3
            if self.nextLargeGridRow is None or self.nextLargeGridColumn is None:
                if self.large_grid_wins[row][col] == 0:
                    self.large_grid_frames[i].configure(fg_color="yellow")
                else:
                    self.large_grid_frames[i].configure(fg_color="transparent")
            elif self.large_grid_wins[self.nextLargeGridRow][self.nextLargeGridColumn] != 0:
                if self.large_grid_wins[row][col] == 0:
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