import customtkinter as ctk
import pygame
import random
import sys

# הגדרת עיצוב כללי ל-customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- מחלקת עמוד הפתיחה ב-CustomTkinter ---
class SnakeMenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Snake Game - תפריט פתיחה")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        self.selected_mode = None
        self.back_to_games = False  # משתנה חדש שבודק אם ביקשנו לחזור אחורה

        # כותרת המשחק
        self.title_label = ctk.CTkLabel(
            self, 
            text="🐍 Snake Game 🐍", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#50FA7B"  
        )
        self.title_label.pack(pady=(50, 20))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="בחר מצב משחק / Select Game Mode:", 
            font=ctk.CTkFont(family="Arial", size=16)
        )
        self.subtitle_label.pack(pady=(0, 30))

        # כפתור מצב קלאסי
        self.btn_classic = ctk.CTkButton(
            self,
            text="🎮 Classic Mode (רגיל)",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=260,
            height=50,
            command=lambda: self.set_mode_and_close("classic")
        )
        self.btn_classic.pack(pady=12)

        # כפתור מצב קוביות חוסמות
        self.btn_obstacles = ctk.CTkButton(
            self,
            text="🤖 Obstacle Mode (קוביות חוסמות)",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            fg_color="#FFB86C",       
            hover_color="#E09F53",
            text_color="#1E1E2E",     
            width=260,
            height=50,
            command=lambda: self.set_mode_and_close("obstacles")
        )
        self.btn_obstacles.pack(pady=12)

        # --- כפתור חזרה ל-Games Center ---
        self.btn_back = ctk.CTkButton(
            self,
            text="⬅️ חזרה ל-Games Center",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=260,
            height=50,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=30)  # מרווח קצת יותר גדול למטה לעיצוב נקי

    def set_mode_and_close(self, mode):
        self.selected_mode = mode
        self.destroy()

    def return_to_main_menu(self):
        """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
        self.back_to_games = True
        self.destroy()


# --- מחלקת מסך הפסד (Game Over) ב-CustomTkinter ---
class GameOverWindow(ctk.CTk):
    def __init__(self, score):
        super().__init__()
        
        self.title("Game Over")
        # תיקון קל בקוד המקורי שלך: החלפנו את ה-* ב-x במידות הגאומטריה למניעת קריסה
        self.geometry("1000x650")
        self.resizable(False, False)
        
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
            fg_color="#50FA7B",
            hover_color="#40D268",
            text_color="#1E1E2E",
            width=220,
            height=45,
            command=lambda: self.select_action("restart")
        )
        self.btn_restart.pack(pady=10)

        # כפתור חזרה לתפריט הראשי של הנחש
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
        """שומרת את הבחירה וסוגרת את חלון ה-Game Over"""
        self.action_chosen = action
        self.destroy()


# --- הגדרות וקבועים עבור Pygame ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
GRID_SIZE = 20  

COLOR_BACKGROUND = (40, 42, 54)   
COLOR_SNAKE_HEAD = (80, 250, 123)  
COLOR_SNAKE_BODY = (64, 210, 100)  
COLOR_FOOD = (255, 85, 85)         
COLOR_OBSTACLE = (255, 184, 108)   
COLOR_TEXT = (248, 248, 242)       


def generate_food(snake, obstacles):
    while True:
        x = random.randint(0, (WINDOW_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake and (x, y) not in obstacles:
            return x, y


def generate_obstacle(snake, food, obstacles):
    while True:
        x = random.randint(0, (WINDOW_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake and (x, y) != food and (x, y) not in obstacles:
            return x, y


def run_pygame_game(game_mode):
    """מריצה את משחק ה-Pygame ומחזירה את הניקוד הסופי שהושג"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("GameCenter - Snake Game")
    clock = pygame.time.Clock()

    snake = [(100, 100), (80, 100), (60, 100)]
    obstacles = []
    direction = (GRID_SIZE, 0)
    food = generate_food(snake, obstacles)
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                    direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                    direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                    direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                    direction = (GRID_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
            game_over = True
            continue

        if new_head in snake:
            game_over = True
            continue

        if game_mode == "obstacles" and new_head in obstacles:
            game_over = True
            continue

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            if game_mode == "obstacles":
                new_obs = generate_obstacle(snake, food, obstacles)
                obstacles.append(new_obs)
            food = generate_food(snake, obstacles)
        else:
            snake.pop()

        screen.fill(COLOR_BACKGROUND)

        for obs in obstacles:
            pygame.draw.rect(screen, COLOR_OBSTACLE, pygame.Rect(obs[0], obs[1], GRID_SIZE - 2, GRID_SIZE - 2))

        pygame.draw.rect(screen, COLOR_FOOD, pygame.Rect(food[0], food[1], GRID_SIZE, GRID_SIZE))

        for i, segment in enumerate(snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2))

        font = pygame.font.SysFont("arial", 24)
        mode_str = "Classic" if game_mode == "classic" else "Obstacles"
        score_text = font.render(f"Score: {score}  |  Mode: {mode_str}", True, COLOR_TEXT)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    return score  


# --- לולאת ניהול המשחק הראשית והניווט ---
def main():
    current_mode = None

    while True:
        if current_mode is None:
            menu = SnakeMenuApp()
            menu.mainloop()
            
            # אם לחצו על כפתור החזרה ל-Games, נשבור את הלולאה ונצא מהקובץ
            if menu.back_to_games:
                break
                
            # אם המשתמש סגר את התפריט ב-X בלי לבחור ובלי ללחוץ על חזרה
            if menu.selected_mode is None:
                break
            current_mode = menu.selected_mode

        # הפעלת המשחק ב-Pygame וקבלת הניקוד הסופי
        final_score = run_pygame_game(current_mode)

        # פתיחת חלון ה-Game Over ב-CustomTkinter
        game_over_win = GameOverWindow(final_score)
        game_over_win.mainloop()

        # בדיקת ההחלטה של המשתמש
        if game_over_win.action_chosen == "restart":
            continue
        elif game_over_win.action_chosen == "menu":
            current_mode = None
        else:
            break


if __name__ == "__main__":
    main()