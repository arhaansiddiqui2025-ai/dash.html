import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- MOBILE COMPATIBILITY & SCALING ---
# Standard internal resolution (16:9 aspect ratio)
BASE_WIDTH, BASE_HEIGHT = 1280, 720

# Get actual device screen info (adapts to mobile screens)
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w if screen_info.current_w > 0 else BASE_WIDTH
SCREEN_HEIGHT = screen_info.current_h if screen_info.current_h > 0 else BASE_HEIGHT

# Scale factors to ensure everything fits perfectly on any screen
SF_X = SCREEN_WIDTH / BASE_WIDTH
SF_Y = SCREEN_HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Geometry Dash Python Clone")
clock = pygame.time.Clock()

# --- GAME CONSTANTS (Scaled) ---
GRAVITY = 0.8 * SF_Y
JUMP_STRENGTH = -14 * SF_Y
SPEED = 8 * SF_X
FLOOR_Y = SCREEN_HEIGHT - (120 * SF_Y)

# Colors
BG_COLORS = [(20, 10, 40), (10, 40, 20), (40, 10, 10), (30, 30, 10), (10, 30, 30),
             (30, 10, 30), (20, 20, 20), (0, 40, 50), (50, 0, 40), (20, 50, 10)]
BLOCK_COLOR = (0, 200, 255)
SPIKE_COLOR = (255, 50, 50)
PORTAL_COLOR = (255, 200, 0)

# --- 10 LEVEL DESIGN DATA ---
# 'b' = Block, 's' = Spike, 'p' = Win Portal. Numbers dictate X-grid position (multiplied by 60px)
LEVELS = {
    1: [('s', 10), ('s', 15), ('b', 18), ('s', 22), ('s', 23), ('b', 28), ('b', 29), ('s', 35), ('p', 42)],
    2: [('b', 8), ('s', 12), ('s', 13), ('b', 18), ('b', 19), ('s', 20), ('s', 25), ('b', 30), ('p', 38)],
    3: [('s', 8), ('b', 12), ('s', 16), ('b', 17), ('s', 18), ('b', 24), ('s', 25), ('s', 30), ('p', 40)],
    4: [('s', 6), ('s', 10), ('b', 14), ('b', 15), ('s', 16), ('s', 22), ('b', 26), ('s', 32), ('p', 45)],
    5: [('b', 8), ('s', 9), ('b', 14), ('s', 15), ('b', 20), ('s', 21), ('b', 26), ('s', 27), ('p', 38)],
    6: [('s', 10), ('s', 12), ('s', 18), ('b', 22), ('b', 23), ('s', 24), ('s', 30), ('s', 32), ('p', 42)],
    7: [('b', 7), ('b', 9), ('s', 13), ('s', 14), ('b', 18), ('s', 24), ('b', 28), ('s', 29), ('p', 40)],
    8: [('s', 8), ('s', 9), ('s', 10), ('b', 15), ('b', 16), ('s', 22), ('s', 23), ('b', 28), ('p', 42)],
    9: [('b', 6), ('s', 12), ('b', 15), ('s', 16), ('b', 22), ('s', 28), ('b', 32), ('s', 33), ('p', 45)],
    10: [('s', 8), ('b', 12), ('s', 13), ('b', 17), ('s', 22), ('b', 26), ('s', 30), ('s', 35), ('p', 50)]
}

class Player:
    def __init__(self):
        self.size = int(50 * SF_Y)
        self.x = 150 * SF_X
        self.y = FLOOR_Y - self.size
        self.vel_y = 0
        self.is_grounded = True
        self.rotation = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, jump_intent):
        # Apply Gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.is_grounded = False

        # Floor Collision
        if self.y >= FLOOR_Y - self.size:
            self.y = FLOOR_Y - self.size
            self.vel_y = 0
            self.is_grounded = True

        # Handle Jump (Triggers on Screen Tap / Click / Space)
        if jump_intent and self.is_grounded:
            self.vel_y = JUMP_STRENGTH
            self.is_grounded = False

        # Update Rect position
        self.rect.y = self.y

        # Rotation effect based on jumping
        if not self.is_grounded:
            self.rotation += 5
        else:
            # Snap to nearest 90 degrees when landing smoothly
            self.rotation = round(self.rotation / 90) * 90

    def draw(self, surface):
        # Draw a sleek neon square with rotation
        pygame_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(pygame_surface, (0, 255, 150), (0, 0, self.size, self.size), border_radius=int(6 * SF_Y))
        pygame.draw.rect(pygame_surface, (255, 255, 255), (0, 0, self.size, self.size), int(4 * SF_Y), border_radius=int(6 * SF_Y))
        
        rotated_surface = pygame.transform.rotate(pygame_surface, -self.rotation)
        new_rect = rotated_surface.get_rect(center=(self.x + self.size/2, self.y + self.size/2))
        surface.blit(rotated_surface, new_rect.topleft)

