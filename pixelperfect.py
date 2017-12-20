import math, random, sys
import pygame
from pygame.locals import *

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# define display surface			
W, H = 1080, 600
HW, HH = W / 2, H / 2
AREA = W * H
leg_offset, leg_height, difference = 50, 40, 27
leg_length = 9.7

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Pixel Perfect Collision")
FPS = 120

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

obstacle = pygame.image.load("obstacle-400x399.png").convert_alpha()
background = pygame.image.load("image_resources/blue.jpg").convert_alpha()
obstacle_mask = pygame.mask.from_surface(obstacle)
obstacle_rect = obstacle.get_rect()
ox = HW - obstacle_rect.center[0]
oy = HH - obstacle_rect.center[1]

leg, leg_mask, leg_rect = [],[],[]
for i in range(0,6):
	leg.append(pygame.image.load("image_resources/leg.png").convert_alpha())
	leg_mask.append(pygame.mask.from_surface(leg[i]))
	leg_rect.append(leg[i].get_rect())


leg.append(pygame.image.load("image_resources/body.png").convert_alpha())
leg_mask.append(pygame.mask.from_surface(leg[6]))
leg_rect.append(leg[6].get_rect())

leg.append(pygame.image.load("image_resources/body.png").convert_alpha())
leg_mask.append(pygame.mask.from_surface(leg[7]))
leg_rect.append(leg[7].get_rect())

leg.append(pygame.image.load("image_resources/head.png").convert_alpha())
leg_mask.append(pygame.mask.from_surface(leg[8]))
leg_rect.append(leg[8].get_rect())

mx, my = 0 , 0
movex,movey = 0, 0
rotate, spin = [0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0]
temp = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
temp_two = [[0.0, 0.0], [0.0, 0.0]]

