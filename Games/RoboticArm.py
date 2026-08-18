import sys
import os
import math
import pygame
import customtkinter as ctk

# CustomTkinter Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BG_COLOR = (24, 24, 27)         # Dark Gray
ARM_COLOR = (234, 179, 8)       # Industrial Yellow
JOINT_COLOR = (71, 85, 105)     # Metallic Gray
BOX_COLOR = (239, 68, 68)       # Red
BASE_ZONE_COLOR = (34, 197, 94) # Green
TEXT_COLOR = (241, 245, 249)


class CargoStackerPygame:
    """Pygame Game Loop Class"""
    def __init__(self, parent_launcher):
        self.launcher = parent_launcher
        
        pygame.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robotic Arm - Cargo Stacker")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)

        # Joystick initialization
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        # Arm parameters (increased lengths and centered positions for easier reach)
        self.base_x = 350
        self.base_y = SCREEN_HEIGHT - 100
        self.length1 = 220
        self.length2 = 190

        # Joint angles
        self.angle1 = -math.pi / 2.5
        self.angle2 = math.pi / 3

        # Gripper & Box parameters
        self.is_holding = False
        self.gripper_open = True
        self.box_size = 40
        
        # Target drop zone base (moved closer to the robotic arm)
        self.drop_zone = pygame.Rect(600, SCREEN_HEIGHT - 110, 140, 10)
        
        # Game Management
        self.stacked_boxes = []
        self.reset_new_box()

        self.score = 0
        self.game_over = False

    def reset_new_box(self):
        """Spawns a new box at the pick-up station"""
        self.current_box = {
            'x': 180,
            'y': SCREEN_HEIGHT - 120,
            'vx': 0,
            'vy': 0,
            'is_falling': False
        }

    def get_joint_positions(self):
        elbow_x = self.base_x + self.length1 * math.cos(self.angle1)
        elbow_y = self.base_y + self.length1 * math.sin(self.angle1)

        hand_x = elbow_x + self.length2 * math.cos(self.angle1 + self.angle2)
        hand_y = elbow_y + self.length2 * math.sin(self.angle1 + self.angle2)

        return (elbow_x, elbow_y), (hand_x, hand_y)

    def handle_input(self):
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.launcher)
            return

        speed = 0.03
        if self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            deadzone = 0.1
            if abs(axis_x) > deadzone:
                self.angle1 += axis_x * speed
            if abs(axis_y) > deadzone:
                self.angle2 += axis_y * speed

            button_trigger = self.joystick.get_button(0)
            self.gripper_open = not button_trigger
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: self.angle1 -= speed
            if keys[pygame.K_RIGHT]: self.angle1 += speed
            if keys[pygame.K_UP]: self.angle2 -= speed
            if keys[pygame.K_DOWN]: self.angle2 += speed
            self.gripper_open = not keys[pygame.K_SPACE]

        # Angle constraints
        self.angle1 = max(-math.pi + 0.1, min(-0.1, self.angle1))
        self.angle2 = max(-math.pi / 1.1, min(math.pi / 1.1, self.angle2))

    def update_logic(self):
        if self.game_over:
            return

        _, (hand_x, hand_y) = self.get_joint_positions()

        # Distance between box and gripper
        dist = math.hypot(hand_x - self.current_box['x'], hand_y - self.current_box['y'])

        # Grab box
        if not self.gripper_open and dist < 45 and not self.is_holding and not self.current_box['is_falling']:
            self.is_holding = True

        # Release box
        if self.gripper_open and self.is_holding:
            self.is_holding = False
            self.current_box['is_falling'] = True

        # Update box position
        if self.is_holding:
            self.current_box['x'] = hand_x
            self.current_box['y'] = hand_y
        elif self.current_box['is_falling']:
            # Apply gravity
            self.current_box['vy'] += 0.5
            self.current_box['y'] += self.current_box['vy']

            # Target stacking Y height
            target_y = self.drop_zone.y - (self.box_size / 2) - (len(self.stacked_boxes) * self.box_size)
            
            # X limits for balance
            if len(self.stacked_boxes) == 0:
                min_x = self.drop_zone.left
                max_x = self.drop_zone.right
            else:
                top_box_x = self.stacked_boxes[-1]['x']
                min_x = top_box_x - (self.box_size * 0.7)
                max_x = top_box_x + (self.box_size * 0.7)

            # Check alignment on landing
            if self.current_box['y'] >= target_y:
                if min_x <= self.current_box['x'] <= max_x:
                    # Successful drop
                    self.current_box['y'] = target_y
                    self.current_box['is_falling'] = False
                    self.stacked_boxes.append({'x': self.current_box['x'], 'y': target_y})
                    self.score += 1
                    self.reset_new_box()
                else:
                    # Missed / Collapsed
                    self.game_over = True

            # Out of bounds
            if self.current_box['y'] > SCREEN_HEIGHT - 80:
                self.game_over = True

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Floor & Base
        pygame.draw.rect(self.screen, (51, 65, 85), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Target Zone
        pygame.draw.rect(self.screen, BASE_ZONE_COLOR, self.drop_zone)
        target_txt = self.font.render("BUILD TOWER HERE", True, BASE_ZONE_COLOR)
        self.screen.blit(target_txt, (self.drop_zone.x - 10, self.drop_zone.y + 15))

        # Robotic Arm Base
        pygame.draw.rect(self.screen, JOINT_COLOR, (self.base_x - 30, self.base_y, 60, 40))

        # Arm Links
        (elbow_x, elbow_y), (hand_x, hand_y) = self.get_joint_positions()
        pygame.draw.line(self.screen, ARM_COLOR, (self.base_x, self.base_y), (elbow_x, elbow_y), 14)
        pygame.draw.line(self.screen, ARM_COLOR, (elbow_x, elbow_y), (hand_x, hand_y), 10)
        pygame.draw.circle(self.screen, JOINT_COLOR, (self.base_x, self.base_y), 12)
        pygame.draw.circle(self.screen, JOINT_COLOR, (int(elbow_x), int(elbow_y)), 10)

        # Gripper
        grip_gap = 18 if self.gripper_open else 6
        pygame.draw.circle(self.screen, (220, 38, 38), (int(hand_x), int(hand_y)), 5)
        pygame.draw.line(self.screen, TEXT_COLOR, (hand_x - grip_gap, hand_y + 12), (hand_x, hand_y), 4)
        pygame.draw.line(self.screen, TEXT_COLOR, (hand_x + grip_gap, hand_y + 12), (hand_x, hand_y), 4)

        # Render Stacked Boxes
        for b in self.stacked_boxes:
            rect = pygame.Rect(b['x'] - self.box_size // 2, b['y'] - self.box_size // 2, self.box_size, self.box_size)
            pygame.draw.rect(self.screen, (34, 197, 94), rect, border_radius=4)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, width=2, border_radius=4)

        # Render Current Box
        curr_rect = pygame.Rect(self.current_box['x'] - self.box_size // 2, self.current_box['y'] - self.box_size // 2, self.box_size, self.box_size)
        pygame.draw.rect(self.screen, BOX_COLOR, curr_rect, border_radius=4)

        # HUD / Text
        score_txt = f"Tower Height: {self.score} Boxes"
        ctrl_txt = "Controls: Stick X (Shoulder) | Stick Y (Elbow) | Trigger/Space (Grip)"
        self.screen.blit(self.font.render(score_txt, True, TEXT_COLOR), (20, 20))
        self.screen.blit(self.font.render(ctrl_txt, True, (148, 163, 184)), (20, 50))

        # Game Over Overlay
        if self.game_over:
            over_surf = self.big_font.render("TOWER COLLAPSED!", True, (239, 68, 68))
            restart_surf = self.font.render("Press 'R' to Restart or Close Window to Exit", True, TEXT_COLOR)
            self.screen.blit(over_surf, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))

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
class CargoStackerLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Robotic Arm: Cargo Stacker")
        self.geometry("550x550")
        self.resizable(False, False)

        # Main Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🏗️ Cargo Stacker", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#EDC22E"
        )
        self.title_label.pack(pady=(30, 10))

        # Description
        self.desc_label = ctk.CTkLabel(
            self, 
            text="Mission: Build the highest tower possible!\nUse the robotic arm to grab boxes\nand stack them precisely on top of each other.",
            font=ctk.CTkFont(size=15),
            justify="center"
        )
        self.desc_label.pack(pady=10)

        # Controls Info Panel
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10)
        self.info_frame.pack(padx=40, pady=15, fill="x")

        instructions = (
            "🎮 Controls:\n"
            "• Joystick X / Left-Right Arrows: Move Shoulder\n"
            "• Joystick Y / Up-Down Arrows: Move Elbow\n"
            "• Trigger / Spacebar: Open/Close Gripper\n\n"
            "⚠️ Warning: Off-center drops will cause the tower to collapse!"
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
            text="▶️ Start Game", 
            font=ctk.CTkFont(size=18, weight="bold"),
            height=45,
            fg_color="#22c55e",
            hover_color="#16a34a",
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
        game = CargoStackerPygame(self)
        game.run()

    def return_to_gamecenter(self):
        self.destroy()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = CargoStackerLauncher()
    app.mainloop()