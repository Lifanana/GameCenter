import os
import sys
import random
import customtkinter as ctk
import pygame

# ==========================================
# 1. חלון פתיחה (CustomTkinter) - מעודכן ללא חיתוך כפתורים!
# ==========================================
class PacmanStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pacman - Start Menu")
        self.geometry("500x480")  # הגדלנו את הגובה ל-480 כדי למנוע חיתוך
        self.resizable(False, False)
        self.back_to_games = False  
        ctk.set_appearance_mode("dark")
        
        self.title_label = ctk.CTkLabel(
            self, text="🟡 PAC-MAN 🟡", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#F1C40F"
        )
        self.title_label.pack(pady=(25, 15))
        
        self.name_label = ctk.CTkLabel(self, text="Enter Your Name:", font=("Arial", 14))
        self.name_label.pack(pady=2)
        self.name_input = ctk.CTkEntry(self, placeholder_text="Player", width=200)
        old_name = os.environ.get("PACMAN_PLAYER_NAME", "Player 1")
        self.name_input.insert(0, old_name)
        self.name_input.pack(pady=5)

        # כפתור התחלה בגובה 60
        self.start_btn = ctk.CTkButton(
            self, text="🎮 Start Game 🎮",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B", hover_color="#444444",
            border_width=2, border_color="#F1C40F", height=60,
            command=self.launch_game
        )
        self.start_btn.pack(pady=(20, 10))

        # כפתור חזרה בגובה 50
        self.btn_back = ctk.CTkButton(
            self,
            text="⬅️ Back to Games Center",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=240,
            height=50,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=10)

        self.player_name = "Player"
        self.should_start = False

    def return_to_main_menu(self):
        self.back_to_games = True
        self.destroy()

    def launch_game(self):
        self.player_name = self.name_input.get().strip() or "Player"
        os.environ["PACMAN_PLAYER_NAME"] = self.player_name
        self.should_start = True
        self.destroy()

# ==========================================
# 2. מאגר המבוכים (מפות שונות)
# ==========================================
LEVELS = [
    # שלב 1: מבוך קלאסי בסיסי
    [
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,1,0,0,0,0,1],
        [1,0,1,1,0,0,0,0,1,1,0,1],
        [1,0,1,1,0,1,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,0,1,1,0,0,1,1,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,1,1],
        [1,0,0,1,1,1,1,1,1,0,0,1],
        [1,0,1,1,0,0,0,0,1,1,0,1],
        [1,0,0,0,0,1,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1]
    ],
    # שלב 2: מבוך ה"זירה המעגלית" (הרבה מרחב פתוח אך פניות חדות)
    [
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,0,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,1,0,1,0,1],
        [1,0,0,0,1,1,1,1,0,0,0,1],
        [1,0,1,0,1,1,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,0,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1]
    ],
    # שלב 3: ה"גריד הצפוף" (מעברים צרים וצפופים, קשה מאוד להתחמק!)
    [
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,1,0,1,0,1,0,0,1],
        [1,0,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,0,1,1,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,0,1,1,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,0,1,1,0,1],
        [1,0,0,0,0,1,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1]
    ]
]

