import tkinter as tk
import random

# --- CONFIGURATION & SCALING ---
BASE_WIDTH, BASE_HEIGHT = 1280, 720

root = tk.Tk()
root.title("Geometry Dash Python Clone (Tkinter)")

# Force fullscreen for mobile-like scaling
root.attributes("-fullscreen", True)
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

# Fallback if window dimensions aren't fetched instantly
if SCREEN_WIDTH <= 0: SCREEN_WIDTH = BASE_WIDTH
if SCREEN_HEIGHT <= 0: SCREEN_HEIGHT = BASE_HEIGHT

# Scale factors 
SF_X = SCREEN_WIDTH / BASE_WIDTH
SF_Y = SCREEN_HEIGHT / BASE_HEIGHT

# Canvas configuration
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#140a28", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- GAME CONSTANTS ---
GRAVITY = 0.7 * SF_Y
JUMP_STRENGTH = -13.5 * SF_Y
SPEED = 8 * SF_X
FLOOR_Y = SCREEN_HEIGHT - (120 * SF_Y)

BG_COLORS = ["#140a28", "#0a2814", "#280a0a", "#1e1e0a", "#0a1e1e",
             #6       #7       #8       #9       #10
             "#1e0a1e", "#141414", "#002832", "#320028", "#14320a"]
BLOCK_COLOR = "#00c8ff"
SPIKE_COLOR = "#ff3232"
PORTAL_COLOR = "#ffc800"

# --- 10 LEVEL DESIGN DATA ---
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

    def update(self, jump_intent):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.is_grounded = False

        if self.y >= FLOOR_Y - self.size:
            self.y = FLOOR_Y - self.size
            self.vel_y = 0
            self.is_grounded = True

        if jump_intent and self.is_grounded:
            self.vel_y = JUMP_STRENGTH
            self.is_grounded = False

    def get_coords(self):
        return self.x, self.y, self.x + self.size, self.y + self.size

