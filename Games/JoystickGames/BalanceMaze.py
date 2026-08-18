import sys
import math
import random
import pygame
import customtkinter as ctk

# CustomTkinter Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Constants & Display Configuration ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BG_COLOR = (15, 23, 42)         # Deep slate background
BOARD_COLOR = (30, 41, 59)      # Tilt board color
WALL_COLOR = (148, 163, 184)    # Maze walls
BALL_COLOR = (59, 130, 246)     # Vibrant blue ball
BALL_SHINE = (147, 197, 253)    # 3D Highlight
GOAL_COLOR = (34, 197, 94)      # Finish zone green
HOLE_COLOR = (2, 6, 23)         # Pit holes
TEXT_COLOR = (241, 245, 249)
RED_ACCENT = (239, 68, 68)


class BalanceMazePygame:
    """Core Physics Engine and Maze Renderer using Pygame"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher

        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Balance & Maze Pro - Precision Physics")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 42, bold=True)

        # Joystick initialization
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Physics variables
        self.tilt_x = 0.0
        self.tilt_y = 0.0
        self.ball_radius = 12
        self.ball_x = 180.0
        self.ball_y = 180.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.friction = 0.985

        # Game state tracking
        self.time_left = 45.0  # Seconds to reach the finish
        self.game_over = False
        self.game_over_reason = ""
        self.won = False

        # Board Boundary
        self.board_rect = pygame.Rect(120, 100, 760, 500)

        # Maze Walls
        self.walls = [
            # Outer board borders
            pygame.Rect(120, 100, 760, 15),
            pygame.Rect(120, 585, 760, 15),
            pygame.Rect(120, 100, 15, 500),
            pygame.Rect(865, 100, 15, 500),
            
            # Inner maze pathway
            pygame.Rect(250, 100, 15, 350),
            pygame.Rect(380, 230, 15, 370),
            pygame.Rect(510, 100, 15, 350),
            pygame.Rect(640, 230, 15, 370),
            pygame.Rect(750, 100, 15, 350)
        ]

        # Dangerous Pit Holes
        self.holes = [
            {"x": 200, "y": 300, "radius": 20},
            {"x": 315, "y": 180, "radius": 22},
            {"x": 450, "y": 480, "radius": 22},
            {"x": 575, "y": 250, "radius": 22},
            {"x": 700, "y": 380, "radius": 22},
        ]

        # Goal Zone
        self.goal = pygame.Rect(780, 480, 70, 70)

    def handle_input(self):
        if self.game_over or self.won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            deadzone = 0.08
            self.tilt_x = axis_x if abs(axis_x) > deadzone else 0.0
            self.tilt_y = axis_y if abs(axis_y) > deadzone else 0.0
        else:
            # Keyboard controls backup
            keys = pygame.key.get_pressed()
            self.tilt_x = (1.0 if keys[pygame.K_RIGHT] else 0.0) - (1.0 if keys[pygame.K_LEFT] else 0.0)
            self.tilt_y = (1.0 if keys[pygame.K_DOWN] else 0.0) - (1.0 if keys[pygame.K_UP] else 0.0)

    def update_physics(self):
        if self.game_over or self.won:
            return

        # Update countdown timer
        self.time_left -= 1.0 / FPS
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            self.game_over_reason = "TIME EXPIRED!"

        # Acceleration derived from tilt angle
        gravity_mult = 0.48
        accel_x = self.tilt_x * gravity_mult
        accel_y = self.tilt_y * gravity_mult

        # Velocity updates with surface friction
        self.vel_x = (self.vel_x + accel_x) * self.friction
        self.vel_y = (self.vel_y + accel_y) * self.friction

        # X-Axis movement + Wall collision check
        self.ball_x += self.vel_x
        ball_rect_x = pygame.Rect(int(self.ball_x - self.ball_radius), int(self.ball_y - self.ball_radius), 
                                 self.ball_radius * 2, self.ball_radius * 2)
        for wall in self.walls:
            if ball_rect_x.colliderect(wall):
                if self.vel_x > 0:
                    self.ball_x = wall.left - self.ball_radius
                elif self.vel_x < 0:
                    self.ball_x = wall.right + self.ball_radius
                self.vel_x = -self.vel_x * 0.35  # Elastic bounce

        # Y-Axis movement + Wall collision check
        self.ball_y += self.vel_y
        ball_rect_y = pygame.Rect(int(self.ball_x - self.ball_radius), int(self.ball_y - self.ball_radius), 
                                 self.ball_radius * 2, self.ball_radius * 2)
        for wall in self.walls:
            if ball_rect_y.colliderect(wall):
                if self.vel_y > 0:
                    self.ball_y = wall.top - self.ball_radius
                elif self.vel_y < 0:
                    self.ball_y = wall.bottom + self.ball_radius
                self.vel_y = -self.vel_y * 0.35  # Elastic bounce

        # Check Pit Hole Falling
        for hole in self.holes:
            dist = math.hypot(self.ball_x - hole["x"], self.ball_y - hole["y"])
            if dist < hole["radius"] - 2:
                self.game_over = True
                self.game_over_reason = "FELL INTO A PIT!"

        # Check Goal Arrival
        ball_point = (int(self.ball_x), int(self.ball_y))
        if self.goal.collidepoint(ball_point):
            self.won = True

    def draw(self):
        self.screen.fill(BG_COLOR)

        # 1. Main Maze Board
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board_rect, border_radius=10)

        # 2. Finish Zone
        pygame.draw.rect(self.screen, GOAL_COLOR, self.goal, border_radius=8)
        goal_text = self.font.render("FINISH", True, BG_COLOR)
        self.screen.blit(goal_text, (self.goal.x + 4, self.goal.y + 22))

        # 3. Pit Holes (Hazards)
        for hole in self.holes:
            pygame.draw.circle(self.screen, HOLE_COLOR, (hole["x"], hole["y"]), hole["radius"])
            pygame.draw.circle(self.screen, RED_ACCENT, (hole["x"], hole["y"]), hole["radius"], 2)

        # 4. Maze Walls
        for wall in self.walls:
            pygame.draw.rect(self.screen, WALL_COLOR, wall, border_radius=3)

        # 5. Physics Ball Render
        if not (self.game_over and "PIT" in self.game_over_reason):
            pygame.draw.circle(self.screen, BALL_COLOR, (int(self.ball_x), int(self.ball_y)), self.ball_radius)
            pygame.draw.circle(self.screen, BALL_SHINE, (int(self.ball_x - 3), int(self.ball_y - 3)), 4)

        # 6. HUD / Dashboard Status
        tilt_str = f"Tilt -> Pitch (Y): {self.tilt_y * 100:.0f}% | Roll (X): {self.tilt_x * 100:.0f}%"
        self.screen.blit(self.font.render(tilt_str, True, TEXT_COLOR), (20, 20))

        time_color = RED_ACCENT if self.time_left < 10 else TEXT_COLOR
        time_str = f"Time Remaining: {self.time_left:.1f}s"
        self.screen.blit(self.font.render(time_str, True, time_color), (SCREEN_WIDTH - 250, 20))

        # Win / Loss Messaging Overlays
        if self.won:
            win_surf = self.big_font.render("MAZE CLEARED! PERFECT BALANCE!", True, GOAL_COLOR)
            restart_surf = self.font.render("Press 'R' to Play Again", True, TEXT_COLOR)
            self.screen.blit(win_surf, (SCREEN_WIDTH // 2 - 320, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 30))

        elif self.game_over:
            over_surf = self.big_font.render(self.game_over_reason, True, RED_ACCENT)
            restart_surf = self.font.render("Press 'R' to Retry or Exit Window", True, TEXT_COLOR)
            self.screen.blit(over_surf, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 30))

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
class BalanceMazeLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JoysticGames - Balance & Maze Launcher")
        self.geometry("550x550")
        self.resizable(False, False)

        # Main Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🎯 Balance & Maze Pro", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#60a5fa"
        )
        self.title_label.pack(pady=(30, 10))

        # Subtitle Description
        self.desc_label = ctk.CTkLabel(
            self, 
            text="Tilt the board to guide the steel ball through the maze.\nAvoid pit traps and reach the green exit before time runs out!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Instructions Frame
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=40, pady=15, fill="x")

        instructions = (
            "🎮 Game Controls & Objectives:\n"
            "• Joystick Axis / Arrow Keys: Tilt the Maze Board\n"
            "• Guide the ball to the green FINISH zone\n"
            "• Complete the course in under 45 seconds\n\n"
            "⚠️ Beware of black pit holes!"
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
            text="▶️ Start Challenge", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.start_game
        )
        self.start_button.pack(pady=(10, 10), padx=50, fill="x")

        # Return to GameCenter Button
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
        game = BalanceMazePygame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = BalanceMazeLauncher()
    app.mainloop()