# -*- coding: utf-8 -*-
import numpy as np
import random
import trainer
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding, Reshape
from keras.optimizers import Adam
from collections import deque
from keras import backend as K

EPISODES = 5000


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
    model.add(Dense(32, input_dim=self.state_size, activation='relu'))
    # model.add(LSTM(24))
    # model.add(Embedding(200, 128))
    model.add(Reshape((4, 8), input_shape=(32,0)))
    model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    # model.add(Dense(12, activation='relu'))
    # model.add(Dense(8, activation='relu'))
    # model.add(Dense(4, activation='relu'))
    # model.add(Dense(16, activation='relu'))
    model.add(Dense(self.action_size, activation='linear'))
    model.compile(loss=self._huber_loss,
            optimizer=Adam(lr=self.learning_rate))
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
  # env = t('CartPole-v1')
  env = trainer.new();
  # state_size = env.observation_space.shape[0]
  # action_size = env.action_space.n
  # agent = DQNAgent(state_size, action_size)
  state_size = len(env.observation_space())
  action_size = len(env.actions)
  agent = DQNAgent(state_size, action_size)
  agent.load("./save/tsp_model.h5")
  done = False
  batch_size = 64

  reward_avg = 0.0
  rewards = []
  for e in range(EPISODES):
    state = env.new_game()
    state = np.reshape(state, [1, state_size])
    for time in range(500):
      # env.render()
      action = agent.act(state)
      next_state, reward, done = env.step(action)
      next_state = np.reshape(next_state, [1, state_size])
      agent.remember(state, action, reward, next_state, done)
      state = next_state
      if done:
        agent.update_target_model()
        rewards.append(reward)
        if len(rewards) > 10:
          rewards.pop(0)
        reward_avg = np.average(rewards)

        print("episode: {}/{}, score: {:.2}, time:{} e: {:.2}"
              .format(e, EPISODES, reward_avg, time, agent.epsilon))
        break
    if len(agent.memory) > batch_size:
      agent.replay(batch_size)
    if e % 100 == 0:
      agent.save("./save/tsp_model.h5")
