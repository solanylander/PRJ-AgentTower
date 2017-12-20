import math, random, sys, pygame
from pygame.locals import *
from part import part

class ant:

	def __init__(self):
		self.parts = []
		self.backup = []
		self.colliding = []
		parts = self.parts
		backup = self.backup
		self.locked = [0,0,0,0,0,0,0,0,0]
		# add the head and body parts
		parts.append(part(0, 100, 0))
		parts.append(part(0, 0, 0))
		parts.append(part(0, 0, 0))
		# Load the image files
		parts[0].loadImage("image_resources/body.png")
		parts[1].loadImage("image_resources/body.png")
		parts[2].loadImage("image_resources/head.png")
		# Set the constraints of the body parts so that the agents cannot fold in on themselves
		parts[0].setConstraint((0, 360))
		parts[1].setConstraint(((parts[0].getRotation() - 90) % 360, (parts[0].getRotation() + 90) % 360))
		parts[2].setConstraint(((parts[1].getRotation() - 90) % 360, (parts[1].getRotation() + 90) % 360))

		# Add the leg parts
		parts.append(part(310, 0, 0))
		parts.append(part(50, 0, 0))
		parts.append(part(50, 0, 0))
		parts.append(part(0, 0, 0))
		parts.append(part(0, 0, 0))
		parts.append(part(0, 0, 0))
		for i in range(3,6):
			# Load the image files and set the constraints
			parts[i].loadImage("image_resources/leg.png")
			parts[i + 3].loadImage("image_resources/leg.png")
			parts[i].setConstraint((0, 360))
			parts[i + 3].setConstraint(((parts[i].getRotation() - 90) % 360, (parts[i].getRotation() + 90) % 360))

		for j in range(0,9):
			backup.append(part(0, 0, 0))
			self.colliding.append(False)

		# Backup objects that can be used to revert object overlaps and handle collisions
		self.objects = []

	# Return an array of all the individual ant parts
	def getParts(self):
		return self.parts

	# Handles movement calculations
	def move(self, xy, movement):
		parts = self.parts
		colliding = self.colliding
		for g in range(0,9):
			colliding[g] = False
		pos = parts[0].getPosition()
		pivot = (pos[0] + xy[0], pos[1] + xy[1])

		for iterate in range(0,9):
			self.setConstraints()

			self.stored(True)
			parts[iterate].rotation(movement[iterate])
			self.setPositions(pivot)

			if self.collide():
				self.stored(False)

		angle = (parts[6].getRotation() + movement[6] / 180 * math.pi * 12), -math.cos((180.0 + parts[6].getRotation() + movement[6]) / 180 * math.pi * 12)
		print(angle)
		point = (parts[6].getPosition()[0] + 12 + angle[0], parts[6].getPosition()[1] + 12 + angle[1])
		return point
		for k in range(6,9):
			if colliding[k]:
				print("colliding")
		#gravity
		#pivot = (pivot[0], pivot[1] + 1.0)
		#self.stored(True)
		#self.setPositions(pivot)
		#if self.collide():
		#	self.stored(False)

	def stored(self, setup):
		one = []
		two = []
		if setup:
			two = self.parts
			one = self.backup
		else:
			two = self.backup
			one = self.parts

		for k in range(0,9):
			one[k].setPosition(two[k].getPosition())
			one[k].setConstraint(two[k].getConstraint())
			one[k].setRotation(two[k].getRotation())
		
	def setConstraints(self):
		parts = self.parts
		parts[0].setConstraint((0, 360))
		parts[1].setConstraint(((parts[0].getRotation() - 90) % 360, (parts[0].getRotation() + 90) % 360))
		parts[2].setConstraint(((parts[1].getRotation() - 90) % 360, (parts[1].getRotation() + 90) % 360))
		parts[3].setConstraint((0, 360))
		parts[4].setConstraint((0, 360))
		parts[5].setConstraint((0, 360))
		parts[6].setConstraint(((parts[3].getRotation() - 90) % 360, (parts[3].getRotation() + 90) % 360))
		parts[7].setConstraint(((parts[4].getRotation() - 90) % 360, (parts[4].getRotation() + 90) % 360))
		parts[8].setConstraint(((parts[5].getRotation() - 90) % 360, (parts[5].getRotation() + 90) % 360))

	def setPositions(self, pivot):
		parts = self.parts
		backRotation = (math.cos(parts[0].getRotation() / 180 * math.pi), math.sin((180.0 + parts[0].getRotation()) / 180 * math.pi))
		frontRotation = (math.cos(parts[1].getRotation() / 180 * math.pi), math.sin((180.0 + parts[1].getRotation()) / 180 * math.pi))
		parts[0].setPosition(pivot)
		pos = parts[0].getPosition()
		parts[1].setPosition((pos[0] + (backRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0)))
		parts[2].setPosition((pos[0] + (backRotation[0] * 39.0) + (frontRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0) + (frontRotation[1] * 39.0)))
		parts[3].setPosition((pos[0] + 38 + (backRotation[0] * 12), pos[1] + 40 + (backRotation[1] * 12)))
		legRotation = (math.sin(parts[3].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[3].getRotation()) / 180 * math.pi))
		parts[6].setPosition((pos[0] + 38 + (backRotation[0] * 12) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 12) + (legRotation[1] * 11.5)))
		parts[4].setPosition((pos[0] + 38 + (backRotation[0] * 39), pos[1] + 40 + (backRotation[1] * 39)))
		legRotation = (math.sin(parts[4].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[4].getRotation()) / 180 * math.pi))
		parts[7].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 39) + (legRotation[1] * 11.5)))
		parts[5].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39) + (frontRotation[1] * 25.0)))
		legRotation = (math.sin(parts[5].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[5].getRotation()) / 180 * math.pi))
		parts[8].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39)  + (legRotation[1] * 11.5)+ (frontRotation[1] * 25.0)))
					
	def checkPositions(self, xy):
		parts = self.parts
		pos = parts[0].getPosition()
		backRotation = (math.cos(parts[0].getRotation() / 180 * math.pi), math.sin((180.0 + parts[0].getRotation()) / 180 * math.pi))
		frontRotation = (math.cos(parts[1].getRotation() / 180 * math.pi), math.sin((180.0 + parts[1].getRotation()) / 180 * math.pi))
		if (pos[0] + xy[0], pos[1] + xy[1]) != parts[0].getPosition():
			return False
		if (pos[0] + (backRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0)) != parts[1].getPosition():
			return False
		if (pos[0] + (backRotation[0] * 39.0) + (frontRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0) + (frontRotation[1] * 39.0)) != parts[2].getPosition():
			return False
		if (pos[0] + 38 + (backRotation[0] * 12), pos[1] + 40 + (backRotation[1] * 12)) != parts[3].getPosition():
			return False
		legRotation = (math.sin(parts[3].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[3].getRotation()) / 180 * math.pi))
		if (pos[0] + 38 + (backRotation[0] * 12) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 12) + (legRotation[1] * 11.5)) != parts[6].getPosition():
			return False
		if (pos[0] + 38 + (backRotation[0] * 39), pos[1] + 40 + (backRotation[1] * 39)) != parts[4].getPosition():
			return False
		legRotation = (math.sin(parts[4].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[4].getRotation()) / 180 * math.pi))
		if (pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 39) + (legRotation[1] * 11.5)) != parts[7].getPosition():
			return False
		if (pos[0] + 38 + (backRotation[0] * 39) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39) + (frontRotation[1] * 25.0)) != parts[5].getPosition():
			return False
		legRotation = (math.sin(parts[5].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[5].getRotation()) / 180 * math.pi))
		if (pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39)  + (legRotation[1] * 11.5)+ (frontRotation[1] * 25.0)) != parts[8].getPosition():
			return False
		return True

	# Handles Collisions between the ant and the world
	def collide(self):
		parts = self.parts
		colliding = self.colliding
		# For legs check if they are colliding with other legs from the same ant. Body parts are behind the legs so they can overlap
		# But an agent cannot cross its legs
		for position in range(0,9):
			if position > 2:
				for j in range(3,9):
					# Dont check collisions when the 2 parts are from the same leg. E.g "Thigh" and "Calf"
					if (position % 3) != (j % 3):			
						offset = (int(self.parts[position].getPosition()[0] - self.parts[j].getPosition()[0]), int(self.parts[position].getPosition()[1] - self.parts[j].getPosition()[1]))
						result = self.parts[j].getMask().overlap(self.parts[position].getMask(), offset)
						# If they collide return true
						if result:
							colliding[position] = True
							return True

			# Check collisions against all the other objects in the world which exclude itself
			for k in range(len(self.objects)):
				offset = (int(self.objects[k][1] - parts[position].getPosition()[0]), int(self.objects[k][2] - parts[position].getPosition()[1]))
				result =  self.parts[position].getMask().overlap(self.objects[k][0], offset)
				if result:
					colliding[position] = True
					return True

		return False

	def addObject(self, obj):
		self.objects.append(obj)

	def run(self, DS):
		for i in range(0,9):
			DS.blit(self.parts[i].getImage(), self.parts[i].getPosition())