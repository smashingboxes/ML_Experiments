import generate_training_data
import random

class Trainer:
  def __init__(self, training_data):
    self.training_data = training_data

    self.actions = [
        'next_point', # set cursor to next available point
        'choose_point' # locks in this point as the next
      ]

    self.state = {
        'current_distance': 0, # track calculated distance of selected points
        'current_points': [], # start as an empty list
        'remaining_points': [], # init with ranomized version of game points
        'best_distance': 0, # init as game score
        'best_points': [] # init as game points
      }

    self.new_game()

  def new_game(self):
    game = random.choice(self.training_data)
    points = list(game['data'])
    random.shuffle(points)
    print(points, game['data'])

    self.state['best_points'] = list(game['data'])
    self.state['best_distance'] = game['score']
    self.state['current_distance'] = 0
    self.state['current_points'] = [points.pop()]
    self.state['remaining_points'] = points


def env():
  training_data = generate_training_data.load_data()
  trainer = Trainer(training_data)
  print(trainer.state)
  return trainer

if __name__ == "__main__":
  env()
