import math, random, sys, pygame, os, time
from pygame.locals import *
from agent import Agent
from part import Part
from block import Block

# define display surface			
W, H = 1080, 600
HW, HH = W / 2, H / 2
AREA = W * H

# define some colors
BLUE = (0, 255, 200, 255)

# Place window in the center of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,80)
# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ant Tower Project")
FPS = 120
trainingNum = 50

# Get the image resources for the world
pointers = [None, None, None]
pointers[0] = pygame.image.load("image_resources/pointer.png").convert_alpha()
pointers[1] = pygame.image.load("image_resources/pointerTwo.png").convert_alpha()
pointers[2] = pygame.image.load("image_resources/pointerThree.png").convert_alpha()

blocks, agents = [],[]
agentNumber = 1
# Adds agents into the world
for p in range(0,agentNumber):
	agents.append(Agent((50,-25 + 175 * p)))
	blocks.append(Block(0, 0, 55 + p * 175))
	blocks[p].loadImage("image_resources/flat_floor.png")
# Tell all agents about the objects within the world so they can detect collisions
for i in range(len(agents)):
	for j in range(len(blocks)):
		agents[i].addObject((blocks[j].getMask(), blocks[j].getPosition()[0], blocks[j].getPosition()[1]))

timer = 1000
counter = 0
# main loop
while True:
	# Key Listeners for movement and quitting
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

	if timer < 0:
		timer = 1000
		counter = counter + 1
		for k in range(len(agents)):
			score = agents[k].getCog()[0]
			agents[k].reset(counter < trainingNum, score, False)
			if counter == trainingNum:
				agents[k].nextStep()
		print(counter)

	else:
		timer = timer - 1

	# Control specific agents
	for j in range(len(agents)):
		agents[j].move(counter < trainingNum)
	if counter >= trainingNum:
		# Draw world
		DS.fill(BLUE)
		for i in range(len(blocks)):
			DS.blit(blocks[i].getImage(), blocks[i].getPosition())
		# Draw agents
		for i in range(len(agents)):
			agents[i].run(DS)
			# Pointer for agents center of gravity
			cog = agents[i].getCog()
			DS.blit(pointers[1], (int(cog[0]), int(cog[1])))
			markers = agents[i].getMarkers()
			# Pointer for collision points
			for j in range(len(markers)):
				DS.blit(pointers[0], (int(markers[j][0]), int(markers[j][1])))
		pygame.display.update()
		CLOCK.tick(FPS)