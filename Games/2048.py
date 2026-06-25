import customtkinter as ctk
import pygame
import random
import sys

# הגדרת עיצוב כללי ל-customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- מחלקת עמוד הפתיחה ב-CustomTkinter ---
class MenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("2048 - תפריט פתיחה")
        self.geometry("450x400")
        #self.resizable(False, False)
        
        self.start_game_chosen = False

        # כותרת המשחק
        self.title_label = ctk.CTkLabel(
            self, 
            text="🔢 2048 Game 🔢", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#EDC22E"  # צבע הזהב של אריח 2048
        )
        self.title_label.pack(pady=(60, 20))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="ברוכים הבאים למשחק 2048 החדש שלכם!", 
            font=ctk.CTkFont(family="Arial", size=16)
        )
        self.subtitle_label.pack(pady=(0, 40))

        # כפתור התחלת המשחק
        self.btn_start = ctk.CTkButton(
            self,
            text="🎮 התחל משחק / Start Game",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=260,
            height=55,
            corner_radius=10,
            command=self.start_game
        )
        self.btn_start.pack(pady=12)

        # כפתור יציאה
        self.btn_exit = ctk.CTkButton(
            self,
            text="🚪 יציאה / Exit",
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#A83232",
            hover_color="#822121",
            width=150,
            height=40,
            command=self.destroy
        )
        self.btn_exit.pack(pady=(40, 10))

    def start_game(self):
        self.start_game_chosen = True
        self.destroy()


# --- מחלקת מסך הפסד (Game Over) ב-CustomTkinter ---
class GameOverWindow(ctk.CTk):
    def __init__(self, score):
        super().__init__()
        
        self.title("Game Over")
        self.geometry("400x350")
        #self.resizable(False, False)
        
        self.action_chosen = None  # ישמור "restart" או "menu"

        # כותרת הפסד
        self.title_label = ctk.CTkLabel(
            self, 
            text="💥 GAME OVER 💥", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#FF5555"
        )
        self.title_label.pack(pady=(40, 10))

        # הצגת הניקוד הסופי
        self.score_label = ctk.CTkLabel(
            self, 
            text=f"הניקוד שלך: {score}\nFinal Score: {score}", 
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#F8F8F2"
        )
        self.score_label.pack(pady=20)

        # כפתור משחק מחדש
        self.btn_restart = ctk.CTkButton(
            self,
            text="🔄 לשחק מחדש / Restart",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#EDC22E",
            hover_color="#CBA320",
            text_color="#1E1E2E",
            width=220,
            height=45,
            command=lambda: self.select_action("restart")
        )
        self.btn_restart.pack(pady=10)

        # כפתור חזרה לתפריט הראשי
        self.btn_menu = ctk.CTkButton(
            self,
            text="🏠 תפריט ראשי / Main Menu",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#444444",
            hover_color="#333333",
            width=220,
            height=45,
            command=lambda: self.select_action("menu")
        )
        self.btn_menu.pack(pady=10)

    def select_action(self, action):
        self.action_chosen = action
        self.destroy()


# --- הגדרות וקבועים עבור Pygame ---

GRID_SIZE = 4
TILE_SIZE = 140
GAP_SIZE = 20
TOP_PANEL = 100  
WINDOW_SIZE = (GRID_SIZE*TILE_SIZE) + ((GRID_SIZE + 1) * GAP_SIZE)
WIDTH = WINDOW_SIZE
HEIGHT = WINDOW_SIZE + TOP_PANEL

COLOR_BG = (187, 173, 160)
COLOR_EMPTY_TILE = (205, 193, 180)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_TEXT_LIGHT = (249, 246, 242)

TILE_COLORS = {
    2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46)
}


def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 4 if random.random() < 0.1 else 2


def reset_game():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board


def compress(board):
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    changed = False
    for r in range(GRID_SIZE):
        pos = 0
        for c in range(GRID_SIZE):
            if board[r][c] != 0:
                new_board[r][pos] = board[r][c]
                if pos != c:
                    changed = True
                pos += 1
    return new_board, changed


