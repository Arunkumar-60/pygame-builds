import pygame
import time
import random

# Initialize pygame
pygame.init()

# Initialize font

FONT = pygame.font.SysFont('Arial', 32)

# Set window size

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Set up the window

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Title, Background image and ICON

pygame.display.set_caption("Rain Dodge!")

ICON = pygame.image.load('./public/img/raindrop.png')

pygame.display.set_icon(ICON)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('./public/img/black.jpg'),(WINDOW_WIDTH, WINDOW_HEIGHT))


# Player object

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

PLAYER_VELOCITY = 5


# FONT

FONT = pygame.font.SysFont('Arial', 32)

def draw(player,elapsed_time):
    
    GAME_WINDOW.blit(BACKGROUND_IMAGE , (0,0))
    pygame.draw.rect(GAME_WINDOW, "lavender" , player)

    score_text = FONT.render("Score: " + str(int(elapsed_time)), True, (255,255,255))
    GAME_WINDOW.blit(score_text, (10, 10))
    pygame.display.update()







# Game Loop

def main():
    run = True

    player = pygame.Rect(200, WINDOW_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock  = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0


    while run:
        clock.tick(90)
        elapsed_time = time.time() - start_time

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT or pygame.K_a] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT or pygame.K_d] and player.x + PLAYER_WIDTH + PLAYER_VELOCITY <= (WINDOW_WIDTH):
            player.x += PLAYER_VELOCITY
        
        draw(player,elapsed_time)

    
    pygame.quit()

if __name__ == "__main__":
    main()