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

# Load assets and scale images
dino_img = pygame.image.load('dino.png')
cactus_img = pygame.image.load('cactus.png')

# Scale the images to appropriate sizes
dino_img = pygame.transform.scale(dino_img, (40, 40))  # Dino size: 40x40
cactus_img = pygame.transform.scale(cactus_img, (30, 60))  # Cactus size: 30x60

# Game variables
ground_y = SCREEN_HEIGHT - 70
dino_x, dino_y = 50, ground_y - 40
dino_width, dino_height = 40, 40
jumping = False
gravity = 1.5
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
    # Randomize cactus height by moving it vertically between two heights
    cactus_y = random.choice([ground_y - 60, ground_y - 50, ground_y - 70])  # Random heights
    return [cactus_x, cactus_y]

def detect_collision(dino_rect, cactus_rect):
    return dino_rect.colliderect(cactus_rect)

def reset_game():
    global dino_y, jumping, velocity_y, cacti, score
    dino_y = ground_y - dino_height
    jumping = False
    velocity_y = 0
    cacti = []
    score = 0

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
        velocity_y = -15  # Initial velocity when jumping

    # Dino jumping logic
    if jumping:
        dino_y += velocity_y
        velocity_y += gravity
        if dino_y >= ground_y - dino_height:  # Ground collision detection
            dino_y = ground_y - dino_height
            jumping = False

    # Generate new cactus with random spacing
    if len(cacti) == 0 or cacti[-1][0] < SCREEN_WIDTH - random.randint(150, 400):  # Randomized distance
        cacti.append(generate_cactus())

    # Move and draw cactus
    for cactus in cacti:
        cactus[0] -= cactus_speed

    # Remove cactus if it moves off screen
    if cacti and cacti[0][0] < -40:
        cacti.pop(0)
        score += 1  # Increase score when player dodges a cactus

    # Detect collisions
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    for cactus in cacti:
        cactus_rect = pygame.Rect(cactus[0], cactus[1], 30, 60)  # Adjust cactus size for collision
        if detect_collision(dino_rect, cactus_rect):
            # Game Over
            print(f"Game Over! Your score: {score}")
            reset_game()

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
