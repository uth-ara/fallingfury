import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Fury")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load fonts
font = pygame.font.Font(r"C:\Users\user\Desktop\compare\pixel_font.TTF", 28)  # Adjust font size for better fit
title_font = pygame.font.Font(r"C:\Users\user\Desktop\compare\pixel_font.TTF", 70)  # Larger font for title


# Load images
play_button = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\play_button.png").convert_alpha()
quit_button = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\quit_button.png").convert_alpha()
play_again_button = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\play_again.png").convert_alpha()
player_image = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\ship.png").convert_alpha()
monster_image = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\monster.png").convert_alpha()
meteor_image = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\meteor.png").convert_alpha()
heart_image = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\heart.png").convert_alpha()
monster_ball_image = pygame.image.load(r"C:\Users\user\fallingfury\assets\images\bomb.png").convert_alpha()
# Resize images
play_button = pygame.transform.scale(play_button, (300, 80))
quit_button = pygame.transform.scale(quit_button, (300, 80))
play_again_button = pygame.transform.scale(play_again_button, (300, 80))
player_image = pygame.transform.scale(player_image, (50, 50))
monster_image = pygame.transform.scale(monster_image, (80, 80))
meteor_image = pygame.transform.scale(meteor_image, (30, 30))
heart_image = pygame.transform.scale(heart_image, (30, 30))

# Load and scale monster's ball image

ball_size = (25, 25)  # Adjust size
monster_ball_image = pygame.transform.scale(monster_ball_image, ball_size) 

# Button positions
play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
quit_button_rect = quit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
play_again_button_rect = play_again_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))


# Starfield effect
def generate_stars(count=100):
    return [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 4)] for _ in range(count)]

def update_stars(stars):
    for star in stars:
        star[1] += 1  # Increase speed
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

def draw_stars(stars):
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

# Game variables
stars = generate_stars()
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 60
player_speed = 5
monster_x, monster_y = 120,90  # Monster in top-left
bombs = []
lives = 5
score = 0

def draw_lives():
    for i in range(lives):
        screen.blit(heart_image, (20 + i * 35, 20))

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 300, 20))

def draw_monster():
    screen.blit(monster_image, (monster_x, monster_y))

def draw_monster_balls():
    global monster_balls
    for ball in monster_balls:
        screen.blit(monster_ball_image, (ball[0], ball[1]))  # Draw ball


def draw_bombs():
    for bomb in bombs:
        screen.blit(meteor_image, (bomb[0], bomb[1]))

def main_menu():
    while True:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        draw_text("FALLING", WIDTH // 2, HEIGHT // 4 - 50, title_font, WHITE)
        draw_text("FURY", WIDTH // 2, HEIGHT // 4 + 20, title_font, WHITE)
        screen.blit(play_button, play_button_rect)
        screen.blit(quit_button, quit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
def game_over_screen():
    while True:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        
        draw_text(f"Game Over! Score: {score}", WIDTH // 2, HEIGHT // 3, font, WHITE)
        screen.blit(play_again_button, play_again_button_rect)
        screen.blit(quit_button, quit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    return "restart"
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
def draw_text(text, x, y, font, color=WHITE):
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)

def game_loop():
    global player_x, lives, score
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Player movement
        #bomb movement
        screen.blit(player_image, (player_x, player_y))
        draw_monster()
        draw_bombs()
        draw_lives()
        draw_score()
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.quit()

# Run game
while True:
    main_menu()
    action = game_loop()
    if action != "restart":
        break # type: ignore