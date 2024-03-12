"""_summary_
code will be used to calculate the probability of landing on a specific square in the game of Monopoly
the code will include a variable for changing the number of "players" in the game
the code will include a variable for changing the number of "community chest cards" in the deck
the code will include a variable for changing the number of "chance cards" in the deck
the code will include a variable for changing the number of "go to jail cards" in the deck

average number of rolls per game = 40 - 60 (https://www.reddit.com/r/monopoly/comments/qdjer7/comment/hhmxd0f/?utm_source=share&utm_medium=web2x&context=3)

_Groups_
Brown - 2 squares
Light Blue - 3 squares
Pink - 3 squares
Orange - 3 squares
Red - 3 squares
Yellow - 3 squares
Green - 3 squares
Blue - 2 squares
Railroads - 4 squares
Utilities - 2 squares


In the normal game
_Community_
Go to go - 0
*get £200
*pay £50
*get £50
*get out of jail
Go to jail - 10
*Get £20
*Get £10
*Get £100
*Pay £100
*Pay £50
*Get £25
*Pay £40-house, £115-hotel
*Get £10
*Get £100

_Chance_
Go to go - 0
Trafalgar square - 24
Mayfair - 39
Pall mall - 11
Nearest station (x2) - 5, 15, 25, 35
Nearest utility - 12, 28
*Bank pays you £50
*Get out of jail
Back 3 spaces 
Go to jail - 10
*General repairs £25-house, £100-hotel 
*Speeding fine £15
Kings cross station - 25
*Pay each player £50
*Collect £150
""" 


#importing the random module
from doctest import debug
import json
from math import log
import random
import logging
import time

def debugMode():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug mode is on")
    return True

def infoMode():
    logging.basicConfig(level=logging.INFO)
    logging.info("Info mode is on")
    return True

debugMode() if input("Debug mode? (y/n): ").lower() == "y" else "none"
infoMode() if input("Info mode? (y/n): ").lower() == "y" else logging.basicConfig(level=logging.WARNING)

#creates a dictionary for the data to be stored
timesLanded = {} 
#creating a list of the 40 squares on the board
listOfSquares = ["go","Brown(1)","community chest(1)","Brown(2)","income tax","Railroad(1)","Light Blue(1)","chance(1)","Light Blue(2)","Light Blue(3)",
       "jail","Pink(1)","utility(1)","Pink(2)","Pink(3)","Railroad(2)","Orange(1)","community chest(2)","Orange(2)","Orange(3)",
       "free parking","Red(1)","chance(2)","Red(2)","Red(3)","Railroad(3)","Yellow(1)","Yellow(2)","utility(2)","Yellow(3)",
       "go to jail","Green(1)","Green(2)","community chest(3)","Green(3)","Railroad(4)","chance(3)","Blue(1)","luxury tax","Blue(2)"]


logging.info("Times landed list created")
logging.debug(timesLanded)

#Variables that can be changed to modify the game
players = 4

communityCards = 16 #community chest cards
comJail = 1
comGo = 1

chanceCards = 16 #chance card 
chanceJail = 1
chanceGo = 1 


#Creates a list of players, each player has a value will will act as their position on the board
playerList = []
for i in range(players):
    playerList.append({i+1:0})
logging.info("Player list created")
logging.debug(playerList)
time.sleep(1)

def updateProbability(square): #function to update the probability of landing on a square
        #access the timesLanded list and add 1 to the value of the square in the current game 
        timesLanded[gameNum][listOfSquares[square]] += 1
        
        logging.info("Probability updated")
        logging.debug(timesLanded)

def diceRoll(): #function to roll the dice
    dice1 = random.randint(1,6) #randomly selects a number between 1 and 6
    dice2 = random.randint(1,6) #randomly selects a number between 1 and 6
    
    roll = dice1 + dice2 #adds the two numbers together to get the roll
    logging.info("Dice rolled")
    logging.debug((f"{dice1}+{dice2} = {roll}"))
    return roll #returns roll variable

def communityChest(): #function to draw a community chest card
    card = random.randint(1,communityCards) #randomly selects a number (card)
    logging.debug(card)
    
    if card <= (prob := comJail): #if number is <= number of jail cards (and set prob to that number)
        logging.info("Community chest - jail")
        return 10 #return jail

    elif card <= comGo + prob: #elif number is between prob and number of go cards 
        logging.info("Community chest - go")
        return 0 #return go
    
    else: #else
        logging.info("Community - NONE")
        return "NONE" #return NONE
    
