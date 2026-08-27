import sys
import math
import random
import pygame
import customtkinter as ctk

# CustomTkinter Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WATER_COLOR = (15, 23, 42)         # Night water
HOVER_COLOR = (245, 158, 11)       # Rescue orange
SPOTLIGHT_COLOR = (254, 240, 138)  # Light yellow
SURVIVOR_COLOR = (239, 68, 68)     # Survivor red
BASE_COLOR = (34, 197, 94)         # Safety green
TEXT_COLOR = (241, 245, 249)
GOLD_ACCENT = (250, 204, 21)

# Status Colors
GREEN_ONLINE = (34, 197, 94)
RED_OFFLINE = (239, 68, 68)


class Survivor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rescued = False


class DirectionalHovercraftPygame:
    """Hovercraft Rescue Engine with Live Joystick Status Indicator"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hovercraft Rescue - Directional Night Search")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 38, bold=True)

        # Joystick setup
        self.joystick = None
        self.check_joystick()

        # Hovercraft parameters
        self.x = 110.0
        self.y = 110.0
        self.heading_angle = 0.0      # Facing angle (degrees)
        self.spotlight_offset = 0.0   # Optional manual spotlight angle
        self.speed = 5.5

        # Survivors & Safe Base
        self.survivors = [Survivor(random.randint(300, 920), random.randint(120, 620)) for _ in range(6)]
        self.onboard_survivors = 0
        self.saved_survivors = 0
        self.base_rect = pygame.Rect(40, 40, 140, 140)

        self.won = False

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

    def handle_input(self):
        if self.won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        # Check connection state on each frame
        self.check_joystick()

        move_x = 0.0
        move_y = 0.0

        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            deadzone = 0.2
            if abs(axis_x) > deadzone: move_x = axis_x
            if abs(axis_y) > deadzone: move_y = axis_y

            # Optional Twist (Axis 2) for Independent Spotlight control
            if self.joystick.get_numaxes() > 2:
                twist = self.joystick.get_axis(2)
                if abs(twist) > deadzone:
                    self.spotlight_offset += twist * 4.0
        else:
            # Keyboard 4-directional controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: move_x = -1.0
            if keys[pygame.K_RIGHT]: move_x = 1.0
            if keys[pygame.K_UP]: move_y = -1.0
            if keys[pygame.K_DOWN]: move_y = 1.0

            if keys[pygame.K_a]: self.spotlight_offset -= 4.0
            if keys[pygame.K_d]: self.spotlight_offset += 4.0

        # Direct 4-Directional Movement Logic
        if move_x != 0 or move_y != 0:
            angle_rad = math.atan2(move_y, move_x)
            self.heading_angle = math.degrees(-angle_rad)

            magnitude = math.hypot(move_x, move_y)
            if magnitude > 1.0:
                move_x /= magnitude
                move_y /= magnitude

            self.x += move_x * self.speed
            self.y += move_y * self.speed

    def update_physics(self):
        if self.won:
            return

        # Keep inside screen borders
        self.x = max(30, min(SCREEN_WIDTH - 30, self.x))
        self.y = max(30, min(SCREEN_HEIGHT - 30, self.y))

        # Survivor Pickup Check
        hover_rect = pygame.Rect(self.x - 22, self.y - 22, 44, 44)
        for s in self.survivors:
            if not s.rescued and hover_rect.collidepoint(s.x, s.y):
                if self.onboard_survivors < 3:  # Max capacity = 3
                    s.rescued = True
                    self.onboard_survivors += 1

        # Base Drop-off Check
        if hover_rect.colliderect(self.base_rect) and self.onboard_survivors > 0:
            self.saved_survivors += self.onboard_survivors
            self.onboard_survivors = 0

            if self.saved_survivors == len(self.survivors):
                self.won = True

    def draw(self):
        self.screen.fill(WATER_COLOR)

        # 1. Base / Safety Zone
        pygame.draw.rect(self.screen, BASE_COLOR, self.base_rect, 3, border_radius=8)
        base_txt = self.font.render("BASE", True, BASE_COLOR)
        self.screen.blit(base_txt, (self.base_rect.x + 42, self.base_rect.y + 55))

        # 2. Spotlight Cone Calculation
        total_spotlight_deg = self.heading_angle + self.spotlight_offset
        spot_rad = math.radians(-total_spotlight_deg)

        cone_length = 260
        cone_width = 0.38  # Spread angle in radians

        p1 = (self.x, self.y)
        p2 = (self.x + math.cos(spot_rad - cone_width) * cone_length, self.y + math.sin(spot_rad - cone_width) * cone_length)
        p3 = (self.x + math.cos(spot_rad + cone_width) * cone_length, self.y + math.sin(spot_rad + cone_width) * cone_length)

        spot_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(spot_surface, (254, 240, 138, 65), [p1, p2, p3])
        self.screen.blit(spot_surface, (0, 0))

        # 3. Survivors Visibility
        for s in self.survivors:
            if not s.rescued:
                dist = math.hypot(s.x - self.x, s.y - self.y)
                angle_to_s = math.degrees(math.atan2(-(s.y - self.y), s.x - self.x))
                angle_diff = (angle_to_s - total_spotlight_deg + 180) % 360 - 180

                if dist < 85 or (dist < cone_length and abs(angle_diff) < 24):
                    pygame.draw.circle(self.screen, SURVIVOR_COLOR, (int(s.x), int(s.y)), 7)
                    pygame.draw.circle(self.screen, (255, 255, 255), (int(s.x), int(s.y)), 9, 1)

        # 4. Hovercraft Rendering
        hover_surface = pygame.Surface((44, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(hover_surface, (30, 41, 59), (0, 0, 44, 28))
        pygame.draw.ellipse(hover_surface, HOVER_COLOR, (4, 3, 36, 22))
        pygame.draw.rect(hover_surface, (15, 23, 42), (0, 9, 8, 10))  # Rear thruster

        rotated_hover = pygame.transform.rotate(hover_surface, self.heading_angle)
        rect = rotated_hover.get_rect(center=(int(self.x), int(self.y)))
        self.screen.blit(rotated_hover, rect.topleft)

        # 5. HUD Dashboard Left
        hud_onboard = self.font.render(f"Onboard: {self.onboard_survivors}/3", True, TEXT_COLOR)
        hud_saved = self.font.render(f"Saved: {self.saved_survivors}/{len(self.survivors)}", True, BASE_COLOR)

        self.screen.blit(hud_onboard, (20, SCREEN_HEIGHT - 65))
        self.screen.blit(hud_saved, (20, SCREEN_HEIGHT - 35))

        # -------------------------------------------------------------
        # 6. TOP RIGHT IN-GAME JOYSTICK INDICATOR
        # -------------------------------------------------------------
        indicator_x = SCREEN_WIDTH - 210
        indicator_y = 20

        # Background badge
        pygame.draw.rect(self.screen, (30, 41, 59), (indicator_x, indicator_y, 190, 36), border_radius=18)

        if self.joystick:
            # Online state
            pygame.draw.circle(self.screen, GREEN_ONLINE, (indicator_x + 20, indicator_y + 18), 7)
            status_txt = self.small_font.render("JOYSTICK ONLINE", True, GREEN_ONLINE)
        else:
            # Offline / Keyboard state
            pygame.draw.circle(self.screen, RED_OFFLINE, (indicator_x + 20, indicator_y + 18), 7)
            status_txt = self.small_font.render("KEYBOARD MODE", True, RED_OFFLINE)

        self.screen.blit(status_txt, (indicator_x + 35, indicator_y + 9))

        # Victory Message
        if self.won:
            win_txt = self.big_font.render("ALL SURVIVORS RESCUED!", True, GOLD_ACCENT)
            restart_txt = self.font.render("Press 'R' to Play Again", True, TEXT_COLOR)
            self.screen.blit(win_txt, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(restart_txt, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30))

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


# --- Launcher UI (CustomTkinter) ---
class HovercraftLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Hovercraft Rescue Launcher")
        self.geometry("550x580")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🚁 Hovercraft Rescue Pro", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#f59e0b"
        )
        self.title_label.pack(pady=(25, 5))

        # -------------------------------------------------------------
        # LAUNCHER JOYSTICK STATUS INDICATOR
        # -------------------------------------------------------------
        self.status_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=20)
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
            text="Navigate the pitch-black sea in direct 4-directional movement.\nUse your spotlight to locate survivors and transport them to BASE!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Instructions Box
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=40, pady=10, fill="x")

        instructions = (
            "🎮 Game Controls & Rules:\n"
            "• Stick / Up-Down-Left-Right: Direct 4-Way Movement\n"
            "• Keyboard 'A' / 'D' or Joystick Twist: Rotate Spotlight\n"
            "• Hovercraft Capacity: Maximum 3 survivors at once\n"
            "• Return to green BASE zone to drop off rescued survivors\n\n"
            "🚨 Goal: Rescue all 6 survivors to win!"
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
            fg_color="#d97706",
            hover_color="#b45309",
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

        # Start polling joystick status in launcher
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
        game = DirectionalHovercraftPygame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = HovercraftLauncher()
    app.mainloop()