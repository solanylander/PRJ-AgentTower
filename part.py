import math, random, sys, pygame
from pygame.locals import *

# Individual Ant part (leg, torso, head)
class Part:

	# Rotate image (Only works for square images)
	def rotImage(self, image, angle):
	    rect = image.get_rect()
	    rotatedImage = pygame.transform.rotate(image, angle)
	    rect.center = rotatedImage.get_rect().center
	    rotatedImage = rotatedImage.subsurface(rect).copy()
	    return rotatedImage

	# Initialise a body part with a rotation, position and if it is the main piece (back body segment)
	def __init__(self, rotate, x, y, main):
		self.rotate = rotate
		self.position = (x, y)
		self.main = main
		self.sensorLoad = []

	# Load an body parts image and save it
	def loadImage(self, image):
		# Image unrotated. Saves the program having to repeated call the file the image is saved in
		self.imageLoad = pygame.image.load(image).convert_alpha()

		# Rotate the image and take its mask (Used to calculate collisions)
		self.image = self.rotImage(self.imageLoad, self.rotate)
		self.mask = pygame.mask.from_surface(self.image)

	# Load an body parts sensors
	def loadSensors(self, sensors):
		self.sensorLoad = []
		self.sensors = []
		self.sensorsMask = []
		for i in range(len(sensors)):
			self.sensorLoad.append(pygame.image.load(sensors[i]).convert_alpha())
			self.sensors.append(self.rotImage(self.sensorLoad[i], self.rotate))
			self.sensorsMask.append(pygame.mask.from_surface(self.sensors[i]))

	# Set parts position
	def setPosition(self, xy):
		self.position = xy

	# Get parts position
	def getPosition(self):
		return self.position

	# Set parts constraint
	def setConstraint(self, constraint):
		self.constraint = constraint

	# Get parts constraint 
	def getConstraint(self):
		return self.constraint

	# Set parts weight
	def setWeight(self, weight):
		self.weight = weight

	# Get parts weight 
	def getWeight(self):
		return self.weight

	# Rotate the body part by the value of amount with consideration to the body parts constraints
	def rotation(self, amount):
		# When the back part is rotated it needs a pivot so the connecting point to the front torso is used
		distance = (0,0)
		if self.main and amount != 0:
			# Find the distance between where the back part is and where it should be after rotating
			distance = (math.cos(self.rotate / 180 * math.pi) * 39.0, math.sin((self.rotate / 180 * math.pi)) * 39.0)
			distanceTwo = (math.cos((self.rotate + amount) / 180 * math.pi) * 39.0, math.sin(((self.rotate + amount) / 180 * math.pi)) * 39.0)
			distance = (distance[0] - distanceTwo[0], distanceTwo[1] - distance[1])

		l, u, r = self.constraint[0], self.constraint[1], self.rotate
		r = (r + amount) % 360.0

		# Handles angles so that the angles loop between 360 and 0
		one, two, three, four = abs(l - r), abs(u - r), abs(abs(l - r) - 360), abs(abs(u - r) - 360)
		if one > three:
			one = three
		if two > four:
			two = four

		# If the angle is now outside of the bounds lock it to the constraints
		if l > u and (r < l and r > u):
			if one > two:
				r = u
			else:
				r = l
			distance = (0.0, 0.0)
		elif l < u and (r < l or r > u):
			if one > two:
				r = u
			else:
				r = l
			distance = (0.0, 0.0)

		# Rotate the and get the image mask
		self.rotate = r;
		self.image = self.rotImage(self.imageLoad, self.rotate)
		self.mask = pygame.mask.from_surface(self.image)
		self.sensors = []
		self.sensorsMask = []
		# Rotate sensors
		for i in range(len(self.sensorLoad)):
			self.sensors.append(self.rotImage(self.sensorLoad[i], self.rotate))
			self.sensorsMask.append(pygame.mask.from_surface(self.sensors[i]))
		return distance

	# Set the parts rotation to a specific value. Used in the parts initialisation
	def setRotation(self, rotation):
		self.rotate = rotation

	# Get the parts rotation
	def getRotation(self):
		return self.rotate

	# Get the parts image rotated
	def getImage(self):
		return self.image

	# Get the parts mask
	def getMask(self):
		return self.mask

	# Get the sensor images
	def getSensors(self):
		return self.sensors

	# Get the sensor masks
	def getSensorMasks(self):
		return self.sensorsMask
