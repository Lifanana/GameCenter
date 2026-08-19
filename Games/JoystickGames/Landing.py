import sys
import math
import random
import pygame
import customtkinter as ctk

# CustomTkinter Styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
SPACE_BG = (15, 23, 42)
LANDER_COLOR = (241, 245, 249)
THRUSTER_COLOR = (249, 115, 22)
PAD_COLOR = (234, 179, 8)
ROCK_COLOR = (71, 85, 105)
TEXT_COLOR = (241, 245, 249)
SUCCESS_COLOR = (34, 197, 94)
ALERT_COLOR = (239, 68, 68)


class LanderGame:
    """Titan Expedition - Lunar Lander Style Game"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lander Probe: Titan Expedition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 42, bold=True)

        # Joystick Setup
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Physics & State
        self.x = 150.0
        self.y = 100.0
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.04
        self.fuel = 100.0
        self.thrust_power = 0.12

        # Wind hazard (changes slightly each run)
        self.wind_x = random.uniform(-0.02, 0.02)

        # Active thrusters for rendering
        self.thrust_up = False
        self.thrust_left = False
        self.thrust_right = False

        # Target Landing Pad
        self.pad_rect = pygame.Rect(750, 580, 120, 18)

        # Obstacles (Mountains/Obstacles)
        self.rocks = [
            pygame.Rect(0, 620, 1000, 80),          # Ground
            pygame.Rect(350, 420, 120, 200),        # Center Mountain
            pygame.Rect(550, 200, 80, 250)          # Floating Asteroid/Cliff
        ]

        # Game Status
        self.landed = False
        self.crashed = False
        self.status_msg = ""

    def handle_input(self):
        if self.landed or self.crashed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        self.thrust_up = False
        self.thrust_left = False
        self.thrust_right = False

        if self.fuel <= 0:
            return

        move_x = 0.0
        move_y = 0.0

        if self.joystick:
            move_x = self.joystick.get_axis(0)
            move_y = self.joystick.get_axis(1)

            DEADZONE = 0.2
            if abs(move_x) < DEADZONE: move_x = 0
            if abs(move_y) < DEADZONE: move_y = 0

            # Emergency Stabilizer (Button 0)
            if self.joystick.get_button(0) and self.fuel > 0:
                self.vx *= 0.85
                self.vy *= 0.85
                self.fuel -= 0.4
                self.thrust_up = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: move_x = -1.0
            if keys[pygame.K_RIGHT]: move_x = 1.0
            if keys[pygame.K_UP]: move_y = -1.0
            if keys[pygame.K_DOWN]: move_y = 1.0

        # Thrust application
        if move_y < -0.3:  # Main Thruster (Upward)
            self.vy += move_y * self.thrust_power
            self.fuel -= 0.15
            self.thrust_up = True

        if move_x < -0.3:  # Left RCS (Pushes Right)
            self.vx += move_x * (self.thrust_power * 0.7)
            self.fuel -= 0.08
            self.thrust_right = True

        elif move_x > 0.3:  # Right RCS (Pushes Left)
            self.vx += move_x * (self.thrust_power * 0.7)
            self.fuel -= 0.08
            self.thrust_left = True

    def update_physics(self):
        if self.landed or self.crashed:
            return

        # Apply Environmental Physics
        self.vy += self.gravity
        self.vx += self.wind_x

        self.x += self.vx
        self.y += self.vy

        probe_rect = pygame.Rect(self.x - 16, self.y - 16, 32, 32)

        # Screen boundary check
        if self.x < 15 or self.x > SCREEN_WIDTH - 15 or self.y < 15:
            self.crashed = True
            self.status_msg = "CRASHED! Out of bounds."
            return

        # Check Landing Pad Collision
        if probe_rect.colliderect(self.pad_rect):
            speed = math.hypot(self.vx, self.vy)
            if speed <= 1.8 and abs(self.vx) < 1.0:
                self.landed = True
                self.status_msg = "PERFECT LANDING! Mission Accomplished!"
            else:
                self.crashed = True
                self.status_msg = f"CRASHED! Landing speed too high ({speed:.1f} m/s)."
            return

        # Check Obstacle Collision
        for rock in self.rocks:
            if probe_rect.colliderect(rock):
                self.crashed = True
                self.status_msg = "CRASHED! Hit terrain obstacle."
                return

    def draw(self):
        self.screen.fill(SPACE_BG)

        # 1. Draw Terrain & Obstacles
        for rock in self.rocks:
            pygame.draw.rect(self.screen, ROCK_COLOR, rock, border_radius=6)

        # 2. Draw Target Landing Pad
        pygame.draw.rect(self.screen, PAD_COLOR, self.pad_rect, border_radius=4)
        pygame.draw.rect(self.screen, SUCCESS_COLOR, (self.pad_rect.x + 10, self.pad_rect.y + 4, 100, 10))

        # 3. Draw Lander Probe
        px, py = int(self.x), int(self.y)
        # Body
        pygame.draw.polygon(self.screen, LANDER_COLOR, [
            (px, py - 16), (px + 14, py + 8), (px - 14, py + 8)
        ])
        # Landing Legs
        pygame.draw.line(self.screen, LANDER_COLOR, (px - 10, py + 8), (px - 18, py + 18), 3)
        pygame.draw.line(self.screen, LANDER_COLOR, (px + 10, py + 8), (px + 18, py + 18), 3)

        # Thruster Flames
        if self.thrust_up:
            pygame.draw.polygon(self.screen, THRUSTER_COLOR, [(px - 6, py + 10), (px + 6, py + 10), (px, py + 24)])
        if self.thrust_left:
            pygame.draw.polygon(self.screen, THRUSTER_COLOR, [(px - 14, py - 2), (px - 24, py + 2), (px - 14, py + 6)])
        if self.thrust_right:
            pygame.draw.polygon(self.screen, THRUSTER_COLOR, [(px + 14, py - 2), (px + 24, py + 2), (px + 14, py + 6)])

        # 4. HUD Telemetry
        speed = math.hypot(self.vx, self.vy)
        speed_color = SUCCESS_COLOR if speed <= 1.8 else ALERT_COLOR

        txt_speed = self.font.render(f"Speed: {speed:.2f} m/s", True, speed_color)
        txt_wind = self.font.render(f"Crosswind: {self.wind_x*100:+.1f} m/s", True, TEXT_COLOR)
        self.screen.blit(txt_speed, (20, 20))
        self.screen.blit(txt_wind, (20, 50))

        # Fuel Meter
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 85, 180, 18), border_radius=4)
        fuel_w = int((max(0, self.fuel) / 100.0) * 176)
        fuel_color = SUCCESS_COLOR if self.fuel > 30 else ALERT_COLOR
        if fuel_w > 0:
            pygame.draw.rect(self.screen, fuel_color, (22, 87, fuel_w, 14), border_radius=3)
        txt_fuel = self.font.render("FUEL", True, TEXT_COLOR)
        self.screen.blit(txt_fuel, (210, 82))

        # Game End Messages
        if self.landed:
            msg = self.big_font.render("MISSION SUCCESS!", True, SUCCESS_COLOR)
            sub = self.font.render("Press 'R' to Play Again", True, TEXT_COLOR)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 180, 80))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - 100, 130))
        elif self.crashed:
            msg = self.big_font.render(self.status_msg, True, ALERT_COLOR)
            sub = self.font.render("Press 'R' to Retry Mission", True, TEXT_COLOR)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 260, 80))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - 100, 130))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update_physics()
            self.draw()

        pygame.quit()
        self.launcher.deiconify()


# --- CustomTkinter Launcher ---
class LanderLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Lander Probe Launcher")
        self.geometry("550x550")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🌕 Lander Probe: Titan", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#eab308"
        )
        self.title_label.pack(pady=(30, 10))

        # Description
        self.desc_label = ctk.CTkLabel(
            self, 
            text="Navigate the probe through gravity and crosswinds.\nLand smoothly on the golden pad without crashing into terrain!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Instructions Box
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=40, pady=15, fill="x")

        instructions = (
            "🎮 Game Controls & Rules:\n"
            "• Stick UP: Main Engine (Fights Gravity)\n"
            "• Stick Left/Right: Side RCS Thrusters\n"
            "• Button 0 (Trigger): Emergency Stabilizer Brakes\n"
            "• Landing Rule: Speed MUST be below 1.8 m/s on the pad!\n\n"
            "⚠️ Watch out for crosswinds and mountain obstacles!"
        )
        self.info_text = ctk.CTkLabel(
            self.info_frame, 
            text=instructions, 
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        self.info_text.pack(pady=15, padx=15)

        # Start Button
        self.start_button = ctk.CTkButton(
            self, 
            text="▶️ Launch Mission", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#ca8a04",
            hover_color="#a16207",
            command=self.start_game
        )
        self.start_button.pack(pady=(10, 10), padx=50, fill="x")

        # Exit Button
        self.exit_button = ctk.CTkButton(
            self, 
            text="🏠 Back to GameCenter", 
            font=ctk.CTkFont(size=15),
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            command=self.return_to_gamecenter
        )
        self.exit_button.pack(pady=5, padx=50, fill="x")

    def start_game(self):
        self.withdraw()
        game = LanderGame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = LanderLauncher()
    app.mainloop()