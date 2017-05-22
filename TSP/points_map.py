# functions to generate a map for a TSP
import numpy as np
import math

def points(count = 10, mapsize = 100):
  points = np.zeros((count,2))
  i = 0
  for p in points:
    points[i][0] = np.random.randint(0, mapsize)
    points[i][1] = np.random.randint(0, mapsize)
    i += 1

  return points

def distance(point1, point2):
  return math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))

def dist_between_points(points):
  dist = 0.0
  i = 0
  for p in points:
    if i > 0:
      dist += distance(points[i], points[i-1])
    i += 1

  return dist
