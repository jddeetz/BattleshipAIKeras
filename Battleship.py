print(" Welcome to Battleship AI Edition!\n")
print("                                  ")
print("            |>                    ")
print("         |> |> |>         \|/     ")
print("~~~~~~~~\========/~~~~~~~~~o~~~~~\n")

import numpy as np
import pickle
import keras

#Load the keras model
model=pickle.load(open("model.pkl",'rb'))


filename=input("Please enter the name of the CSV file containing the positions of the ships, or press ENTER: ")

if not filename: filename="Sample.csv"

opened=0

while opened==0:
    try:
        user_board=np.loadtxt(open(filename, "rb"), delimiter=",")
        opened=1
    except: 
        print("That file does not seem to exist.\n")
        filename=input("Please enter the name of the CSV file containing the positions of the ships: ")
    
#Select a ai_board
import random

ai_board=np.loadtxt(open("Boards/"+str(random.randint(1,10))+".csv", "rb"), delimiter=",")

user_fog_board=np.zeros_like(user_board)-1

winner=0

#Import showboard module
import DisplayBoard as db

while winner==0:
    print("It is your turn, what do you wish to do?")
    print("Enemies board:")
    db.display(ai_board,'a')
    print("Your board:")
    db.display(user_board,'u')
    
    #Prompt user for which space to fire on
    collet_spec=0
    while collet_spec==0:
        collet=input("Enter the column [A-J] of the location you wish to fire your cannons: ")
        if collet in "ABCDEFGHIJ": 
            collet_spec=1
            x="ABCDEFGHIJ".rindex(collet)
        
    rownum_spec=0
    while rownum_spec==0:
        rownum=input("Enter the row [0-9] of the location you wish to fire your cannons: ")
        if rownum in "0123456789": 
            rownum_spec=1
            y=int(rownum)
    
    #Fire the missile!
    if ai_board[y,x]==1:
        print("Your cannons have hit a ship!")
        ai_board[y,x]=3
    else:
        print("Miss!")
        ai_board[y,x]=2
    
    #Check for win condition
    if 1 not in ai_board: 
        print("You have sunk all of the enemies ships!\nCONGRATULATIONS!")
        break
    
    #Now it is the AI's turn. Predict the proba's of all squares
    predicted=model.predict(user_fog_board.reshape(1,1,10,10)).reshape(10,10)
    
    #Find the max proba of the array
    selected=0
    while selected==0:
        y,x = np.unravel_index(np.argmax(predicted, axis=None), predicted.shape)
        if user_fog_board[y,x]!=-1: predicted[y,x]=0
        else:
            selected=1
            
    #Fire the missile!
    print("The AI fires on "+"ABCDEFGHIJ"[x]+'-'+str(y))
    if user_board[y,x]==1:
        print("The enemies cannons have hit your ship!")
        user_board[y,x]=3
        user_fog_board[y,x]=1
    else:
        print("Your ships have evaded danger!")
        user_board[y,x]=2

        user_fog_board[y,x]=0
    
    #Check for loss condition
    if 1 not in user_board: 
        print("All of your ships have sunk!\nGAME OVER!")
        break
    
    
    
    
    
    