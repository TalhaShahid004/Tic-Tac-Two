
<h1 align="center">Tic-Tac-Two</h1>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python Version">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </a>
</p>

<p align="center">
  This repository contains an implementation of the Ultimate Tic Tac Toe game, a more complex version of the classic Tic Tac Toe, along with AI opponents using Minimax with Alpha-Beta pruning and Monte Carlo Tree Search (MCTS).
</p>



## Project Description
This project provides an implementation of the Ultimate Tic Tac Toe game. It features a graphical user interface (GUI) built with the `customtkinter` library, allowing interactive gameplay. The game involves a 3x3 grid of 3x3 grids, offering a challenging twist to the traditional Tic Tac Toe. Additionally, the project includes AI opponents that use Minimax with Alpha-Beta pruning and Monte Carlo Tree Search (MCTS) algorithms to play against.

## Main Features
- Interactive GUI using `customtkinter`.
- Mouse-based gameplay.
- Highlighted playable large grids.
- Visual indicators for game state.
- Winning condition detection for both small and large grids.
- AI opponents using Minimax with Alpha-Beta Pruning and MCTS algorithms.

## Installation and Setup
To set up the project on your local machine, follow these steps:

1.  Clone the repository to your local machine:
    ```bash
    git clone https://github.com/TalhaShahid004/Tic-Tac-Two.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Tic-Tac-Two
    ```
3. Ensure you have Python 3.12 installed. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project
To run the game, execute the following command:
```bash
python Mini_vs_Monte_Autonomous.py
```
or
```bash
python Mini_vs_Monte_UTTT.py
```
or
```bash
python Minimax_alphabeta_UTTT.py
```
or
```bash
python MonteCarlo_UTTT.py
```
or
```bash
python mini_vs_random.py
```
or
```bash
python monte_vs_random.py
```
These will launch different versions of the game.

## Dependencies and Tools
-   **Python**: Version 3.12 or higher.
-   **customtkinter**: For building the GUI.
-   **random**: For randomizing moves.
-   **math**: For mathematical operations in MCTS algorithm.
-   **copy**: For deep copy of data structures

## Contribution Guide
Contributions are welcome! To contribute to this project, please follow these steps:
1.  Fork the repository.
2.  Create a new branch for your feature or fix.
3.  Make your changes and commit them with clear messages.
4.  Push your changes to your forked repository.
5.  Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. 
