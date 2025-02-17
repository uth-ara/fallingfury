import pygame
import random

# Initialize Pygame
pygame.init()

game_over_sound = pygame.mixer.Sound("assets/audio/completion or end of game (1) (online-audio-converter.com).mp3")  # game over sound 
game_over_sound.set_volume(1.0)  # Adjust volume

#click sound
button_click_sound = pygame.mixer.Sound("assets/audio/click.mp3")
button_click_sound.set_volume(1.0)  # Adjust volume

#hit sound
hit_sound = pygame.mixer.Sound("assets/audio/hittt (online-audio-converter.com).mp3")
hit_sound.set_volume(1.0)

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Fury")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load fonts
font = pygame.font.Font("assets/font/pixel_font.TTF", 28)  # Adjust font size for better fit
title_font = pygame.font.Font("assets/font/pixel_font.TTF", 70)  # Larger font for title


# Load images
play_button = pygame.image.load("assets/images/play_button.png")
quit_button = pygame.image.load("assets/images/quit_button.png")
play_again_button = pygame.image.load("assets/images/play_again.png")
player_image = pygame.image.load("assets/images/ship.png")
monster_image = pygame.image.load("assets/images/monster.png")
meteor_image = pygame.image.load("assets/images/meteor.png")
heart_image = pygame.image.load("assets/images/heart.png")

# Resize images
play_button = pygame.transform.scale(play_button, (300, 80))
quit_button = pygame.transform.scale(quit_button, (300, 80))
play_again_button = pygame.transform.scale(play_again_button, (300, 80))
player_image = pygame.transform.scale(player_image, (120, 120))
monster_image = pygame.transform.scale(monster_image, (120, 120))
monster_size = (120, 120)
meteor_image = pygame.transform.scale(meteor_image, (40, 40))
heart_image = pygame.transform.scale(heart_image, (40, 40))

# Load and scale monster's ball image
monster_ball_image = pygame.image.load("assets/images/bomb.png")
ball_size = (50, 50)  # Adjust size
monster_ball_image = pygame.transform.scale(monster_ball_image, ball_size)

# Load and scale monster's missile
monster_balls = []
ball_release_time = 0
ball_speed = 5 #10
monster_fire_start_time = 0  # Track when the monster should start firing
monster_fire_delay = 10000  # 10 seconds delay before the monster starts firing
ball_directions = [(-1, 1), (0, 1), (1, 1)]# Left-down, straight-down, right-down
# (dx, dy) directions: down, diagonal, horizontal

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
player_y = HEIGHT - 120
player_speed = 5
monster_x, monster_y = 120,90  # Monster in top-left
bombs = []
lives = 5
score = 0
player_size = 50
game_state = "menu"
bomb_speed = 5
bomb_spawn_rate = 1

def draw_lives():
    spacing = 45  # Adjust this value to increase or decrease spacing
    for i in range(lives):
        screen.blit(heart_image, (20 + i * spacing, 20))  # Increased spacing between hearts


def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 300, 20))

def draw_monster():
    screen.blit(monster_image, (monster_x, monster_y))

def draw_monster_balls():
    global monster_balls
    for ball in monster_balls:
        screen.blit(monster_ball_image, (ball[0], ball[1]))  # Draw ball
        
# Load and play background music
pygame.mixer.music.load("assets/audio/bgm.mp3")  # Replace with your actual file path
pygame.mixer.music.set_volume(0.05)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely

def draw_bombs():
    for bomb in bombs:
        screen.blit(meteor_image, (bomb[0], bomb[1]))
def handle_player_movement(keys):
    global player_x
    # Move left if LEFT key is pressed and player is within screen bounds
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    # Move right if RIGHT key is pressed and player is within screen bounds
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

# Function to handle game controls (quit, pause, etc.)
# Function to handle game controls (quit, pause, etc.)
def handle_game_controls():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit if close button is clicked
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Go to main menu instead of quitting
            main_menu()
    return True


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
                    button_click_sound.play()
                    pygame.time.wait(200) #delay
                    return
                if quit_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    pygame.time.wait(1000) #delay
                    pygame.quit()
                    exit()

        pygame.display.update()