# ==========================================
# 3. קוד המשחק ב-Pygame
# ==========================================
def run_pacman_game(player_name):
    pygame.init()
    
    WIDTH, HEIGHT = 600, 680
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Levels")
    clock = pygame.time.Clock()
    
    # צבעים
    BLACK = (10, 10, 20)
    BLUE = (33, 150, 243)
    YELLOW = (255, 238, 0)
    RED = (231, 76, 60)
    WHITE = (255, 255, 255)
    GREEN = (46, 204, 113)
    
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 42, bold=True)
    
    TILE_SIZE = 45
    
    # משתני התקדמות שלבים
    current_level_idx = 0
    score = 0
    lives = 3
    game_over = False
    win = False

    # פונקציית טעינת שלב
    def load_level(level_idx):
        raw_grid = LEVELS[level_idx]
        grid_copy = [row[:] for row in raw_grid]
        
        # חישוב אופסט למרכוז המפה בחלון
        start_x = (WIDTH - (len(raw_grid[0]) * TILE_SIZE)) // 2
        start_y = ((HEIGHT - (len(raw_grid) * TILE_SIZE)) // 2) + 30
        
        total_dots = sum(row.count(0) for row in raw_grid)
        
        # התאמת מהירות הרוח לפי מספר השלב (שלב גבוה יותר = רוח מהירה יותר)
        ghost_speed_ms = max(150, 260 - (level_idx * 45))
        
        return {
            "grid": grid_copy,
            "px": 1, "py": 1,         # פקמן מתחיל תמיד למעלה משמאל
            "gx": 10, "gy": 9,        # רוח מתחילה למטה מימין
            "total_dots": total_dots,
            "dots_eaten": 0,
            "start_x": start_x,
            "start_y": start_y,
            "ghost_speed": ghost_speed_ms
        }

    # טוענים את השלב הראשון
    lvl = load_level(current_level_idx)

    running = True
    return_to_menu = False
    
    move_cooldown = 140 # קצב תנועת שחקן
    last_move = 0
    last_ghost_move = 0

    while running:
        current_time = pygame.time.get_ticks()
        screen.fill(BLACK)
        
        # 1. ניהול אירועים
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return_to_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return_to_menu = True
                if game_over and event.key == pygame.K_x:
                    # איפוס מוחלט מההתחלה
                    current_level_idx = 0
                    score = 0
                    lives = 3
                    game_over = False
                    win = False
                    lvl = load_level(current_level_idx)
        
        # 2. תנועת שחקן
        keys = pygame.key.get_pressed()
        if not game_over and current_time - last_move > move_cooldown:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]: dx = -1
            elif keys[pygame.K_RIGHT]: dx = 1
            elif keys[pygame.K_UP]: dy = -1
            elif keys[pygame.K_DOWN]: dy = 1
            
            if dx != 0 or dy != 0:
                nx, ny = lvl["px"] + dx, lvl["py"] + dy
                # וידוא גבולות מפה וקירות
                if 0 <= nx < len(lvl["grid"][0]) and 0 <= ny < len(lvl["grid"]):
                    if lvl["grid"][ny][nx] != 1: 
                        lvl["px"], lvl["py"] = nx, ny
                        last_move = current_time
                        
                        # אכילת נקודת אוכל
                        if lvl["grid"][ny][nx] == 0:
                            lvl["grid"][ny][nx] = -1 # מסמנים כנאכל
                            score += 10
                            lvl["dots_eaten"] += 1
                            
                            # האם כל הנקודות בשלב הנוכחי נאכלו?
                            if lvl["dots_eaten"] >= lvl["total_dots"]:
                                if current_level_idx < len(LEVELS) - 1:
                                    # מעבר לשלב הבא!
                                    current_level_idx += 1
                                    lvl = load_level(current_level_idx)
                                    # אפקט קצר למעבר שלב
                                    screen.fill(BLACK)
                                    next_lvl_txt = large_font.render(f"LEVEL {current_level_idx + 1}!", True, GREEN)
                                    screen.blit(next_lvl_txt, (WIDTH // 2 - next_lvl_txt.get_width() // 2, HEIGHT // 2))
                                    pygame.display.flip()
                                    pygame.time.wait(1200)
                                    last_ghost_move = pygame.time.get_ticks()
                                else:
                                    # ניצחון מוחלט (השלים את כל המפות)
                                    win = True
                                    game_over = True

        # 3. תנועת רוח רפאים (מהירות מושפעת מרמת השלב)
        if not game_over and current_time - last_ghost_move > lvl["ghost_speed"]:
            last_ghost_move = current_time
            gdx, gdy = 0, 0
            if lvl["gx"] < lvl["px"]: gdx = 1
            elif lvl["gx"] > lvl["px"]: gdx = -1
            elif lvl["gy"] < lvl["py"]: gdy = 1
            elif lvl["gy"] > lvl["py"]: gdy = -1
            
            # בדיקת קיר בנתיב המועדף
            if lvl["grid"][lvl["gy"] + gdy][lvl["gx"] + gdx] != 1:
                lvl["gx"] += gdx
                lvl["gy"] += gdy
            else: # אלגוריתם תנועה אקראי קליל אם נתקע בקיר
                moves = [(0,1), (0,-1), (1,0), (-1,0)]
                random.shuffle(moves)
                for mx, my in moves:
                    if lvl["grid"][lvl["gy"] + my][lvl["gx"] + mx] != 1:
                        lvl["gx"] += mx
                        lvl["gy"] += my
                        break
                        
            # בדיקת פגיעה בפקמן
            if lvl["px"] == lvl["gx"] and lvl["py"] == lvl["gy"]:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # מחזיר רק את השחקן והרוח לנקודת ההתחלה של השלב בלי לאפס נקודות שכבר נאכלו
                    lvl["px"], lvl["py"] = 1, 1
                    lvl["gx"], lvl["gy"] = 10, 9

        # 4. ציור המפה (המבוך)
        for r in range(len(lvl["grid"])):
            for c in range(len(lvl["grid"][0])):
                rect = pygame.Rect(lvl["start_x"] + c * TILE_SIZE, lvl["start_y"] + r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if lvl["grid"][r][c] == 1:
                    pygame.draw.rect(screen, BLUE, rect, border_radius=4)
                    pygame.draw.rect(screen, BLACK, rect, width=2)
                elif lvl["grid"][r][c] == 0: 
                    pygame.draw.circle(screen, WHITE, rect.center, 5)

        # 5. ציור ישויות
        pac_rect = pygame.Rect(lvl["start_x"] + lvl["px"] * TILE_SIZE, lvl["start_y"] + lvl["py"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.circle(screen, YELLOW, pac_rect.center, TILE_SIZE // 2 - 3)
        
        ghost_rect = pygame.Rect(lvl["start_x"] + lvl["gx"] * TILE_SIZE, lvl["start_y"] + lvl["gy"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.circle(screen, RED, ghost_rect.center, TILE_SIZE // 2 - 3)

        # 6. ציור סרגל עליון
        pygame.draw.rect(screen, (20, 20, 40), (0, 0, WIDTH, 65))
        name_lbl = font.render(f"👤 {player_name}", True, WHITE)
        score_lbl = font.render(f"Score: {score}", True, YELLOW)
        level_lbl = font.render(f"LVL: {current_level_idx + 1}/3", True, GREEN)
        lives_lbl = font.render(f"Lives: {'❤️' * lives}", True, RED)
        
        screen.blit(name_lbl, (15, 20))
        screen.blit(score_lbl, (160, 20))
        screen.blit(level_lbl, (290, 20))
        screen.blit(lives_lbl, (WIDTH - lives_lbl.get_width() - 15, 20))

        # 7. מסך סוף משחק
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            title_text = "🎉 YOU CONQUERED ALL LABYRINTHS! 🎉" if win else "GAME OVER 💀"
            title = large_font.render(title_text, True, YELLOW if win else RED)
            score_txt = font.render(f"Final Score: {score}", True, WHITE)
            restart_txt = font.render("Press 'X' to restart from Level 1", True, WHITE)
            exit_txt = font.render("Press 'ESC' to return to menu", True, BLUE)
            
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 30))
            screen.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    return return_to_menu

# ==========================================
# 4. ניתוב הפעלה ראשי
# ==========================================
if __name__ == "__main__":
    while True:
        menu = PacmanStartWindow()
        menu.mainloop()
        
        if menu.back_to_games:
            break
            
        if menu.should_start:
            play_again = run_pacman_game(menu.player_name)
            if not play_again:
                break
        else:
            break