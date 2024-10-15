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
RED = (255, 0, 0)
GRAY = (100, 100, 100)

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

# Game states
game_over = False

def draw_dino(x, y):
    screen.blit(dino_img, (x, y))

def draw_cactus(cacti):
    for cactus in cacti:
        screen.blit(cactus_img, (cactus[0], cactus[1]))

def generate_cactus():
    cactus_x = SCREEN_WIDTH
    cactus_y = random.choice([ground_y - 60, ground_y - 50, ground_y - 70])  # Random heights
    return [cactus_x, cactus_y]

def detect_collision(dino_rect, cactus_rect):
    return dino_rect.colliderect(cactus_rect)

def reset_game():
    global dino_y, jumping, velocity_y, cacti, score, game_over
    dino_y = ground_y - dino_height
    jumping = False
    velocity_y = 0
    cacti = []
    score = 0
    game_over = False

def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, font, BLACK, x + (width // 2) - 20, y + (height // 4))

def quit_game():
    pygame.quit()
    quit()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
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
                game_over = True

        # Draw the game objects
        draw_dino(dino_x, dino_y)
        draw_cactus(cacti)

        # Draw the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        # Game over screen with Retry and Quit buttons
        draw_text("Game Over", font, RED, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 3)
        draw_text(f"Your Score: {score}", font, BLACK, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 3 + 50)
        
        # Retry button
        draw_button("Retry", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50, GRAY, RED, reset_game)
        
        # Quit button
        draw_button("Quit", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 60, 160, 50, GRAY, RED, quit_game)

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(FPS)

# Quit the game
pygame.quit()
