import pygame
import random
import sys

# אתחול pygame
pygame.init()

# הגדרת קבועים
WINDOW_SIZE = 500
GRID_SIZE = 4
TILE_SIZE = 100
GAP_SIZE = 15
TOP_PANEL = 80  # שטח עליון לניקוד ולטקסט

# מימדי חלון המשחק
WIDTH = WINDOW_SIZE
HEIGHT = WINDOW_SIZE + TOP_PANEL

# פלטת צבעים (סגנון 2048 המקורי)
COLOR_BG = (187, 173, 160)
COLOR_EMPTY_TILE = (205, 193, 180)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_TEXT_LIGHT = (249, 246, 242)

# מילון צבעים לכל אריח לפי הערך שלו
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# הגדרת מסך
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameCenter - 2048")


def add_new_tile(board):
    """מוסיף אריח חדש (2 או 4) במיקום ריק אקראי"""
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 4 if random.random() < 0.1 else 2


def reset_game():
    """מאתחל לוח חדש עם שני אריחים התחלתיים"""
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board


def compress(board):
    """דוחף את כל האריחים שמאלה (בלי לחבר עדיין)"""
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
    """מחבר אריחים זהים צמודים שמאלה"""
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
    """מסובב את הלוח ב-90 מעלות עם כיוון השעון (עוזר לנו ליישם תנועות לכל הכיוונים בלוגיקה של שמאלה)"""
    return [list(x) for x in zip(*board[::-1])]


def move_left(board, score):
    """תנועה שמאלה: דחיסה -> חיבור -> דחיסה שוב"""
    b1, changed1 = compress(board)
    b2, changed2, score = merge(b1, score)
    b3, changed3 = compress(b2)
    return b3, (changed1 or changed2 or changed3), score


def move_right(board, score):
    """תנועה ימינה: סיבוב 180 מעלות, הזזה שמאלה, וסיבוב חזרה"""
    b = rotate(rotate(board))
    b, changed, score = move_left(b, score)
    return rotate(rotate(b)), changed, score


def move_up(board, score):
    """תנועה למעלה: סיבוב 270 מעלות, הזזה שמאלה, וסיבוב חזרה"""
    b = rotate(rotate(rotate(board)))
    b, changed, score = move_left(b, score)
    return rotate(b), changed, score


def move_down(board, score):
    """תנועה למטה: סיבוב 90 מעלות, הזזה שמאלה, וסיבוב חזרה"""
    b = rotate(board)
    b, changed, score = move_left(b, score)
    return rotate(rotate(rotate(b))), changed, score


def check_game_over(board):
    """בודק אם אין יותר מהלכים חוקיים בלוח"""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return False
            if r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
            if c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
    return True


def draw_interface(board, score):
    """מצייר את הלוח, האריחים והניקוד"""
    screen.fill(COLOR_BG)
    
    # ציור פאנל הניקוד העליון
    font_score = pygame.font.SysFont("arial", 30, bold=True)
    text_score = font_score.render(f"SCORE: {score}", True, COLOR_TEXT_LIGHT)
    screen.blit(text_score, (20, 20))
    
    # ציור רשת האריחים
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            # חישוב מיקום ויזואלי על המסך
            x = c * TILE_SIZE + (c + 1) * GAP_SIZE
            y = r * TILE_SIZE + (r + 1) * GAP_SIZE + TOP_PANEL
            
            # צבע האריח
            tile_color = TILE_COLORS.get(val, (60, 58, 50)) if val != 0 else COLOR_EMPTY_TILE
            pygame.draw.rect(screen, tile_color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=6)
            
            # ציור המספר בפנים
            if val != 0:
                font_size = 40 if val < 100 else (32 if val < 1000 else 24)
                font_tile = pygame.font.SysFont("arial", font_size, bold=True)
                text_color = COLOR_TEXT_DARK if val in [2, 4] else COLOR_TEXT_LIGHT
                text_surface = font_tile.render(str(val), True, text_color)
                text_rect = text_surface.get_rect(center=(x + TILE_SIZE/2, y + TILE_SIZE/2))
                screen.blit(text_surface, text_rect)


def main():
    board = reset_game()
    score = 0
    game_over = False

    while True:
        draw_interface(board, score)
        
        if game_over:
            # מסך Game Over עמום
            s = pygame.Surface((WIDTH, HEIGHT))
            s.set_alpha(200)
            s.fill((238, 228, 218))
            screen.blit(s, (0, 0))
            font_go = pygame.font.SysFont("arial", 50, bold=True)
            text_go = font_go.render("GAME OVER", True, COLOR_TEXT_DARK)
            text_rect = text_go.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text_go, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and not game_over:
                moved = False
                
                if event.key == pygame.K_LEFT:
                    board, moved, score = move_left(board, score)
                elif event.key == pygame.K_RIGHT:
                    board, moved, score = move_right(board, score)
                elif event.key == pygame.K_UP:
                    board, moved, score = move_up(board, score)
                elif event.key == pygame.K_DOWN:
                    board, moved, score = move_down(board, score)
                
                # אם משהו זז, נוסיף אריח חדש ונבדוק אם המשחק נגמר
                if moved:
                    add_new_tile(board)
                    if check_game_over(board):
                        game_over = True


if __name__ == "__main__":
    main()