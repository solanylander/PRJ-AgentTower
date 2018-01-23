import  numpy as np
import matplotlib.pyplot as plt

X = np.array([[0,0,1],
				[0,1,1],
				[1,0,1],
				[1,1,1]]) # (4,3)

y = np.array([[0,0,1,1]]).T # (4,1)

# plt.matshow(np.hstack((X,y)), fignum = 10, cmap = plt.cm.gray)
# plt.show()

# sigmoid
def nonlin(x, deriv = False):
	if deriv == True:
		return x * (1 - x)
	return 1 / (1 + np.exp(-x))

Xaxis = np.arange(-5, 5, 0.2)

# plt.plot(Xaxis, nonlin(Xaxis))
# plt.show()

np.random.seed(1)

# initialise weight
syn0 = 2 * np.random.random((3,4)) - 1
syn1 = 2 * np.random.random((4,1)) - 1
print(X)
print(syn0)
print(np.dot(X, syn0))
for iter in range(60000):

	# forward propagation
	l0 = X
	l1 = nonlin(np.dot(l0, syn0))
	l2 = nonlin(np.dot(l1, syn1))

	# how bad did we do?
	l2_error = y - l2

	if (iter % 10000) == 0:
		print("Error: ", str(np.mean(np.abs(l2_error))))

	# multiply how much we missed by slope of the sigmoid (nonlin function)
	l2_delta = l2_error * nonlin(l2, True)

	# how much did each l1 value contribute to the l2 error (according to weights)
	l1_error = l2_delta.dot(syn1.T)
	l1_delta = l1_error * nonlin(l1, True)

	# update weights
	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)


print("output: ")
print(l2)