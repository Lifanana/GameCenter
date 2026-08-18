import os
import sys
import customtkinter as ctk
import pygame

# ==========================================
# 1. חלון פתיחה (CustomTkinter)
# ==========================================
class PongStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ping Pong - Start Menu")
        self.geometry("500x480")
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        self.title_label = ctk.CTkLabel(
            self, text="🏓 PING PONG 🏓", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#2ECC71"
        )
        self.title_label.pack(pady=(35, 20))
        
        self.mode_label = ctk.CTkLabel(self, text="Select Game Mode:", font=("Arial", 16))
        self.mode_label.pack(pady=5)
        self.mode_combo = ctk.CTkComboBox(self, values=["Single Player (vs AI)", "Two Players (Local)"], width=220)
        self.mode_combo.set("Single Player (vs AI)")
        self.mode_combo.pack(pady=5)

        self.start_btn = ctk.CTkButton(
            self, text="🎮 Start Match 🎮",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B", hover_color="#444444",
            border_width=2, border_color="#2ECC71", height=50,
            command=self.launch_game
        )
        self.start_btn.pack(pady=45)

        # כפתור חזרה ל-Games Center
        self.btn_back = ctk.CTkButton(
            self,
            text="⬅️ Back to Games Center",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=260,
            height=60,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=30)

        self.vs_ai = True
        self.should_start = False

    def return_to_main_menu(self):
         """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
         self.back_to_games = True
         self.destroy()
        
       

    def launch_game(self):
        self.vs_ai = "vs AI" in self.mode_combo.get()
        self.should_start = True
        self.destroy()

# ==========================================
# 2. קוד המשחק ב-Pygame
# ==========================================
def run_pong_game(vs_ai):
    pygame.init()
    
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong")
    clock = pygame.time.Clock()
    
    # צבעים
    DARK_BG = (26, 26, 36)
    WHITE = (255, 255, 255)
    BLUE = (52, 152, 219)
    RED = (231, 76, 60)
    
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 42, bold=True)
    
    # הגדרות אובייקטים
    pad_w, pad_h = 15, 100
    p1_y = (HEIGHT - pad_h) // 2
    p2_y = (HEIGHT - pad_h) // 2
    
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 6, 6
    ball_size = 15
    
    # ניקוד
    p1_score = 0
    p2_score = 0
    max_score = 5
    game_over = False
    winner = ""

    running = True
    return_to_menu = False

    while running:
        screen.fill(DARK_BG)
        
        for event in pygame.get_events() if hasattr(pygame, 'get_events') else pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return_to_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return_to_menu = True
                if game_over and event.key == pygame.K_x:
                    p1_score = 0
                    p2_score = 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                    game_over = False

        # תנועת שחקנים
        keys = pygame.key.get_pressed()
        if not game_over:
            # שחקן 1 (W/S)
            if keys[pygame.K_w] and p1_y > 10: p1_y -= 7
            if keys[pygame.K_s] and p1_y < HEIGHT - pad_h - 10: p1_y += 7
            
            # שחקן 2 / מחשב
            if vs_ai:
                # בינה מלאכותית פשוטה שעוקבת אחרי הכדור
                if p2_y + pad_h // 2 < ball_y and p2_y < HEIGHT - pad_h - 10:
                    p2_y += 5
                elif p2_y + pad_h // 2 > ball_y and p2_y > 10:
                    p2_y -= 5
            else:
                # שחקן 2 אנושי (חיצים)
                if keys[pygame.K_UP] and p2_y > 10: p2_y -= 7
                if keys[pygame.K_DOWN] and p2_y < HEIGHT - pad_h - 10: p2_y += 7

            # תנועת כדור
            ball_x += ball_dx
            ball_y += ball_dy
            
            # התנגשות קירות (למעלה ולמטה)
            if ball_y <= 10 or ball_y >= HEIGHT - 10:
                ball_dy *= -1
                
            # התנגשות במטקות
            p1_rect = pygame.Rect(30, p1_y, pad_w, pad_h)
            p2_rect = pygame.Rect(WIDTH - 30 - pad_w, p2_y, pad_w, pad_h)
            ball_rect = pygame.Rect(ball_x - ball_size//2, ball_y - ball_size//2, ball_size, ball_size)
            
            if ball_rect.colliderect(p1_rect):
                ball_dx = abs(ball_dx) + 0.5 # הגברת מהירות קלה
                ball_dx *= 1 # כיוון ימינה
            elif ball_rect.colliderect(p2_rect):
                ball_dx = -abs(ball_dx) - 0.5
                
            # פסילה / נקודה
            if ball_x < 0:
                p2_score += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = 6
            elif ball_x > WIDTH:
                p1_score += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = -6
                
            # בדיקת ניצחון
            if p1_score >= max_score:
                game_over = True
                winner = "Player 1"
            elif p2_score >= max_score:
                game_over = True
                winner = "AI" if vs_ai else "Player 2"

        # ציור מגרש
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        
        # ציור מטקות וכדור
        pygame.draw.rect(screen, BLUE, (30, p1_y, pad_w, pad_h), border_radius=5)
        pygame.draw.rect(screen, RED, (WIDTH - 30 - pad_w, p2_y, pad_w, pad_h), border_radius=5)
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_size // 2)

        # ציור תוצאה
        p1_lbl = large_font.render(str(p1_score), True, BLUE)
        p2_lbl = large_font.render(str(p2_score), True, RED)
        screen.blit(p1_lbl, (WIDTH // 4, 30))
        screen.blit(p2_lbl, (3 * WIDTH // 4 - p2_lbl.get_width(), 30))

        # מסך סיום
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            title = large_font.render(f"{winner} WINS! 🎉", True, WHITE)
            restart_txt = font.render("Press 'X' to Play Again", True, WHITE)
            exit_txt = font.render("Press 'ESC' to return to menu", True, RED)
            
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 20))
            screen.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    return return_to_menu

if __name__ == "__main__":
    while True:
        menu = PongStartWindow()
        menu.mainloop()
        if menu.should_start:
            if not run_pong_game(menu.vs_ai):
                break
        else:
            break