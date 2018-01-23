import math, random, sys, pygame
from pygame.locals import *
from ant import ant
from part import part
from block import block
import os

# define display surface			
W, H = 1080, 600
HW, HH = W / 2, H / 2
AREA = W * H
movex,movey = 0, 0

# define some colors
BLUE = (0, 255, 200, 255)

# initialise display
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,80)
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ant Tower Project")
FPS = 120

# Get the image resources for the world
pointer = pygame.image.load("image_resources/pointer.png").convert_alpha()
pointerTwo = pygame.image.load("image_resources/pointerTwo.png").convert_alpha()

# Holds the movement values that get inputted into an agent
movement = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
player = 4
blocks = []
gravity = False
# Add 2 ants into the world
ants = []
for p in range(0,4):
	ants.append(ant())
	blocks.append(block(0, 0, 580 - p * 175))
	blocks[p].loadImage("image_resources/flat_floor.png")
for i in range(len(ants)):
	ants[i].move((50,-50 + 175 * i), movement)
	for j in range(len(blocks)):
		ants[i].addObject((blocks[j].getMask(), blocks[j].getPosition()[0], blocks[j].getPosition()[1]))
# main loop
while True:
	# Key Listeners for movement and quitting
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_a:
				movex = -1
			elif event.key == K_d:
				movex = 1
			elif event.key == K_w:
				movey = -1
			elif event.key == K_s:
				movey = 1
			if event.key == K_1:
				player = 0
			elif event.key == K_2:
				player = 1
			elif event.key == K_3:
				player = 2
			elif event.key == K_4:
				player = 3
			elif event.key == K_5:
				player = 4
			elif event.key == K_p:
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
				movement[3] = movement[3]
			if event.key == K_r or event.key == K_t:
				movement[4] = movement[4]
			if event.key == K_y or event.key == K_u:
				movement[5] = movement[5]
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
				movement[9] = movement[9]
			if event.key == K_z or event.key == K_x:
				movement[10] = movement[10]
			if event.key == K_c or event.key == K_v:
				movement[11] = movement[11]
			if event.key == K_b or event.key == K_n:
				movement[12] = 0
			if event.key == K_m or event.key == K_COMMA:
				movement[13] = 0
			if event.key == K_PERIOD or event.key == K_SLASH:
				movement[14] = 0
			if event.key == K_a:
				movex = 0
			elif event.key == K_d:
				movex = 0
			elif event.key == K_w:
				movey = 0
			elif event.key == K_s:
				movey = 0

	# Draw world
	DS.fill(BLUE)
	for i in range(len(blocks)):
		DS.blit(blocks[i].getImage(), blocks[i].getPosition())

	if player == 4:
		for j in range(len(ants)):
			ants[j].move((movex,movey), movement)
	else:
		ants[player].move((movex,movey), movement)
	# Draw ants
	for i in range(len(ants)):
		ants[i].run(DS)
		cog = ants[i].getCog()
		DS.blit(pointerTwo, (int(cog[0]), int(cog[1])))
		markers = ants[i].getMarkers()
		for j in range(len(markers)):
			DS.blit(pointer, (int(markers[j][0]), int(markers[j][1])))
	pygame.display.update()
	CLOCK.tick(FPS)