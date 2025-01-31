import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Initialize font
pygame.font.init()

# Initialize pygame sounder
pygame.mixer.init()


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Laser+1.mp3'))

GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Game_Over.wav'))

YELLOW_WINS_SOUND = pygame.mixer.Sound(os.path.join('Assets','Yellow_Wins.mp3'))

RED_WINS_SOUND = pygame.mixer.Sound(os.path.join('Assets','RED_Wins.mp3'))

DRAW_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Draw.wav'))


# Set window size

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GAME_BORDER_WIDTH = 10


# Define colors

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

GREY = (104,104,104)


# Set up the window

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

GAME_BORDER = pygame.Rect((WINDOW_WIDTH//2) - (GAME_BORDER_WIDTH//2) ,0,10,WINDOW_HEIGHT)

GAME_STATS = pygame.Rect(0,0,WINDOW_WIDTH,60)
# Define FONTS

HEALTH_FONT = pygame.font.SysFont('arial', 30)
WINNER_FONT = pygame.font.SysFont('comicsans',80)


# Title, Background image and ICON

pygame.display.set_caption("Space Dodge!")

ICON = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))

pygame.display.set_icon(ICON)



BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')),(WINDOW_WIDTH, WINDOW_HEIGHT))

# Game Speed

FPS = 60
SPACESHIP_VELOCITY = 5
BULLET_VELOCITY = 10

# SPACESHIP object

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))



SPACESHIP_WIDTH  = 100
SPACESHIP_HEIGHT= 100

# SPACE BULLETS
BULLET_WIDTH=10
BULLET_HEIGHT=5
MAX_BULLETS = 7



#SPACESHIP CONFIG AND POSITIONING 

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

#SPACESHIP HEALTH CONFIGURATION

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2



def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_ammo, yellow_ammo):
    # Clear background and draw borders
    GAME_WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.draw.rect(GAME_WINDOW, WHITE, GAME_BORDER)
    
    # Render health and ammo texts
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, RED)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, YELLOW)
    red_ammo_text = HEALTH_FONT.render(f"Ammo Left: {red_ammo}", 1, RED)
    yellow_ammo_text = HEALTH_FONT.render(f"Ammo Left: {yellow_ammo}", 1, YELLOW)

    # Calculate the maximum width of any text
    max_width = max(red_health_text.get_width(), yellow_health_text.get_width(), 
                    red_ammo_text.get_width(), yellow_ammo_text.get_width())
    
    # Add some padding around the texts
    padding = 10

    # Dynamically resize the width of GAME_STATS to fit the longest text
    GAME_STATS.width = WINDOW_WIDTH  # Extra padding for left and right
    
    # Dynamically resize the height of GAME_STATS to fit two lines of text
    GAME_STATS.height = max(red_health_text.get_height(), red_ammo_text.get_height()) * 2 + padding  # Two lines of text

    # Draw background for the stats
    pygame.draw.rect(GAME_WINDOW, GREY, GAME_STATS)

    # Set vertical offset for positioning
    vertical_offset = padding

    # Draw Red Health and Ammo
    GAME_WINDOW.blit(red_health_text, (WINDOW_WIDTH - red_health_text.get_width() - padding, vertical_offset))
    GAME_WINDOW.blit(red_ammo_text, (WINDOW_WIDTH - red_ammo_text.get_width() - padding, vertical_offset + red_health_text.get_height()))

    # Draw Yellow Health and Ammo
    GAME_WINDOW.blit(yellow_health_text, (padding, vertical_offset))
    GAME_WINDOW.blit(yellow_ammo_text, (padding, vertical_offset + yellow_health_text.get_height()))

    # Draw the spaceships
    GAME_WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    GAME_WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw bullets for both players
    for yellow_bullet in yellow_bullets:
        pygame.draw.rect(GAME_WINDOW, YELLOW, yellow_bullet)

    for red_bullet in red_bullets:
        pygame.draw.rect(GAME_WINDOW, RED, red_bullet)

    # Update the display
    pygame.display.update()



