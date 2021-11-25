
# Minesweeper
Hello there :) 
I made the infamous minesweeper game in python.
You can either play the game on the command line or run a solver which automatically tries to play the game.

## Installation and Setup:

`python3 -m venv env`

`source env/bin/activate`

`pip3 install -r requirements.txt`

## To play:

`python3 play.py  n  num_mines` 
n represents the size of the board (n x n)
num_mines represents the number of mines on the board

## To run the solver:

`python3 run_solver.py n num_mines num_trials`
n represents the size of the board (n x n)
num_mines represents the number of mines on the board
num_trials represents the number of times the solver plays the game
