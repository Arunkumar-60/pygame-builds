import pygame
import time
import random

# Initialize pygame
pygame.init()

# Initialize font
pygame.font.init()

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

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 32

PLAYER_VELOCITY = 5

DROP_WIDTH = 5
DROP_HEIGHT = 10

DROP_VELOCITY = 3


# FONT

FONT= pygame.font.SysFont('arial', 30)

def draw(player,elapsed_time,drops):
    
    GAME_WINDOW.blit(BACKGROUND_IMAGE , (0,0))
    pygame.draw.rect(GAME_WINDOW, "lavender" , player)
    time_text=FONT.render(f'Time : {round(elapsed_time)}s',1,'white')
    GAME_WINDOW.blit(time_text,(10,10))
    for drop in drops:
        pygame.draw.rect(GAME_WINDOW, "lightblue", drop)


    pygame.display.update()







# Game Loop

def main():
    run = True

    player = pygame.Rect(200, WINDOW_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock  = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0


    # drop
    drop_add_increment = 2000
    drop_count = 0

    drops = []
    hit = False


    while run:

        drop_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if drop_count > drop_add_increment:
            for _ in range (random.randint(2,7)):
                drop_x = random.randint(0, WINDOW_WIDTH - DROP_WIDTH)
                drop = pygame.Rect(drop_x, -DROP_HEIGHT, DROP_WIDTH , DROP_HEIGHT)
                drops.append(drop)

            
            drop_add_increment = max(200, drop_add_increment - 50)
            drop_count = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT or pygame.K_a] and player.x - PLAYER_VELOCITY >=0:
            player.x -= PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT or pygame.K_d] and player.x + PLAYER_WIDTH + PLAYER_VELOCITY <= (WINDOW_WIDTH):
            player.x += PLAYER_VELOCITY

        
        for drop in drops[:]:
            drop.y += DROP_VELOCITY
            
            if drop.y > WINDOW_HEIGHT:
                drops.remove(drop)
            elif(drop.y + DROP_HEIGHT >= player.y) and (drop.colliderect(player)):
                drops.remove(drop)
                hit = True
                break

        if hit:
            lost_text = FONT.render('You lost', 1, 'white')
            GAME_WINDOW.blit(lost_text, (WINDOW_WIDTH//2 - lost_text.get_width()//2, WINDOW_HEIGHT//2 - lost_text.get_height()//2))
            score_text = FONT.render(f'Score : {round(elapsed_time)}s', 1, 'white')
            GAME_WINDOW.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 + lost_text.get_height()))
            pygame.display.update()
            time.sleep(10)
            break
            
        
        draw(player,elapsed_time, drops)

    
    pygame.quit()

if __name__ == "__main__":
    main()