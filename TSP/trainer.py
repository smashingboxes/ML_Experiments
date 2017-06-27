import generate_training_data
import points_map
import random
import math

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
    _selected_point = self.selected_point()
    _last_selected_point = self.last_selected_point()
    space = [
      _selected_point,
      _last_selected_point,
      [ points_map.distance(_last_selected_point, _selected_point),
        points_map.distance(_selected_point, self.state['current_points'][0]),
        self.state['current_distance'],
        len(self.state['remaining_points']) ]
    ]
    return self.flatten_list(space)

  def is_done(self):
    return (len(self.state['remaining_points']) <= 0)

  def selected_point(self):
    if (self.is_done()):
      return [ False, False ]

    return self.state['remaining_points'][ self.state['selected_point_index'] ]

  def last_selected_point(self):
    return self.state['current_points'][-1]

  def new_game(self):
    game = random.choice(self.training_data)
    points = list(game['data'])
    random.shuffle(points)
    # print(points, game['data'])

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
    # print('Selecting Point: ', self.state['remaining_points'][index])
    self.move_selected_point(index)
    self.next_point()
    _score = 0.0 + self.score()

    if (len(self.state['remaining_points']) == 1):
      _score = self.handle_map_finished(_score)

    return _score

  def handle_map_finished(self, _score):
    self.move_selected_point(0)
    self.state['current_distance'] += points_map.distance(
      self.state['current_points'][0],
      self.state['current_points'][-1]
    )
    _score = _score + self.score()
    return _score

  def move_selected_point(self, index):
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
    score_offset_p = max(0.0, (score_p - 0.45))
    return (score_offset_p)

  def agent_score(self):
    return self.relative_score()

  def high_score(self):
    return self.state['high_score']

  def relative_score(self):
    return self.state['current_score'] / self.high_score()


def new():
  training_data = generate_training_data.load_data()
  trainer = Trainer(training_data)
  return trainer


def main():
  training_data = generate_training_data.load_data()
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