# handle user inputs
# also now limiting the object within the game_board_window
def yellow_handle_movement(keys_pressed , yellow):
    if keys_pressed[pygame.K_a] and yellow.x-SPACESHIP_VELOCITY>0: #left
        yellow.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_d] and (yellow.x+SPACESHIP_VELOCITY+SPACESHIP_WIDTH-(GAME_BORDER_WIDTH/2))<(GAME_BORDER.x): #right
        yellow.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y-SPACESHIP_VELOCITY-GAME_STATS.height>0: #up
        yellow.y -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_s] and (yellow.y+SPACESHIP_VELOCITY+SPACESHIP_HEIGHT)<(WINDOW_HEIGHT): #down
        yellow.y += SPACESHIP_VELOCITY

def red_handle_movement(keys_pressed , red):
    if keys_pressed[pygame.K_LEFT] and red.x-SPACESHIP_VELOCITY>(GAME_BORDER.x+GAME_BORDER_WIDTH): #left
        red.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x+SPACESHIP_WIDTH+SPACESHIP_VELOCITY<(WINDOW_WIDTH): #right
        red.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_UP] and (red.y-SPACESHIP_VELOCITY-GAME_STATS.height)>0: #up
        red.y -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_DOWN] and (red.y+SPACESHIP_VELOCITY+SPACESHIP_HEIGHT)<WINDOW_HEIGHT: #down
        red.y += SPACESHIP_VELOCITY

def handle_bullets(yellow_bullets, red_bullets , yellow, red):
    for yellow_bullet in yellow_bullets:
        yellow_bullet.x += BULLET_VELOCITY
        if red.colliderect(yellow_bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(yellow_bullet)
        if yellow_bullet.x>WINDOW_WIDTH:
            yellow_bullets.remove(yellow_bullet)

    for red_bullet in red_bullets:
        red_bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(red_bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(red_bullet)
        if red_bullet.x<0-BULLET_WIDTH:
            red_bullets.remove(red_bullet)

def display_winner(text):
    if text=='YELLOW WINS!':
        draw_text = WINNER_FONT.render(text,1,YELLOW)
        YELLOW_WINS_SOUND.play()

    elif text=='RED WINS!':
        draw_text = WINNER_FONT.render(text,1,RED)
        RED_WINS_SOUND.play()

    elif text == 'IT IS A DRAW!':
        draw_text = WINNER_FONT.render(text,1,WHITE)
        DRAW_SOUND.play()
        pygame.time.delay(3000)
        pygame.mixer.stop()
        
    
    GAME_WINDOW.blit(draw_text,( ((WINDOW_WIDTH/2)-(draw_text.get_width()/2))  , (WINDOW_HEIGHT/2 - draw_text.get_height()/2)) )
    pygame.display.update()
    
def reset_main():
    red = pygame.Rect(800,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    red_ammo = 50
    yellow_ammo=50

    return red, yellow, yellow_bullets, red_bullets, red_health, yellow_health, red_ammo, yellow_ammo
    


def main():
    red = pygame.Rect(800,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    red_ammo = 50
    yellow_ammo = 50

    # Game loop
    clock = pygame.time.Clock()
    run = True

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS and yellow_ammo>0:
                    yellow_ammo -=1  # decrease ammo count when shooting
                    yellow_bullet=pygame.Rect(yellow.x+SPACESHIP_WIDTH, yellow.y+(SPACESHIP_HEIGHT//2) , BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(yellow_bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS and red_ammo>0:
                    red_ammo -=1  # decrease ammo count when shooting
                    red_bullet=pygame.Rect(red.x,red.y+(SPACESHIP_HEIGHT//2), BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(red_bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()
        
        
        winner_text=''

        if yellow_health<=0:
            winner_text = "RED WINS!"
        
        if red_health<=0:
            winner_text = "YELLOW WINS!"
        
        if red_ammo == 0 and yellow_ammo == 0 and red_bullets==[] and yellow_bullets==[]:
            if red_health>yellow_health:
                winner_text = "RED WINS!"
            elif yellow_health>red_health:
                winner_text = "YELLOW WINS!"
            elif red_health == yellow_health:
                winner_text = "IT IS A DRAW!"
        
        if winner_text!= '':
            
            GAME_OVER_SOUND.play()
            pygame.time.delay(1000)
            display_winner(winner_text)
            pygame.time.delay(4000)
            pygame.event.clear()
            red, yellow, yellow_bullets, red_bullets, red_health, yellow_health, red_ammo, yellow_ammo = reset_main()
            


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        draw(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health,red_ammo,yellow_ammo)

    




    


if __name__ == "__main__":
    main()