import pygame
import sys
import random

# --- Configuration & Constants ---
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 15
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (150, 150, 150)
RED   = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE  = (50, 50, 255)

class PongGame:
    def __init__(self):
        pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PyPong")
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.SysFont(None, 32)
            self.large_font = pygame.font.SysFont(None, 48)
        except Exception:
            self.font = None 
            self.large_font = None

        # --- Menu/Setting Variables ---
        self.state = "MENU"  # States: MENU, PLAYING, GAME_OVER
        self.difficulty = 6 # AI Speed
        self.win_score = 10
        self.paddle_color = WHITE
        self.ball_color = WHITE
        
        # Menu selection tracking
        self.menu_index = 0
        self.menu_options = [
            "Difficulty: Normal", 
            "Win Score: 10", 
            "Paddle Color: White", 
            "Ball Color: White",
            "START GAME"
        ]

        self.reset_game()

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.reset_ball()
        self.reset_paddles()

    def reset_ball(self):
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 5 * random.choice([-1, 1])
        self.ball_dy = 5 * random.choice([-1, 1])

    def reset_paddles(self):
        self.player_rect = pygame.Rect(50, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ai_rect = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)

    def handle_menu_input(self, event):
        """Handles menu navigation and selection."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                # Handle selection logic
                if self.menu_index == 0: # Difficulty
                    self.difficulty = 4 if self.difficulty == 6 else (8 if self.difficulty == 4 else 6)
                    self.menu_options[0] = f"Difficulty: {'Hard' if self.difficulty==8 else 'Easy' if self.difficulty==4 else 'Normal'}"
                elif self.menu_index == 1: # Win Score
                    # If current score is 20, next press makes it 10 (reset)
                    # Otherwise, add 5
                    if self.win_score >= 20:
                        self.win_score = 10
                    else:
                        self.win_score += 5
                    self.menu_options[1] = f"Win Score: {self.win_score}"
                elif self.menu_index == 2: # Paddle Color
                    self.paddle_color = BLUE if self.paddle_color == WHITE else (WHITE if self.paddle_color == BLUE else RED)
                    self.menu_options[2] = f"Paddle Color: {'Blue' if self.paddle_color==BLUE else 'White' if self.paddle_color==WHITE else 'Red'}"
                elif self.menu_index == 3: # Ball Color
                    self.ball_color = GREEN if self.ball_color == WHITE else (WHITE if self.ball_color == GREEN else BLUE)
                    self.menu_options[3] = f"Ball Color: {'Green' if self.ball_color==GREEN else 'White' if self.ball_color==WHITE else 'Blue'}"
                elif self.menu_index == 4: # Start Game
                    if self.win_score < 5: self.win_score = 5 # Safety check
                    self.state = "PLAYING"
                    self.reset_game()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_rect.top > 0:
            self.player_rect.y -= 7
        if keys[pygame.K_DOWN] and self.player_rect.bottom < HEIGHT:
            self.player_rect.y += 7

    def update(self):
        if self.state != "PLAYING":
            return

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= 0 or self.ball_y >= HEIGHT - BALL_SIZE:
            self.ball_dy *= -1

        # AI Movement using dynamic difficulty
        if self.ai_rect.centery < self.ball_y and self.ai_rect.bottom < HEIGHT:
            self.ai_rect.y += self.difficulty
        elif self.ai_rect.centery > self.ball_y and self.ai_rect.top > 0:
            self.ai_rect.y -= self.difficulty

        ball_rect = pygame.Rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE)
        
        if ball_rect.colliderect(self.player_rect):
            self.ball_dx = abs(self.ball_dx) * 1.05 
            self.ball_dy *= 1.05

        if ball_rect.colliderect(self.ai_rect):
            self.ball_dx = -abs(self.ball_dx) * 1.05
            self.ball_dy *= 1.05

        if self.ball_x < 0:
            self.ai_score += 1
            if self.ai_score >= self.win_score:
                self.state = "GAME_OVER"
            else:
                self.reset_ball()
        elif self.ball_x > WIDTH:
            self.player_score += 1
            if self.player_score >= self.win_score:
                self.state = "GAME_OVER"
            else:
                self.reset_ball()

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.large_font.render("PONG SETTINGS", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(self.menu_options):
            color = GREEN if i == self.menu_index else WHITE
            text = self.font.render(option, True, color)
            x_pos = WIDTH // 2 - text.get_width() // 2
            y_pos = 250 + (i * 40)
            self.screen.blit(text, (x_pos, y_pos))

    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        else:
            self.screen.fill(BLACK)
            pygame.draw.line(self.screen, GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
            pygame.draw.rect(self.screen, self.paddle_color, self.player_rect)
            pygame.draw.rect(self.screen, self.paddle_color, self.ai_rect)
            pygame.draw.ellipse(self.screen, self.ball_color, (self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            self.screen.blit(player_text, (WIDTH // 4, 20))
            self.screen.blit(ai_text, (3 * WIDTH // 4, 20))

            if self.state == "GAME_OVER":
                winner = "Player" if self.player_score >= self.win_score else "Computer"
                msg = self.large_font.render(f"{winner} Wins!", True, WHITE)
                sub_msg = self.font.render("Press R to Restart or M for Menu", True, GRAY)
                text_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(msg, text_rect)
                self.screen.blit(sub_msg, (WIDTH//2 - sub_msg.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.state == "MENU":
                    self.handle_menu_input(event)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r and self.state == "GAME_OVER":
                            self.reset_game()
                            self.state = "PLAYING"
                        if event.key == pygame.K_m and self.state == "GAME_OVER":
                            self.state = "MENU"

            if self.state == "PLAYING":
                self.handle_input()
                self.update()
            
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = PongGame()
    game.run()
