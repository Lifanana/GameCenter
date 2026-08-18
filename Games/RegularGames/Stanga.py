import os
import sys
import math
import customtkinter as ctk
import pygame

# ==========================================
# 1. חלון התחלה באמצעות CustomTkinter
# ==========================================
class StangaStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Stanga - Start Menu")
        self.geometry("500x480")  # שינוי גודל החלון ל-500x480
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        # כותרת ראשית
        self.title_label = ctk.CTkLabel(
            self, 
            text="⚽ STANGA ⚽", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#EDC22E"
        )
        self.title_label.pack(pady=(30, 20))
        
        # הסבר קצר על החוקים
        self.rules_label = ctk.CTkLabel(
            self,
            text="Rules: Each player stays in their half.\nHit the curb/post = 1 Pt | Clean Goal = 3 Pts\nFirst to 10 wins!",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#BBBBBB"
        )
        self.rules_label.pack(pady=(0, 20))

        # מסגרת לקלט שמות שחקנים
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10)

        # שחקן 1 (שמאל)
        self.p1_label = ctk.CTkLabel(self.input_frame, text="Player 1 (Left - WASD):", font=("Arial", 14))
        self.p1_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.p1_input = ctk.CTkEntry(self.input_frame, placeholder_text="Name 1", width=180)
        self.p1_input.insert(0, "Player 1")
        self.p1_input.grid(row=0, column=1, padx=10, pady=5)

        # שחקן 2 (ימין)
        self.p2_label = ctk.CTkLabel(self.input_frame, text="Player 2 (Right - Arrows):", font=("Arial", 14))
        self.p2_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.p2_input = ctk.CTkEntry(self.input_frame, placeholder_text="Name 2", width=180)
        self.p2_input.insert(0, "Player 2")
        self.p2_input.grid(row=1, column=1, padx=10, pady=5)

        # כפתור התחלה
        self.start_btn = ctk.CTkButton(
            self,
            text="⚽ Start Game ⚽",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#444444",
            border_width=2,
            border_color="#EDC22E",
            height=50,
            command=self.launch_game
        )
        self.start_btn.pack(pady=30)

         # כפתור חזרה ל-Games Center
        self.btn_back = ctk.CTkButton(
            self,
            text="⬅️ Back to Games Center",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=260,
            height=100,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=30)
        
        # נתונים שיועברו למשחק
        self.p1_name = "Player 1"
        self.p2_name = "Player 2"
        self.should_start = False

    def return_to_main_menu(self):
         """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
         self.back_to_games = True
         self.destroy()

    def launch_game(self):
        self.p1_name = self.p1_input.get().strip() or "Player 1"
        self.p2_name = self.p2_input.get().strip() or "Player 2"
        self.should_start = True
        self.destroy()  # סגירת חלון ההתחלה כדי לפתוח את ה-Pygame


# ==========================================
# 2. קוד המשחק הפיזיקלי באמצעות Pygame
# ==========================================
def run_stanga_game(p1_name, p2_name):
    pygame.init()
    
    # מימדי חלון המשחק
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stanga Soccer")
    clock = pygame.time.Clock()
    
    # גוונים וצבעים
    FIELD_GREEN = (34, 139, 34)
    LINE_WHITE = (255, 255, 255)
    RED = (220, 50, 50)
    BLUE = (50, 120, 220)
    BALL_COLOR = (240, 240, 240)
    CURB_COLOR = (120, 120, 120)  # צבע ה"מדרכה"/עמודים
    
    # פיזיקה בסיסית
    FRICTION = 0.985  # חיכוך להאטת הכדור
    
    # ישויות המשחק
    class Player:
        def __init__(self, x, y, color, is_left):
            self.x = x
            self.y = y
            self.radius = 25
            self.color = color
            self.speed = 6
            self.is_left = is_left
            
        def move(self, keys):
            # תנועה לשחקן שמאל (WASD)
            if self.is_left:
                if keys[pygame.K_w]: self.y -= self.speed
                if keys[pygame.K_s]: self.y += self.speed
                if keys[pygame.K_a]: self.x -= self.speed
                if keys[pygame.K_d]: self.x += self.speed
                # חסימת מעבר קו האמצע וחריגת גבולות
                self.x = max(self.radius, min(self.x, WIDTH // 2 - self.radius - 5))
            # תנועה לשחקן ימין (חצים)
            else:
                if keys[pygame.K_UP]: self.y -= self.speed
                if keys[pygame.K_DOWN]: self.y += self.speed
                if keys[pygame.K_LEFT]: self.x -= self.speed
                if keys[pygame.K_RIGHT]: self.x += self.speed
                # חסימת מעבר קו האמצע וחריגת גבולות
                self.x = max(WIDTH // 2 + self.radius + 5, min(self.x, WIDTH - self.radius))
                
            self.y = max(self.radius + 50, min(self.y, HEIGHT - self.radius - 20))

        def draw(self):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)

    class Ball:
        def __init__(self):
            self.reset()
            self.radius = 15

        def reset(self):
            self.x = WIDTH // 2
            self.y = HEIGHT // 2
            self.vx = 0
            self.vy = 0

        def move(self):
            self.x += self.vx
            self.y += self.vy
            # הפעלת חיכוך
            self.vx *= FRICTION
            self.vy *= FRICTION

            # הגבלת מהירות מינימלית לעצירה מוחלטת
            if abs(self.vx) < 0.1: self.vx = 0
            if abs(self.vy) < 0.1: self.vy = 0

            # התנגשות בקירות עליון ותחתון
            if self.y - self.radius <= 50:
                self.y = 50 + self.radius
                self.vy *= -1
            elif self.y + self.radius >= HEIGHT - 20:
                self.y = HEIGHT - 20 - self.radius
                self.vy *= -1

        def draw(self):
            pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius, 1)

    # יצירת האובייקטים
    player1 = Player(150, HEIGHT // 2, RED, is_left=True)
    player2 = Player(850, HEIGHT // 2, BLUE, is_left=False)
    ball = Ball()

    # הגדרות שערים ו"מדרכות" (Stanga Target)
    # השער ממוקם במרכז הקיר, העמודים של השער הם הסטנגה
    GOAL_Y1 = HEIGHT // 2 - 80
    GOAL_Y2 = HEIGHT // 2 + 80
    POST_RADIUS = 15

    p1_score = 0
    p2_score = 0
    font = pygame.font.SysFont("Arial", 26, bold=True)
    announce_text = ""
    announce_timer = 0

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                     pygame.quit()
                     return True

        # עדכון תנועות
        player1.move(keys)
        player2.move(keys)
        ball.move()

        # --- חישוב פיזיקת בעיטה והתנגשות שחקנים בכדור ---
        for p in [player1, player2]:
            dx = ball.x - p.x
            dy = ball.y - p.y
            dist = math.hypot(dx, dy)
            if dist < p.radius + ball.radius:
                # זווית ההתנגשות
                angle = math.atan2(dy, dx)
                # הרחקת הכדור מהשחקן שלא יידבקו
                overlap = (p.radius + ball.radius) - dist
                ball.x += math.cos(angle) * overlap
                ball.y += math.sin(angle) * overlap
                
                # העברת עוצמת תנועת השחקן לכדור (תוספת כוח בעיטה)
                ball.vx = math.cos(angle) * 11
                ball.vy = math.sin(angle) * 11

        # --- בדיקת פגיעות שער או סטנגה ---
        # עמודים (Stanga) - שמאל
        for post_y in [GOAL_Y1, GOAL_Y2]:
            dx = ball.x - 10
            dy = ball.y - post_y
            if math.hypot(dx, dy) < ball.radius + POST_RADIUS:
                # שחקן 2 פגע בעמוד של שחקן 1 (סטנגה!)
                p2_score += 1
                announce_text = f"STANGA! {p2_name} scores 1 Pt!"
                announce_timer = 90
                ball.reset()

        # עמודים (Stanga) - ימין
        for post_y in [GOAL_Y1, GOAL_Y2]:
            dx = ball.x - (WIDTH - 10)
            dy = ball.y - post_y
            if math.hypot(dx, dy) < ball.radius + POST_RADIUS:
                # שחקן 1 פגע בעמוד של שחקן 2 (סטנגה!)
                p1_score += 1
                announce_text = f"STANGA! {p1_name} scores 1 Pt!"
                announce_timer = 90
                ball.reset()

        # שערים (גול נקי) - שמאל
        if ball.x - ball.radius <= 10:
            if GOAL_Y1 < ball.y < GOAL_Y2:
                p2_score += 3
                announce_text = f"GOAL!!! {p2_name} scores 3 Pts!"
                announce_timer = 90
            ball.reset()

        # שערים (גול נקי) - ימין
        if ball.x + ball.radius >= WIDTH - 10:
            if GOAL_Y1 < ball.y < GOAL_Y2:
                p1_score += 3
                announce_text = f"GOAL!!! {p1_name} scores 3 Pts!"
                announce_timer = 90
            ball.reset()

        # --- בדיקת מנצח ---
        # --- בדיקת מנצח (הראשון שמגיע ל-3 נקודות) ---
        game_over = False
        winner_name = ""
        
        if p1_score >= 9:
            game_over = True
            winner_name = p1_name
        elif p2_score >= 9:
            game_over = True
            winner_name = p2_name

        # --- מסך סיום משחק (אם יש מנצח) ---
        if game_over:
            # עצירת תנועת הכדור והשחקנים
            ball.vx, ball.vy = 0, 0
            
            # ציור רקע כהה חצי שקוף על כל המסך
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((10, 10, 10))
            screen.blit(overlay, (0, 0))

            # גופן גדול להכרזה
            large_font = pygame.font.SysFont("Arial", 40, bold=True)
            winner_lbl = large_font.render(f"🏆 {winner_name} Wins! 🏆", True, (255, 215, 0))
            
            # כתוביות הסבר להמשך
            restart_lbl = font.render("Press 'R' to Play Again", True, (255, 255, 255))
            exit_lbl = font.render("Press 'ESC' to Exit to Main Menu", True, (200, 50, 50))

            # מרכוז הטקסטים על המסך
            screen.blit(winner_lbl, (WIDTH // 2 - winner_lbl.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(restart_lbl, (WIDTH // 2 - restart_lbl.get_width() // 2, HEIGHT // 2 + 10))
            screen.blit(exit_lbl, (WIDTH // 2 - exit_lbl.get_width() // 2, HEIGHT // 2 + 60))
            
            pygame.display.flip()

            # לולאת המתנה לקלט של השחקן (מחדש או יציאה)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # משחק מחדש
                            p1_score = 0
                            p2_score = 0
                            player1.__init__(150, HEIGHT // 2, RED, is_left=True)
                            player2.__init__(850, HEIGHT // 2, BLUE, is_left=False)
                            ball.reset()
                            waiting = False
                        if event.key == pygame.K_ESCAPE:  # חזרה ל-Game Center
                            running = False
                            waiting = False
            continue  # מדלג על ציור המשחק הרגיל וממשיך לסיבוב הבא

        # --- ציור המסך הרגיל (קורה רק אם המשחק עדיין פעיל) ---
        screen.fill(FIELD_GREEN)

        # קווי מגרש
        pygame.draw.rect(screen, LINE_WHITE, (10, 50, WIDTH - 20, HEIGHT - 70), 5) # מסגרת
        pygame.draw.line(screen, LINE_WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 20), 4) # קו חצי
        pygame.draw.circle(screen, LINE_WHITE, (WIDTH // 2, HEIGHT // 2), 80, 4) # עיגול אמצע

        # ציור שערים ועמודי סטנגה
        pygame.draw.rect(screen, CURB_COLOR, (0, GOAL_Y1, 10, GOAL_Y2 - GOAL_Y1))
        pygame.draw.circle(screen, (200, 200, 0), (10, GOAL_Y1), POST_RADIUS)
        pygame.draw.circle(screen, (200, 200, 0), (10, GOAL_Y2), POST_RADIUS)

        pygame.draw.rect(screen, CURB_COLOR, (WIDTH - 10, GOAL_Y1, 10, GOAL_Y2 - GOAL_Y1))
        pygame.draw.circle(screen, (200, 200, 0), (WIDTH - 10, GOAL_Y1), POST_RADIUS)
        pygame.draw.circle(screen, (200, 200, 0), (WIDTH - 10, GOAL_Y2), POST_RADIUS)

        # ציור שחקנים וכדור
        player1.draw()
        player2.draw()
        ball.draw()

        # תצוגת תוצאה ופרטי שחקנים למעלה
        p1_lbl = font.render(f"{p1_name}: {p1_score}", True, RED)
        p2_lbl = font.render(f"{p2_name}: {p2_score}", True, BLUE)
        screen.blit(p1_lbl, (50, 10))
        screen.blit(p2_lbl, (WIDTH - 50 - p2_lbl.get_width(), 10))

        # הצגת הכרזות מיוחדות (גול/סטנגה) במרכז
        if announce_timer > 0:
            announce_lbl = font.render(announce_text, True, (255, 230, 0))
            back_rect = pygame.Rect(WIDTH // 2 - announce_lbl.get_width() // 2 - 20, HEIGHT // 2 - 40, announce_lbl.get_width() + 40, 60)
            pygame.draw.rect(screen, (0, 0, 0), back_rect)  # מלבן שחור ונקי ללא שגיאות בורדר!
            screen.blit(announce_lbl, (WIDTH // 2 - announce_lbl.get_width() // 2, HEIGHT // 2 - 25))
            announce_timer -= 1

        pygame.display.flip()

    pygame.quit()


# ==========================================
# 3. ניתוב הפעלה ראשי
# ==========================================
if __name__ == "__main__":
    while True:
        menu = StangaStartWindow()
        menu.mainloop()
        
        # אם המשתמש לחץ על כפתור חזרה ל-Games Center
        if menu.back_to_games:
            break
            
        # אם המשתמש לחץ על כפתור התחלת משחק
        if menu.should_start:
            # מריצים את המשחק ושומרים את הערך המוחזר (True ל-ESC, False ליציאה)
            should_return_to_menu = run_stanga_game(menu.p1_name, menu.p2_name)
            
            # אם לא לחצו ESC (למשל סגרו את החלון ב-X), נצא מהלולאה
            if not should_return_to_menu:
                break
            # אם לחצו ESC, הלולאה תמשיך ותפתח שוב את חלון ה-StangaStartWindow
        else:
            break        
