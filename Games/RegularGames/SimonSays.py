import os
import sys
import time
import random
import math
import customtkinter as ctk
import pygame


# ==========================================
# 1. חלון התחלה באמצעות CustomTkinter
# ==========================================
class SimonStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Simon Says - Start Menu")
        self.geometry("500x480")
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        # כותרת ראשית צבעונית
        self.title_label = ctk.CTkLabel(
            self, 
            text="🧠 SIMON SAYS 🧠", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#5AD282"
        )
        self.title_label.pack(pady=(30, 20))
        
        # שם שחקן
        self.name_label = ctk.CTkLabel(self, text="Enter Your Name:", font=("Arial", 16))
        self.name_label.pack(pady=5)
        self.name_input = ctk.CTkEntry(self, placeholder_text="Player", width=200)
        self.name_input.insert(0, "Player 1")
        self.name_input.pack(pady=5)

        # בחירת רמת קושי (משפיעה על מהירות הבזקי האור)
        self.difficulty_label = ctk.CTkLabel(self, text="Select Difficulty:", font=("Arial", 16))
        self.difficulty_label.pack(pady=(15, 5))
        self.difficulty_combo = ctk.CTkComboBox(
            self, 
            values=["Easy (Slow)", "Medium (Normal)", "Hard (Fast)"],
            width=200
        )
        self.difficulty_combo.set("Medium (Normal)")
        self.difficulty_combo.pack(pady=5)

        # כפתור התחלה
        self.start_btn = ctk.CTkButton(
            self,
            text="🎮 Play Game 🎮",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#444444",
            border_width=2,
            border_color="#5AD282",
            height=50,
            command=self.launch_game
        )
        self.start_btn.pack(pady=40)

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

        self.player_name = "Player"
        self.speed_ms = 800  # מהירות ברירת מחדל במילישניות
        self.should_start = False
        
    def return_to_main_menu(self):
         """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
         self.back_to_games = True
         self.destroy()

    def launch_game(self):
        self.player_name = self.name_input.get().strip() or "Player"
        diff = self.difficulty_combo.get()
        if "Easy" in diff:
            self.speed_ms = 1000
        elif "Hard" in diff:
            self.speed_ms = 400
        else:
            self.speed_ms = 700
            
        self.should_start = True
        self.destroy()


# ==========================================
# 2. קוד המשחק באמצעות Pygame
# ==========================================
def run_simon_game(player_name, flash_speed):
    pygame.init()
    pygame.mixer.init()
    
    # מימדי חלון
    WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simon Says")
    clock = pygame.time.Clock()
    
    # פונקציה לייצור צליל סינתטי במידה ואין קבצי אודיו חיצוניים
    def generate_sound(frequency, duration=0.3):
        sample_rate = 44100
        num_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(num_samples):
            # יצירת גל סינוס בסיסי
            t = float(i) / sample_rate
            value = int(math.sin(2.0 * math.pi * frequency * t) * 127 + 128)
            buf.append(value)
        
        # המרה לסאונד תואם Pygame
        sound = pygame.mixer.Sound(buffer=buf)
        sound.set_volume(0.3)
        return sound

    # יצירת צלילים ייחודיים לכל כפתור
    sounds = {
        0: generate_sound(261.63), # ירוק - דו (C4)
        1: generate_sound(329.63), # אדום - מי (E4)
        2: generate_sound(392.00), # צהוב - סול (G4)
        3: generate_sound(523.25)  # כחול - דו גבוה (C5)
    }

    # צבעים רגילים (כבויים)
    GREEN_DARK = (15, 110, 45)
    RED_DARK = (135, 15, 15)
    YELLOW_DARK = (145, 125, 15)
    BLUE_DARK = (15, 55, 135)
    
    # צבעים מוארים (דלוקים)
    GREEN_BRIGHT = (46, 204, 113)
    RED_BRIGHT = (231, 76, 60)
    YELLOW_BRIGHT = (241, 196, 15)
    BLUE_BRIGHT = (52, 152, 219)
    
    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    # מיקומי כפתורים (4 ריבועים גדולים)
    # [X, Y, Width, Height]
    buttons = [
        {"rect": pygame.Rect(70, 130, 170, 170), "color_dark": GREEN_DARK, "color_bright": GREEN_BRIGHT, "sound": sounds[0]}, # שמאל למעלה (ירוק)
        {"rect": pygame.Rect(260, 130, 170, 170), "color_dark": RED_DARK, "color_bright": RED_BRIGHT, "sound": sounds[1]},   # ימין למעלה (אדום)
        {"rect": pygame.Rect(70, 320, 170, 170), "color_dark": YELLOW_DARK, "color_bright": YELLOW_BRIGHT, "sound": sounds[2]}, # שמאל למטה (צהוב)
        {"rect": pygame.Rect(260, 320, 170, 170), "color_dark": BLUE_DARK, "color_bright": BLUE_BRIGHT, "sound": sounds[3]}   # ימין למטה (כחול)
    ]

    # משתני משחק
    pattern = []
    player_pattern = []
    game_state = "START" # "START", "SHOWING", "PLAYER_TURN", "GAMEOVER"
    score = 0
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 42, bold=True)
    
    active_button = None
    flash_timer = 0

    # פונקציה להאיר כפתור ולהשמיע את הסאונד שלו
    def flash_button(btn_index):
        nonlocal active_button, flash_timer
        active_button = btn_index
        buttons[btn_index]["sound"].play()
        flash_timer = pygame.time.get_ticks() + flash_speed

    # הוספת צעד חדש לרצף
    def add_step():
        pattern.append(random.randint(0, 3))

    running = True
    showing_index = 0
    show_next_time = 0

    while running:
        current_time = pygame.time.get_ticks()
        screen.fill(BG_COLOR)

        # קבלת אירועים
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYER_TURN":
                mouse_pos = event.pos
                for index, btn in enumerate(buttons):
                    if btn["rect"].collidepoint(mouse_pos):
                        flash_button(index)
                        player_pattern.append(index)
                        
                        # בדיקה אם השחקן טעה
                        current_step = len(player_pattern) - 1
                        if player_pattern[current_step] != pattern[current_step]:
                            game_state = "GAMEOVER"
                        # בדיקה אם השחקן השלים את כל הרצף בהצלחה
                        elif len(player_pattern) == len(pattern):
                            score += 1
                            game_state = "SHOWING"
                            player_pattern = []
                            showing_index = 0
                            show_next_time = current_time + 1000 # השהייה קלה לפני הסבב הבא
                            add_step()
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True
                if game_state == "GAMEOVER":
                    if event.key == pygame.K_x:  # התחלה מחדש עם האות X
                        pattern = []
                        player_pattern = []
                        score = 0
                        game_state = "START"
                    elif event.key == pygame.K_ESCAPE:  # חזרה לתפריט הראשי
                        running = False

        # לוגיקת המצבים של המשחק
        if game_state == "START":
            add_step()
            game_state = "SHOWING"
            showing_index = 0
            show_next_time = current_time + 500

        elif game_state == "SHOWING":
            # ניהול הצגת הרצף של סיימון לשחקן בקצב הנבחר
            if active_button is None and current_time > show_next_time:
                if showing_index < len(pattern):
                    flash_button(pattern[showing_index])
                    showing_index += 1
                    show_next_time = current_time + flash_speed + 150 # הבזק + מרווח קצר
                else:
                    game_state = "PLAYER_TURN"

        # כיבוי כפתור פעיל לאחר סיום זמן ההבזק
        if active_button is not None and current_time > flash_timer:
            active_button = None

        # --- ציור המסך ---

        # ציור הכפתורים הצבעוניים
        for index, btn in enumerate(buttons):
            color = btn["color_bright"] if active_button == index else btn["color_dark"]
            pygame.draw.rect(screen, color, btn["rect"], border_radius=15)
            # מסגרת כהה עדינה מסביב לכל כפתור
            pygame.draw.rect(screen, (10, 10, 10), btn["rect"], width=3, border_radius=15)

        # ציור בר המידע העליון
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, 60))
        name_lbl = font.render(f"👤 {player_name}", True, TEXT_COLOR)
        score_lbl = font.render(f"Score: {score}", True, (241, 196, 15))
        
        screen.blit(name_lbl, (20, 18))
        screen.blit(score_lbl, (WIDTH - score_lbl.get_width() - 20, 18))

        # כתובית עזר למרכז המסך (לפי המצב)
        if game_state == "SHOWING":
            status_txt = font.render("Watch Simon...", True, (231, 76, 60))
        elif game_state == "PLAYER_TURN":
            status_txt = font.render("Your Turn! Repeat the pattern", True, (46, 204, 113))
        else:
            status_txt = font.render("", True, TEXT_COLOR)
            
        if status_txt:
            screen.blit(status_txt, (WIDTH // 2 - status_txt.get_width() // 2, 85))

        # מסך GameOver
        if game_state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
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
        clock.tick(60)

    pygame.quit()


# ==========================================
# 3. ניתוב הפעלה ראשי
# ==========================================
if __name__ == "__main__":
    while True:
        menu = SimonStartWindow()
        menu.mainloop()
        
        # אם המשתמש לחץ על כפתור חזרה ל-Games Center
        if menu.back_to_games:
            break
            
        # אם המשתמש לחץ על כפתור התחלת משחק
        if menu.should_start:
            # מריצים את המשחק ושומרים את הערך המוחזר (True ל-ESC, False ליציאה)
            should_return_to_menu = run_simon_game(menu.player_name, menu.speed_ms)
            
            # אם לא לחצו ESC (למשל סגרו את החלון ב-X), נצא מהלולאה
            if not should_return_to_menu:
                break
            # אם לחצו ESC, הלולאה תמשיך ותפתח שוב את חלון ה-SimonStartWindow
        else:
            break        