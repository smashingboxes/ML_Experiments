from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding
import numpy as np
import random
import sys
import time
import os.path
import points_map

# -*- coding: utf-8 -*-
import json

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def generate_data_point():
  points_iterator = points_map.points()

  low_dist = 0
  low_points_store = []
  points = []
  iteration_count = 0
  cont = True

  try:
    while cont == True:
      iteration_count += 1
      points = points_iterator.next()
      dist = points_map.dist_between_points(points)
      sys.stdout.write("Permutation progress: %f %f %f  \r" % (iteration_count, dist, low_dist) )
      sys.stdout.flush()

      if low_dist == 0 or dist < low_dist:
        low_points_store = points
        low_dist = dist

  except StopIteration:
    pass

  print(low_points_store, low_dist, iteration_count)
  return { 'data': low_points_store, 'score': low_dist }


def write_data(data):
    # Write JSON file
  with io.open('training_data.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data)
    outfile.write(to_unicode(str_))

def load_data():
  # Read JSON file
  try:
    f = open('training_data.json', 'rb')
    with f as data_file:
      data_loaded = json.load(data_file)
  except IOError:
    print "Could not read file:", 'training_data.json'
    data_loaded = []

  return data_loaded

def generate_training_data_loop():
  i = 10
  full_data = load_data()

  while i > 0:
    i -= 1
    data_point = generate_data_point()
    full_data.append(data_point)
    write_data(full_data)
    pass

def main():
  generate_training_data_loop()

main();
