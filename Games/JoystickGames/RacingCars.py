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
GRASS_COLOR = (34, 197, 94)      # Track grass
TRACK_COLOR = (51, 65, 85)       # Asphalt
BORDER_COLOR = (241, 245, 249)    # Track border
CAR_COLOR = (239, 68, 68)        # Red car
CAR_ROOF = (185, 28, 28)
OIL_COLOR = (15, 23, 42)         # Oil hazard
BOOST_COLOR = (234, 179, 8)      # Turbo boost
TEXT_COLOR = (241, 245, 249)
GOLD_ACCENT = (250, 204, 21)


class DirectionalRacingPygame:
    """Racing Engine with Direct 4-Directional Movement"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Joystick Racing Pro - Directional Mode")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 42, bold=True)

        # Joystick initialization
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Car properties
        self.car_x = 500.0
        self.car_y = 575.0
        self.car_angle = 0.0  # 0 = Right, 90 = Up, 180 = Left, 270 = Down
        self.base_speed = 6.5
        self.speed = 6.5

        # Track definition
        self.track_inner = [
            (250, 200), (750, 200), (800, 300), (750, 500), 
            (500, 450), (350, 500), (200, 400)
        ]
        self.track_outer = [
            (150, 100), (850, 100), (950, 300), (850, 600), 
            (500, 550), (300, 600), (100, 400)
        ]

        # Pickups and Hazards
        self.oil_slicks = [(300, 150), (820, 220), (600, 520)]
        self.turbo_pads = [(700, 150), (400, 530)]

        # Game state
        self.laps = 0
        self.target_laps = 3
        self.checkpoint_passed = False
        self.current_lap_time = 0.0
        self.best_lap_time = None
        self.boost_timer = 0
        self.won = False

    def is_on_track(self, x, y):
        """Check if car is on the asphalt road"""
        point = (x, y)
        in_outer = pygame.Rect(100, 100, 850, 500).collidepoint(point)
        in_inner = pygame.Rect(200, 200, 600, 300).collidepoint(point)
        return in_outer and not in_inner

    def handle_input(self):
        if self.won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        move_x = 0.0
        move_y = 0.0

        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            deadzone = 0.2
            if abs(axis_x) > deadzone: move_x = axis_x
            if abs(axis_y) > deadzone: move_y = axis_y
        else:
            # Keyboard fallback
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: move_x = -1.0
            if keys[pygame.K_RIGHT]: move_x = 1.0
            if keys[pygame.K_UP]: move_y = -1.0
            if keys[pygame.K_DOWN]: move_y = 1.0

        # Turbo Speed Multiplier
        if self.boost_timer > 0:
            current_speed = self.base_speed * 1.6
            self.boost_timer -= 1
        else:
            current_speed = self.base_speed

        # Grass Slowdown Penalty
        if not self.is_on_track(self.car_x, self.car_y):
            current_speed *= 0.5

        # Direct 4-Directional Movement Logic
        if move_x != 0 or move_y != 0:
            # Determine dominant move direction or vector angle
            angle_rad = math.atan2(-move_y, move_x)
            self.car_angle = math.degrees(angle_rad)

            # Normalize diagonal speed
            magnitude = math.hypot(move_x, move_y)
            if magnitude > 1.0:
                move_x /= magnitude
                move_y /= magnitude

            # Update position directly
            self.car_x += move_x * current_speed
            self.car_y += move_y * current_speed

    def update_physics(self):
        if self.won:
            return

        self.current_lap_time += 1.0 / FPS

        # Turbo Pad Collision
        for pad in self.turbo_pads:
            if math.hypot(self.car_x - pad[0], self.car_y - pad[1]) < 25:
                self.boost_timer = 60

        # Oil Slick Hazard Collision
        for oil in self.oil_slicks:
            if math.hypot(self.car_x - oil[0], self.car_y - oil[1]) < 25:
                # Random spin on oil
                self.car_angle += random.choice([-90, 90, 180])

        # Lap Checkpoint Logic
        if 480 < self.car_x < 520 and 500 < self.car_y < 620:
            if self.checkpoint_passed:
                self.laps += 1
                self.checkpoint_passed = False

                if self.best_lap_time is None or self.current_lap_time < self.best_lap_time:
                    self.best_lap_time = self.current_lap_time
                self.current_lap_time = 0.0

                if self.laps >= self.target_laps:
                    self.won = True

        elif 480 < self.car_x < 520 and 100 < self.car_y < 200:
            self.checkpoint_passed = True

    def draw(self):
        self.screen.fill(GRASS_COLOR)

        # Track rendering
        pygame.draw.polygon(self.screen, TRACK_COLOR, self.track_outer)
        pygame.draw.polygon(self.screen, BORDER_COLOR, self.track_outer, 5)
        pygame.draw.polygon(self.screen, GRASS_COLOR, self.track_inner)
        pygame.draw.polygon(self.screen, BORDER_COLOR, self.track_inner, 5)

        # Hazards & Boosters
        for oil in self.oil_slicks:
            pygame.draw.circle(self.screen, OIL_COLOR, oil, 22)
        for pad in self.turbo_pads:
            pygame.draw.circle(self.screen, BOOST_COLOR, pad, 18)

        # Finish Line
        pygame.draw.line(self.screen, BORDER_COLOR, (500, 550), (500, 600), 6)

        # Render Car Rotated to Facing Direction
        car_surface = pygame.Surface((34, 18), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, CAR_COLOR, (0, 0, 34, 18), border_radius=4)
        pygame.draw.rect(car_surface, CAR_ROOF, (10, 3, 14, 12), border_radius=2)

        if self.boost_timer > 0:
            pygame.draw.circle(car_surface, BOOST_COLOR, (0, 9), 6)

        rotated_car = pygame.transform.rotate(car_surface, self.car_angle)
        new_rect = rotated_car.get_rect(center=(int(self.car_x), int(self.car_y)))
        self.screen.blit(rotated_car, new_rect.topleft)

        # HUD Overlay
        hud_txt = f"Lap: {self.laps}/{self.target_laps}  |  Time: {self.current_lap_time:.1f}s"
        self.screen.blit(self.font.render(hud_txt, True, TEXT_COLOR), (20, 20))

        if self.best_lap_time:
            best_txt = f"Best Lap: {self.best_lap_time:.2f}s"
            self.screen.blit(self.font.render(best_txt, True, GOLD_ACCENT), (SCREEN_WIDTH - 220, 20))

        if self.won:
            win_surf = self.big_font.render("RACE FINISHED! VICTORY!", True, GOLD_ACCENT)
            restart_surf = self.font.render("Press 'R' to Race Again", True, TEXT_COLOR)
            self.screen.blit(win_surf, (SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 30))

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
class DirectionalRacingLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Directional Racing Launcher")
        self.geometry("550x550")
        self.resizable(False, False)

        self.title_label = ctk.CTkLabel(
            self, 
            text="🏎️ Direct Control Racing", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ef4444"
        )
        self.title_label.pack(pady=(30, 10))

        self.desc_label = ctk.CTkLabel(
            self, 
            text="Drive directly in 4 directions!\nUp/Down to go Up/Down, Left/Right to go Left/Right.",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=40, pady=15, fill="x")

        instructions = (
            "🎮 Direct Controls:\n"
            "• Stick / Keys UP: Move Up\n"
            "• Stick / Keys DOWN: Move Down\n"
            "• Stick / Keys LEFT: Move Left\n"
            "• Stick / Keys RIGHT: Move Right\n\n"
            "🏁 Collect Yellow Turbos & complete 3 Laps!"
        )
        self.info_text = ctk.CTkLabel(
            self.info_frame, 
            text=instructions, 
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        self.info_text.pack(pady=15, padx=15)

        self.start_button = ctk.CTkButton(
            self, 
            text="▶️ Start Race", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.start_game
        )
        self.start_button.pack(pady=(10, 10), padx=50, fill="x")

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
        game = DirectionalRacingPygame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = DirectionalRacingLauncher()
    app.mainloop()