import math
import sys
import pygame
import customtkinter as ctk

# CustomTkinter Styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# הגדרות חלון Pygame
WIDTH, HEIGHT = 800, 600

# --- מחלקת חלון הפתיחה (Launcher) ---
class TrackingLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tracking Simulator - Launcher")
        self.geometry("480x460")
        self.resizable(False, False)

        # כותרת ראשית
        self.title_label = ctk.CTkLabel(
            self, 
            text="🎯 Tracking Algorithm Simulator", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00ff78"
        )
        self.title_label.pack(pady=(25, 10))

        # אינדיקטור ג'ויסטיק ב-Launcher
        self.status_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=20)
        self.status_frame.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            padx=15,
            pady=6
        )
        self.status_label.pack()

        # תיבת הסבר
        self.info_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=10)
        self.info_frame.pack(padx=30, pady=10, fill="x")

        instructions = (
            "📌 מצבי הפעלה:\n"
            "• ללא ג'ויסטיק: המטרה תנוע במסלול אוטומטי (שמונה).\n"
            "• עם ג'ויסטיק מחובר: תוכל לשלוט ידנית במטרה (העיגול האדום)\n"
            "  والכוונת הירוקה תעקוב אחריך אוטומטית!"
        )
        self.info_text = ctk.CTkLabel(
            self.info_frame, 
            text=instructions, 
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.info_text.pack(pady=12, padx=12)

        # כפתור הפעלה
        self.start_button = ctk.CTkButton(
            self, 
            text="▶️ התחל סימולציה", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            fg_color="#00aa55",
            hover_color="#008844",
            command=self.start_simulation
        )
        self.start_button.pack(pady=(15, 10), padx=40, fill="x")

        # הפעלת בדיקת ג'ויסטיק בלולאה בתוך ה-Launcher
        self.update_launcher_joystick_status()

    def update_launcher_joystick_status(self):
        """בדיקה ועדכון רציף של סטטוס הג'ויסטיק בחלון הפתיחה"""
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            js = pygame.joystick.Joystick(0)
            js.init()
            name = js.get_name()
            self.status_label.configure(
                text=f"🟢 JOYSTICK ONLINE: {name}",
                text_color="#22c55e"
            )
        else:
            self.status_label.configure(
                text="🔴 NO JOYSTICK (AUTOMATIC MODE)",
                text_color="#ef4444"
            )
        
        # רענון כל שנייה
        self.after(1000, self.update_launcher_joystick_status)

    def start_simulation(self):
        """סגירת חלון הפתיחה והרצת הסימולציה"""
        self.withdraw()
        run_simulation(self)


# --- לולאת הסימולציה של Pygame ---
def run_simulation(launcher_window):
    pygame.init()
    pygame.joystick.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tracking Algorithm Simulator (Dummy Camera)")
    clock = pygame.time.Clock()

    font_small = pygame.font.SysFont("Arial", 14, bold=True)

    # צבעים
    BLACK = (15, 15, 15)
    RED = (255, 60, 60)
    GREEN = (0, 255, 120)
    WHITE = (200, 200, 200)
    GREEN_ONLINE = (34, 197, 94)
    RED_OFFLINE = (239, 68, 68)

    # משתני הסימולציה
    joystick = None
    target_pos = [200.0, 150.0]
    target_angle = 0.0
    target_speed = 0.03
    tracker_pos = [400.0, 300.0]
    KP = 0.08
    MAX_TRACKER_SPEED = 5.0

    def check_joystick():
        nonlocal joystick
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            if not joystick:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
        else:
            joystick = None

    def update_target():
        nonlocal target_angle, joystick
        check_joystick()

        if joystick:
            move_x = joystick.get_axis(0)
            move_y = joystick.get_axis(1)

            DEADZONE = 0.2
            if abs(move_x) > DEADZONE:
                target_pos[0] += move_x * 6.0
            if abs(move_y) > DEADZONE:
                target_pos[1] += move_y * 6.0

            target_pos[0] = max(20, min(WIDTH - 20, target_pos[0]))
            target_pos[1] = max(20, min(HEIGHT - 20, target_pos[1]))
        else:
            target_angle += target_speed
            center_x, center_y = WIDTH / 2, HEIGHT / 2
            target_pos[0] = center_x + math.sin(target_angle) * 250
            target_pos[1] = center_y + math.sin(target_angle * 2) * 150

    def track_target():
        error_x = target_pos[0] - tracker_pos[0]
        error_y = target_pos[1] - tracker_pos[1]

        vel_x = error_x * KP
        vel_y = error_y * KP

        speed = math.hypot(vel_x, vel_y)
        if speed > MAX_TRACKER_SPEED:
            vel_x = (vel_x / speed) * MAX_TRACKER_SPEED
            vel_y = (vel_y / speed) * MAX_TRACKER_SPEED

        tracker_pos[0] += vel_x
        tracker_pos[1] += vel_y

    def draw_joystick_indicator():
        indicator_x = WIDTH - 200
        indicator_y = 15

        pygame.draw.rect(
            screen, (30, 41, 59), (indicator_x, indicator_y, 185, 32), border_radius=16
        )

        if joystick:
            pygame.draw.circle(
                screen, GREEN_ONLINE, (indicator_x + 18, indicator_y + 16), 6
            )
            status_txt = font_small.render("JOYSTICK ONLINE", True, GREEN_ONLINE)
        else:
            pygame.draw.circle(
                screen, RED_OFFLINE, (indicator_x + 18, indicator_y + 16), 6
            )
            status_txt = font_small.render("AUTOMATIC MODE", True, RED_OFFLINE)

        screen.blit(status_txt, (indicator_x + 32, indicator_y + 8))

    # לולאת המשחק
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_target()
        track_target()

        screen.fill(BLACK)

        # ציור מטרה
        pygame.draw.circle(
            screen, RED, (int(target_pos[0]), int(target_pos[1])), 12
        )

        # ציור כוונת
        tx, ty = int(tracker_pos[0]), int(tracker_pos[1])
        pygame.draw.circle(screen, GREEN, (tx, ty), 18, 2)
        pygame.draw.line(screen, GREEN, (tx - 25, ty), (tx + 25, ty), 1)
        pygame.draw.line(screen, GREEN, (tx, ty - 25), (tx, ty + 25), 1)

        # קו שגיאה
        pygame.draw.line(
            screen,
            WHITE,
            (tx, ty),
            (int(target_pos[0]), int(target_pos[1])),
            1,
        )

        draw_joystick_indicator()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    # החזרת חלון הפתיחה כאשר סוגרים את חלון הסימולציה
    launcher_window.deiconify()


if __name__ == "__main__":
    app = TrackingLauncher()
    app.mainloop()