# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 22:21:45 2020

@author: Shubham Buchunde
"""

# Part 1 - Data Preprocessing

# Importing the libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing the training set
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_sc= sc.fit_transform(training_set)

#creating a datastructutre with 60 timestamps and 1 output
x_train = []
y_train = []
for i in range(60,1258):
    x_train.append(training_set_sc[i-60:i,0])
    y_train.append(training_set_sc[i,0])
x_train, y_train =  np.array(x_train), np.array(y_train)

# Reshaping
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))


# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()
# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50,return_sequences=True, input_shape= (x_train.shape[1], 1)))
regressor.add(Dropout(0.20))
# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.20))
# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.20))
# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.20))
# Adding the output layer
regressor.add(Dense(units=1))
# Compiling the RNN
regressor.compile(optimizer='adam',loss='mean_squared_error')

#fitting the RNN to the Training set
regressor.fit(x_train,y_train, epochs = 100, batch_size=32)

#Part- 3 Making the prediction
# Getting the real stock price of 2017
dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values
# Getting the predicted stock price of 2017
dataset_total = pd.concat((dataset_train['Open'],dataset_test['Open']),axis=0)
inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values
inputs=inputs.reshape(-1,1)
inputs = sc.transform(inputs)

x_test= []
for i in range(60,80):
    x_test.append(inputs[i-60:i,0])
    
x_test=  np.array(x_test)


x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_stock_price = regressor.predict(x_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    
# Visualising the results
plt.plot(real_stock_price,color = 'red',label='Real google stock price')
plt.plot(predicted_stock_price,color = 'blue',label='Predicted google stock price')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()


















