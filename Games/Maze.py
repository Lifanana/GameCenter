import pygame
import random
import sys
import customtkinter as ctk

# הגדרת עיצוב כללי ל-customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# --- מחלקת עמוד הפתיחה ב-CustomTkinter ---
class MazeMenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Maze Game - תפריט פתיחה")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        self.selected_mode = None
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center

        # כותרת המשחק
        self.title_label = ctk.CTkLabel(
            self, 
            text="🌀 The Lost Maze 🌀", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#56B8FF"  
        )
        self.title_label.pack(pady=(50, 20))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="בחר מצב משחק / Select Game Mode:", 
            font=ctk.CTkFont(family="Arial", size=16)
        )
        self.subtitle_label.pack(pady=(0, 30))

        # כפתור מצב קלאסי (מבוך גלוי)
        self.btn_classic = ctk.CTkButton(
            self,
            text="🔓 Classic Mode (מבוך גלוי)",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=260,
            height=50,
            command=lambda: self.set_mode_and_close("classic")
        )
        self.btn_classic.pack(pady=12)

        # כפתור מצב ערפל קרב
        self.btn_fog = ctk.CTkButton(
            self,
            text="🌫️ Fog of War (ערפל קרב)",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            fg_color="#FFB86C",       
            hover_color="#E09F53",
            text_color="#1E1E2E",     
            width=260,
            height=50,
            command=lambda: self.set_mode_and_close("fog")
        )
        self.btn_fog.pack(pady=12)

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

    def set_mode_and_close(self, mode):
        self.selected_mode = mode
        self.destroy()

    def return_to_main_menu(self):
        """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
        self.back_to_games = True
        self.destroy()


# --- מחלקת מסך ניצחון / סיום ב-CustomTkinter ---
class GameWinWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Victory!")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        self.action_chosen = None  # ישמור "restart" או "menu"

        # כותרת ניצחון
        self.title_label = ctk.CTkLabel(
            self, 
            text="🏆 VICTORY! 🏆", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#50FA7B"  
        )
        self.title_label.pack(pady=(40, 10))

        # הודעת הצלחה
        self.congrats_label = ctk.CTkLabel(
            self, 
            text="כל הכבוד! הצלחת לפתור את המבוך ולמצוא את היציאה!\nWell done! You successfully escaped the maze!", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="#F8F8F2"
        )
        self.congrats_label.pack(pady=30)

        # כפתור משחק מחדש (מייצר מבוך חדש)
        self.btn_restart = ctk.CTkButton(
            self,
            text="🔄 שלב הבא / Next Level",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#50FA7B",
            hover_color="#40D268",
            text_color="#1E1E2E",
            width=220,
            height=45,
            command=lambda: self.select_action("restart")
        )
        self.btn_restart.pack(pady=10)

        # כפתור חזרה לתפריט המבוך
        self.btn_menu = ctk.CTkButton(
            self,
            text="🏠 תפריט המשחק / Game Menu",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#444444",
            hover_color="#333333",
            width=220,
            height=45,
            command=lambda: self.select_action("menu")
        )
        self.btn_menu.pack(pady=10)

    def select_action(self, action):
        """שומרת את הבחירה וסוגרת את החלון"""
        self.action_chosen = action
        self.destroy()


# --- הגדרות וקבועים עבור Pygame ---
WIDTH = 1000
HEIGHT = 650
GRID_SIZE = 25  
COLS = (WIDTH - 40) // GRID_SIZE
ROWS = (HEIGHT - 40) // GRID_SIZE

# צבעים
BG_COLOR = (20, 24, 33)       
WALL_COLOR = (45, 55, 72)     
PATH_COLOR = (15, 23, 42)     
UNEXPLORED = (5, 5, 10)       
PLAYER_COLOR = (56, 189, 248)  
GOAL_COLOR = (34, 197, 94)    


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.visible = False  


def generate_maze(grid):
    """אלגוריתם DFS ליצירת המבוך באופן אקראי"""
    stack = []
    current = grid[0][0]
    current.visited = True
    
    while True:
        neighbors = []
        r, c = current.r, current.c
        
        if r > 0 and not grid[r-1][c].visited:
            neighbors.append((grid[r-1][c], 'top', 'bottom'))
        if r < ROWS - 1 and not grid[r+1][c].visited:
            neighbors.append((grid[r+1][c], 'bottom', 'top'))
        if c > 0 and not grid[r][c-1].visited:
            neighbors.append((grid[r][c-1], 'left', 'right'))
        if c < COLS - 1 and not grid[r][c+1].visited:
            neighbors.append((grid[r][c+1], 'right', 'left'))
        
        if neighbors:
            next_cell, wall_curr, wall_next = random.choice(neighbors)
            current.walls[wall_curr] = False
            next_cell.walls[wall_next] = False
            next_cell.visited = True
            stack.append(current)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break


def reveal_area(grid, r, c):
    """מגלה את האזור סביב השחקן עבור מצב Fog"""
    radius = 3
    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                grid[nr][nc].visible = True


def run_pygame_maze(game_mode):
    """מריצה את משחק המבוך ב-Pygame ומחזירה סטטוס בהתאם לאופן היציאה מהמשחק"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GameCenter - Maze Game")
    clock = pygame.time.Clock()

    # יצירת מבוך
    grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]
    generate_maze(grid)

    player_pos = [0, 0]
    goal_pos = [ROWS - 1, COLS - 1]

    # במצב קלאסי הכל גלוי מיד, במצב ערפל מגלים בהדרגה
    if game_mode == "classic":
        for r in range(ROWS):
            for c in range(COLS):
                grid[r][c].visible = True
    else:
        reveal_area(grid, player_pos[0], player_pos[1])

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return "menu"  # <-- שינוי: החזרה ישירה לתפריט ללא מסך הניצחון!
                
                r, c = player_pos
                current_cell = grid[r][c]
                
                if event.key == pygame.K_UP and not current_cell.walls['top']:
                    player_pos[0] -= 1
                elif event.key == pygame.K_DOWN and not current_cell.walls['bottom']:
                    player_pos[0] += 1
                elif event.key == pygame.K_LEFT and not current_cell.walls['left']:
                    player_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and not current_cell.walls['right']:
                    player_pos[1] += 1

                # עדכון ערפל הקרב אם אנחנו במצב Fog
                if game_mode == "fog":
                    reveal_area(grid, player_pos[0], player_pos[1])

        # בדיקת הגעה ליעד (ניצחון)
        if player_pos == goal_pos:
            pygame.quit()
            return "win"  # <-- שינוי: השחקן אכן הגיע ליציאה והשלים את המבוך

        # ציור
        screen.fill(BG_COLOR)
        offset_x, offset_y = 20, 20

        for r in range(ROWS):
            for c in range(COLS):
                cell = grid[r][c]
                x = offset_x + c * GRID_SIZE
                y = offset_y + r * GRID_SIZE
                
                if cell.visible:
                    pygame.draw.rect(screen, PATH_COLOR, (x, y, GRID_SIZE, GRID_SIZE))
                    
                    if cell.walls['top']:
                        pygame.draw.line(screen, WALL_COLOR, (x, y), (x + GRID_SIZE, y), 2)
                    if cell.walls['bottom']:
                        pygame.draw.line(screen, WALL_COLOR, (x, y + GRID_SIZE), (x + GRID_SIZE, y + GRID_SIZE), 2)
                    if cell.walls['left']:
                        pygame.draw.line(screen, WALL_COLOR, (x, y), (x, y + GRID_SIZE), 2)
                    if cell.walls['right']:
                        pygame.draw.line(screen, WALL_COLOR, (x + GRID_SIZE, y), (x + GRID_SIZE, y + GRID_SIZE), 2)
                else:
                    pygame.draw.rect(screen, UNEXPLORED, (x, y, GRID_SIZE, GRID_SIZE))

        # ציור המטרה (ריבוע ירוק)
        goal_x = offset_x + goal_pos[1] * GRID_SIZE
        goal_y = offset_y + goal_pos[0] * GRID_SIZE
        pygame.draw.rect(screen, GOAL_COLOR, (goal_x + 3, goal_y + 3, GRID_SIZE - 6, GRID_SIZE - 6), border_radius=4)

        # ציור השחקן (ריבוע כחול)
        play_x = offset_x + player_pos[1] * GRID_SIZE
        play_y = offset_y + player_pos[0] * GRID_SIZE
        pygame.draw.rect(screen, PLAYER_COLOR, (play_x + 3, play_y + 3, GRID_SIZE - 6, GRID_SIZE - 6), border_radius=4)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return "exit"


# --- לולאת ניהול המשחק הראשית והניווט ---
def main():
    current_mode = None

    while True:
        if current_mode is None:
            menu = MazeMenuApp()
            menu.mainloop()
            
            # אם לחצו על כפתור החזרה ל-Games Center, נצא מהקובץ
            if menu.back_to_games:
                break
                
            # אם המשתמש סגר את התפריט ב-X בלי לבחור ובלי ללחוץ על חזרה
            if menu.selected_mode is None:
                break
            current_mode = menu.selected_mode

        # הפעלת משחק המבוך ב-Pygame וקבלת תוצאת הריצה
        result = run_pygame_maze(current_mode)

        # אם סיימנו את המבוך בהצלחה, מציגים את מסך הניצחון
        if result == "win":
            win_win = GameWinWindow()
            win_win.mainloop()

            if win_win.action_chosen == "restart":
                continue
            elif win_win.action_chosen == "menu":
                current_mode = None
            else:
                break
        
        # אם המשתמש לחץ על ESC, נחזיר אותו ישירות לתפריט הראשי
        elif result == "menu":
            current_mode = None
            
        # אם המשחק נסגר לחלוטין (ב-X)
        else:
            break


if __name__ == "__main__":
    main()