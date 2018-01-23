import math, random, sys, pygame, os
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

# Get the image resources for the world
pointers = [None, None, None]
pointers[0] = pygame.image.load("image_resources/pointer.png").convert_alpha()
pointers[1] = pygame.image.load("image_resources/pointerTwo.png").convert_alpha()
pointers[2] = pygame.image.load("image_resources/pointerThree.png").convert_alpha()

# Holds the movement values that get inputted into an agent
movement = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
player = 4
blocks = []
gravity = False
# Adds agents into the world
agents = []
for p in range(0,1):
	agents.append(Agent((50,-50 + 175 * p)))
	blocks.append(Block(0, 0, 580 - p * 175))
	blocks[p].loadImage("image_resources/flat_floor.png")
# Tell all agents about the objects within the world so they can detect collisions
for i in range(len(agents)):
	agents[i].move(movement)
	for j in range(len(blocks)):
		agents[i].addObject((blocks[j].getMask(), blocks[j].getPosition()[0], blocks[j].getPosition()[1]))
# main loop
while True:
	# Key Listeners for movement and quitting
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_1:
				player = 0
			if event.key == K_2:
				player = 1
			if event.key == K_3:
				player = 2
			if event.key == K_4:
				player = 3
			if event.key == K_p:
				gravity = True
			if event.key == K_q:
				movement[3] = 1
			if event.key == K_e:
				movement[3] = -1
			if event.key == K_r:
				movement[4] = 1
			if event.key == K_t:
				movement[4] = -1
			if event.key == K_y:
				movement[5] = 1
			if event.key == K_u:
				movement[5] = -1
			if event.key == K_i:
				movement[6] = 1
			if event.key == K_o:
				movement[6] = -1
			if event.key == K_p:
				movement[7] = 1
			if event.key == K_LEFTBRACKET:
				movement[7] = -1
			if event.key == K_RIGHTBRACKET:
				movement[8] = 1
			if event.key == K_BACKSLASH:
				movement[8] = -1
			if event.key == K_f:
				movement[0] = -1
			if event.key == K_g:
				movement[0] = 1
			if event.key == K_h:
				movement[1] = -1
			if event.key == K_j:
				movement[1] = 1
			if event.key == K_k:
				movement[2] = -1
			if event.key == K_l:
				movement[2] = 1
			if event.key == K_RETURN:
				movement[9] = -1
			if event.key == K_SEMICOLON:
				movement[9] = 1
			if event.key == K_z:
				movement[10] = 1
			if event.key == K_x:
				movement[10] = -1
			if event.key == K_c:
				movement[11] = 1
			if event.key == K_v:
				movement[11] = -1
			if event.key == K_b:
				movement[12] = -1
			if event.key == K_n:
				movement[12] = 1
			if event.key == K_m:
				movement[13] = -1
			if event.key == K_COMMA:
				movement[13] = 1
			if event.key == K_PERIOD:
				movement[14] = -1
			if event.key == K_SLASH:
				movement[14] = 1
		if event.type == KEYUP:
			if event.key == K_p:
				gravity = False
			if event.key == K_q or event.key == K_e:
				movement[3] = 0
			if event.key == K_r or event.key == K_t:
				movement[4] = 0
			if event.key == K_y or event.key == K_u:
				movement[5] = 0
			if event.key == K_i or event.key == K_o:
				movement[6] = 0
			if event.key == K_p or event.key == K_LEFTBRACKET:
				movement[7] = 0
			if event.key == K_RIGHTBRACKET or event.key == K_BACKSLASH:
				movement[8] = 0
			if event.key == K_f or event.key == K_g:
				movement[0] = 0
			if event.key == K_h or event.key == K_j:
				movement[1] = 0
			if event.key == K_k or event.key == K_l:
				movement[2] = 0
			if event.key == K_SEMICOLON or event.key == K_RETURN:
				movement[9] = 0
			if event.key == K_z or event.key == K_x:
				movement[10] = 0
			if event.key == K_c or event.key == K_v:
				movement[11] = 0
			if event.key == K_b or event.key == K_n:
				movement[12] = 0
			if event.key == K_m or event.key == K_COMMA:
				movement[13] = 0
			if event.key == K_PERIOD or event.key == K_SLASH:
				movement[14] = 0

	# Draw world
	DS.fill(BLUE)
	for i in range(len(blocks)):
		DS.blit(blocks[i].getImage(), blocks[i].getPosition())
	# Control specific agents
	if player == 4:
		for j in range(len(agents)):
			agents[j].move(movement)
	else:
		agents[player].move(movement)
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