def chance(): #function to draw a chance card
    card = random.randint(1,chanceCards) #randomly selects a number (card)
    logging.debug(card)
    
    if card <= (prob := chanceJail): #if number is <= number of jail cards (and set prob to that number)
        logging.info("Chance - jail")
        return 10 #return jail

    elif card <= chanceGo + prob: #elif number is between prob and number of community cards
        logging.info("Chance - Community Chest") 
        return 0 #return community chest
    
    else: #else
        logging.info("Chance - NONE")
        return "NONE" #return NONE

def movePlayer(): #function to move player
    for player in playerList: #for each player in playerList
        roll = diceRoll() #roll the dice and save as roll
        
        #Move player
        if player[list(player)[0]] + roll > 39: #if player position + roll is greater than 39
            player[list(player)[0]] = player[list(player)[0]] + roll - 40 #subtract 40 from the total
            
            logging.info("Player moved") 
            logging.debug(player) 
            #Add new location onto probability list
            updateProbability(player[list(player)[0]]) #update probability of landing on square
            
            
        else: #else
            player[list(player)[0]] += roll #add roll to player position
            
            logging.info("Player moved")    
            logging.debug(player) 
            updateProbability(player[list(player)[0]]) #update probability of landing on square
        
        
        #Go to jail
        if player[list(player)[0]] == 30: #if player lands on go to jail
            player[list(player)[0]] = 10 #move player to jail
            
            logging.info("Player moved to jail")
            logging.debug(player) 
            updateProbability(player[list(player)[0]]) #update probability of landing on square
            
            
        #Community chest
        elif player[list(player)[0]] == 2 or player[list(player)[0]] == 17 or player[list(player)[0]] == 33: #if player lands on community chest
            draw = communityChest() #move player to community chest
            
            if draw == "NONE":
                pass
            else:
                player[list(player)[0]] = draw
            
            logging.info("Player moved to community chest")
            logging.debug(player)
            updateProbability(player[list(player)[0]]) #update probability of landing on square
        
        #Chance
        elif player[list(player)[0]] == 7 or player[list(player)[0]] == 22 or player[list(player)[0]] == 36: #if player lands on chance
            draw = chance() #move player to chance
            
            if draw == "NONE": #if draw is NONE
                pass
            else: #else
                player[list(player)[0]] = draw
            
            logging.info("Player moved to chance")
            logging.debug(player)
            updateProbability(player[list(player)[0]]) #update probability of landing on square       


#Ask user for number of rolls
while True:
    try:
        games = int(input("\nHow many games? ")) #get user input
        rolls = int(input("How many rolls per game? ")) #get user input
        
        break #break out of loop
    except ValueError: #if user input is not a number
        print("Please input a number") #print error message
        
logging.info("Number of games set")   
logging.info("Number of rolls set")
logging.debug(games)
logging.debug(rolls)


gameNum = 0 #global variable for game number
for i in range(games):
    gameNum = i+1 #add 1 to gameNum
    
    #creates a new dictionary for each game with a dictionaries for each square
    timesLanded[gameNum] = {"go":0,"Brown(1)":0,"community chest(1)":0,"Brown(2)":0,"income tax":0,"Railroad(1)":0,"Light Blue(1)":0,"chance(1)":0,"Light Blue(2)":0,"Light Blue(3)":0,
         "jail":0,"Pink(1)":0,"utility(1)":0,"Pink(2)":0,"Pink(3)":0,"Railroad(2)":0,"Orange(1)":0,"community chest(2)":0,"Orange(2)":0,"Orange(3)":0,
         "free parking":0,"Red(1)":0,"chance(2)":0,"Red(2)":0,"Red(3)":0,"Railroad(3)":0,"Yellow(1)":0,"Yellow(2)":0,"utility(2)":0,"Yellow(3)":0,
         "go to jail":0,"Green(1)":0,"Green(2)":0,"community chest(3)":0,"Green(3)":0,"Railroad(4)":0,"chance(3)":0,"Blue(1)":0,"luxury tax":0,"Blue(2)":0}
    
    for ii in range(rolls): #for the number of rolls
        movePlayer() #call movePlayer function
        f = open("timesLanded.json", "w") #open file 
        json.dump(timesLanded, f, indent=4) #dump timesLanded data into file
        f.close() #close file
       
    logging.warning(f"Game {gameNum} complete")