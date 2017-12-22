import math, random, sys, pygame
from pygame.locals import *
from ant import ant
from part import part

# define display surface			
W, H = 1080, 600
HW, HH = W / 2, H / 2
AREA = W * H
movex,movey = 0, 0

# define some colors
BLUE = (0, 255, 200, 255)

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ant Tower Project")
FPS = 120

# Get the image resources for the world
floor = pygame.image.load("image_resources/flat_floor.png").convert_alpha()
floor_mask = pygame.mask.from_surface(floor)
wall = pygame.image.load("image_resources/flat_floor.png").convert_alpha()
wall_mask = pygame.mask.from_surface(wall)
pointer = pygame.image.load("image_resources/pointer.png").convert_alpha()
pointerTwo = pygame.image.load("image_resources/pointerTwo.png").convert_alpha()

# Holds the movement values that get inputted into an agent
movement = [0,0,0,0,0,0,0,0,0]
gravity = False
# Add 2 ants into the world
ants = []
ants.append(ant())
for i in range(len(ants)):
	ants[i].move((150 * i,30), movement, gravity)
	ants[i].addObject((floor_mask, 0, 500))
	ants[i].addObject((wall_mask, -1000, 300))
	ants[i].addObject((wall_mask, 1000, 300))
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
			if event.key == K_p:
				gravity = True
			if event.key == K_e:
				movement[0] = 1
			if event.key == K_r:
				movement[0] = -1
			if event.key == K_t:
				movement[1] = 1
			if event.key == K_y:
				movement[1] = -1
			if event.key == K_u:
				movement[2] = 1
			if event.key == K_i:
				movement[2] = -1
			if event.key == K_f:
				movement[3] = 1
			if event.key == K_g:
				movement[3] = -1
			if event.key == K_h:
				movement[4] = 1
			if event.key == K_j:
				movement[4] = -1
			if event.key == K_k:
				movement[5] = 1
			if event.key == K_l:
				movement[5] = -1
			if event.key == K_x:
				movement[6] = -1
			if event.key == K_c:
				movement[6] = 1
			if event.key == K_v:
				movement[7] = -1
			if event.key == K_b:
				movement[7] = 1
			if event.key == K_n:
				movement[8] = -1
			if event.key == K_m:
				movement[8] = 1
		if event.type == KEYUP:
			if event.key == K_p:
				gravity = False
			if event.key == K_e or event.key == K_r:
				movement[0] = 0
			if event.key == K_t or event.key == K_y:
				movement[1] = 0
			if event.key == K_u or event.key == K_i:
				movement[2] = 0
			if event.key == K_f or event.key == K_g:
				movement[3] = 0
			if event.key == K_h or event.key == K_j:
				movement[4] = 0
			if event.key == K_k or event.key == K_l:
				movement[5] = 0
			if event.key == K_x or event.key == K_c:
				movement[6] = 0
			if event.key == K_v or event.key == K_b:
				movement[7] = 0
			if event.key == K_n or event.key == K_m:
				movement[8] = 0
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
	DS.blit(floor, (int(0), int(500)))
	DS.blit(wall, (int(-1000), int(300)))
	DS.blit(wall, (int(1000), int(300)))

	# Draw ants
	for i in range(len(ants)):
		ants[i].move((movex,movey), movement, gravity)
		ants[i].run(DS)
		cog = ants[i].getCog()
		DS.blit(pointerTwo, (int(cog[0]), int(cog[1])))
		mark = ants[i].getMarkers()
		DS.blit(pointer, (int(mark[0][0]), int(mark[0][1])))
	pygame.display.update()
	CLOCK.tick(FPS)