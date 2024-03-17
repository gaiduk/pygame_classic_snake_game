import pygame, random


pygame.init()


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SnakE")



# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 + 100

snake_dx = 0
snake_dy = 0

score = 0

# Set colors
GREEN = (0, 255, 0)
DARKGREEN = (11, 52, 11)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255)

# Set fonts
font = pygame.font.SysFont('gabriola', 48)

# Set text
title_text = font.render("~~Snake~~", True, GREEN, DARKGREEN)
title_text_rect = title_text.get_rect()
title_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

game_over_text = font.render("GAME OVER", True, RED, DARKGREEN)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to try again", True, RED, DARKGREEN)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 68)


# Set audio
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")

# Set images (rect)
apple_coord = (random.randint(50, WINDOW_WIDTH - 50), random.randint(50, WINDOW_HEIGHT - 50), SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord= (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coord= []

# main game loop


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake_dx = SNAKE_SIZE
                snake_dy = 0

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    # Update score
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)

    # Добавляем коорд головы на первое место массива, и удаляем последний элемент массива
    body_coord.insert(0, head_coord)
    body_coord.pop()

    # Update coord of the snake head
    head_x = head_x + snake_dx
    head_y = head_y + snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for game over
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH\
            or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coord:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(continue_text, continue_text_rect)
        pygame.display.update()

        in_pause = True
        while in_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    head_x = WINDOW_WIDTH // 2
                    head_y = WINDOW_HEIGHT // 2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    snake_dx = 0
                    snake_dy = 0
                    body_coord = []
                    score = 0

                    in_pause = False

                if event.type == pygame.QUIT:
                    in_pause = False
                    running = False

    # Check collision
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coord.append(head_coord)

    # fill surface
    display_surface.fill(WHITE)

    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(score_text, score_text_rect)

    # Blit assets
    for body in body_coord:
        pygame.draw.rect(display_surface, DARKGREEN, body)

    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    # Update display and clock tick
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()