# Ultimate Tic Tac Toe

Ultimate Tic Tac Toe is an advanced variation of the classic Tic Tac Toe game. It introduces a new level of strategy and complexity by incorporating a nested grid structure. The game is played on a 3x3 grid of 3x3 grids, resulting in a total of 81 cells.

## How to Play

1. The game is played by two players, X and O, who take turns marking their symbol in an empty cell.
2. The objective is to win three grids in a row, either horizontally, vertically, or diagonally.
3. Each move is played in a small 3x3 grid, and the position of the move within the small grid determines the large grid where the opponent must play their next move.
4. If a player is sent to a large grid that has already been won, they can choose to play in any other available large grid.
5. The game continues until a player wins three grids in a row or all the grids are filled, resulting in a draw.

## Features

- Graphical user interface using the `customtkinter` library
- Interactive gameplay with mouse clicks
- Visual indicators for the current turn and large grid availability
- Winning condition detection for both small and large grids
- Display of the winning player

## Future Enhancements

The current implementation of Ultimate Tic Tac Toe provides a basic gameplay experience. However, there are several exciting enhancements planned for the future, including:

### AI Functionality with Minimax and Alpha-Beta Pruning

One of the key goals is to introduce AI functionality to the game, allowing players to compete against a computer opponent. The AI will utilize the minimax algorithm along with alpha-beta pruning to make intelligent moves.

- Minimax is a recursive algorithm commonly used in two-player games with perfect information. It aims to minimize the potential loss for a worst-case scenario while maximizing the potential gain.
- Alpha-beta pruning is an optimization technique that reduces the number of nodes evaluated in the minimax search tree. It eliminates branches that are guaranteed to be worse than the current best move, significantly improving the efficiency of the algorithm.

By implementing minimax with alpha-beta pruning, the AI opponent will be able to analyze the game state, consider various possible moves, and choose the most optimal move to maximize its chances of winning.

### Additional Features

In addition to the AI functionality, other planned enhancements include:

- Difficulty levels for the AI opponent, allowing players to choose between easy, medium, and hard difficulties.
- A game menu system for easy navigation and game customization.
- Sound effects and visual animations to enhance the gaming experience.
- Game statistics and leaderboard to keep track of player performances.
- Online multiplayer functionality, enabling players to compete against each other remotely.

## Contributing

Contributions to the Ultimate Tic Tac Toe project are welcome! If you have any ideas, suggestions, or bug reports, please open an issue on the GitHub repository. If you'd like to contribute code, you can fork the repository, make your changes, and submit a pull request.

