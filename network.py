import gym, random, os, tflearn
import tensorflow as tf
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
LR = 1e-3

class Network:
	def __init__(self):
		self.trainingData = []
		self.scores = []
		self.acceptedScores = []
		self.gameMemory = []
		self.prevObs = []


	def initialPopulation(self, observation):
		observation = np.array(observation)
		action = random.randrange(0,30)
		self.gameMemory.append([observation, action])
		return action


	def nextGame(self, score):
		if score > 0:
			self.acceptedScores.append(self.scores)
		for data in self.gameMemory:
			output = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			output[data[1]] = 1
			self.trainingData.append([data[0], output])
		self.scores.append(score)
		self.gameMemory = []
		self.prevObs = []

	def afterInitial(self):
		trainingDataSave = np.array(self.trainingData)
		np.save('saved.npy', trainingDataSave)
		self.choices = []
		self.scores = []


	def neuralNetworkModel(self, input_size):
		network = input_data(shape=[None, input_size, 1], name='input')

		network = fully_connected(network, 128, activation='relu')
		network = dropout(network, 0.8)


		network = fully_connected(network, 256, activation='relu')
		network = dropout(network, 0.8)


		network = fully_connected(network, 512, activation='relu')
		network = dropout(network, 0.8)


		network = fully_connected(network, 256, activation='relu')
		network = dropout(network, 0.8)


		network = fully_connected(network, 128, activation='relu')
		network = dropout(network, 0.8)

		network = fully_connected(network, 30, activation='softmax')
		network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

		model = tflearn.DNN(network, tensorboard_dir='log')
		return model

	def trainModel(self):
		X = np.array([i[0] for i in self.trainingData]).reshape(-1, len(self.trainingData[0][0]), 1)
		y = [i[1] for i in self.trainingData]

		self.model = self.neuralNetworkModel(input_size = len(X[0]))

		self.model.fit({'input':X}, {'targets':y}, n_epoch=3, snapshot_step=500, show_metric=True, run_id='openaistuff')

	def nextGameCompleted(self, score):
		self.scores.append(score)
		self.gameMemory = []

	def completed(self, observation):
		observation = np.array(observation)
		action = np.argmax(self.model.predict(observation.reshape(-1, len(observation), 1))[0])
		self.choices.append(action)
		self.gameMemory.append([observation, action])
		return action
