import math, random, sys, pygame
from pygame.locals import *

# Individual Ant part (leg, torso, head)
class block:

	# Rotate image (Only works for square images)
	def rot_image(self, image, angle):
	    rect = image.get_rect()
	    rot_image = pygame.transform.rotate(image, angle)
	    rect.center = rot_image.get_rect().center
	    rot_image = rot_image.subsurface(rect).copy()
	    return rot_image

	# Initialise a body part with a rotation, position and if it is the main piece (back body segment)
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

	# Get parts position
	def getPosition(self):
		return self.position

	# Rotate the body part by the value of amount with consideration to the body parts constraints
	def rotation(self, amount):
		# Rotate the and get the image mask
		self.rotate = r;
		self.image = self.rot_image(self.imageload, self.rotate)
		self.mask = pygame.mask.from_surface(self.image)

	# Get the parts rotation
	def getRotation(self):
		return self.rotate

	# Get the parts image rotated
	def getImage(self):
		return self.image

	# Get the parts mask
	def getMask(self):
		return self.mask
