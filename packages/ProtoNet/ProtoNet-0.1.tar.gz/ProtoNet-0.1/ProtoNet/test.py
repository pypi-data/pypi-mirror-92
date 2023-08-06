import sys
sys.path.append(".")

from Models.Model import Model
from Layers.Dense import Dense

import numpy as np

x_train = np.array([[[0]], [[1]], [[2]], [[3]]])
y_train = np.array([[[2]], [[4]], [[6]], [[8]]])

nn = Model()
nn.add(Dense(input_shape=1, output_shape=1, activation='linear'))
nn.use('mae')
nn.train(x_train, y_train, epochs=1000, learning_rate=0.01)
