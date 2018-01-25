import torch
import numpy as np
from torch import autograd, nn, optim
import torch.nn.functional as F

input_size = 172
hidden_size = 100
num_classes = 30

def sigmoid(x):
	output = 1 / (1 + np.exp(-x))
	return output

def sigmoidOutputToDerivative(output):
		return output*(1-output)

class Network:
	# N is batch size; D_in is input dimension;
	# H is hidden dimension; D_out is output dimension.
	def __init__(self):
		#np.random.seed(1)
		self.W1 = 2 * np.random.random((input_size, hidden_size)) - 1
		self.W2 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W3 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W4 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W5 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W6 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W7 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W8 = 2 * np.random.random((hidden_size, hidden_size)) - 1
		self.W9 = 2 * np.random.random((hidden_size, num_classes)) - 1

	def input(self, values):
		inputs = np.array(values)
		middle = sigmoid(np.dot(inputs, self.W1))
		middle = sigmoid(np.dot(middle, self.W2))
		middle = sigmoid(np.dot(middle, self.W3))
		middle = sigmoid(np.dot(middle, self.W4))
		middle = sigmoid(np.dot(middle, self.W5))
		middle = sigmoid(np.dot(middle, self.W6))
		middle = sigmoid(np.dot(middle, self.W7))
		middle = sigmoid(np.dot(middle, self.W8))
		output = sigmoid(np.dot(middle, self.W9))
		print(output)
		return np.argmax(output)

	def update(self, gradiant):
		layer10Delta = gradiant * sigmoidOutputToDerivative(layer10)
		layer9Error = layer10Delta.dot(self.W9.T)
		layer9Delta = layer9Error * sigmoidOutputToDerivative(layer9)

		self.W9 -= layer9.T.dot(layer10Delta)
		self.W8 -= layer8.T.dot(layer9Delta)