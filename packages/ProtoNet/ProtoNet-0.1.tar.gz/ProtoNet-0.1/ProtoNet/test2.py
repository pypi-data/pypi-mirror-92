import sys
sys.path.append(".")
import numpy as np

from Models.LossFunctions import getLossFunctions
y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

dct = getLossFunctions()

print(dct['mse'][0](np.array([10]),np.array([10])))