class Game:
    def __init__(self):
        self.current_level = 1
        self.jump_intent = False
        self.reset_level()
        
        # Key/Touch Bindings
        root.bind("<space>", lambda e: self.trigger_jump())
        root.bind("<Up>", lambda e: self.trigger_jump())
        root.bind("<Button-1>", lambda e: self.trigger_jump()) # Universal touch screen / mouse tap
        root.bind("<Escape>", lambda e: root.destroy())

    def trigger_jump(self):
        self.jump_intent = True

    def reset_level(self):
        self.player = Player()
        self.obstacles = []
        self.particles = []
        self.camera_x = 0
        self.state = "PLAYING"
        
        grid_size = 60 * SF_X
        level_data = LEVELS[self.current_level]
        
        for obs_type, grid_x in level_data:
            real_x = grid_x * grid_size + 800 * SF_X
            if obs_type == 'b':
                self.obstacles.append({'type': 'block', 'x1': real_x, 'y1': FLOOR_Y - grid_size, 'x2': real_x + grid_size, 'y2': FLOOR_Y})
            elif obs_type == 's':
                self.obstacles.append({'type': 'spike', 'x1': real_x, 'y1': FLOOR_Y - grid_size, 'x2': real_x + grid_size, 'y2': FLOOR_Y})
            elif obs_type == 'p':
                self.obstacles.append({'type': 'portal', 'x1': real_x, 'y1': FLOOR_Y - (grid_size * 2), 'x2': real_x + grid_size, 'y2': FLOOR_Y})

    def spawn_particles(self):
        if self.player.is_grounded and random.random() < 0.4:
            self.particles.append({
                'x': self.player.x,
                'y': FLOOR_Y,
                'vx': -SPEED * 0.5,
                'vy': -random.random() * 3,
                'life': 15
            })

    def check_collision(self, px1, py1, px2, py2, ox1, oy1, ox2, oy2):
        # AABB Overlap bounding box check
        return not (px2 < ox1 or px1 > ox2 or py2 < oy1 or py1 > oy2)

    def game_loop(self):
        if self.state == "PLAYING":
            self.camera_x += SPEED
            self.player.update(self.jump_intent)
            self.spawn_particles()
            self.jump_intent = False # Reset intent after registering

            # Handle particles
            for p in self.particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)

            # Process Obstacles and Overlaps
            px1, py1, px2, py2 = self.player.get_coords()
            
            for obs in self.obstacles:
                ox1 = obs['x1'] - self.camera_x
                ox2 = obs['x2'] - self.camera_x
                oy1 = obs['y1']
                oy2 = obs['y2']

                if self.check_collision(px1, py1, px2, py2, ox1, oy1, ox2, oy2):
                    if obs['type'] == 'spike':
                        self.state = "GAME_OVER"
                    elif obs['type'] == 'portal':
                        self.state = "WIN"
                    elif obs['type'] == 'block':
                        # Top physics landing landing zone check
                        if py2 <= oy1 + (15 * SF_Y) and self.player.vel_y >= 0:
                            self.player.y = oy1 - self.player.size
                            self.player.vel_y = 0
                            self.player.is_grounded = True
                        else:
                            self.state = "GAME_OVER"

        elif self.jump_intent:
            self.jump_intent = False
            if self.state == "GAME_OVER":
                self.reset_level()
            elif self.state == "WIN":
                self.current_level = self.current_level + 1 if self.current_level < 10 else 1
                self.reset_level()

        self.draw()
        # Schedule the next frame (~60 FPS)
        root.after(16, self.game_loop)

    def draw(self):
        canvas.delete("all")
        
        # Background Uniform fill
        canvas.configure(bg=BG_COLORS[self.current_level - 1])

        # Floor Draw
        canvas.create_rectangle(0, FLOOR_Y, SCREEN_WIDTH, SCREEN_HEIGHT, fill="#0a0a0f", outline="")
        canvas.create_line(0, FLOOR_Y, SCREEN_WIDTH, FLOOR_Y, fill="white", width=int(3 * SF_Y))

        # Particles Draw
        for p in self.particles:
            r = int(random.randint(2, 4) * SF_Y)
            canvas.create_oval(p['x']-r, p['y']-r, p['x']+r, p['y']+r, fill="#00ff96", outline="")

        # Obstacles Render Viewport optimization
        for obs in self.obstacles:
            ox1 = obs['x1'] - self.camera_x
            ox2 = obs['x2'] - self.camera_x
            if -100 < ox2 and ox1 < SCREEN_WIDTH + 100:
                if obs['type'] == 'block':
                    canvas.create_rectangle(ox1, obs['y1'], ox2, obs['y2'], fill=BLOCK_COLOR, outline="white", width=2)
                elif obs['type'] == 'spike':
                    canvas.create_polygon(ox1, obs['y2'], (ox1+ox2)/2, obs['y1'], ox2, obs['y2'], fill=SPIKE_COLOR, outline="white", width=2)
                elif obs['type'] == 'portal':
                    canvas.create_oval(ox1, obs['y1'], ox2, obs['y2'], fill=PORTAL_COLOR, outline="white", width=3)

        # Player Graphic Render
        px1, py1, px2, py2 = self.player.get_coords()
        canvas.create_rectangle(px1, py1, px2, py2, fill="#00ff96", outline="white", width=int(4 * SF_Y))

        # UI Overlay Data
        canvas.create_text(20 * SF_X, 20 * SF_Y, text=f"LEVEL {self.current_level}/10", fill="white", font=("Arial", int(24 * SF_Y), "bold"), anchor="nw")

        if self.state == "GAME_OVER":
            canvas.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text="CRASHED! Tap Screen to Retry", fill="#ff3232", font=("Arial", int(28 * SF_Y), "bold"), justify="center")
        elif self.state == "WIN":
            msg = "ALL LEVELS CLEARED!" if self.current_level == 10 else "LEVEL PASSED! Tap to Continue"
            canvas.create_text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, text=msg, fill="#32ff32", font=("Arial", int(28 * SF_Y), "bold"), justify="center")

# --- INITIALIZE EXECUTION ---
game = Game()
root.after(16, game.game_loop)
root.mainloop()
