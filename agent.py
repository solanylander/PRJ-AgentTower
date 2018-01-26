import math, random, sys, pygame
from pygame.locals import *
from part import Part
from network import Network

class Agent:

	def __init__(self, xy):
		self.sensors = []
		self.colliding = []
		self.network = Network()
		self.locked = [0,0,0,0,0,0,0,0,0]
		self.cog = (0,0)
		self.counter = 0
		self.xy = xy
		self.reset(False, 0, True)

		# Initialise the backup storage for the parts information with 0 values
		self.backup = []
		for k in range(0,15):
			self.backup.append(Part(0, 0, 0, False))
			self.colliding.append(False)

		# Backup objects that can be used to revert object overlaps and handle collisions
		self.objects = []

	# Reset agent
	def reset(self, stage, score, init):
		parts = []
		# add the head and body parts
		parts.append(Part(0, self.xy[0], self.xy[1], True))
		parts.append(Part(0, 0, 0, False))
		parts.append(Part(0, 0, 0, False))
		# Load the image files
		parts[0].loadImage("image_resources/body.png")
		parts[1].loadImage("image_resources/body.png")
		parts[2].loadImage("image_resources/head.png")
		# Body parts and heads weight
		parts[0].setWeight(23.44)
		parts[1].setWeight(11.72)
		parts[2].setWeight(8.24)

		# Add the leg parts
		for i in range(0, 2):
			parts.append(Part(310, 0, 0, False))
			parts.append(Part(50, 0, 0, False))
			parts.append(Part(50, 0, 0, False))
			parts.append(Part(0, 0, 0, False))
			parts.append(Part(0, 0, 0, False))
			parts.append(Part(0, 0, 0, False))
		for l in range(3, 15):
			# Load the image files and set the constraints
			parts[l].loadImage("image_resources/leg.png")
			parts[l].setWeight(0.66)
		self.parts = parts
		self.centerOfGravity()
		self.setSensors()
		self.setConstraints()
		if not init:
			if stage:
				self.network.nextGame(self.getCog()[0] - score)
			else:
				self.network.nextGameCompleted(self.getCog()[0] - score)

	# Handles movement calculations
	def move(self, stage):
		movement = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.sensorCollide()
		if stage:
			move = self.network.initialPopulation(self.sensorCollisions)
		else:
			move = self.network.completed(self.sensorCollisions)
		for k in range(len(movement)):
			if k == move:
				movement[k] = 1
			elif k == move - 15:
				movement[k] = -1

		parts = self.parts
		colliding = self.colliding
		xy = (0, 0)
		# Initialise the points of contact to -1 since that is outside the world view
		self.box = [(-1,-1), (-1,-1), (-1,-1), (-1,-1)]

		# Initialise array to say no parts are colliding with the world
		for g in range(0,15):
			colliding[g] = False
		# Get the position of the agents main pivot (the point at which its back segment rotates around)
		pos = parts[0].getPosition()
		# This is WASD so I can move the agent easily
		# The agent is also raised by one pixel so it can rotate corners without getting stuck in the ground. An extra 1 is added to the gravity
		# to negate this
		pivot = (pos[0] + xy[0], pos[1] + xy[1] - 1.0)

		# Rotate each part
		for iterate in range(0,15):
			# Reset each parts constraints with regards to the moves previous parts made
			self.setConstraints()
			# Store a copy of the agent
			self.stored(True)
			# Rotate one body part with the values sent into the function
			backMove = parts[iterate].rotation(movement[iterate])
			if iterate == 0:
				pivot = (pivot[0] + backMove[0], pivot[1] + backMove[1])
			# If the top part of the leg is moved rotate the bottom as well
			# The bottom segment can still be rotated seperately
			if(iterate > 2 and iterate < 6 or iterate > 8 and iterate < 12):
				parts[iterate + 3].rotation(movement[iterate])
			# Move all parts in relation to the rotation just made
			self.setPositions(pivot)
			# If the part collided with the world revert the changes with the copy previously made
			if self.collide():
				self.stored(False)
				if iterate == 0:
					pivot = (pivot[0] - backMove[0], pivot[1] - backMove[1])
		# The agent is now affected by gravity
		pivot = self.gravity(pivot)

		# When the agent pushes off with a leg the rest of its body should move with it
		self.interactiveMove(pivot, movement)
		self.centerOfGravity()
		# If the agents center of gravity is to the left of all its points of contacts fall to the left
		if self.box[0][0] != -1 and self.box[0][0] > self.cog[0]:
			self.fallRotation(pivot, True)
		# If the agents center of gravity is to the right of all its points of contacts fall to the right
		elif self.box[1][0] != -1 and self.box[1][0] < self.cog[0]:
			self.fallRotation(pivot, False)
		# print(self.inputMatrix)

	# When the agent is hanging on an edge over its center of gravity it should tip in that direction
	def fallRotation(self, pivot, left):
			parts = self.parts
			# X,Y distances between the agents point of contact with the world and the agents main pivot point.
			# (The pivot is where the agent bases all calculations from and is the rotation point for its back)
			distanceXY = None
			# Torque is the distance the agents center of gravity is from the collision point being used
			torque = None
			# If the agent is falling to the left use the left most collision point otherwise use the rightmost
			if left:
				distanceXY = (self.box[0][0] - (parts[0].getPosition()[0] + 50), self.box[0][1] - (parts[0].getPosition()[1] + 50))
				torque = (self.cog[0] - self.box[0][0]) / 25
			else:
				distanceXY = (self.box[1][0] - (parts[0].getPosition()[0] + 50), self.box[1][1] - (parts[0].getPosition()[1] + 50))
				torque = (self.cog[0] - self.box[1][0]) / 25

			# Actual distance between the agents point of contact with the world and the agents main pivot point
			distanceH = math.sqrt(distanceXY[0] * distanceXY[0] + distanceXY[1] * distanceXY[1])

			# The angle between the collision point being used and the agents pivot point. The agent will be rotated around the point of collision
			# since when you fall you fall around the last place you were touching the ground
			currentAngle = None
			if(distanceXY[0] == 0):
				currentAngle = 90
			else:
				currentAngle = math.atan(distanceXY[1]/distanceXY[0]) * 180.0 / math.pi

			# The X,Y distances between the agents point of contact with the world and where the agents main pivot point will be after the rotation
			newXY = (math.cos((180.0 + currentAngle + torque) / 180 * math.pi), -math.sin((currentAngle + torque) / 180 * math.pi))
			newXY = (-abs(newXY[0] * distanceH), -abs(newXY[1] * distanceH))
			# Difference between where the pivot point is and where it will be after the rotation
			if(distanceXY[0] < 0):	
				newXY = (distanceXY[0] - newXY[0], newXY[1])
			else:
				newXY = (distanceXY[0] + newXY[0], newXY[1])
			if(distanceXY[1] < 0):
				newXY = (newXY[0], newXY[1] - distanceXY[1])
			else:
				newXY = (newXY[0], newXY[1] + distanceXY[1])
			# Once the agent has successfully rotated without colliding with the world passed = True
			passed = False
			# Store a backup of the agent
			self.stored(True)
			# Keep attempting to rotate the agent whilst moving it slightly away from the point of contact. Since the agents legs do not have rounded edges sometimes its
			# corner will get stuck in the ground so this gives it a little room to work with
			for horizontal in range(0,5):
				# Move vertically first since this will be negated by gravity and only move horizontally if necessary
				for vertical in range(0,5):
					# Move slightly left if the agent is falling to the left otherwise move slightly right, also move up
					if left:
						newPivot = (pivot[0] + newXY[0] - (0.3 * horizontal), pivot[1] + newXY[1] - (0.8 * vertical))
					else:
						newPivot = (pivot[0] + newXY[0] + (0.3 * horizontal), pivot[1] + newXY[1] - (0.8 * vertical))
					# Move and rotate the agent
					self.setPositions(newPivot)
					self.rotateAll(-torque)
					# If the agent collides with the world reset it with the stored values otherwise finish iterating and break
					if self.collide():
						self.stored(False)
					else:
						passed = True
						break
				if passed:
					break

	# Agent is affected by gravity
	def gravity(self, pivot):
		# Decrement multiple times instead of just lowering once since this way if it collides in the middle it will go as close as possible
		for i in range(0,3):
			# Store a copy of the agent
			self.stored(True)
			# Lower the agent by 1
			pivot = (pivot[0], pivot[1] + 1.0)
			self.setPositions(pivot)
			# If the agent collides with the world revert the move
			if self.collide():
				self.stored(False)
				# Reset the pivot if the agent is reset
				pivot = (pivot[0], pivot[1] - 1.0)
		return pivot

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
		for q in range(0,15):
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
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 27) + (partRotations[5][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 27) + (partRotations[5][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 12) + (partRotations[3][0] * 12) + (partRotations[6][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 12) + (partRotations[3][1] * 12) + (partRotations[6][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[4][0] * 12) + (partRotations[7][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[4][1] * 12) + (partRotations[7][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 27) + (partRotations[5][0] * 12) + (partRotations[8][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 27) + (partRotations[5][1] * 12) + (partRotations[8][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 12) + (partRotations[9][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 12) + (partRotations[9][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[10][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[10][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 27) + (partRotations[11][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 27) + (partRotations[11][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 12) + (partRotations[9][0] * 12) + (partRotations[12][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 12) + (partRotations[9][1] * 12) + (partRotations[12][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[10][0] * 12) + (partRotations[13][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[10][1] * 12) + (partRotations[13][1] * 5) + 13))
		centers.append((pos[0] + 38 + (partRotations[0][0] * 39) + (partRotations[1][0] * 27) + (partRotations[11][0] * 12) + (partRotations[14][0] * 5) + 13, pos[1] + 40 + (partRotations[0][1] * 39) + (partRotations[1][1] * 27) + (partRotations[11][1] * 12) + (partRotations[14][1] * 5) + 13))
		
		# Add all parts center of gravity multiplied by there specific weight
		for i in range(0,15):
			self.cog = (self.cog[0] + (centers[i][0] * parts[i].getWeight()), self.cog[1] + (centers[i][1] * parts[i].getWeight()))
			weight += parts[i].getWeight()
		# Divide by the total weight of the agent
		self.cog = (self.cog[0] / weight, self.cog[1] / weight)

	# When the agent pushes off with a leg the rest of its body should follow
	def interactiveMove(self, pivot, movement):
		colliding = self.colliding
		parts = self.parts
		# Bottom parts of the legs
		for p in range(6,9):
			# If they are colliding with the world
			if colliding[p]:
				# If you move the top part of the leg move the agent as well
				for q in range(0,2):
					# If the part is trying to move
					if movement[p - (3 * q)] != 0:
						# If the bottom part of theleg is at its maximum rotation then ignore any movement by the bottom part and just use the top part
						if (parts[p].getRotation() != parts[p].getConstraint()[0] and parts[p].getRotation() != parts[p].getConstraint()[1]) or q == 1:
							# Calculate the difference between where the pivot of the leg was and where it will be after moving
							angle = (math.sin((parts[p - (3 * q)].getRotation()) / 180 * math.pi)), -math.cos((180.0 + parts[p - (3 * q)].getRotation()) / 180 * math.pi)
							angle = (angle[0] * 12, angle[1] * 12)
							# New location
							newAngle = (-math.sin((parts[p - (3 * q)].getRotation() + movement[p - (3 * q)]) / 180 * math.pi)), math.cos((180.0 + parts[p - (3 * q)].getRotation() + movement[p - (3 * q)]) / 180 * math.pi)
							newAngle = (newAngle[0] * 12 + angle[0], newAngle[1] * 12 + angle[1] - 0.05)

							# Move the entire agent by the difference
							pivot = (pivot[0] + newAngle[0], pivot[1] + newAngle[1])
							# Store a copy of the agent
							self.stored(True)
							# Rotate and move the part
							parts[p - (3 * q)].setRotation(parts[p - (3 * q)].getRotation() + movement[p - (3 * q)])
							self.setPositions(pivot)
							# If the movement pushes the agent into a wall revert the changes to the agent using the stored copy
							if self.collide() and newAngle[1] > 0:
								self.stored(False)
		for p in range(12,15):
			# If they are colliding with the world
			if colliding[p]:
				# If you move the top part of the leg move the agent as well
				for q in range(0,2):
					# If the part is trying to move
					if movement[p - (3 * q)] != 0:
						# If the bottom part of theleg is at its maximum rotation then ignore any movement by the bottom part and just use the top part
						if (parts[p].getRotation() != parts[p].getConstraint()[0] and parts[p].getRotation() != parts[p].getConstraint()[1]) or q == 1:
							# Calculate the difference between where the pivot of the leg was and where it will be after moving
							angle = (math.sin((parts[p - (3 * q)].getRotation()) / 180 * math.pi)), -math.cos((180.0 + parts[p - (3 * q)].getRotation()) / 180 * math.pi)
							angle = (angle[0] * 12, angle[1] * 12)
							# New location
							newAngle = (-math.sin((parts[p - (3 * q)].getRotation() + movement[p - (3 * q)]) / 180 * math.pi)), math.cos((180.0 + parts[p - (3 * q)].getRotation() + movement[p - (3 * q)]) / 180 * math.pi)
							newAngle = (newAngle[0] * 12 + angle[0], newAngle[1] * 12 + angle[1] - 0.05)

							# Move the entire agent by the difference
							pivot = (pivot[0] + newAngle[0], pivot[1] + newAngle[1])
							# Store a copy of the agent
							self.stored(True)
							# Rotate and move the part
							parts[p - (3 * q)].setRotation(parts[p - (3 * q)].getRotation() + movement[p - (3 * q)])
							self.setPositions(pivot)
							# If the movement pushes the agent into a wall revert the changes to the agent using the stored copy
							if self.collide() and newAngle[1] > 0:
								self.stored(False)

	# If setup is true store a copy of the agent otherwise replace the current agents details with the stored copy
	def stored(self, setup):
		one = []
		two = []
		if setup:
			two = self.parts
			one = self.backup
		else:
			two = self.backup
			one = self.parts
		for k in range(0,15):
			one[k].setPosition(two[k].getPosition())
			one[k].setConstraint(two[k].getConstraint())
			one[k].setRotation(two[k].getRotation())
			if not setup:
				one[k].rotation(0)

	# Rotate entire agent
	def rotateAll(self, amount):
		for iterate in range(0,15):
			self.parts[iterate].rotation(amount)
	
	# Set the constraints of each part
	def setConstraints(self):
		parts = self.parts
		parts[0].setConstraint(((parts[1].getRotation() - 90) % 360, (parts[1].getRotation() + 90) % 360))
		parts[1].setConstraint(((parts[0].getRotation() - 90) % 360, (parts[0].getRotation() + 90) % 360))
		parts[2].setConstraint(((parts[1].getRotation() - 90) % 360, (parts[1].getRotation() + 90) % 360))
		for i in range(0,2):
			offset = i * 6
			parts[3 + offset].setConstraint((0, 360))
			parts[4 + offset].setConstraint((0, 360))
			parts[5 + offset].setConstraint((0, 360))
			parts[6 + offset].setConstraint(((parts[3 + offset].getRotation() - 90) % 360, (parts[3 + offset].getRotation() + 90) % 360))
			parts[7 + offset].setConstraint(((parts[4 + offset].getRotation() - 90) % 360, (parts[4 + offset].getRotation() + 90) % 360))
			parts[8 + offset].setConstraint(((parts[5 + offset].getRotation() - 90) % 360, (parts[5 + offset].getRotation() + 90) % 360))

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
		for i in range(0,2):
			offset = i * 6
			# Back leg (top)
			parts[3 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 12), pos[1] + 40 + (backRotation[1] * 12)))
			legRotation = (math.sin(parts[3 + offset].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[3 + offset].getRotation()) / 180 * math.pi))
			# Back leg (bottom)
			parts[6 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 12) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 12) + (legRotation[1] * 11.5)))
			# Middle leg (top)
			parts[4 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 39), pos[1] + 40 + (backRotation[1] * 39)))
			legRotation = (math.sin(parts[4 + offset].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[4 + offset].getRotation()) / 180 * math.pi))
			# Middle leg (bottom)
			parts[7 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5), pos[1] + 40 + (backRotation[1] * 39) + (legRotation[1] * 11.5)))
			# Front leg (top)
			parts[5 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (frontRotation[0] * 27), pos[1] + 40 + (backRotation[1] * 39) + (frontRotation[1] * 27)))
			# Front leg (bottom)
			legRotation = (math.sin(parts[5 + offset].getRotation() / 180 * math.pi), -math.cos((180.0 + parts[5 + offset].getRotation()) / 180 * math.pi))
			parts[8 + offset].setPosition((pos[0] + 38 + (backRotation[0] * 39) + (legRotation[0] * 11.5) + (frontRotation[0] * 27), pos[1] + 40 + (backRotation[1] * 39)  + (legRotation[1] * 11.5)+ (frontRotation[1] * 27)))

	# Handles Collisions between the ant and the world
	def collide(self):
		parts = self.parts
		objects = self.objects
		colliding = self.colliding
		ret = False
		# For legs check if they are colliding with other legs from the same ant. Body parts are behind the legs so they can overlap
		# But an agent cannot cross its legs
		for position in range(0,15):
			if position > 2 and position < 9:
				for j in range(3,9):
					# Dont check collisions when the 2 parts are from the same leg. E.g "Thigh" and "Calf"
					if (position % 3) != (j % 3):			
						offset = (int(parts[position].getPosition()[0] - parts[j].getPosition()[0]), int(parts[position].getPosition()[1] - parts[j].getPosition()[1]))
						result = parts[j].getMask().overlap(parts[position].getMask(), offset)
						# If they collide return true
						if result:
							ret = True
			elif position > 8:
				for j in range(9,15):
					# Dont check collisions when the 2 parts are from the same leg. E.g "Thigh" and "Calf"
					if (position % 3) != (j % 3):			
						offset = (int(parts[position].getPosition()[0] - parts[j].getPosition()[0]), int(parts[position].getPosition()[1] - parts[j].getPosition()[1]))
						result = parts[j].getMask().overlap(parts[position].getMask(), offset)
						# If they collide return true
						if result:
							ret = True

			# Check collisions against all the other objects in the world which exclude itself
			for k in range(len(objects)):
				offset = (int(objects[k][1] - parts[position].getPosition()[0]), int(objects[k][2] - parts[position].getPosition()[1]))
				result = parts[position].getMask().overlap(objects[k][0], offset)
				if result:
					self.collisionBox((parts[position].getPosition()[0] + result[0], parts[position].getPosition()[1] + result[1]))
					colliding[position] = True
					ret = True
		return ret

	def sensorCollide(self):
		parts = self.parts
		objects = self.objects
		collisions = []
		for i in range(len(parts)):
			masks = parts[i].getSensorMasks()
			for j in range(len(masks)):
				collide = 0
				for k in range(len(objects)):
					offset = (int(objects[k][1] - parts[i].getPosition()[0]), int(objects[k][2] - parts[i].getPosition()[1]))
					result = masks[j].overlap(objects[k][0], offset)
					if result:
						collide = 1

				if i > 2 and i < 9:
					for j in range(3,9):
						# Dont check collisions when the 2 parts are from the same leg. E.g "Thigh" and "Calf"
						if (i % 3) != (j % 3):			
							offset = (int(parts[i].getPosition()[0] - parts[j].getPosition()[0]), int(parts[i].getPosition()[1] - parts[j].getPosition()[1]))
							result = parts[j].getMask().overlap(parts[i].getMask(), offset)
							# If they collide return true
							if result:
								collide = 1
				elif i > 8:
					for j in range(9,15):
						# Dont check collisions when the 2 parts are from the same leg. E.g "Thigh" and "Calf"
						if (i % 3) != (j % 3):			
							offset = (int(parts[i].getPosition()[0] - parts[j].getPosition()[0]), int(parts[i].getPosition()[1] - parts[j].getPosition()[1]))
							result = parts[j].getMask().overlap(parts[i].getMask(), offset)
							# If they collide return true
							if result:
								collide = 1

				collisions.append(collide)
		for j in range(len(parts)):
				collisions.append(parts[j].getRotation() / 360.0)
				one = abs(parts[j].getRotation() - parts[j].getConstraint()[0])
				two = abs(parts[j].getRotation() - parts[j].getConstraint()[1])
				if one < 1 or one > 359:
					collisions.append(1)
				else:
					collisions.append(0)
				if two < 1 or two > 359:
					collisions.append(1)
				else:
					collisions.append(0)
		self.sensorCollisions = collisions

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
		parts = self.parts
		for i in range(3,9):
			DS.blit(parts[i].getImage(), parts[i].getPosition())
		for i in range(0,3):
			DS.blit(parts[i].getImage(), parts[i].getPosition())
		for i in range(9,15):
			DS.blit(parts[i].getImage(), parts[i].getPosition())
		for i in range(len(parts)):
			sensors = parts[i].getSensors()
			for j in range(len(sensors)):
				DS.blit(sensors[j], parts[i].getPosition())

	# Return an array of all the individual ant parts
	def getParts(self):
		return self.parts

	# Return the agents center of gravity
	def getCog(self):
		return self.cog

	# Retrun any markers that should be drawn on screen
	def getMarkers(self):
		return self.box

	# Set the sensor images
	def setSensors(self):
		parts = self.parts
		parts[0].loadSensors(["image_resources/sensors/body1.png", "image_resources/sensors/body2.png", "image_resources/sensors/body3.png", "image_resources/sensors/body4.png","image_resources/sensors/body5.png", "image_resources/sensors/body6.png","image_resources/sensors/body7.png", "image_resources/sensors/body8.png","image_resources/sensors/body9.png", "image_resources/sensors/body10.png","image_resources/sensors/body11.png", "image_resources/sensors/body12.png"])
		parts[1].loadSensors(["image_resources/sensors/body1.png", "image_resources/sensors/body2.png", "image_resources/sensors/body3.png", "image_resources/sensors/body4.png","image_resources/sensors/body5.png", "image_resources/sensors/body6.png","image_resources/sensors/body7.png", "image_resources/sensors/body8.png","image_resources/sensors/body9.png", "image_resources/sensors/body10.png","image_resources/sensors/body11.png", "image_resources/sensors/body12.png"])
		parts[2].loadSensors(["image_resources/sensors/head1.png", "image_resources/sensors/head2.png", "image_resources/sensors/head3.png", "image_resources/sensors/head4.png","image_resources/sensors/head5.png", "image_resources/sensors/head6.png","image_resources/sensors/head7.png", "image_resources/sensors/head8.png","image_resources/sensors/head9.png", "image_resources/sensors/head10.png","image_resources/sensors/head11.png", "image_resources/sensors/head12.png", "image_resources/sensors/head13.png"])
		for i in range(3, 15):
			parts[i].loadSensors(["image_resources/sensors/leg1.png","image_resources/sensors/leg2.png","image_resources/sensors/leg3.png","image_resources/sensors/leg4.png","image_resources/sensors/leg5.png","image_resources/sensors/leg6.png","image_resources/sensors/leg7.png","image_resources/sensors/leg8.png","image_resources/sensors/leg9.png","image_resources/sensors/leg10.png"])

	def nextStep(self):
		self.network.afterInitial()
		self.network.trainModel()