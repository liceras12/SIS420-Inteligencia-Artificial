import gym
from gym import spaces
import numpy as np
import random

# Definición del entorno personalizado
class PuzzleEnv(gym.Env):
    def __init__(self):
        super(PuzzleEnv, self).__init__()
        self.rows = 3
        self.cols = 3
        self.goal_state = np.arange(1, self.rows * self.cols + 1).reshape((self.rows, self.cols))
        self.goal_state[-1, -1] = 0  # Espacio vacío representado por 0

        self.action_space = spaces.Discrete(4)  # 4 acciones: 0=arriba, 1=abajo, 2=izquierda, 3=derecha
        self.observation_space = spaces.Box(0, self.rows * self.cols, shape=(self.rows, self.cols), dtype=int)
        self.reset()

    def reset(self):
        self.state = self.goal_state.copy()
        flat_state = self.state.flatten()
        np.random.shuffle(flat_state)
        self.state = flat_state.reshape((self.rows, self.cols))
        self.empty_pos = tuple(zip(*np.where(self.state == 0)))[0]
        return self.state

    def step(self, action):
        new_empty_pos = list(self.empty_pos)

        if action == 0:  # arriba
            new_empty_pos[0] -= 1
        elif action == 1:  # abajo
            new_empty_pos[0] += 1
        elif action == 2:  # izquierda
            new_empty_pos[1] -= 1
        elif action == 3:  # derecha
            new_empty_pos[1] += 1

        if (0 <= new_empty_pos[0] < self.rows and 0 <= new_empty_pos[1] < self.cols):
            self.state[self.empty_pos], self.state[tuple(new_empty_pos)] = self.state[tuple(new_empty_pos)], self.state[self.empty_pos]
            self.empty_pos = tuple(new_empty_pos)

        done = np.array_equal(self.state, self.goal_state)
        reward = 1 if done else -0.1
        return self.state, reward, done, {}

    def render(self, mode='human'):
        print(self.state)

# Implementación del agente Q-learning
class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.env = env
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_state(self, state):
        return tuple(map(tuple, state))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return self.env.action_space.sample()
        else:
            state = self.get_state(state)
            if state not in self.q_table:
                return self.env.action_space.sample()
            return max(self.q_table[state], key=self.q_table[state].get)

    def learn(self, state, action, reward, next_state):
        state = self.get_state(state)
        next_state = self.get_state(next_state)

        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.env.action_space.n)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.env.action_space.n)

        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def update_exploration_rate(self):
        self.exploration_rate *= self.exploration_decay

# Entrenamiento del agente
def train_agent(episodes=100):
    env = PuzzleEnv()
    agent = QLearningAgent(env)

    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
        agent.update_exploration_rate()

        if episode % 10 == 0:
            print(f'Episode {episode}, Exploration Rate: {agent.exploration_rate}')

    return agent, env

# Evaluación del agente
def evaluate_agent(agent, env):
    state = env.reset()
    env.render()
    done = False
    while not done:
        action = agent.choose_action(state)
        state, reward, done, _ = env.step(action)
        env.render()

if __name__ == "__main__":
    agent, env = train_agent()
    evaluate_agent(agent, env)
