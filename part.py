import math, random, sys, pygame
from pygame.locals import *

# Individual Ant part (leg, torso, head)
class part:

	# Rotate image (Only works for square images)
	def rot_image(self, image, angle):
	    rect = image.get_rect()
	    rot_image = pygame.transform.rotate(image, angle)
	    rect.center = rot_image.get_rect().center
	    rot_image = rot_image.subsurface(rect).copy()
	    return rot_image

	# Initialise a body part with a rotation and its position
	def __init__(self, rotate, x, y):
		self.rotate = rotate
		self.position = (x, y)

	# Load an body parts image and save it
	def loadImage(self, image):
		# Image unrotated. Saves the program having to repeated call the file the image is saved in
		self.imageload = pygame.image.load(image).convert_alpha()

		# Rotate the image and take its mask (Used to calculate collisions)
		self.image = self.rot_image(self.imageload, self.rotate)
		self.mask = pygame.mask.from_surface(self.image)

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

	# Set parts constraint
	def setWeight(self, weight):
		self.weight = weight

	# Get parts weight 
	def getWeight(self):
		return self.weight

	# Rotate the body part by the value of amount with consideration to the body parts constraints
	def rotation(self, amount):
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

		if l < u and (r < l or r > u):
			if one > two:
				r = u
			else:
				r = l

		# Rotate the and get the image mask
		self.rotate = r;
		self.image = self.rot_image(self.imageload, self.rotate)
		self.mask = pygame.mask.from_surface(self.image)

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
