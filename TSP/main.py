# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import trainer
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding, Reshape
from keras.optimizers import Adam
from collections import deque
from keras import backend as K

EPISODES = 50000


class DQNAgent:
  def __init__(self, state_size, action_size):
    self.state_size = state_size
    self.action_size = action_size
    self.memory = deque(maxlen=2000)
    self.gamma = 0.95    # discount rate
    self.epsilon = 1.0  # exploration rate
    self.epsilon_min = 0.05
    self.epsilon_decay = 0.9995
    self.learning_rate = 0.001
    self.model = self._build_model()
    self.target_model = self._build_model()
    self.update_target_model()

  def _huber_loss(self, target, prediction):
    # sqrt(1+error^2)-1
    error = prediction - target
    return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

  def _build_model(self):
    # Neural Net for Deep-Q learning Model
    model = Sequential()
    model.add(Dense(16, input_dim=self.state_size, activation='relu'))

    # LSTM?
    # model.add(Embedding(1024, 1024))
    # model.add(LSTM(1024))

    model.add(Dense(128, activation='relu'))
    model.add(Dense(self.action_size, activation='linear'))

    model.compile(loss=self._huber_loss,
      optimizer=Adam(lr=self.learning_rate))

    #model.compile(loss='mse', optimizer='adam')
    # model.compile(loss='kullback_leibler_divergence',
      # optimizer='adam')
    return model

  def update_target_model(self):
    # copy weights from model to target_model
    self.target_model.set_weights(self.model.get_weights())

  def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))

  def act(self, state):
    if np.random.rand() <= self.epsilon:
      return random.randrange(self.action_size)
    act_values = self.model.predict(state)
    return np.argmax(act_values[0])  # returns action

  def replay(self, batch_size):
    minibatch = random.sample(self.memory, batch_size)
    for state, action, reward, next_state, done in minibatch:
      target = self.model.predict(state)
      if done:
        target[0][action] = reward
      else:
        a = self.model.predict(next_state)[0]
        t = self.target_model.predict(next_state)[0]
        target[0][action] = reward + self.gamma * t[np.argmax(a)]
      self.model.fit(state, target, epochs=1, verbose=0)
    if self.epsilon > self.epsilon_min:
      self.epsilon *= self.epsilon_decay

  def load(self, name):
    self.model.load_weights(name)

  def save(self, name):
    self.model.save_weights(name)


if __name__ == "__main__":
  env = trainer.new();
  state_size = len(env.observation_space())
  print(env.observation_space())
  action_size = len(env.actions)
  agent = DQNAgent(state_size, action_size)
  agent.load("./save/tsp_model.h5")
  done = False
  batch_size = 64

  for e in range(EPISODES):
    state = env.new_game()
    state = np.reshape(state, [1, state_size])
    reward_avg = 0.0
    for time in range(500):
      # env.render()
      action = agent.act(state)
      next_state, reward, done = env.step(action)
      reward_avg += reward
      next_state = np.reshape(next_state, [1, state_size])
      # print("reward: {}".format(reward))

      agent.remember(state, action, reward, next_state, done)
      state = next_state
      if done:
        agent.update_target_model()
        print("episode: {}/{}, score: {:.2}, time:{} e: {:.2}"
              .format(e, EPISODES, reward, time, agent.epsilon))

        break
    if len(agent.memory) > batch_size:
       agent.replay(batch_size)
    if e > 100 and e % 1000 == 0:
       print('Save model')
       agent.save("./save/tsp_model.h5")