class Game:
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.font = pygame.font.Font(None, int(40 * SF_Y))
        self.reset_level()

    def reset_level(self):
        self.player = Player()
        self.obstacles = []
        self.particles = []
        self.camera_x = 0
        self.state = "PLAYING" # PLAYING, WIN, GAME_OVER
        
        # Build the level based on data
        grid_size = 60 * SF_X
        level_data = LEVELS[self.current_level]
        
        for obs_type, grid_x in level_data:
            real_x = grid_x * grid_size + 800 * SF_X
            if obs_type == 'b': # Block
                rect = pygame.Rect(real_x, FLOOR_Y - grid_size, grid_size, grid_size)
                self.obstacles.append({'type': 'block', 'rect': rect})
            elif obs_type == 's': # Spike
                rect = pygame.Rect(real_x, FLOOR_Y - grid_size, grid_size, grid_size)
                self.obstacles.append({'type': 'spike', 'rect': rect})
            elif obs_type == 'p': # Win Portal
                rect = pygame.Rect(real_x, FLOOR_Y - (grid_size * 2), grid_size, grid_size * 2)
                self.obstacles.append({'type': 'portal', 'rect': rect})

    def spawn_particles(self):
        if self.player.is_grounded:
            if random.random() < 0.4:
                self.particles.append({
                    'x': self.player.x,
                    'y': FLOOR_Y,
                    'vx': -SPEED * 0.5,
                    'vy': -random.random() * 3,
                    'life': 15
                })

    def update(self, jump_intent):
        if self.state == "PLAYING":
            self.camera_x += SPEED
            self.player.update(jump_intent)
            self.spawn_particles()

            # Update particles
            for p in self.particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)

            # Check Collisions
            player_rect = self.player.rect
            for obs in self.obstacles:
                # Shift obstacle relative to moving camera
                shifted_rect = obs['rect'].move(-self.camera_x, 0)
                
                if player_rect.colliderect(shifted_rect):
                    if obs['type'] == 'spike':
                        self.state = "GAME_OVER"
                    elif obs['type'] == 'block':
                        # If colliding from above, land on block
                        if player_rect.bottom <= shifted_rect.top + (15 * SF_Y) and self.player.vel_y >= 0:
                            self.player.y = obs['rect'].top - self.player.size
                            self.player.vel_y = 0
                            self.player.is_grounded = True
                        else: # Crashed into the side of a block
                            self.state = "GAME_OVER"
                    elif obs['type'] == 'portal':
                        self.state = "WIN"

        elif jump_intent: # Tap screen to restart or advance
            if self.state == "GAME_OVER":
                self.reset_level()
            elif self.state == "WIN":
                if self.current_level < 10:
                    self.current_level += 1
                    self.reset_level()
                else:
                    self.current_level = 1 # Loop back to 1
                    self.reset_level()

    def draw(self):
        # Dynamic BG Color matching the level
        screen.fill(BG_COLORS[self.current_level - 1])

        # Draw Floor Line
        pygame.draw.line(screen, (255, 255, 255), (0, FLOOR_Y), (SCREEN_WIDTH, FLOOR_Y), int(4 * SF_Y))
        pygame.draw.rect(screen, (10, 10, 15), (0, FLOOR_Y, SCREEN_WIDTH, SCREEN_HEIGHT - FLOOR_Y))

        # Draw Particles
        for p in self.particles:
            pygame.draw.circle(screen, (0, 255, 150), (int(p['x']), int(p['y'])), int(random.randint(2, 5) * SF_Y))

        # Draw Obstacles
        for obs in self.obstacles:
            shifted_rect = obs['rect'].move(-self.camera_x, 0)
            # Only render if visible on screen
            if -shifted_rect.width < shifted_rect.x < SCREEN_WIDTH:
                if obs['type'] == 'block':
                    pygame.draw.rect(screen, BLOCK_COLOR, shifted_rect, border_radius=int(4 * SF_Y))
                    pygame.draw.rect(screen, (255, 255, 255), shifted_rect, int(2 * SF_Y), border_radius=int(4 * SF_Y))
                elif obs['type'] == 'spike':
                    pts = [
                        (shifted_rect.midtop),
                        (shifted_rect.bottomleft),
                        (shifted_rect.bottomright)
                    ]
                    pygame.draw.polygon(screen, SPIKE_COLOR, pts)
                    pygame.draw.polygon(screen, (255, 255, 255), pts, int(2 * SF_Y))
                elif obs['type'] == 'portal':
                    pygame.draw.ellipse(screen, PORTAL_COLOR, shifted_rect)
                    pygame.draw.ellipse(screen, (255, 255, 255), shifted_rect, int(3 * SF_Y))

        # Draw Player
        self.player.draw(screen)

        # UI Text Overlays
        lvl_txt = self.font.render(f"LEVEL {self.current_level}/10", True, (255, 255, 255))
        screen.blit(lvl_txt, (20 * SF_X, 20 * SF_Y))

        if self.state == "GAME_OVER":
            over_txt = self.font.render("CRASHED! Tap Screen to Retry", True, (255, 50, 50))
            text_rect = over_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(over_txt, text_rect)
        elif self.state == "WIN":
            win_msg = "ALL LEVELS CLEARED!" if self.current_level == 10 else "LEVEL PASSED! Tap to Continue"
            win_txt = self.font.render(win_msg, True, (50, 255, 50))
            text_rect = win_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(win_txt, text_rect)

# --- MAIN GAME LOOP ---
game = Game()
running = True

while running:
    jump_intent = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # KEYBOARD CONTROL (For desktop testing)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump_intent = True
            if event.key == pygame.K_ESCAPE:
                running = False
                
        # MOBILE COMPATIBILITY: Screen tap triggers a jump or event selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            jump_intent = True

    game.update(jump_intent)
    game.draw()
    
    pygame.display.flip()
    clock.tick(60) # Locked 60 FPS frame rate

pygame.quit()
sys.exit()
