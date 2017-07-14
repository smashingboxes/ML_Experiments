import generate_training_data
import points_map
import random
import math
import numpy as np

class Trainer:
  def __init__(self, training_data):
    self.training_data = training_data

    self.actions = [
      'next_point', # set cursor to next available point
      'prev_point', # set cursor to prev available point
      'select_point' # locks in this point as the next
    ]

    self.action_map = {
      'next_point': self.next_point,
      'prev_point': self.prev_point,
      'select_point': self.select_point
    }

    self.SCORE_MUL = 100
    self.flatten_list = lambda l: [item for sublist in l for item in sublist]
    self.normalize_list = lambda n: [float(i)/max(raw) in n for i in raw]

    self.state = {
      'selected_point_index': 0,
      'high_score': 1,
      'current_score': 0., #
      'current_distance': 0., # track calculated distance of selected points
      'current_points': [], # start as an empty list
      'remaining_points': [], # init with ranomized version of game points
      'best_distance': 0., # init as game score
      'best_points': [] # init as game points
    }

    self.new_game()

  def observation_space(self):
    selected_point = self.selected_point()
    next_selected_point_1 = self.selected_point( self.remaining_point_index_by_offset(1) )
    next_selected_point_2 = self.selected_point( self.remaining_point_index_by_offset(2) )
    next_selected_point_3 = self.selected_point( self.remaining_point_index_by_offset(3) )

    current_points_head = self.current_points_head()
    space = [
      current_points_head,
      [self.state['current_distance']],
      self.point_data_for_observation_space(selected_point, current_points_head),
      self.point_data_for_observation_space(next_selected_point_1, current_points_head),
      self.point_data_for_observation_space(next_selected_point_2, current_points_head),
      self.point_data_for_observation_space(next_selected_point_3, current_points_head)
    ]
    return (self.flatten_list(space));

  def point_data_for_observation_space(self, selected_point, current_points_head):
    return np.array([
        selected_point,
        [ points_map.distance(current_points_head, selected_point),
          points_map.distance(selected_point, self.state['current_points'][0]) ]
      ]).flatten().tolist()

  def remaining_point_index_by_offset(self, offset = 0):
    if (self.is_done()):
      return [ False, False ]

    return (self.state['selected_point_index'] + offset) % len(self.state['remaining_points'])

  def is_done(self):
    return (len(self.state['remaining_points']) <= 0)

  def selected_point(self, index = None):
    if (self.is_done()):
      return [ False, False ]

    if (index is None):
      index = self.state['selected_point_index']

    return self.state['remaining_points'][ index ]

  def current_points_head(self):
    return self.state['current_points'][-1]

  def new_game(self):
    game = random.choice(self.training_data)
    points = list(game['data'])
    random.shuffle(points)

    self.state['best_points'] = list(game['data'])
    self.state['best_distance'] = game['score']
    self.state['selected_point_index'] = 0
    self.state['current_score'] = 0
    self.state['current_distance'] = 0.
    self.state['current_points'] = [points.pop()]
    self.state['remaining_points'] = points
    self.state['high_score'] = self.SCORE_MUL * (len(self.state['best_points']) - 1)

    return self.observation_space()

  def step(self, index):
    reward = self.do_action(index)
    next_state = self.observation_space()
    done = self.is_done()
    if (done):
      reward = (self.state['best_distance'] / self.state['current_distance'])
    return next_state, reward, done

  def do_action(self, index):
    action_name = self.actions[index]
    return self.action_map[action_name]()

  def next_point(self):
    return self.move_to_point(1)

  def prev_point(self):
    return self.move_to_point(-1)

  def move_to_point(self, dir):
    if (self.is_done()):
      return False

    self.state['selected_point_index'] = (self.state['selected_point_index'] + dir) % len(self.state['remaining_points'])

    return 0.0

  def select_point(self):
    if (self.is_done()):
      return False

    index = self.state['selected_point_index']
    _score = self.check_point_correctness(self.state['remaining_points'][index])
    self.transfer_selected_point(index)
    self.next_point()

    if (len(self.state['remaining_points']) == 1):
       _score = self.handle_map_finished(_score)

    return _score

  def check_point_correctness(self, chosen_point):
    expected_best_point = self.find_best_point_in_direction(1)
    expected_best_point_alt = self.find_best_point_in_direction(-1)
    measure = (expected_best_point == chosen_point) or (expected_best_point_alt == chosen_point)
    return 1. if measure else -1.

  def find_best_point_in_direction(self, direction):
    return self.state['best_points'][ (self.state['best_points'].index(self.state['current_points'][-1]) + direction) % len(self.state['best_points']) ]

  def handle_map_finished(self, _score):
    self.transfer_selected_point(0)
    self.state['current_distance'] += points_map.distance(
      self.state['current_points'][0],
      self.state['current_points'][-1]
    )
    _score += self.relative_score()
    return _score

  def transfer_selected_point(self, index):
    point = self.state['remaining_points'].pop(index)
    self.state['current_points'].append(point)
    self.state['current_distance'] += points_map.distance(
      self.state['current_points'][-1],
      self.state['current_points'][-2]
    )
    self.state['current_score'] += self.score()

  def score(self):
    avg_best = self.state['best_distance'] / len(self.state['best_points'])
    score_p = min(1.0,
      avg_best / (self.state['current_distance'] / len(self.state['current_points'])))
    score_offset_p = max(0.0, (score_p - 0.8))
    return (score_offset_p / 10.)

  def agent_score(self):
    return self.relative_score()

  def high_score(self):
    return self.state['high_score']

  def relative_score(self):
    return self.state['best_distance'] / self.state['current_distance']


def new():
  training_data = generate_training_data.load_normalized_data()
  trainer = Trainer(training_data)
  return trainer


def main():
  training_data = generate_training_data.load_normalized_data()
  trainer = Trainer(training_data)
  print(trainer.state)

  score = 0
  for x in xrange(1,10):
    if (trainer.do_action(0) == False):
      break;
    score += trainer.do_action(1)

    print("Points: ", trainer.state['current_points'])
    print("Distance: ", trainer.state['current_distance'])
    print("Score: ", score)

  print("Final Score", score / trainer.high_score())

  return trainer

if __name__ == "__main__":
  main()
