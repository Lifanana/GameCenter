import customtkinter as ctk
import pygame
import sys
import random

# --- הגדרות קבועות ל-Pygame ---
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
TEXT_COLOR = (255, 255, 255)

# --- פונקציות לוגיקת המשחק (Pygame) ---

def run_pygame_game(game_mode, menu_window):
    """הפעלת חלון המשחק של Pygame בהתאם למצב שנבחר"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('איקס עיגול - Pygame')
    
    font_large = pygame.font.SysFont('Arial', 45, bold=True)
    font_small = pygame.font.SysFont('Arial', 18, bold=False)
    
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False

    def draw_lines():
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "O":
                    center = (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    pygame.draw.circle(screen, O_COLOR, center, 60, 15)
                elif board[row][col] == "X":
                    offset = 55
                    x_pos = col * SQUARE_SIZE
                    y_pos = row * SQUARE_SIZE
                    pygame.draw.line(screen, X_COLOR, (x_pos + offset, y_pos + offset), (x_pos + SQUARE_SIZE - offset, y_pos + SQUARE_SIZE - offset), 20)
                    pygame.draw.line(screen, X_COLOR, (x_pos + SQUARE_SIZE - offset, y_pos + offset), (x_pos + offset, y_pos + SQUARE_SIZE - offset), 20)

    def check_win(current_player):
        for row in range(BOARD_ROWS):
            if board[row][0] == board[row][1] == board[row][2] == current_player: return True
        for col in range(BOARD_COLS):
            if board[0][col] == board[1][col] == board[2][col] == current_player: return True
        if board[0][0] == board[1][1] == board[2][2] == current_player: return True
        if board[2][0] == board[1][1] == board[0][2] == current_player: return True
        return False

    def is_board_full():
        return all(board[r][c] != " " for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

    def draw_winner_text(text):
        text_surface = font_large.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        bg_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 10, text_rect.width + 40, text_rect.height + 20)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        screen.blit(text_surface, text_rect)
        
        sub_text = font_small.render("Press SPACE to Restart | Press M for Menu", True, TEXT_COLOR)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(sub_text, sub_rect)

    def ai_move():
        nonlocal player, game_over
        if game_over: return
        
        # 1. התקפה
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    if check_win("O"):
                        game_over = True
                        draw_figures()
                        draw_winner_text("The Robot Wins!")
                        return
                    board[r][c] = " "
        
        # 2. הגנה
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    if check_win("X"):
                        board[r][c] = "O"
                        player = "X"
                        draw_figures()
                        return
                    board[r][c] = " "

        # 3. מרכז
        if board[1][1] == " ":
            board[1][1] = "O"
            player = "X"
            draw_figures()
            return

        # 4. פינות ואקראי
        empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == " "]
        if empty:
            r, c = random.choice(empty)
            board[r][c] = "O"
            if check_win("O"):
                game_over = True
                draw_winner_text("The Robot Wins!")
            elif is_board_full():
                game_over = True
                draw_winner_text("Tie Game!")
            else:
                player = "X"
            draw_figures()

    # תחילת המשחק - ציור ראשוני
    draw_lines()

    # לולאת Pygame
    in_game = True
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game_mode == "pvp" or (game_mode == "ai" and player == "X"):
                    mouseX, mouseY = event.pos
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    
                    if board[clicked_row][clicked_col] == " ":
                        board[clicked_row][clicked_col] = player
                        draw_figures()
                        
                        if check_win(player):
                            game_over = True
                            draw_winner_text(f"Player {player} Wins!")
                        elif is_board_full():
                            game_over = True
                            draw_winner_text("Tie Game!")
                        else:
                            player = "O" if player == "X" else "X"

            if event.type == pygame.KEYDOWN:
                # איפוס משחק (Space)
                if event.key == pygame.K_SPACE and game_over:
                    screen.fill(BG_COLOR)
                    draw_lines()
                    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                    player = "X"
                    game_over = False
                
                # חזרה לתפריט הראשי (M) - סגירת חלון Pygame והחזרת CustomTkinter
                if event.key == pygame.K_m:
                    pygame.quit()  # סוגר את חלון ה-Pygame
                    menu_window.deiconify()  # מחזיר ומציג את חלון ה-CustomTkinter
                    return  # יוצא מהפונקציה חזרה לתפריט

        if game_mode == "ai" and player == "O" and not game_over:
            pygame.time.delay(400)
            ai_move()

        if pygame.get_init():  # מונע שגיאה במקרה ש-pygame.quit() כבר רץ
            pygame.display.update()


# --- הגדרת תפריט פתיחה עם CustomTkinter ---

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("תפריט ראשי - איקס עיגול")
        self.geometry("400x400") # הגדלנו מעט את הגובה כדי להכיל את הכפתור החדש בנוחות
        self.resizable(False, False)
        
        # כותרת ראשית
        self.title_label = ctk.CTkLabel(
            self, 
            text="Tic Tac Toe", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold")
        )
        self.title_label.pack(pady=(40, 10))
        
        # תת כותרת
        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="בחר מצב משחק כדי להתחיל:", 
            font=ctk.CTkFont(family="Arial", size=16)
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # כפתור 1: שחקן נגד שחקן
        self.btn_pvp = ctk.CTkButton(
            self, 
            text="שחקן נגד שחקן (מקומי)", 
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=260,
            height=45,
            corner_radius=8,
            command=self.start_pvp
        )
        self.btn_pvp.pack(pady=10)
        
        # כפתור 2: שחקן נגד רובוט
        self.btn_ai = ctk.CTkButton(
            self, 
            text="שחקן נגד רובוט חכם", 
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=260,
            height=45,
            corner_radius=8,
            command=self.start_ai
        )
        self.btn_ai.pack(pady=10)

        # כפתור 3: יציאה מהתוכנית
        self.btn_exit = ctk.CTkButton(
            self, 
            text="🚪 יציאה / Exit", 
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#A83232",
            hover_color="#822121",
            width=150,
            height=40,
            corner_radius=8,
            command=self.destroy
        )
        self.btn_exit.pack(pady=(25, 10))
        
    def start_pvp(self):
        self.withdraw()  # מחביא את חלון התפריט (במקום למחוק אותו)
        run_pygame_game("pvp", self)  # שולח את חלון התפריט כפרמטר למשחק
        
    def start_ai(self):
        self.withdraw()  # מחביא את חלון התפריט
        run_pygame_game("ai", self)  # שולח את חלון התפריט כפרמטר למשחק

# הרצת התפריט הראשי
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()