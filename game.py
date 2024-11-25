import pygame
import sys
import random
import math
from board import Board
from constants import *
from computer_player import ComputerPlayer

class VictoryParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, PARTICLE_SPEED)
        self.life = 255
        self.size = random.randint(4, PARTICLE_SIZE)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 2
        return self.life > 0

    def draw(self, screen):
        alpha = max(0, min(255, self.life))
        particle_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        particle_color = (*self.color[:3], alpha)
        pygame.draw.circle(particle_surface, particle_color, (self.size//2, self.size//2), self.size//2)
        screen.blit(particle_surface, (int(self.x - self.size//2), int(self.y - self.size//2)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Puissance 4")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.computer = ComputerPlayer()
        self.current_player = 1
        self.game_mode = 'two_players'
        self.animation = None
        self.game_over = False
        self.victory_animation = None
        self.particles = []
        self.victory_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.victory_font = pygame.font.Font(None, VICTORY_FONT_SIZE)

    def start_victory_animation(self):
        self.victory_animation = {
            'scale': 0,
            'alpha': 0,
            'rotation': 0
        }
        # Create initial particles
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        color = RED if self.current_player == 1 else YELLOW
        for _ in range(PARTICLE_COUNT):
            self.particles.append(VictoryParticle(center_x, center_y, color))

    def update_victory_animation(self):
        if not self.victory_animation:
            return

        # Update victory text animation
        self.victory_animation['scale'] = min(1.0, self.victory_animation['scale'] + 0.05)
        self.victory_animation['alpha'] = min(255, self.victory_animation['alpha'] + 5)
        self.victory_animation['rotation'] = (self.victory_animation['rotation'] + 1) % 360

        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Add new particles occasionally
        if random.random() < 0.1:
            color = RED if self.current_player == 1 else YELLOW
            self.particles.append(VictoryParticle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                color
            ))

    def draw_victory_animation(self):
        if not self.victory_animation:
            return

        # Draw semi-transparent overlay
        self.victory_overlay.fill(VICTORY_OVERLAY_COLOR)
        self.screen.blit(self.victory_overlay, (0, 0))

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw victory text with animation
        text = f"Joueur {self.current_player} gagne!"
        text_surface = self.victory_font.render(text, True, VICTORY_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

        # Apply scale and rotation
        scaled_surface = pygame.transform.rotozoom(
            text_surface,
            self.victory_animation['rotation'],
            self.victory_animation['scale']
        )
        scaled_rect = scaled_surface.get_rect(center=(WIDTH//2, HEIGHT//2))

        # Apply alpha
        alpha_surface = pygame.Surface(scaled_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, self.victory_animation['alpha']))
        scaled_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.screen.blit(scaled_surface, scaled_rect)

    def handle_click(self, pos):
        if self.animation or self.game_over:
            return

        col = pos[0] // CELL_SIZE
        if 0 <= col < COLS and self.board.is_valid_move(col):
            row = self.board.get_next_row(col)
            self.animation = {
                'token': {'player': self.current_player, 'col': col},
                'y': 0,
                'target_y': row * CELL_SIZE
            }

    def update_animation(self):
        if not self.animation:
            return

        self.animation['y'] += ANIMATION_SPEED
        if self.animation['y'] >= self.animation['target_y']:
            row = self.animation['target_y'] // CELL_SIZE
            col = self.animation['token']['col']
            player = self.animation['token']['player']
            
            self.board.make_move(row, col, player)
            if self.board.check_win(row, col, player):
                self.game_over = True
                self.start_victory_animation()
            else:
                self.current_player = 3 - self.current_player
                if self.game_mode == 'vs_computer' and self.current_player == 2 and not self.game_over:
                    self.computer_move()
            
            self.animation = None

    def computer_move(self):
        if not self.game_over:
            col = self.computer.get_move(self.board)
            if col is not None and self.board.is_valid_move(col):
                row = self.board.get_next_row(col)
                self.animation = {
                    'token': {'player': 2, 'col': col},
                    'y': 0,
                    'target_y': row * CELL_SIZE
                }

    def draw(self):
        self.screen.fill(BLUE)
        self.board.draw(self.screen)
        
        # Draw falling token animation
        if self.animation:
            x = self.animation['token']['col'] * CELL_SIZE
            y = self.animation['y']
            color = RED if self.animation['token']['player'] == 1 else YELLOW
            pygame.draw.circle(self.screen, color, 
                             (x + CELL_SIZE//2, y + CELL_SIZE//2), 
                             CELL_SIZE//2 - 5)

        # Draw game status if not in victory animation
        if not self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Tour du Joueur {self.current_player}", True, WHITE)
            self.screen.blit(text, (10, HEIGHT - 40))

        # Draw victory animation
        if self.game_over:
            self.draw_victory_animation()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_1:
                        self.game_mode = 'two_players'
                        self.reset_game()
                    elif event.key == pygame.K_2:
                        self.game_mode = 'vs_computer'
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.update_animation()
            if self.game_over:
                self.update_victory_animation()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.board = Board()
        self.current_player = 1
        self.animation = None
        self.game_over = False
        self.victory_animation = None
        self.particles = []

if __name__ == '__main__':
    game = Game()
    game.run()