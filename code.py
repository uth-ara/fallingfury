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

# Load Pixel Font
font = pygame.font.Font("assets/font/pixel_font.ttf", 28)  # Adjust font size for better fit
title_font = pygame.font.Font("assets/font/pixel_font.ttf", 70)  # Larger font for title

# Load button images with transparency
play_button = pygame.image.load("assets/images/play_button.png")
quit_button = pygame.image.load("assets/images/quit_button.png")
play_again_button = pygame.image.load("assets/images/play_again.png")

play_button = pygame.transform.scale(play_button, (300, 80))
quit_button = pygame.transform.scale(quit_button, (300, 80))
play_again_button = pygame.transform.scale(play_again_button, (300, 80))

play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
quit_button_rect = quit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
play_again_button_rect = play_again_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Starfield effect
def generate_stars(count=100):
    return [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 4)] for _ in range(count)]

def update_stars(stars):
    for star in stars:
        star[1] += 0.5  # Move stars down slowly
        if star[1] > HEIGHT:
            star[1] = 0  # Reset star to top
            star[0] = random.randint(0, WIDTH)

def draw_stars(stars):
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

stars = generate_stars()

def draw_text(text, x, y, font, color=WHITE):
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)

def main_menu():
    while True:
        screen.fill(BLACK)  # Set black background
        update_stars(stars)
        draw_stars(stars)  # Draw moving stars
        
        # Title Text with proper padding
        draw_text("FALLING", WIDTH // 2, HEIGHT // 4 - 50, title_font, WHITE)
        draw_text("FURY", WIDTH // 2, HEIGHT // 4 + 20, title_font, WHITE)
        
        # Draw buttons
        screen.blit(play_button, play_button_rect)
        screen.blit(quit_button, quit_button_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return  # Start game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        
        pygame.display.update()

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        
        draw_text(f"Game Over! Score: {score}", WIDTH // 2, HEIGHT // 3, font, WHITE)
        
        # Draw buttons
        screen.blit(play_again_button, play_again_button_rect)
        screen.blit(quit_button, quit_button_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    return "restart"  # Restart game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        
        pygame.display.update()

def game_loop():
    clock = pygame.time.Clock()
    running = True
    score = 0  # Placeholder score variable
    while running:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Allow ESC to trigger game over screen
        
        pygame.display.update()
        clock.tick(30)
    
    return game_over_screen(score)

# Run main menu first
while True:
    main_menu()
    action = game_loop()
    if action != "restart":
        break  # Quit if the user does not choose to restart

pygame.quit()
