# Monopoly Probability Simulator
A simple program to find the probability of landing on each square in Monopoly

The program simulates a roll for each player and moves them to the appropriate square, 
chance cards and community chests can move the player so they have been implemented. 
However, property purchacing isnt neccesary so I haven't added it (yet). 

When the program is run the user can input the number of games to run and the number of rolls per game.
The program will then iterate through each game and simulate each players movement, 
and keep a recored how many times a square is landed on. When the program finishes it will output to a json file, 
which can be imported into Excel to create tables and graphs for analysing the results

## pseudocode
for each player 
roll dice
update player location 
add 1 to squares timesLandedOn
if on community chest or chance draw card
if card will move player, move and update position value, add 1 to squares timesLandedOn

## Features
- custom value for number of games and rolls per game
- variable for changing the number of "players" in the game
- variable for changing the number of "community chest cards" in the deck
- variable for changing the number of "chance cards" in the deck
- variable for changing the number of "go to jail cards" in the deck
