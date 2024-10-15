import pygame
import random

# Initialize pygame
pygame.init()

# Set the game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set game clock and FPS
clock = pygame.time.Clock()
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
dino_img = pygame.image.load('dino.png')  # Use a small dino image file here
cactus_img = pygame.image.load('cactus.png')  # Use a small cactus image file

# Game variables
ground_y = SCREEN_HEIGHT - 70
dino_x, dino_y = 50, ground_y - 40
dino_width, dino_height = 40, 40
jump_height = 150
jumping = False
gravity = 10
velocity_y = 0

# Cactus settings
cactus_speed = 10
cacti = []

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_dino(x, y):
    screen.blit(dino_img, (x, y))

def draw_cactus(cacti):
    for cactus in cacti:
        screen.blit(cactus_img, (cactus[0], cactus[1]))

def generate_cactus():
    cactus_x = SCREEN_WIDTH
    cactus_y = ground_y - 40
    return [cactus_x, cactus_y]

def detect_collision(dino_rect, cactus_rect):
    return dino_rect.colliderect(cactus_rect)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Jumping mechanism
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        velocity_y = -gravity * 2

    # Dino jumping logic
    if jumping:
        dino_y += velocity_y
        velocity_y += gravity
        if dino_y >= ground_y - dino_height:
            dino_y = ground_y - dino_height
            jumping = False

    # Generate new cactus
    if len(cacti) == 0 or cacti[-1][0] < SCREEN_WIDTH - 200:
        cacti.append(generate_cactus())

    # Move and draw cactus
    for cactus in cacti:
        cactus[0] -= cactus_speed

    # Remove cactus if it moves off screen
    if cacti[0][0] < -40:
        cacti.pop(0)
        score += 1  # Increase score when player dodges a cactus

    # Detect collisions
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    for cactus in cacti:
        cactus_rect = pygame.Rect(cactus[0], cactus[1], 40, 40)
        if detect_collision(dino_rect, cactus_rect):
            running = False

    # Draw the game objects
    draw_dino(dino_x, dino_y)
    draw_cactus(cacti)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(FPS)

# Quit the game
pygame.quit()
