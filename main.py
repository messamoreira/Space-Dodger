import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Dodger")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# Meteors
meteor_size = 50
meteors = []

# Clock and score
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont(None, 35)

def detect_collision(player_pos, meteor_pos):
    p_x, p_y = player_pos
    m_x, m_y = meteor_pos
    if (m_x < p_x < m_x + meteor_size or p_x < m_x < p_x + player_size) and \
       (m_y < p_y < m_y + meteor_size or p_y < m_y < p_y + player_size):
        return True
    return False

# Game loop
running = True
meteor_frequency = 25
meteor_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Create meteors
    meteor_timer += 1
    if meteor_timer > meteor_frequency:
        meteor_timer = 0
        new_meteor_pos = [random.randint(0, WIDTH - meteor_size), 0]
        new_meteor_speed = random.randint(5, 15)
        meteors.append([new_meteor_pos, new_meteor_speed])

    # Move and draw meteors
    for meteor in meteors[:]:
        meteor[0][1] += meteor[1]
        if meteor[0][1] > HEIGHT:
            meteors.remove(meteor)

    # Collision detection
    for meteor in meteors:
        if detect_collision(player_pos, meteor[0]):
            running = False
            break

    # Update score
    score = pygame.time.get_ticks() // 1000

    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw meteors
    for meteor in meteors:
        pygame.draw.rect(screen, RED, (meteor[0][0], meteor[0][1], meteor_size, meteor_size))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("Game Over", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

# Wait for a moment before quitting
pygame.time.wait(2000)

pygame.quit()
sys.exit()
