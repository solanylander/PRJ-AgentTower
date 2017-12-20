#Code by Umut Bilgic, Ankara, Turkey.
#Public release: 11/16/2013
#Release version: 1.1 Beta - Working coin and point system.
 
from pygame.locals import *
import pygame
import sys
import time
import random
import math
 
image_resources = "image_resources/"
sound_resources = "sound_resources/"
 
width,height = 400,400
size = (width,height)
 
clock = pygame.time.Clock()
FPS = 115
 
coin_offset = 60
points = -1
kill_switch = 0
 
def quit_game():
    pygame.quit()
    sys.exit("System exit.")
 
class GetSource:
    def background(self,image):
        return pygame.image.load(image_resources + image).convert()
    def player(self,image):
        return pygame.image.load(image_resources + image).convert_alpha()
   
class Wall(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(pygame.color.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class Player(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_resources + image).convert_alpha()
        self.rect = self.image.get_rect()
       
class Coin(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_resources + image).convert_alpha()
        self.rect = self.image.get_rect()
       
pygame.init()
 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame App")
background = GetSource().background("bg_solid_black_square.jpg")
player = GetSource().player("red_rectangle.png")
player_dimension = player.get_width()
 
x,y = width/2-player_dimension,height/2-player_dimension
movex,movey = 0,0
 
walls = pygame.sprite.Group()
players = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
 
wall_1 = Wall("white", 0, 0, width, 5)
wall_2 = Wall("white", 0, 0, 5, height)
wall_3 = Wall("white", 0, height-5, width, 5)
wall_4 = Wall("white", width-5, 0, 5, height)
player = Player("red_rectangle.png")
coin = Coin("coin.png")
 
walls.add(wall_1,wall_2,wall_3,wall_4)
players.add(player)
coins.add(coin)
all_sprites.add(wall_1,wall_2,wall_3,wall_4,player,coin)
player.image = pygame.transform.rotate(player.image,30)
 
while True:
 
    clock.tick(FPS)
 
    ticks = pygame.time.get_ticks()
   
    collide_list_1 = pygame.sprite.spritecollideany(wall_1,players)
    collide_list_2 = pygame.sprite.spritecollideany(wall_2,players)
    collide_list_3 = pygame.sprite.spritecollideany(wall_3,players)
    collide_list_4 = pygame.sprite.spritecollideany(wall_4,players)
    collide_list_5 = pygame.sprite.spritecollideany(coin,  players)
   
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        if event.type == KEYDOWN:
            if event.key == K_q:
                quit_game()
            elif event.key == K_a:
                movex = -1
            elif event.key == K_d:
                movex = 1
            elif event.key == K_w:
                movey = -1
            elif event.key == K_s:
                movey = 1
               
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                movex = 0
            if event.key == K_w or event.key == K_s:
                movey = 0
 
    if collide_list_1 != None:
        movey = 0
        y += 1
    if collide_list_2 != None:
        movex = 0
        x += 1
    if collide_list_3 != None:
        movey = 0
        y -= 1
    if collide_list_4 != None:
        movex = 0
        x -= 1
    else:    
        x += movex
        y += movey
 
    player.rect.x = x
    player.rect.y = y
 
    screen.blit(background, (0,0))
 
    if  kill_switch == 0:
        coin.rect.x = random.randint(0,width-coin_offset)
        coin.rect.y = random.randint(0,height-coin_offset)
        kill_switch = 1
       
    pygame.display.set_caption("Points: "+str(points))
   
    if collide_list_5 != None:
        points += 1
        coin.rect.x = random.randint(0,width-coin_offset)
        coin.rect.y = random.randint(0,height-coin_offset)
                                   
    all_sprites.draw(screen)
    all_sprites.update()
   
    pygame.display.update()