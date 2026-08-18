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
SPACE_BG = (10, 15, 26)          # Deep space
STATION_COLOR = (148, 163, 184)  # Metallic silver
DOCK_PORT_COLOR = (34, 197, 94)  # Docking green
SHIP_COLOR = (59, 130, 246)     # Spacecraft blue
THRUSTER_COLOR = (249, 115, 22)  # Thruster orange
TEXT_COLOR = (241, 245, 249)
ALERT_COLOR = (239, 68, 68)     # Warning red
GOLD_ACCENT = (250, 204, 21)


class DirectionalSpaceSimulator:
    """Space Docking Simulator with Direct 4-Directional Movement"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Docking Simulator - Direct Control")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 38, bold=True)

        # Joystick setup
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Spacecraft state
        self.ship_x = 180.0
        self.ship_y = 350.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.ship_angle = 0.0     # Facing angle
        self.rcs_active = False

        # Space Station & Docking Port
        self.station_x = 820
        self.station_y = 350
        self.dock_rect = pygame.Rect(self.station_x - 45, self.station_y - 30, 25, 60)

        # Game Status
        self.docked = False
        self.crashed = False

    def handle_input(self):
        if self.docked or self.crashed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        move_x = 0.0
        move_y = 0.0
        self.rcs_active = False

        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            deadzone = 0.2
            if abs(axis_x) > deadzone: move_x = axis_x
            if abs(axis_y) > deadzone: move_y = axis_y

            # Emergency Brakes (Button 0)
            if self.joystick.get_button(0):
                self.vel_x *= 0.88
                self.vel_y *= 0.88
        else:
            # Keyboard 4-directional RCS controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: move_x = -1.0
            if keys[pygame.K_RIGHT]: move_x = 1.0
            if keys[pygame.K_UP]: move_y = -1.0
            if keys[pygame.K_DOWN]: move_y = 1.0

            if keys[pygame.K_SPACE]:  # Emergency Brakes
                self.vel_x *= 0.88
                self.vel_y *= 0.88

        # Direct 4-Directional RCS Acceleration Logic
        if move_x != 0 or move_y != 0:
            self.rcs_active = True
            thrust_accel = 0.16

            # Rotate ship towards movement vector
            angle_rad = math.atan2(move_y, move_x)
            self.ship_angle = math.degrees(-angle_rad)

            # Apply thrust vector
            magnitude = math.hypot(move_x, move_y)
            if magnitude > 1.0:
                move_x /= magnitude
                move_y /= magnitude

            self.vel_x += move_x * thrust_accel
            self.vel_y += move_y * thrust_accel

    def update_physics(self):
        if self.docked or self.crashed:
            return

        # Position updates (Inertial motion with minimal space drag)
        self.ship_x += self.vel_x
        self.ship_y += self.vel_y
        self.vel_x *= 0.992
        self.vel_y *= 0.992

        # Screen boundaries check
        if not (15 <= self.ship_x <= SCREEN_WIDTH - 15 and 15 <= self.ship_y <= SCREEN_HEIGHT - 15):
            self.crashed = True

        # Docking Port Collision Check
        ship_rect = pygame.Rect(self.ship_x - 16, self.ship_y - 16, 32, 32)
        if ship_rect.colliderect(self.dock_rect):
            speed = math.hypot(self.vel_x, self.vel_y)

            # Docking requires low impact speed (< 1.8 m/s)
            if speed < 1.8:
                self.docked = True
                self.vel_x = 0
                self.vel_y = 0
            else:
                self.crashed = True

    def draw(self):
        self.screen.fill(SPACE_BG)

        # 1. Space Station Rendering
        pygame.draw.circle(self.screen, STATION_COLOR, (self.station_x + 50, self.station_y), 65)
        pygame.draw.rect(self.screen, (51, 65, 85), (self.station_x + 30, self.station_y - 130, 40, 260))  # Solar Panels
        pygame.draw.rect(self.screen, DOCK_PORT_COLOR, self.dock_rect, 3, border_radius=4)  # Docking Port

        # 2. Spacecraft Rendering
        ship_surface = pygame.Surface((36, 26), pygame.SRCALPHA)
        points = [(32, 13), (0, 0), (8, 13), (0, 26)]
        pygame.draw.polygon(ship_surface, SHIP_COLOR, points)

        if self.rcs_active:
            pygame.draw.polygon(ship_surface, THRUSTER_COLOR, [(0, 7), (-12, 13), (0, 19)])

        rotated_ship = pygame.transform.rotate(ship_surface, self.ship_angle)
        ship_rect = rotated_ship.get_rect(center=(int(self.ship_x), int(self.ship_y)))
        self.screen.blit(rotated_ship, ship_rect.topleft)

        # 3. HUD Dashboard & Telemetry
        speed = math.hypot(self.vel_x, self.vel_y)
        speed_color = DOCK_PORT_COLOR if speed < 1.8 else ALERT_COLOR

        hud_speed = self.font.render(f"Approach Speed: {speed:.2f} m/s", True, speed_color)
        hud_rcs = self.font.render(f"RCS Thrusters: {'ACTIVE' if self.rcs_active else 'IDLE'}", True, TEXT_COLOR)

        self.screen.blit(hud_speed, (20, 20))
        self.screen.blit(hud_rcs, (20, 50))

        # 4. Victory / Crash Overlay
        if self.docked:
            win_txt = self.big_font.render("DOCKING SUCCESSFUL!", True, DOCK_PORT_COLOR)
            restart_txt = self.font.render("Press 'R' to Retry Mission", True, TEXT_COLOR)
            self.screen.blit(win_txt, (SCREEN_WIDTH // 2 - 200, 70))
            self.screen.blit(restart_txt, (SCREEN_WIDTH // 2 - 110, 120))

        elif self.crashed:
            fail_txt = self.big_font.render("CRASH DETECTED! MISSION FAILED", True, ALERT_COLOR)
            restart_txt = self.font.render("Press 'R' to Retry Mission", True, TEXT_COLOR)
            self.screen.blit(fail_txt, (SCREEN_WIDTH // 2 - 270, 70))
            self.screen.blit(restart_txt, (SCREEN_WIDTH // 2 - 110, 120))

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
class SpaceLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Space Docking Launcher")
        self.geometry("550x550")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🚀 Space Docking Pro", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#3b82f6"
        )
        self.title_label.pack(pady=(30, 10))

        # Description
        self.desc_label = ctk.CTkLabel(
            self, 
            text="Navigate deep space using direct 4-directional RCS movement.\nAlign with the Space Station's green docking port at safe speed!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Instructions Box
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=40, pady=15, fill="x")

        instructions = (
            "🎮 Game Controls & Objectives:\n"
            "• Stick / Up-Down-Left-Right: Direct 4-Way RCS Movement\n"
            "• Spacebar / Trigger Button 0: Emergency Brakes\n"
            "• Docking Port: Green target on the space station\n"
            "• Safety Rule: Keep approach speed below 1.8 m/s!\n\n"
            "⚠️ High-speed impact will result in a crash!"
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
            text="▶️ Start Mission", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.start_game
        )
        self.start_button.pack(pady=(10, 10), padx=50, fill="x")

        # Exit to GameCenter Button
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
        game = DirectionalSpaceSimulator(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = SpaceLauncher()
    app.mainloop()