import torch
import numpy as np
from torch.autograd import Variable

dtype = torch.FloatTensor
# dtype = torch.cuda.FloatTensor # Uncomment this to run on GPU

class Network(nn.Module):
	# N is batch size; D_in is input dimension;
	# H is hidden dimension; D_out is output dimension.

	def __init__(self):
        super().__init__()
        self.h1 = nn.Linear(input_size, hidden_size)
        self.h2 = nn.Linear(hidden_size, num_classes)

	def input(self, values):
		inputs = autograd.Variable(torch.from_numpy(np.array(values)))