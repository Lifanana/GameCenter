import sys
import math
import random
import pygame
import customtkinter as ctk

# CustomTkinter Styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Constants ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60

# Colors
DARK_ROAD = (18, 18, 24)
LANE_COLOR = (255, 255, 255)
PLAYER_COLOR = (6, 182, 212)    # Neon Cyan
TRAFFIC_COLOR = (239, 68, 68)   # Red
COIN_COLOR = (234, 179, 8)      # Gold
NITRO_COLOR = (168, 85, 247)    # Purple
GRASS_COLOR = (15, 23, 42)

# Status Colors
GREEN_ONLINE = (34, 197, 94)
RED_OFFLINE = (239, 68, 68)


class CyberpunkDriftGame:
    """Arcade Racing Game with Real-time Joystick Status Indicator"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cyberpunk Drift: Night City")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 44, bold=True)

        # Joystick Setup
        self.joystick = None
        self.check_joystick()

        # Car Dynamics
        self.car_x = SCREEN_WIDTH // 2
        self.car_y = SCREEN_HEIGHT - 120
        self.car_speed = 0.0
        self.max_speed = 12.0
        self.acceleration = 0.25
        self.friction = 0.08

        # Nitro Mechanics
        self.nitro_amount = 100.0
        self.is_nitro_active = False

        # Road Lines Animation
        self.road_offset = 0

        # Entities
        self.traffic = []
        self.coins = []

        self.score = 0
        self.distance = 0
        self.game_over = False

        # Initial Spawns
        for _ in range(3):
            self.spawn_traffic()
        for _ in range(4):
            self.spawn_coin()

    def check_joystick(self):
        """Dynamic runtime check for joystick connection state"""
        pygame.joystick.init()
        count = pygame.joystick.get_count()
        if count > 0:
            if not self.joystick:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
        else:
            self.joystick = None

    def spawn_traffic(self):
        lanes = [280, 390, 500, 610]
        self.traffic.append({
            "x": random.choice(lanes),
            "y": random.randint(-400, -50),
            "speed": random.uniform(2.0, 5.0)
        })

    def spawn_coin(self):
        lanes = [290, 400, 510, 620]
        self.coins.append({
            "x": random.choice(lanes),
            "y": random.randint(-500, -100)
        })

    def handle_input(self):
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        # Check connection on each frame
        self.check_joystick()

        steer = 0.0
        throttle = False
        brake = False
        nitro = False

        if self.joystick:
            steer = self.joystick.get_axis(0)
            pitch = self.joystick.get_axis(1)

            DEADZONE = 0.15
            if abs(steer) < DEADZONE: steer = 0.0

            if pitch < -0.2 or self.joystick.get_button(0):
                throttle = True
            if pitch > 0.4:
                brake = True
            if self.joystick.get_button(1) and self.nitro_amount > 5:
                nitro = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: steer = -1.0
            if keys[pygame.K_RIGHT]: steer = 1.0
            if keys[pygame.K_UP]: throttle = True
            if keys[pygame.K_DOWN]: brake = True
            if keys[pygame.K_LSHIFT] and self.nitro_amount > 5: nitro = True

        # Acceleration Logic
        current_max = self.max_speed * 1.8 if nitro else self.max_speed
        self.is_nitro_active = nitro

        if nitro:
            self.nitro_amount -= 0.6
            self.car_speed += self.acceleration * 2
        elif throttle:
            self.car_speed += self.acceleration
        elif brake:
            self.car_speed -= self.acceleration * 1.5
        else:
            self.car_speed -= self.friction

        # Passive Nitro Recharge
        if not nitro and self.nitro_amount < 100:
            self.nitro_amount += 0.05

        # Speed Clamp
        self.car_speed = max(0.0, min(current_max, self.car_speed))

        # Steering Speed Multiplier
        self.car_x += steer * (5.5 + (self.car_speed * 0.3))

        # Keep on Track Boundary
        if self.car_x < 210 or self.car_x > 670:
            self.car_speed *= 0.92
            if self.car_x < 190: self.car_x = 190
            if self.car_x > 690: self.car_x = 690

    def update_logic(self):
        if self.game_over:
            return

        self.distance += int(self.car_speed)
        self.road_offset = (self.road_offset + self.car_speed) % 80

        car_rect = pygame.Rect(self.car_x - 20, self.car_y - 35, 40, 70)

        # Update Traffic Vehicles
        for car in self.traffic[:]:
            car["y"] += self.car_speed - car["speed"]

            if car["y"] > SCREEN_HEIGHT + 100 or car["y"] < -600:
                if car in self.traffic:
                    self.traffic.remove(car)
                self.spawn_traffic()

            traffic_rect = pygame.Rect(car["x"] - 20, car["y"] - 35, 40, 70)
            if car_rect.colliderect(traffic_rect):
                self.game_over = True

        # Update Coins
        for coin in self.coins[:]:
            coin["y"] += self.car_speed

            coin_rect = pygame.Rect(coin["x"] - 15, coin["y"] - 15, 30, 30)
            if car_rect.colliderect(coin_rect):
                self.score += 250
                if coin in self.coins:
                    self.coins.remove(coin)
                self.spawn_coin()
            elif coin["y"] > SCREEN_HEIGHT + 50:
                if coin in self.coins:
                    self.coins.remove(coin)
                self.spawn_coin()

    def draw(self):
        # 1. Background / Grass
        self.screen.fill(GRASS_COLOR)

        # 2. Main Asphalt Road
        pygame.draw.rect(self.screen, DARK_ROAD, (200, 0, 500, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255), (195, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255), (695, 0, 10, SCREEN_HEIGHT))

        # Lane Markings
        lane_x_positions = [325, 450, 575]
        for lx in lane_x_positions:
            for y in range(-80, SCREEN_HEIGHT + 80, 80):
                pygame.draw.rect(self.screen, LANE_COLOR, (lx - 3, y + int(self.road_offset), 6, 40))

        # 3. Coins
        for coin in self.coins:
            pygame.draw.circle(self.screen, COIN_COLOR, (int(coin["x"]), int(coin["y"])), 12)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(coin["x"]), int(coin["y"])), 6)

        # 4. Traffic Cars
        for car in self.traffic:
            cx, cy = int(car["x"]), int(car["y"])
            pygame.draw.rect(self.screen, TRAFFIC_COLOR, (cx - 20, cy - 35, 40, 70), border_radius=6)
            pygame.draw.rect(self.screen, (255, 255, 255), (cx - 16, cy + 28, 8, 5))
            pygame.draw.rect(self.screen, (255, 255, 255), (cx + 8, cy + 28, 8, 5))

        # 5. Player Sports Car
        px, py = int(self.car_x), int(self.car_y)

        if self.is_nitro_active and self.car_speed > 2:
            flame_h = random.randint(25, 45)
            pygame.draw.polygon(self.screen, NITRO_COLOR, [
                (px - 10, py + 35), (px + 10, py + 35), (px, py + 35 + flame_h)
            ])

        pygame.draw.rect(self.screen, PLAYER_COLOR, (px - 20, py - 35, 40, 70), border_radius=8)
        pygame.draw.rect(self.screen, (15, 23, 42), (px - 14, py - 15, 28, 20), border_radius=3)

        # 6. Dashboard HUD Left
        txt_score = self.font.render(f"Score: {self.score}", True, COIN_COLOR)
        txt_speed = self.font.render(f"Speed: {int(self.car_speed * 18)} km/h", True, (255, 255, 255))
        self.screen.blit(txt_score, (20, 20))
        self.screen.blit(txt_speed, (20, 50))

        # Nitro Bar Gauge
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 90, 160, 16), border_radius=4)
        nitro_w = int((max(0, self.nitro_amount) / 100.0) * 156)
        if nitro_w > 0:
            pygame.draw.rect(self.screen, NITRO_COLOR, (22, 92, nitro_w, 12), border_radius=3)
        txt_nitro = self.font.render("NITRO", True, NITRO_COLOR)
        self.screen.blit(txt_nitro, (190, 86))

        # -------------------------------------------------------------
        # 7. TOP RIGHT IN-GAME JOYSTICK INDICATOR
        # -------------------------------------------------------------
        indicator_x = SCREEN_WIDTH - 210
        indicator_y = 20

        # Background badge
        pygame.draw.rect(self.screen, (15, 23, 42), (indicator_x, indicator_y, 190, 36), border_radius=18)
        
        if self.joystick:
            # Online state
            pygame.draw.circle(self.screen, GREEN_ONLINE, (indicator_x + 20, indicator_y + 18), 7)
            status_txt = self.small_font.render("JOYSTICK ONLINE", True, GREEN_ONLINE)
        else:
            # Offline / Keyboard state
            pygame.draw.circle(self.screen, RED_OFFLINE, (indicator_x + 20, indicator_y + 18), 7)
            status_txt = self.small_font.render("KEYBOARD MODE", True, RED_OFFLINE)

        self.screen.blit(status_txt, (indicator_x + 35, indicator_y + 9))

        # Game Over Screen
        if self.game_over:
            msg = self.big_font.render("CRASHED!", True, TRAFFIC_COLOR)
            sub = self.font.render("Press 'R' to Restart Race", True, (255, 255, 255))
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update_logic()
            self.draw()

        pygame.quit()
        self.launcher.deiconify()


# --- CustomTkinter Launcher ---
class DriftLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.joystick.init()

        self.title("JoysticGames - Cyberpunk Drift Launcher")
        self.geometry("550x580")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🏎️ Cyberpunk Drift", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#06b6d4"
        )
        self.title_label.pack(pady=(25, 5))

        # -------------------------------------------------------------
        # LAUNCHER JOYSTICK STATUS INDICATOR
        # -------------------------------------------------------------
        self.status_frame = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=20)
        self.status_frame.pack(pady=8)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            padx=15,
            pady=4
        )
        self.status_label.pack()

        # Description
        self.desc_label = ctk.CTkLabel(
            self, 
            text="Dodge traffic at high speeds, hit NitroBoost,\nand collect gold coins on the Cyber Highway!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Instructions Box
        self.info_frame = ctk.CTkFrame(self, fg_color="#0F172A", corner_radius=10)
        self.info_frame.pack(padx=40, pady=10, fill="x")

        instructions = (
            "🎮 Controls:\n"
            "• Joystick Left / Right: Steer Vehicle\n"
            "• Stick Forward / Button 0: Throttle (Accelerate)\n"
            "• Stick Down: Brake\n"
            "• Button 1 (or Left Shift): NITRO BOOST ⚡\n\n"
            "⚠️ Avoid red cars and driving off-road!"
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
            text="▶️ Start Race", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#0891b2",
            hover_color="#0e7490",
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

        # Start listening for joystick connection updates in launcher
        self.update_joystick_status()

    def update_joystick_status(self):
        """Continuously polls joystick status in the GUI launcher window"""
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            js = pygame.joystick.Joystick(0)
            js.init()
            name = js.get_name()
            self.status_label.configure(
                text=f"🟢 JOYSTICK CONNECTED: {name}",
                text_color="#22c55e"
            )
        else:
            self.status_label.configure(
                text="🔴 NO JOYSTICK DETECTED (KEYBOARD FALLBACK)",
                text_color="#ef4444"
            )
        
        # Poll state every 1000ms
        self.after(1000, self.update_joystick_status)

    def start_game(self):
        self.withdraw()
        game = CyberpunkDriftGame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = DriftLauncher()
    app.mainloop()