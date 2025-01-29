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


# Ship dimensions

SHIP_WIDTH = 60
SHIP_HEIGHT = 60

#enemies

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50


def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (offset_y,offset_y)) != None

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, LASER_VELOCITY):
        self.y -= LASER_VELOCITY
    
    def off_screen(self,height):
        return not (self.y <= height and self.y>=0)
    
    def collision(self, obj):
        return collide(self, obj)


class Ship:
    
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.cooldown_counter = 0
        self.lasers=[]
    

    
    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for lasers in self.lasers:
            lasers.draw(window)
    
    def move_lasers(self,LASER_VELOCITY,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(LASER_VELOCITY)
            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(objs):
                self.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter =0
        elif self.cooldown_counter > 0:
            self.cooldown_counter = 0

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.get_width() // 2 - 5, self.y - 10, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)

        self.ship_img = pygame.transform.scale(YELLOW_SPACE_SHIP_IMAGE,(SHIP_WIDTH,SHIP_HEIGHT))
        self.laser_img = YELLOW_LASER_IMAGE
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health =  health
        
    
    def move_lasers(self,LASER_VELOCITY,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(LASER_VELOCITY)
            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


class Enemy(Ship):
    #dictonary to map issues
    COLOR_MAP = {
        RED: (pygame.transform.rotate(pygame.transform.scale(RED_SPACE_SHIP_IMAGE,(ENEMY_WIDTH,ENEMY_HEIGHT)),180),RED_LASER_IMAGE),
        GREEN: (pygame.transform.rotate(pygame.transform.scale(GREEN_SPACE_SHIP_IMAGE,(ENEMY_WIDTH,ENEMY_HEIGHT)),180),GREEN_LASER_IMAGE),
        BLUE: (pygame.transform.rotate(pygame.transform.scale(BLUE_SPACE_SHIP_IMAGE,(ENEMY_WIDTH,ENEMY_HEIGHT)),180),BLUE_LASER_IMAGE)
    }
    def __init__(self, x, y,color ,health=100):
        super().__init__(x, y, health)

        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    def move(self,ENEMY_VELOCITY):
        self.y += ENEMY_VELOCITY

# Game loop
def main():
    run = True
    level = 1
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont('arial',50)
    lost_font = pygame.font.SysFont('arial', 70)

    WAVE_LENGTH = 0
    ENEMY_VELOCITY =1
    LASER_VELOCITY = 4
    lost = False
    player = Player(300,650)
    
    enemies = []


    def redraw_window():
        lives_label = HEALTH_FONT.render(f'Lives: {lives}',1, WHITE)
        level_label = HEALTH_FONT.render(f'Level: {level}',1, WHITE)

        GAME_WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
       
        GAME_STATS.width= WINDOW_WIDTH
        GAME_STATS.height= max(lives_label.get_height(),level_label.get_height()) + padding_y*2
        
        
        for enemy in enemies:
            enemy.draw(GAME_WINDOW)
        player.draw(GAME_WINDOW)

        



        pygame.draw.rect(GAME_WINDOW, GREY, GAME_STATS)
        GAME_WINDOW.blit(lives_label, (padding_x, padding_y))
        GAME_WINDOW.blit(level_label, (WINDOW_WIDTH-level_label.get_width()-padding_x,padding_y))
        if lost:
            GAME_WINDOW.blit(lost_font.render('Game Over!',1, RED), (WINDOW_WIDTH/2 - lost_font.render('Game Over!',1, RED).get_width()/2, WINDOW_HEIGHT/2))


        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <=0 or player.health <=0:
            lost = True

            lost_count +=1
            if lost_count > 3 * FPS:
                run=False
            else:
                continue

            
        if len(enemies)==0:
            level += 1
            WAVE_LENGTH += 5
            for i in range(WAVE_LENGTH):
                enemy = Enemy(random.randrange(50, WINDOW_WIDTH-50-ENEMY_WIDTH),random.randint(-1000,-10),random.choice([RED,GREEN,BLUE]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (player.x-PLAYER_VELOCITY > 0): #left
            player.x -= PLAYER_VELOCITY
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (player.x+PLAYER_VELOCITY) < WINDOW_WIDTH - player.get_width() : #right
            player.x += PLAYER_VELOCITY
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (player.y - PLAYER_VELOCITY > 0 + GAME_STATS.height ): #up
            player.y -= PLAYER_VELOCITY
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (player.y + PLAYER_VELOCITY + player.get_height() <WINDOW_HEIGHT ): #down
            player.y += PLAYER_VELOCITY
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(ENEMY_VELOCITY)
            enemy.move_lasers(LASER_VELOCITY,player)
            if enemy.y + enemy.get_height() > WINDOW_HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers( 0 - LASER_VELOCITY , enemies)
        redraw_window()




if __name__ == "__main__":
    main()