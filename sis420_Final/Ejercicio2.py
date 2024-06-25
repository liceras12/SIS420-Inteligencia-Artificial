import numpy as np
import random
from tqdm import tqdm
import pandas as pd
import pickle

class PuzzleBoard:
    def __init__(self):
        self.state = np.arange(1, 10).reshape((3, 3))
        self.state[-1, -1] = 0  # El espacio vacío
        self.goal_state = self.state.copy()

    #devuelve las posiciones validas, desde la posicion vacia
    def valid_moves(self):
        empty_pos = tuple(zip(*np.where(self.state == 0)))[0]
        moves = []
        #movimientos válidos, hacia arriba, abajo, izquierda, derecha
        if empty_pos[0] > 0:
            moves.append((empty_pos[0] - 1, empty_pos[1]))
        if empty_pos[0] < 2:
            moves.append((empty_pos[0] + 1, empty_pos[1]))
        if empty_pos[1] > 0:
            moves.append((empty_pos[0], empty_pos[1] - 1))
        if empty_pos[1] < 2:
            moves.append((empty_pos[0], empty_pos[1] + 1))
        return moves
    
    #actualiza el tablero con el movimiento
    def update(self, move):
        empty_pos = tuple(zip(*np.where(self.state == 0)))[0]
        new_pos = move
        # intercambia el espacio vacio con la nueva posicion
        self.state[empty_pos], self.state[new_pos] = self.state[new_pos], self.state[empty_pos]

    #verifica si el juego a terminado, comparando el estado actual con el objetivo
    def is_game_over(self):
        return np.array_equal(self.state, self.goal_state)

    # Reinicia el tablero mezclando las posiciones y devuelve el estado inicial
    def reset(self):
        self.state = self.goal_state.copy()
        flat_state = self.state.flatten()
        np.random.shuffle(flat_state)
        self.state = flat_state.reshape((3, 3))
        return self.state
#Maneja el juego y la interacción con el agente
class PuzzleGame:
    def __init__(self, player1):
        self.player = player1
        self.board = PuzzleBoard()

    #Para que el agente juegue contra sí mismo durante un número de rondas
    def selfplay(self, rounds=10):
        for _ in tqdm(range(rounds)):
            self.board.reset()
            self.player.reset()
            game_over = False
            while not game_over:
                move = self.player.move(self.board) # el agente decide un movimiento
                self.board.update(move) #actualiza el tablero
                self.player.update(self.board) # actualiza el boatd
                if self.board.is_game_over():
                    game_over = True
            #da la recompensa
            self.reward()
        
    def reward(self):
        if self.board.is_game_over():
            self.player.reward(1)
#implementa el agente de aprendizaje por refuerzo Q-Learning
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.value_function = {}  # Q-table
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for exploration
        self.positions = []  # Stores the states during an episode

    def reset(self):
        self.positions = []

    def move(self, board):
        state = self.get_state(board)
        valid_moves = board.valid_moves()
        if random.uniform(0, 1) < self.epsilon:  # Exploration
            return random.choice(valid_moves)
        else:  # Exploitation
            q_values = [self.value_function.get((state, move), 0) for move in valid_moves]
            max_value = max(q_values)
            return random.choice([move for move, value in zip(valid_moves, q_values) if value == max_value])

    def get_state(self, board):
        return tuple(map(tuple, board.state))

    def update(self, board):
        self.positions.append(self.get_state(board))

    def reward(self, reward):
        self.epsilon *= self.epsilon_decay
        for state in reversed(self.positions):
            if state not in self.value_function:
                self.value_function[state] = 0
            self.value_function[state] += self.alpha * (reward - self.value_function[state])
            reward = self.value_function[state]

if __name__ == "__main__":
    agent = QLearningAgent()
    game = PuzzleGame(agent)
    game.selfplay(10)  # Entrenar al agente con 10,000 episodios

    # Guardar la tabla Q en un archivo
    with open('agente_puzzle.pickle', 'wb') as handle:
        pickle.dump(agent.value_function, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Mostrar las primeras 10 entradas de la tabla Q
    funcion_de_valor = sorted(agent.value_function.items(), key=lambda kv: kv[1], reverse=True)
    tabla = pd.DataFrame({'estado': [x[0] for x in funcion_de_valor], 'valor': [x[1] for x in funcion_de_valor]})
    print(tabla.head(10))
