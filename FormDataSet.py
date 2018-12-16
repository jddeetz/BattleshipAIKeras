import numpy as np
import pickle

#Create a list of boards
boards=[]

#I have manually created ten boards. Let's load those
for i in range(10):
    boards.append(np.loadtxt(open("Boards/"+str(i+1)+".csv", "rb"), delimiter=","))

#Ten game boards is not a lot, it might be possible to create more through transformations
    
#Each of these operations can be performed on a game board and it will still be a valid game board
#Each board can be rotated 0, 90, 180, or 270 degrees
#Each board can be flipped horizonally or vertically

#Lets perform some of these operations to generate more boards
flip_h=[0,1]
flip_v=[0,1]
rotate=[0,1,2,3]

new_boards=[]
for board in boards:
    for h in flip_h:
        for v in flip_v:
            for r in rotate:
                
                if h==1:
                    board=np.fliplr(board)
                if v==1: 
                    board=np.flipud(board)
                
                new_boards.append(np.rot90(board, k=r))

#Now, we have 160 different boards with transformations.
#However, the computer obviously cannot see the whole board.
#In battleship, some of the squares will be unknown, and some will be revealed.                

#In the middle of the game, we can represent the game board with a -1 as a not
#revealed, a 0 as a known empty, and a 1 as a known hit.
                
#The next step in forming the data set will be to randomly construct these game boards, randomly chosen from the list of 160 that we have, and with a random number of reveals.
#We can accomplish this by simply dropping -1's into a given game board.

#How many game boards do we want?
num_train=10000
num_hidden=70

foggy_boards=[]
clear_boards=[]

import random

while len(foggy_boards)<num_train:
    
    #Choose a random board from the set
    board_clear=np.array(new_boards[random.randint(0,len(new_boards)-1)],copy=True)
    board_fog=np.array(board_clear,copy=True)

    #Save the board to clear boards
    clear_boards.append(board_clear)
    
    #There are 100 squares on a board, we can drop -1's at random locations on the board
    for x in range(num_hidden):
        board_fog[random.randint(0,9),random.randint(0,9)]=-1
    
    foggy_boards.append(board_fog)
    
#Save the data
pickle_jar=[foggy_boards,clear_boards]
pickle.dump(pickle_jar, open("training-boards.pkl",'wb') )   
    