def game_over_screen():
    pygame.mixer.Sound.play(game_over_sound)  # Play sound when game over screen appears
    while True:
        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)
        
        draw_text(f"Game Over! Score: {score}", WIDTH // 2, HEIGHT // 3, font, WHITE)
        screen.blit(play_again_button, play_again_button_rect)
        screen.blit(quit_button, quit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                button_click_sound.play()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    pygame.time.wait(200) #delay
                    return "restart"
                if quit_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    pygame.time.wait(1000) #delay
                    pygame.quit()
                    exit()

        pygame.display.update()

        
def draw_text(text, x, y, font, color=WHITE):
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)

def game_loop():
    global player_x, lives,bg_y, score, ball_release_time, monster_balls, bomb_speed, bomb_spawn_rate, monster_fire_start_time
    clock = pygame.time.Clock()
    running = True
    paused=False 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit if close button is clicked
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Handle quit game (could be your menu functionality)
                    running = False
                elif event.key == pygame.K_SPACE:  # Toggle pause on Spacebar press
                    paused = not paused  # Toggle the paused state

        if paused:
            # Show pause message
            screen.fill(BLACK)
            update_stars(stars)
            draw_stars(stars)
            draw_text("Paused", WIDTH // 2, HEIGHT // 2, font, WHITE)
            draw_text("Press Space to Resume", WIDTH // 2, HEIGHT // 3, font, WHITE)
            draw_text("Press Escape for MAIN MENU", WIDTH // 2, HEIGHT // 4, font, WHITE)
            pygame.display.update()
            continue  # Skip the rest of the loop if paused
        running = handle_game_controls()  # Check for quit/pause events first
        if not running:
            break  # Exit loop immediately if quit is detected

        screen.fill(BLACK)
        update_stars(stars)
        draw_stars(stars)

          # Spawn bombs
        if random.randint(1, 20) <= bomb_spawn_rate:
            bombs.append([random.randint(0, WIDTH - 10), 0])
        
        # Move bombs and handle collision
        to_remove = []
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        for bomb in bombs:
            bomb[1] += bomb_speed
            bomb_rect = pygame.Rect(bomb[0], bomb[1], 10, 10)
            
            if bomb[1] > HEIGHT:
                to_remove.append(bomb)
                score += 1  

            if player_rect.colliderect(bomb_rect):
                lives -= 1
                to_remove.append(bomb)

                if lives == 0:
                    game_over_screen()
                    running = False
        
        for bomb in to_remove:
            bombs.remove(bomb)

        # Increase difficulty over time
        if score % 15 == 0 and score > 0:
            bomb_speed += 0.1
            bomb_spawn_rate = min(3, bomb_spawn_rate + 1)

       
         # Release ball every 5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - ball_release_time > 5000:  # 5000ms = 5 seconds
            ball_release_time = current_time  # Reset timer
            # Generate a random X position for the ball to land at the bottom
            target_x = random.randint(0, WIDTH - ball_size[0])

            # Starting position (centered at the monster)
            start_x = monster_x + monster_size[0] // 2
            start_y = monster_y + monster_size[1]

            # Compute directional movement towards the target (normalize speed)
            distance_x = target_x - start_x
            distance_y = HEIGHT - start_y

            # Normalize speed so all balls move at the same speed
            total_distance = (distance_x**2 + distance_y**2) ** 0.5  # Pythagorean theorem
            speed = ball_speed  # Constant falling speed

            dx = (distance_x / total_distance) * speed
            dy = (distance_y / total_distance) * speed  # Ensures it always falls downward

            monster_balls.append([start_x, start_y, dx, dy])

        # Move monster balls and check for collision
        for ball in monster_balls[:]:
            ball[0] += ball[2]  # Move in X direction
            ball[1] += ball[3]  # Move in Y direction

            # Check for collision with the player (UFO)
            ball_rect = pygame.Rect(ball[0], ball[1], ball_size[0], ball_size[1])  # Ball rect
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)  # Player rect

            if player_rect.colliderect(ball_rect):  # If the ball collides with the player
                pygame.mixer.Sound.play(hit_sound)  # Play hit sound
                monster_balls.remove(ball)  # Remove the ball upon collision

            # Remove ball if off-screen
            elif ball[1] > HEIGHT:
                monster_balls.remove(ball)
            # Move monster balls and check for collision
            to_remove_balls = []
            for ball in monster_balls:
                ball[0] += ball[2]  
                ball[1] += ball[3]  
                ball_rect = pygame.Rect(ball[0], ball[1], ball_size[0], ball_size[1])

                if ball_rect.colliderect(player_rect):
                    pygame.mixer.Sound.play(hit_sound)  # Play hit sound
                    lives -= 2  # Correctly decrement lives before removing the ball
                    to_remove_balls.append(ball)

                    if lives <= 0:
                        game_over_screen()
                        running = False
                        break  # Exit loop immediately after game over

                if ball[1] > HEIGHT:  
                    to_remove_balls.append(ball)

            # Remove balls after iteration
            for ball in to_remove_balls:
                if ball in monster_balls:  # Ensure the ball still exists in the list before removing
                    monster_balls.remove(ball)

        # Draw game elements
        screen.blit(player_image, (player_x, player_y))
        draw_monster()
        draw_bombs()
        draw_lives()
        draw_score()
        draw_monster_balls()

        keys = pygame.key.get_pressed()  
        handle_player_movement(keys)  

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Pause on Spacebar press
                paused = not paused  # Toggle pause state
                
        pygame.display.update()
        clock.tick(30)
#       pygame.quit()

# Run game

# Main game loop
while True:
    main_menu()  # Show the main menu
    
    # Reset game variables before starting a new game
    player_x = WIDTH // 2 - 25
    lives = 5
    score = 0
    bombs.clear()
    monster_balls.clear()
    ball_release_time = 0
    monster_fire_start_time = 0

    game_result = game_loop()  # Start the game loop

    if game_result == "game_over":  # If the game ends
        action = game_over_screen()  # Show the game over screen
        if action != "play_again":  # If the player does NOT want to play again
            break  # Exit the loop and quit the game


