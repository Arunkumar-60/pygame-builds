import pygame
import random
import os
import time

# Path

IMAGE_PATH = 'Assets/Img'
AUDIO_PATH = 'Assets/Audio'

#
padding_x=10
padding_y = 20
offset_X=padding_x/2
offset_y=padding_y/2

# Initialize pygame
pygame.init()

# Initialize font
pygame.font.init()

# Define colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (104, 104, 104)

# Set Game Speed

FPS = 60
PLAYER_VELOCITY = 5

# Load Fonts


HEALTH_FONT = pygame.font.SysFont('arial', 30)


# load Images

RED_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_ship_red_small.png'))

GREEN_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_ship_green_small.png'))

BLUE_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_ship_blue_small.png'))


# THIS IS PLAYER SHIP IMAGE

YELLOW_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_ship_yellow.png'))

# load Bullet Images

RED_LASER_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_laser_red.png'))

GREEN_LASER_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_laser_green.png'))

BLUE_LASER_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_laser_blue.png'))

YELLOW_LASER_IMAGE = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_laser_yellow.png'))



# Set window size

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Set up the window

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

GAME_STATS = pygame.Rect(0,0,WINDOW_WIDTH,40)

# Title, Background image and ICON

pygame.display.set_caption("Space Invaders")

ICON = pygame.image.load(os.path.join(
    IMAGE_PATH,'pixel_ship_yellow.png'))

pygame.display.set_icon(ICON)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/Img', 'background-black.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.cooldown_counter = 0
    
    def draw(self, window):
        pygame.draw.rect(GAME_WINDOW, RED , (self.x,self.y,50,50))


# Game loop
def main():
    run = True
    clock = pygame.time.Clock()
    level = 1
    lives = 5

    ship = Ship(300,650)


    def redraw_window():
        lives_label = HEALTH_FONT.render(f'Lives: {lives}',1, WHITE)
        level_label = HEALTH_FONT.render(f'Level: {level}',1, WHITE)

        GAME_WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
       
        GAME_STATS.width= WINDOW_WIDTH
        GAME_STATS.height= max(lives_label.get_height(),level_label.get_height()) + padding_y*2
        pygame.draw.rect(GAME_WINDOW, GREY, GAME_STATS)
        GAME_WINDOW.blit(lives_label, (padding_x, padding_y))
        GAME_WINDOW.blit(level_label, (WINDOW_WIDTH-level_label.get_width()-padding_x,padding_y))
        ship.draw(GAME_WINDOW)





        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (ship.x-PLAYER_VELOCITY>0): #left
            ship.x -= PLAYER_VELOCITY
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (ship.x-PLAYER_VELOCITY + 50)<WINDOW_WIDTH: #right
            ship.x += PLAYER_VELOCITY
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (ship.y - PLAYER_VELOCITY > 0 + GAME_STATS.height ): #up
            ship.y -= PLAYER_VELOCITY
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (ship.y + PLAYER_VELOCITY + 50 <WINDOW_HEIGHT): #down
            ship.y += PLAYER_VELOCITY




        redraw_window()




if __name__ == "__main__":
    main()