# main loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_r:
				spin[0] += 1.0
			if event.key == K_t:
				spin[0] -= 1.0
			if event.key == K_f:
				spin[1] += 1.0
			if event.key == K_g:
				spin[1] -= 1.0
			if event.key == K_v:
				spin[2] += 1.0
			if event.key == K_b:
				spin[2] -= 1.0
			if event.key == K_h:
				spin[3] += 1.0
			if event.key == K_j:
				spin[3] -= 1.0
			if event.key == K_y:
				spin[4] += 1.0
			if event.key == K_u:
				spin[4] -= 1.0
			if event.key == K_n:
				spin[5] += 1.0
			if event.key == K_m:
				spin[5] -= 1.0
			elif event.key == K_a:
				movex = -1
			elif event.key == K_d:
				movex = 1
			elif event.key == K_w:
				movey = -1
			elif event.key == K_s:
				movey = 1
		if event.type == KEYUP:
			if event.key == K_r or event.key == K_t:
				spin[0] = 0.0
			if event.key == K_f or event.key == K_g:
				spin[1] = 0.0
			if event.key == K_v or event.key == K_b:
				spin[2] = 0.0
			if event.key == K_h or event.key == K_j:
				spin[3] = 0.0
			if event.key == K_y or event.key == K_u:
				spin[4] = 0.0
			if event.key == K_n or event.key == K_m:
				spin[5] = 0.0
			elif event.key == K_a:
				movex = 0
			elif event.key == K_d:
				movex = 0
			elif event.key == K_w:
				movey = 0
			elif event.key == K_s:
				movey = 0

	for i in range(0,6):
		rotate[i] += spin[i]
		rotate[i] = rotate[i] % 360
		if i < 3:
			leg[i] = pygame.image.load("image_resources/leg.png").convert_alpha()
			leg[i] = rot_center(leg[i], rotate[i])
			leg_mask[i] = pygame.mask.from_surface(leg[i])
			leg_rect[i] = leg[i].get_rect()

	leg[6] = pygame.image.load("image_resources/body.png").convert_alpha()
	leg[6] = rot_center(leg[6], rotate[4])
	leg_mask[6] = pygame.mask.from_surface(leg[6])
	leg_rect[6] = leg[6].get_rect()
	leg[7] = pygame.image.load("image_resources/body.png").convert_alpha()
	leg[7] = rot_center(leg[7], rotate[3])
	leg_mask[7] = pygame.mask.from_surface(leg[7])
	leg_rect[7] = leg[7].get_rect()
	leg[8] = pygame.image.load("image_resources/head.png").convert_alpha()
	leg[8] = rot_center(leg[8], rotate[5])
	leg_mask[8] = pygame.mask.from_surface(leg[8])
	leg_rect[8] = leg[8].get_rect()


	mx += movex
	my += movey

	for i in range(0,3):
		offset = (int(mx + leg_offset + (i  * difference) - ox), int(my + leg_height - oy))
		result = obstacle_mask.overlap(leg_mask[i], offset)
		for j in range(0,3):
			if i is not j and not result:
				offset = (int((mx  + leg_offset + (i  * difference)) - (mx  + leg_offset + (j  * difference))), int(0.0))
				result = leg_mask[j].overlap(leg_mask[i], offset)

		if result:
			mx -= movex
			my -= movey
			if spin[i] is not 0.0:
				rotate[i] -= spin[i]
				leg[i] = pygame.image.load("image_resources/leg.png").convert_alpha()
				leg[i] = rot_center(leg[i], rotate[i])
				leg_mask[i] = pygame.mask.from_surface(leg[i])
				leg_rect[i] = leg[i].get_rect()

	for i in range(0, 3):
		temp[i][0] = math.sin(rotate[i] / 180 * math.pi) * leg_length
		temp[i][1] = -math.cos((180.0 + rotate[i]) / 180 * math.pi) * leg_length
	for i in range(3, 5):
		temp[i][0] = math.cos(rotate[i] / 180 * math.pi)
		temp[i][1] = math.sin((180.0 + rotate[i]) / 180 * math.pi)
		temp_two[i - 3][0] = -math.sin((180.0 + rotate[i]) / 180 * math.pi) * 4
		temp_two[i - 3][1] = math.cos(rotate[i] / 180 * math.pi) * 4

	print(temp_two[1][0], " ", temp_two[1][1])

	DS.blit(background, (int(0), int(0)))
	DS.blit(obstacle, (int(ox), int(oy)))
	DS.blit(leg[6], (int(mx), int(my)))
	DS.blit(leg[7], (int(mx + (temp[4][0] * 39)), int(my + (temp[4][1] * 39))))
	DS.blit(leg[8], (int(mx + (temp[4][0] * 39) + (temp[3][0] * 39)), int(my + (temp[4][1] * 39) + (temp[3][1] * 39))))

	DS.blit(leg[0], (int(mx + 38 + (temp[4][0] * 12) + temp_two[1][0]), int(my + 40 + (temp[4][1] * 12)  + temp_two[1][1])))
	DS.blit(leg[1], (int(mx + 38 + (temp[4][0] * 39) + temp_two[1][0]), int(my + 40 + (temp[4][1] * 39) + temp_two[1][1])))
	DS.blit(leg[2], (int(mx + 38 + (temp[4][0] * 41) + (temp[3][0] * 25) + temp_two[0][0]), int(my + 40 + (temp[4][1] * 41) + (temp[3][1] * 25) + temp_two[0][1])))

	DS.blit(leg[3], (int(mx + 38 + (temp[4][0] * 12) + (temp[0][0] * 1.15) + temp_two[1][0]), int(my + 40 + (temp[4][1] * 12) + (temp[0][1] * 1.15) + temp_two[1][1])))
	DS.blit(leg[4], (int(mx + 38 + (temp[4][0] * 39) + (temp[1][0] * 1.15) + temp_two[1][0]), int(my + 40 + (temp[4][1] * 39) + (temp[1][1] * 1.15) + temp_two[1][1])))
	DS.blit(leg[5], (int(mx + 38 + (temp[4][0] * 41) + (temp[3][0] * 25) + (temp[2][0] * 1.15) + temp_two[0][0]), int(my + 40 + (temp[4][1] * 41) + (temp[3][1]) * 25 + (temp[2][1] * 1.15) + temp_two[0][1])))

	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)