def merge(board, score):
    changed = False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if board[r][c] != 0 and board[r][c] == board[r][c + 1]:
                board[r][c] *= 2
                score += board[r][c]
                board[r][c + 1] = 0
                changed = True
    return board, changed, score


def rotate(board):
    return [list(x) for x in zip(*board[::-1])]


def move_left(board, score):
    b1, changed1 = compress(board)
    b2, changed2, score = merge(b1, score)
    b3, changed3 = compress(b2)
    return b3, (changed1 or changed2 or changed3), score


def move_right(board, score):
    b = rotate(rotate(board))
    b, changed, score = move_left(b, score)
    return rotate(rotate(b)), changed, score


def move_up(board, score):
    b = rotate(rotate(rotate(board)))
    b, changed, score = move_left(b, score)
    return rotate(b), changed, score


def move_down(board, score):
    b = rotate(board)
    b, changed, score = move_left(b, score)
    return rotate(rotate(rotate(b))), changed, score


def check_game_over(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return False
            if r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
            if c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
    return True


def draw_interface(screen, board, score):
    screen.fill(COLOR_BG)
    font_score = pygame.font.SysFont("arial", 30, bold=True)
    text_score = font_score.render(f"SCORE: {score}", True, COLOR_TEXT_LIGHT)
    screen.blit(text_score, (20, 20))
    
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            x = c * TILE_SIZE + (c + 1) * GAP_SIZE
            y = r * TILE_SIZE + (r + 1) * GAP_SIZE + TOP_PANEL
            
            tile_color = TILE_COLORS.get(val, (60, 58, 50)) if val != 0 else COLOR_EMPTY_TILE
            pygame.draw.rect(screen, tile_color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=6)
            
            if val != 0:
                font_size = 40 if val < 100 else (32 if val < 1000 else 24)
                font_tile = pygame.font.SysFont("arial", font_size, bold=True)
                text_color = COLOR_TEXT_DARK if val in [2, 4] else COLOR_TEXT_LIGHT
                text_surface = font_tile.render(str(val), True, text_color)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE/2, y + TILE_SIZE/2))
                screen.blit(text_surface, text_rect)


def run_pygame_game():
    """מנהלת את לולאת המשחק הראשי ומחזירה את הניקוד בסיום"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GameCenter - 2048")
    
    board = reset_game()
    score = 0
    game_over = False

    while not game_over:
        draw_interface(screen, board, score)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    board, moved, score = move_left(board, score)
                elif event.key == pygame.K_RIGHT:
                    board, moved, score = move_right(board, score)
                elif event.key == pygame.K_UP:
                    board, moved, score = move_up(board, score)
                elif event.key == pygame.K_DOWN:
                    board, moved, score = move_down(board, score)
                
                if moved:
                    add_new_tile(board)
                    if check_game_over(board):
                        game_over = True

    pygame.quit()
    return score


# --- ניהול הריצה והניווט הראשי של המשחק ---
def main():
    show_main_menu = True  # דגל שקובע האם להראות את תפריט הפתיחה

    while True:
        if show_main_menu:
            menu = MenuApp()
            menu.mainloop()
            
            # אם לחצו על ה-X של התפריט ולא על כפתור התחלה, נצא מהתוכנית
            if not menu.start_game_chosen:
                break

        # מריץ את המשחק ומקבל בחזרה את הניקוד הסופי
        final_score = run_pygame_game()

        # פותח את חלון ה-Game Over ומציג את הניקוד
        game_over_win = GameOverWindow(final_score)
        game_over_win.mainloop()

        # ניווט לפי בחירת המשתמש
        if game_over_win.action_chosen == "restart":
            show_main_menu = False  # מדלג על תפריט הפתיחה ומתחיל משחק חדש ישירות
        elif game_over_win.action_chosen == "menu":
            show_main_menu = True   # חוזר להציג את תפריט הפתיחה
        else:
            break                   # אם סגרו את החלון ב-X, התוכנית מסתיימת


if __name__ == "__main__":
    main()