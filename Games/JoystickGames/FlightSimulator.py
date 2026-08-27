import sys
import os
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
SKY_BLUE = (135, 206, 235)
DARK_SKY = (15, 23, 42)
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (239, 68, 68)
GOLD = (234, 179, 8)
CLOUD_GRAY = (203, 213, 225)
FUEL_GREEN = (34, 197, 94)

# Status Colors
GREEN_ONLINE = (34, 197, 94)
RED_OFFLINE = (239, 68, 68)


class FlightSimulatorPygame:
    """Core Flight Simulator Game Engine using Pygame with Dynamic Joystick Indicator"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flight Simulator Pro")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14, bold=True)  # פתרון השגיאה: הוספת פונט קטן לאינדיקטור
        self.big_font = pygame.font.SysFont("Arial", 46, bold=True)

        # Joystick setup
        self.joystick = None
        self.check_joystick()

        # Aircraft parameters
        self.plane_x = SCREEN_WIDTH // 2
        self.plane_y = SCREEN_HEIGHT // 2
        self.pitch = 0
        self.roll = 0
        self.fuel = 100.0  # Fuel bar
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""

        # Entities
        self.rings = []
        self.clouds = []
        self.fuel_canisters = []

        # Spawn initial objects
        for _ in range(3):
            self.spawn_ring()
        for _ in range(4):
            self.spawn_cloud()

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

    def spawn_ring(self):
        """Spawns a target ring"""
        self.rings.append({
            "x": random.randint(150, SCREEN_WIDTH - 150),
            "y": random.randint(150, SCREEN_HEIGHT - 250),
            "size": random.randint(45, 65),
            "speed": random.uniform(1.5, 3.5)
        })

    def spawn_cloud(self):
        """Spawns an obstacle cloud"""
        self.clouds.append({
            "x": random.randint(100, SCREEN_WIDTH - 100),
            "y": random.randint(100, SCREEN_HEIGHT - 300),
            "radius": random.randint(35, 50),
            "speed": random.uniform(1.0, 2.5)
        })

    def spawn_fuel(self):
        """Spawns fuel refill pickup"""
        if len(self.fuel_canisters) < 1 and random.random() < 0.3:
            self.fuel_canisters.append({
                "x": random.randint(150, SCREEN_WIDTH - 150),
                "y": random.randint(150, SCREEN_HEIGHT - 250),
                "speed": random.uniform(1.0, 2.0)
            })

    def handle_input(self):
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        # Check for joystick insertion/removal on every frame
        self.check_joystick()

        axis_roll = 0.0
        axis_pitch = 0.0

        if self.joystick:
            axis_roll = self.joystick.get_axis(0)
            axis_pitch = self.joystick.get_axis(1)

            DEADZONE = 0.08
            if abs(axis_roll) < DEADZONE: axis_roll = 0
            if abs(axis_pitch) < DEADZONE: axis_pitch = 0
        else:
            # Keyboard fallback controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: axis_roll = -0.7
            if keys[pygame.K_RIGHT]: axis_roll = 0.7
            if keys[pygame.K_UP]: axis_pitch = -0.7
            if keys[pygame.K_DOWN]: axis_pitch = 0.7

        # Update flight angles and movement
        self.roll = axis_roll * 30
        self.pitch = axis_pitch * 20

        self.plane_x += axis_roll * 7
        self.plane_y += axis_pitch * 7

        # Keep aircraft within screen bounds
        self.plane_x = max(80, min(SCREEN_WIDTH - 80, self.plane_x))
        self.plane_y = max(80, min(SCREEN_HEIGHT - 120, self.plane_y))

    def update_logic(self):
        if self.game_over:
            return

        # Deplete fuel over time
        self.fuel -= 0.08
        if self.fuel <= 0:
            self.fuel = 0
            self.game_over = True
            self.game_over_reason = "OUT OF FUEL!"

        # Update Rings (Targets)
        for ring in self.rings[:]:
            ring["y"] += ring["speed"]

            dist = math.hypot(self.plane_x - ring["x"], self.plane_y - ring["y"])
            if dist < ring["size"]:
                self.score += 150
                self.fuel = min(100.0, self.fuel + 10)
                if ring in self.rings:
                    self.rings.remove(ring)
                self.spawn_ring()
                self.spawn_fuel()
            elif ring["y"] > SCREEN_HEIGHT - 120:
                if ring in self.rings:
                    self.rings.remove(ring)
                self.spawn_ring()

        # Update Clouds (Obstacles)
        for cloud in self.clouds[:]:
            cloud["y"] += cloud["speed"]
            if cloud["y"] > SCREEN_HEIGHT - 120:
                if cloud in self.clouds:
                    self.clouds.remove(cloud)
                self.spawn_cloud()
            else:
                dist = math.hypot(self.plane_x - cloud["x"], self.plane_y - cloud["y"])
                if dist < cloud["radius"]:
                    self.game_over = True
                    self.game_over_reason = "CRASHED INTO A STORM CLOUD!"

        # Update Fuel Canisters
        for fuel_item in self.fuel_canisters[:]:
            fuel_item["y"] += fuel_item["speed"]

            dist = math.hypot(self.plane_x - fuel_item["x"], self.plane_y - fuel_item["y"])
            if dist < 35:
                self.fuel = min(100.0, self.fuel + 35)
                if fuel_item in self.fuel_canisters:
                    self.fuel_canisters.remove(fuel_item)
            elif fuel_item["y"] > SCREEN_HEIGHT - 120:
                if fuel_item in self.fuel_canisters:
                    self.fuel_canisters.remove(fuel_item)

    def draw(self):
        # Draw sky background
        self.screen.fill(SKY_BLUE)

        # Dynamic ground horizon based on pitch
        horizon_y = (SCREEN_HEIGHT // 2) + (self.pitch * 5) + 100
        pygame.draw.rect(self.screen, GREEN, (0, horizon_y, SCREEN_WIDTH, SCREEN_HEIGHT - horizon_y))

        # 1. Draw Clouds
        for cloud in self.clouds:
            pygame.draw.circle(self.screen, CLOUD_GRAY, (int(cloud["x"]), int(cloud["y"])), cloud["radius"])
            pygame.draw.circle(self.screen, WHITE, (int(cloud["x"]) - 15, int(cloud["y"]) - 5), cloud["radius"] - 10)

        # 2. Draw Target Rings
        for ring in self.rings:
            pygame.draw.circle(self.screen, GOLD, (int(ring["x"]), int(ring["y"])), ring["size"], 8)

        # 3. Draw Fuel Pickups
        for fuel_item in self.fuel_canisters:
            pygame.draw.rect(self.screen, FUEL_GREEN, (fuel_item["x"] - 12, fuel_item["y"] - 15, 24, 30), border_radius=4)
            pygame.draw.rect(self.screen, WHITE, (fuel_item["x"] - 5, fuel_item["y"] - 20, 10, 5))

        # 4. Draw Aircraft (Crosshair HUD)
        pygame.draw.circle(self.screen, RED, (int(self.plane_x), int(self.plane_y)), 8)
        wing_offset_x = math.cos(math.radians(self.roll)) * 45
        wing_offset_y = math.sin(math.radians(self.roll)) * 45
        pygame.draw.line(self.screen, RED, 
                         (self.plane_x - wing_offset_x, self.plane_y - wing_offset_y), 
                         (self.plane_x + wing_offset_x, self.plane_y + wing_offset_y), 6)

        # 5. Draw Heads-Up Display (HUD) Left
        score_txt = self.font.render(f"Score: {self.score}", True, DARK_SKY)
        self.screen.blit(score_txt, (20, 20))

        # Fuel Gauge
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 55, 200, 20), border_radius=5)
        fuel_width = int((self.fuel / 100.0) * 196)
        fuel_color = FUEL_GREEN if self.fuel > 30 else RED
        if fuel_width > 0:
            pygame.draw.rect(self.screen, fuel_color, (22, 57, fuel_width, 16), border_radius=4)
        
        fuel_txt = self.font.render("FUEL", True, WHITE)
        self.screen.blit(fuel_txt, (230, 53))

        # -------------------------------------------------------------
        # 6. TOP RIGHT IN-GAME JOYSTICK INDICATOR
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
            over_surf = self.big_font.render(self.game_over_reason, True, RED)
            restart_surf = self.font.render("Press 'R' to Restart or Close Window to Exit", True, DARK_SKY)
            self.screen.blit(over_surf, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 30))

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


# --- Launcher UI (CustomTkinter) ---
class FlightSimulatorLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Flight Simulator Launcher")
        self.geometry("550x580")
        self.resizable(False, False)

        # Main Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🛩️ Flight Simulator Pro", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#38bdf8"
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
            text="Fly through gold rings to gain points and refuel.\nAvoid storm clouds to prevent crashing!",
            font=ctk.CTkFont(size=15),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Controls Panel
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10)
        self.info_frame.pack(padx=40, pady=10, fill="x")

        instructions = (
            "🎮 Flight Controls:\n"
            "• Joystick X Axis / Arrow Keys Left-Right: Roll / Turn\n"
            "• Joystick Y Axis / Arrow Keys Up-Down: Pitch Up/Down\n"
            "• Collect Fuel Canisters to extend flight time!\n\n"
            "⚠️ Watch out for storm clouds!"
        )
        self.info_text = ctk.CTkLabel(
            self.info_frame, 
            text=instructions, 
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        self.info_text.pack(pady=15, padx=15)

        # Start Game Button
        self.start_button = ctk.CTkButton(
            self, 
            text="▶️ Start Flight", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.start_game
        )
        self.start_button.pack(pady=(10, 10), padx=50, fill="x")

        # Back to GameCenter Button
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
        game = FlightSimulatorPygame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = FlightSimulatorLauncher()
    app.mainloop()