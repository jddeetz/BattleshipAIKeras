#Train an AI to predict whether which squares have 
from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras import metrics
import numpy as np
import pickle
import random

#Get the boards from the saved file
jar=pickle.load(open("training-boards.pkl",'rb'))
foggy_boards=jar[0]
clear_boards=jar[1]

# input board dimensions
board_rows, board_cols = 10, 10

#Reformat foggy and clear boards into numpy arrays with the correct dimensions.
#Split boards into training and test sets
x_train=np.array([]).reshape(0,1,board_rows,board_cols)
x_test=np.array([]).reshape(0,1,board_rows,board_cols)
y_train=np.array([]).reshape(0,1,board_rows,board_cols)
y_test=np.array([]).reshape(0,1,board_rows,board_cols)

for boardnum in range(len(foggy_boards)):
    if random.random()>0.3:
        x_train=np.append(x_train,foggy_boards[boardnum].reshape(1,1,board_rows,board_cols), axis=0)
        y_train=np.append(y_train,clear_boards[boardnum].reshape(1,1,board_rows,board_cols), axis=0)
    else:
        x_test=np.append(x_test,foggy_boards[boardnum].reshape(1,1,board_rows,board_cols), axis=0)
        y_test=np.append(y_test,clear_boards[boardnum].reshape(1,1,board_rows,board_cols), axis=0)    

#Flatten the game board matrices from what we are trying to predict, since the dense
#layers of the NN is doing the same.
y_train=y_train.reshape(y_train.shape[0],100)
y_test=y_test.reshape(y_test.shape[0],100)

#The shape of the input into the NN
input_shape = (1,board_rows, board_cols)

#Training Hyperparameters
batch_size = 100 # Number of examples to train for each epoch
epochs = 100 # Number of training epochs

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

#Specify the model architecture
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape,padding='same'))
model.add(Conv2D(64, (3,3), activation='relu',border_mode='same'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(100, activation='sigmoid'))

#Compile the model above
model.compile(loss=keras.losses.binary_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=["binary_accuracy"])

#Train the model
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))

#Evaluate the test set accuracy
score = model.evaluate(x_test, y_test, verbose=0)

#Print the accuracy on the test set
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#Save the model
pickle.dump(model, open("model.pkl",'wb') ) 