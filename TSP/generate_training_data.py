# -*- coding: utf-8 -*-
import sys
import os.path
import points_map
import json
import random

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

FILENAME = "save/training_data.json"

def generate_data_point():
  num_points = random.randint(7,10)
  num_map_size = random.randint(500,5000)
  print("Points: %d -- Map Size: %d" % (num_points, num_map_size))

  points_iterator = points_map.points(num_points, num_map_size)

  low_dist = 10000000000.
  low_points_store = []
  points = []
  iteration_count = 0
  cont = True

  try:
    while cont == True:
      iteration_count += 1
      points = points_iterator.next()
      dist = points_map.dist_between_points(points, low_dist)
      sys.stdout.write("Permutation progress: %d %f %f  \r" % (iteration_count, dist, low_dist) )
      sys.stdout.flush()

      if dist < low_dist:
        low_points_store = points
        low_dist = dist

  except StopIteration:
    pass

  print(low_points_store, low_dist, iteration_count)
  return { 'data': low_points_store, 'score': low_dist }


def write_data(data):
    # Write JSON file
  with io.open(FILENAME, 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data)
    outfile.write(to_unicode(str_))

def load_data():
  # Read JSON file
  try:
    f = open(FILENAME, 'rb')
    with f as data_file:
      data_loaded = json.load(data_file)
  except IOError:
    print "Could not read file:", 'training_data.json'
    data_loaded = []

  return data_loaded

def generate_training_data_loop():
  i = 100
  full_data = load_data()

  while i > 0:
    i -= 1
    data_point = generate_data_point()
    full_data.append(data_point)
    write_data(full_data)
    pass

def main():
  generate_training_data_loop()

if __name__ == "__main__":
  main();
