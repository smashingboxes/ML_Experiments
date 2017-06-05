from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding
import numpy as np
import random
import time
import os.path
import points_map

points = points_map.points()
dist = points_map.dist_between_points(points)

print(points, dist)
