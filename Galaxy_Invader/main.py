import pygame
import math
import time
import os
import random


# Initialize pygame

pygame.init()

# Initialize font

pygame.font.init()


#path
IMG_PATH = 'Assets/Img'

WIDTH , HEIGHT = 800,800
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

# Title, Background image and ICON

pygame.display.set_caption("Space Invaders")

ICON = pygame.image.load(os.path.join(IMG_PATH, 'pixel_ship_yellow.png'))

pygame.display.set_icon(ICON)



# Define colors

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

GREY = (104,104,104)

def rotate(a):
    return pygame.transform.rotate(a, 180)

# Load images
RED_SPACE_SHIP = rotate(pygame.image.load(os.path.join(IMG_PATH, 'pixel_ship_red_small.png')))

GREEN_SPACE_SHIP = rotate(pygame.image.load(os.path.join(IMG_PATH, 'pixel_ship_green_small.png')))

BLUE_SPACE_SHIP = rotate(pygame.image.load(os.path.join(IMG_PATH, 'pixel_ship_blue_small.png')))

#player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(IMG_PATH, 'pixel_ship_yellow.png'))

# Lasers

RED_LASER = pygame.image.load(os.path.join(IMG_PATH, 'pixel_laser_red.png'))

GREEN_LASER = pygame.image.load(os.path.join(IMG_PATH, 'pixel_laser_green.png'))

BLUE_LASER = pygame.image.load(os.path.join(IMG_PATH, 'pixel_laser_blue.png'))

YELLOW_LASER = pygame.image.load(os.path.join(IMG_PATH, 'pixel_laser_yellow.png'))

# Background

BG = pygame.transform.scale(pygame.image.load(os.path.join(IMG_PATH, 'background-black.png')),(WIDTH,HEIGHT))

# Set up the window



class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        pygame.draw.rect(window, RED , (self.x,self.y,50,50))

def main():
    run =True
    
    FPS=60
    level = 1
    lives = 5
    player_vel = 5
    main_font = pygame.font.SysFont('comicsans', 30)
    player = Ship(300,650)
    clock = pygame.time.Clock()

    


    def redraw_window():
        WIN.blit(BG, (0,0))
        lives_lebel = main_font.render(f"Lives : {lives}", 1 , WHITE)
        level_lebel = main_font.render(f"Level : {level}", 1, WHITE)

        WIN.blit(lives_lebel, (10,10))
        WIN.blit(level_lebel, (WIDTH - level_lebel.get_width() - 10, 10))
        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            # player movement 
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.x -= player_vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.x += player_vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            player.y -= player_vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            player.y += player_vel
main()