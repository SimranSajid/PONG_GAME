import pygame
import sys

# 1. Setup Window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - First to 5 Wins!")
clock = pygame.time.Clock()

# 2. Colors
WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 30)

# 3. Game Rectangles
player = pygame.Rect(50, HEIGHT // 2 - 70, 15, 140)   
opponent = pygame.Rect(WIDTH - 65, HEIGHT // 2 - 70, 15, 140) 
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)  

# 4. Speeds
PLAYER_SPEED = 7
opponent_speed = 5
ball_speed_x = 5
ball_speed_y = 5

# 5. Score Tracking & Fonts
player_score = 0
opponent_score = 0
score_font = pygame.font.SysFont("Arial", 50, bold=True)
game_over_font = pygame.font.SysFont("Arial", 60, bold=True)

# 6. Game State Variable (True = playing, False = game over screen)
game_active = True

# Game Loop
while True:
    # --- 1. HANDLE INPUTS & EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Check for restart key if the game is over
        if not game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reset everything to restart the game
                player_score = 0
                opponent_score = 0
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x = 5
                ball_speed_y = 5
                game_active = True

    # --- 2. RUN GAME LOGIC (Only if game is active!) ---
    if game_active:
        keys = pygame.key.get_pressed()
        
        # Move Player
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += PLAYER_SPEED

        # Stop player from going off screen
        if player.top <= 0: player.top = 0
        if player.bottom >= HEIGHT: player.bottom = HEIGHT

        # Move Ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball wall bounce
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1 

        # AI Opponent movement
        if opponent.centery < ball.y:
            opponent.y += opponent_speed
        elif opponent.centery > ball.y:
            opponent.y -= opponent_speed

        if opponent.top <= 0: opponent.top = 0
        if opponent.bottom >= HEIGHT: opponent.bottom = HEIGHT

        # Ball hits paddles
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1 

        # Score detection
        if ball.left <= 0:
            opponent_score += 1                     
            ball.center = (WIDTH // 2, HEIGHT // 2)  
            ball_speed_x *= -1                      

        if ball.right >= WIDTH:
            player_score += 1                       
            ball.center = (WIDTH // 2, HEIGHT // 2)  
            ball_speed_x *= -1                      

        # Check Win Condition (First to 5)
        if player_score >= 5 or opponent_score >= 5:
            game_active = False # Stops physics and player movement

    # --- 3. DRAW GRAPHICS ---
    screen.fill(BG_COLOR) 
    
    # Draw scores
    player_text = score_font.render(str(player_score), True, WHITE)
    opponent_text = score_font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 30))         
    screen.blit(opponent_text, (3 * WIDTH // 4, 30))   

    # Draw game objects
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball) 
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT)) 

    # Draw Game Over Screen over everything else if someone won
    if not game_active:
        # Determine who won
        if player_score >= 5:
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"
            
        # Render main message and sub-message
        end_text = game_over_font.render(msg, True, (255, 50, 50))
        restart_text = score_font.render("Press SPACE to Play Again", True, WHITE)
        
        # Center the text positions on screen
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)
