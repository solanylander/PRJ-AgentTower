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

		# Body parts and heads weight
		parts[0].setWeight(11.72)
		parts[1].setWeight(11.72)
		parts[2].setWeight(8.24)

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
			# Set the weight of each leg part
			parts[i].setWeight(0.66)
			parts[i + 3].setWeight(0.66)

		# Initialise the backup storage for the parts information with 0 values
		for j in range(0,9):
			backup.append(part(0, 0, 0))
			self.colliding.append(False)

		# Backup objects that can be used to revert object overlaps and handle collisions
		self.objects = []


	# Handles movement calculations
	def move(self, xy, movement, gravity):
		parts = self.parts
		colliding = self.colliding
		self.box = [(-1,-1), (-1,-1), (-1,-1), (-1,-1)]

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
		#gravity
		if gravity:
			pivot = (pivot[0], pivot[1] + 1.0)
			self.stored(True)
			self.setPositions(pivot)
			if self.collide():
				self.stored(False)
				pivot = (pivot[0], pivot[1] - 1.0)

		for q in range(6,9):
			if colliding[q]:
				p = q - 3
				if movement[q] != 0:
					angle = (math.sin((parts[q].getRotation()) / 180 * math.pi)), -math.cos((180.0 + parts[q].getRotation()) / 180 * math.pi)
					angle = (angle[0] * 12, angle[1] * 12)

					newAngle = (-math.sin((parts[q].getRotation() + movement[q]) / 180 * math.pi)), math.cos((180.0 + parts[q].getRotation() + movement[q]) / 180 * math.pi)
					
					newAngle = (newAngle[0] * 12 + angle[0], newAngle[1] * 12 + angle[1] - 0.05)
					pivot = (pivot[0] + newAngle[0], pivot[1] + newAngle[1])


					self.stored(True)
					parts[q].setRotation(parts[q].getRotation() + movement[q])
					self.setPositions(pivot)
					if self.collide() and newAngle[1] > 0:
						self.stored(False)
				if movement[p] != 0:
					angle = (math.sin((parts[p].getRotation()) / 180 * math.pi)), -math.cos((180.0 + parts[p].getRotation()) / 180 * math.pi)
					angle = (angle[0] * 12, angle[1] * 12)

					newAngle = (-math.sin((parts[p].getRotation() + movement[p]) / 180 * math.pi)), math.cos((180.0 + parts[p].getRotation() + movement[p]) / 180 * math.pi)
					
					newAngle = (newAngle[0] * 12 + angle[0], newAngle[1] * 12 + angle[1] - 0.05)
					pivot = (pivot[0] + newAngle[0], pivot[1] + newAngle[1])


					self.stored(True)
					parts[p].setRotation(parts[p].getRotation() + movement[p])
					self.setPositions(pivot)
					if self.collide() and newAngle[1] > 0:
						self.stored(False)


		self.centerOfGravity()

		if self.box[0][0] != -1 and self.box[0][0] > self.cog[0]:
			d = (self.box[0][0] - self.cog[0], self.box[0][1] - self.cog[1])

			distance = math.sqrt(d[0] * d[0] + d[1] * d[1])

			angle = (math.sin((parts[0].getRotation()) / 180 * math.pi)), -math.cos((180.0 + parts[0].getRotation()) / 180 * math.pi)
			angle = (angle[0] * distance, angle[1] * distance)

			newAngle = (-math.sin((parts[0].getRotation() + 1) / 180 * math.pi)), math.cos((180.0 + parts[0].getRotation() + 1) / 180 * math.pi)
			
			newAngle = (newAngle[0] * distance + angle[0], newAngle[1] * distance + angle[1] - 1)
			pivot = (pivot[0] + newAngle[0], pivot[1] + newAngle[1])

			self.stored(True)
			self.setPositions(pivot)
			self.rotateAll(True)
			if self.collide():
				self.stored(False)

		elif self.box[1][0] != -1 and self.box[1][0] < self.cog[0]:
			d = (self.box[1][0] - (parts[0].getPosition()[0] + 50), self.box[1][1] - (parts[0].getPosition()[1] + 50))
			nm = (self.cog[0] - self.box[1][0]) / 25
			print(nm)
			currentAngle = None
			if(d[0] == 0):
				currentAngle = 90
			else:
				currentAngle = math.atan(d[1]/d[0]) * 180.0 / math.pi
			distance = math.sqrt(d[0] * d[0] + d[1] * d[1])
			newAngle = (math.cos((180.0 + currentAngle + nm) / 180 * math.pi), -math.sin((currentAngle + nm) / 180 * math.pi))
			newAngle = (-abs(newAngle[0] * distance), -abs(newAngle[1] * distance))
			if(d[0] < 0):	
				newAngle = (d[0] - newAngle[0], newAngle[1])
			else:
				newAngle = (d[0] + newAngle[0], newAngle[1])
			if(d[1] < 0):
				newAngle = (newAngle[0], newAngle[1] - d[1])
			else:
				newAngle = (newAngle[0], newAngle[1] + d[1])
			self.stored(True)

			passed = False
			for f in range(0,5):
				for g in range(0,5):
					newPivot = (pivot[0] + newAngle[0] + (0.3 * f), pivot[1] + newAngle[1] - (0.8 * g))
					self.setPositions(newPivot)
					self.rotateAll(-nm)
					if self.collide():
						self.stored(False)
					else:
						passed = True
						break
				if passed:
					break



	def gravity(self):
		print("gravity")

	# Calculate the agents center of gravity
	def centerOfGravity(self):
		parts = self.parts
		self.cog = (0,0)
		centers = []
		weight = 0
		# Agents co-ordinate
		pos = parts[0].getPosition()
		# Convert each parts current angle to a 2D vector
		partRotations = []
		for q in range(0,9):
			if q < 3:
				partRotations.append((math.cos(parts[q].getRotation() / 180 * math.pi), math.sin((180.0 + parts[q].getRotation()) / 180 * math.pi)))
			else:
				partRotations.append((math.cos((parts[q].getRotation() - 90) / 180 * math.pi), math.sin((180.0 + (parts[q].getRotation() - 90)) / 180 * math.pi)))

		# Find the center points of each part
		# Calculated by finding the connecting part to the body which is the center point (find top left of image then add half the image width)
		# then calculate the parts rotation and multiply it by the number of pixels away the center of the part is from the images center
		centers.append((pos[0] + (partRotations[0][0] * 17.0) + 50, pos[1] + (partRotations[0][1] * 17.0) + 50))
		centers.append((pos[0] + (partRotations[0][0] * 39.0) + (partRotations[1][0] * 17.0) + 50, pos[1] + (partRotations[0][1] * 39.0) + (partRotations[1][1] * 17.0) + 50))
		centers.append((pos[0] + (partRotations[0][0] * 39.0) + (partRotations[1][0] * 39.0) + (partRotations[2][0] * 9.0) + 50, pos[1] + (partRotations[0][1] * 39.0) + (partRotations[1][1] * 39.0) + (partRotations[2][1] * 9.0) + 50))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 12) + (partRotations[3][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 12) + (partRotations[3][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[4][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[4][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 25.0) + (partRotations[5][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 25.0) + (partRotations[5][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 12) + (partRotations[3][0] * 12) + (partRotations[6][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 12) + (partRotations[3][1] * 12) + (partRotations[6][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[4][0] * 12) + (partRotations[7][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[4][1] * 12) + (partRotations[7][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 25.0) + (partRotations[5][0] * 12) + (partRotations[8][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 25.0) + (partRotations[5][1] * 12) + (partRotations[8][1] * 5) + 13))
		
		# Add all parts center of gravity multiplied by there specific weight
		for i in range(0,9):
			self.cog = (self.cog[0] + (centers[i][0] * parts[i].getWeight()), self.cog[1] + (centers[i][1] * parts[i].getWeight()))
			weight += parts[i].getWeight()
		# Divide by the total weight of the agent
		self.cog = (self.cog[0] / weight, self.cog[1] / weight)

	# If setup store a copy of the agent otherwise replace the current agents details with the stored copy
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
			if not setup:
				one[k].rotation(0)

	# Rotate entire agent
	def rotateAll(self, amount):
		for iterate in range(0,9):
			self.parts[iterate].rotation(amount)
	
	# Set the constraints of each part
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

	# Sets all the parts positions with regards to the agents pivot
	def setPositions(self, pivot):
		parts = self.parts
		# Rotation of the agents abdominal segments
		backRotation = (math.cos(parts[0].getRotation() / 180 * math.pi), math.sin((180.0 + parts[0].getRotation()) / 180 * math.pi))
		frontRotation = (math.cos(parts[1].getRotation() / 180 * math.pi), math.sin((180.0 + parts[1].getRotation()) / 180 * math.pi))
		# Back abdominal segment
		parts[0].setPosition(pivot)
		pos = parts[0].getPosition()
		# Front abdominal segment
		parts[1].setPosition((pos[0] + (backRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0)))
		# Head
		parts[2].setPosition((pos[0] + (backRotation[0] * 39.0) + (frontRotation[0] * 39.0), pos[1] + (backRotation[1] * 39.0) + (frontRotation[1] * 39.0)))
		# Back leg (top)
		parts[3].setPosition((pos[0] + 38 + (backRotation[0] * 12), pos[1] + 40 + (backRotation[1] * 12)))
		legRotation = (math.sin(parts[3].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[3].getRotation()) / 180 * math.pi))
		# Back leg (bottom)
		parts[6].setPosition((pos[0] + 38 + (backRotation[0] * 12) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 12) + (legRotation[1] * 11.5)))
		# Middle leg (top)
		parts[4].setPosition((pos[0] + 38 + (backRotation[0] * 39), pos[1] + 40 + (backRotation[1] * 39)))
		legRotation = (math.sin(parts[4].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[4].getRotation()) / 180 * math.pi))
		# Middle leg (bottom)
		parts[7].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 39) + (legRotation[1] * 11.5)))
		# Front leg (top)
		parts[5].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39) + (frontRotation[1] * 25.0)))
		# Front leg (bottom)
		legRotation = (math.sin(parts[5].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[5].getRotation()) / 180 * math.pi))
		parts[8].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5) + (frontRotation[0] * 25.0), pos[1] + 40 + (backRotation[1] * 39)  + (legRotation[1] * 11.5)+ (frontRotation[1] * 25.0)))

	# Handles Collisions between the ant and the world
	def collide(self):
		parts = self.parts
		colliding = self.colliding
		ret = False
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
							ret = True

			# Check collisions against all the other objects in the world which exclude itself
			for k in range(len(self.objects)):
				offset = (int(self.objects[k][1] - parts[position].getPosition()[0]), int(self.objects[k][2] - parts[position].getPosition()[1]))
				result =  self.parts[position].getMask().overlap(self.objects[k][0], offset)
				if result:
					self.collisionBox((self.parts[position].getPosition()[0] + result[0], self.parts[position].getPosition()[1] + result[1]))
					colliding[position] = True
					ret = True
		return ret


	# Creates a parallelogram around the agent with the corners being the collision points with the highest and lowest x and y values
	# used for calculating gravity and if the agents center of gravity is over an edge (in which case it will fall)
	def collisionBox(self, point):
		# Lowest x value
		if self.box[0][0] == -1 or point[0] < self.box[0][0]:
			self.box[0] = point
		# Highest x value
		if self.box[1][0] == -1 or (point[0] > self.box[1][0] and self.box[1][0] != -1):
			self.box[1] = point
		# Lowest y value
		if self.box[2][1] == -1 or point[1] < self.box[2][1]:
			self.box[2] = point
		# Highest y value
		if self.box[3][1] == -1 or (point[1] > self.box[3][1] and self.box[3][1] != -1):
			self.box[3] = point

	# Add an object in the environment so the ant is aware of the world
	def addObject(self, obj):
		self.objects.append(obj)

	# Draw all the images
	def run(self, DS):
		for i in range(0,9):
			DS.blit(self.parts[i].getImage(), self.parts[i].getPosition())

	# Return an array of all the individual ant parts
	def getParts(self):
		return self.parts

	def getCog(self):
		return self.cog

	def getMarkers(self):
		return [self.box[1]]
