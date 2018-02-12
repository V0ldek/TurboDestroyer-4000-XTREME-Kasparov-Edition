# ConnectFour

Codename: TurboDestroyer 4000 XTREME - Kasparov Edition

A Connect Four game with AI using minimax algorithm with alpha-beta pruning and iterative deepening

Copyright (C) 2016 Mateusz Gienieczko, Franciszek Hnatow, Jan Klinkosz, Piotr Lewandowski and Kamil Turko

Usage:

-- Windows: run bin/ConnectFour.exe executable

-- Linux: run main.py script

Controls:

The player is red and always starts first. Choose the row to insert your token into with keys '1', '2', '3', '4', '5', '6', '7' on your keyboard.

The AI is blue and will think about its move for 10 seconds before performing it.

The game screen will change colors when the game is over: red means player wins, blue means AI wins, purple means draw.

Press 'r' to reset the game.

The screen will flash briefly when you try to perform an illegal move.

The game code consists of four modules:

-- UserInterface - handles GUI and displaying gamestate on screen

-- LevelManager - board representation and modification

-- AIManager - Artificial intelligence logic

-- GameManager - main game loop, communication between other modules

File setup.py creates an executable version for Windows using py2exe module.
