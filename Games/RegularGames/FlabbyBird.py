import os
import sys
import random
import customtkinter as ctk
import pygame

# ==========================================
# 1. חלון התחלה באמצעות CustomTkinter
# ==========================================
class FlappyStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Flappy Bird - Start Menu")
        self.geometry("500x480")
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        # כותרת ראשית
        self.title_label = ctk.CTkLabel(
            self, 
            text="🐦 FLAPPY BIRD 🐦", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#EDC22E"
        )
        self.title_label.pack(pady=(30, 20))
        
        # שם שחקן
        self.name_label = ctk.CTkLabel(self, text="Enter Your Name:", font=("Arial", 16))
        self.name_label.pack(pady=5)
        self.name_input = ctk.CTkEntry(self, placeholder_text="Player", width=200)
        self.name_input.insert(0, "Player 1")
        self.name_input.pack(pady=5)

        # בחירת רמת קושי
        self.difficulty_label = ctk.CTkLabel(self, text="Select Difficulty:", font=("Arial", 16))
        self.difficulty_label.pack(pady=(15, 5))
        self.difficulty_combo = ctk.CTkComboBox(
            self, 
            values=["Easy (Wide Pipes)", "Medium (Normal)", "Hard (Narrow Pipes)"],
            width=200
        )
        self.difficulty_combo.set("Medium (Normal)")
        self.difficulty_combo.pack(pady=5)

        # כפתור התחלה
        self.start_btn = ctk.CTkButton(
            self,
            text="🚀 Start Flying 🚀",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#444444",
            border_width=2,
            border_color="#EDC22E",
            height=50,
            command=self.launch_game
        )
        self.start_btn.pack(pady=40)
        
        self.player_name = "Player"
        self.pipe_gap = 180
        self.should_start = False

        # כפתור חזרה ל-Games Center
        self.btn_back = ctk.CTkButton(
            self,
            text="⬅️ Back to Games Center",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=260,
            height=50,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=30)

    def return_to_main_menu(self):
        """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
        self.back_to_games = True
        self.destroy()

    def launch_game(self):
        self.player_name = self.name_input.get().strip() or "Player"
        diff = self.difficulty_combo.get()
        if "Easy" in diff:
            self.pipe_gap = 220
        elif "Hard" in diff:
            self.pipe_gap = 140
        else:
            self.pipe_gap = 180
            
        self.should_start = True
        self.destroy()


# ==========================================
# 2. קוד המשחק באמצעות Pygame
# ==========================================
def run_flappy_game(player_name, pipe_gap):
    pygame.init()
    
    # מימדי חלון
    WIDTH, HEIGHT = 500, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    
    # צבעים קוסמיים/רטרו
    SKY_BLUE = (104, 136, 252)
    BIRD_COLOR = (244, 208, 63)
    PIPE_COLOR = (39, 174, 96)
    GROUND_COLOR = (212, 172, 13)
    TEXT_COLOR = (255, 255, 255)
    
    # פיזיקת המשחק
    GRAVITY = 0.4
    FLAP_STRENGTH = -7.5
    
    class Bird:
        def __init__(self):
            self.x = 100
            self.y = HEIGHT // 2
            self.radius = 16
            self.velocity = 0

        def update(self):
            self.velocity += GRAVITY
            self.y += self.velocity
            
            # הגבלת נפילה/תקרה
            if self.y < self.radius + 50:  # מתחת לבר הניקוד
                self.y = self.radius + 50
                self.velocity = 0
                
        def flap(self):
            self.velocity = FLAP_STRENGTH

        def draw(self):
            # גוף הציפור
            pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)
            # עין קטנה
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x) + 6, int(self.y) - 4), 3)
            # מקור כתום
            pygame.draw.polygon(screen, (243, 156, 18), [
                (self.x + 12, self.y - 2),
                (self.x + 22, self.y + 2),
                (self.x + 12, self.y + 6)
            ])

    class Pipe:
        def __init__(self, x):
            self.x = x
            self.width = 70
            # גובה פתח רנדומלי במרכז המסך
            self.top_height = random.randint(100, HEIGHT - pipe_gap - 150)
            self.bottom_y = self.top_height + pipe_gap
            self.passed = False

        def update(self, speed):
            self.x -= speed

        def draw(self):
            # צינור עליון
            pygame.draw.rect(screen, PIPE_COLOR, (self.x, 50, self.width, self.top_height - 50))
            pygame.draw.rect(screen, (27, 120, 65), (self.x - 4, self.top_height - 25, self.width + 8, 25))  # שפת הצינור
            
            # צינור תחתון
            pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y - 50))
            pygame.draw.rect(screen, (27, 120, 65), (self.x - 4, self.bottom_y, self.width + 8, 25))

        def collide(self, bird):
            # התנגשות בצינור העליון/תחתון
            if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
                if bird.y - bird.radius < self.top_height or bird.y + bird.radius > self.bottom_y:
                    return True
            return False

    # ישויות
    bird = Bird()
    pipes = [Pipe(WIDTH + 100), Pipe(WIDTH + 400)]
    scroll_speed = 3.5
    
    # ניקוד
    score = 0
    game_state = "PLAYING"  # "PLAYING", "GAMEOVER"
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 42, bold=True)

    running = True
    returned_by_esc = False

    while running:
        clock.tick(60)
        screen.fill(SKY_BLUE)

        # קבלת אירועים
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    returned_by_esc = True
                    running = False

                elif game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        bird.flap()

                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_x:  # משחק מחדש
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 100), Pipe(WIDTH + 400)]
                        score = 0
                        scroll_speed = 3.5
                        game_state = "PLAYING"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "PLAYING":
                    bird.flap()

        if game_state == "PLAYING":
            bird.update()

            # עדכון צינורות
            for pipe in pipes:
                pipe.update(scroll_speed)
                
                # בדיקת פסילה (התנגשות בצינור)
                if pipe.collide(bird):
                    game_state = "GAMEOVER"

                # עדכון ניקוד
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                    # האצה קלה עם הניקוד לאתגר מוגבר!
                    scroll_speed += 0.1

            # מחיקת צינורות שיצאו מהמסך והוספת חדשים
            if pipes[0].x < -pipes[0].width:
                pipes.pop(0)
                # הוספת צינור חדש במרחק קבוע מהצינור האחרון ברשימה
                pipes.append(Pipe(pipes[-1].x + 300))

            # פסילה עקב נפילה לרצפה
            if bird.y + bird.radius >= HEIGHT - 50:
                game_state = "GAMEOVER"

        # --- ציור ---
        
        # ציור צינורות
        for pipe in pipes:
            pipe.draw()

        # ציור רצפה
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 50, WIDTH, 50))
        pygame.draw.rect(screen, (139, 104, 0), (0, HEIGHT - 50, WIDTH, 8))  # שפת הרצפה

        # ציור הציפור
        bird.draw()

        # בר עליון (שם וניקוד)
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, 50))
        name_lbl = font.render(f"👤 {player_name}", True, TEXT_COLOR)
        score_lbl = font.render(f"Score: {score}", True, (241, 196, 15))
        
        screen.blit(name_lbl, (20, 13))
        screen.blit(score_lbl, (WIDTH - score_lbl.get_width() - 20, 13))

        # מסך GameOver
        if game_state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title_txt = large_font.render("GAME OVER", True, (231, 76, 60))
            summary_txt = font.render(f"Final Score: {score}", True, TEXT_COLOR)
            restart_txt = font.render("Press 'X' to Try Again", True, (200, 200, 200))
            exit_txt = font.render("Press 'ESC' to Exit to Menu", True, (231, 76, 60))

            screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(summary_txt, (WIDTH // 2 - summary_txt.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 30))
            screen.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

    pygame.quit()
    return returned_by_esc


# ==========================================
# 3. ניתוב הפעלה ראשי
# ==========================================
if __name__ == "__main__":
    while True:
        menu = FlappyStartWindow()
        menu.mainloop()
        
        # אם המשתמש לחץ על כפתור חזרה ל-Games Center
        if menu.back_to_games:
            break
            
        # אם המשתמש לחץ על כפתור התחלת משחק
        if menu.should_start:
            # מריצים את המשחק ושומרים את הערך המוחזר (True ל-ESC, False ליציאה)
            should_return_to_menu = run_flappy_game(menu.player_name, menu.pipe_gap)
            # אם לא לחצו ESC (למשל סגרו את החלון ב-X), נצא מהלולאה
            if not should_return_to_menu:
                break
        else:
            break