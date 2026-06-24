import pygame
import sys
import random

# 1. אתחול Pygame
pygame.init()

# 2. הגדרת קבועים
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# צבעים (RGB)
BG_COLOR = (28, 170, 156)       # טורקיז כהה לרקע המשחק
LINE_COLOR = (23, 145, 135)     # טורקיז עוד יותר כהה לקווים
X_COLOR = (84, 84, 84)          # אפור כהה לאיקס
O_COLOR = (242, 235, 211)       # שמנת לעיגול
MENU_BG = (40, 50, 70)          # כחול-אפור כהה לרקע התפריט
BUTTON_COLOR = (50, 180, 120)    # ירוק לכפתורים
BUTTON_HOVER = (70, 210, 140)    # ירוק בהיר במעבר עכבר
TEXT_COLOR = (255, 255, 255)    # לבן לטקסט

# הגדרת המסך והגופנים
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('איקס עיגול מורחב - Pygame')

font_large = pygame.font.SysFont('Arial', 45, bold=True)
font_medium = pygame.font.SysFont('Arial', 28, bold=True)
font_small = pygame.font.SysFont('Arial', 18, bold=False)

# 3. משתני מצב המשחק
# game_state יכול להיות: "menu" (תפריט), "game" (משחק)
game_state = "menu"
# game_mode יכול להיות: "pvp" (שני שחקנים) או "ai" (נגד רובוט)
game_mode = "pvp"

board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = "X"
game_over = False

# --- פונקציות הציור והמשחק ---

def draw_lines():
    screen.fill(BG_COLOR)
    # קווים אופקיים
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # קווים אנכיים
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

def is_square_available(row, col):
    return board[row][col] == " "

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def check_win(current_player):
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == current_player: return True
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == current_player: return True
    if board[0][0] == board[1][1] == board[2][2] == current_player: return True
    if board[2][0] == board[1][1] == board[0][2] == current_player: return True
    return False

def draw_winner_text(text):
    text_surface = font_large.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bg_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 10, text_rect.width + 40, text_rect.height + 20)
    pygame.draw.rect(screen, (0, 0, 0), bg_rect)
    screen.blit(text_surface, text_rect)
    
    # הוראות קטנות מתחת לחלון הניצחון
    sub_text = font_small.render("Press SPACE to Restart | Press M for Menu", True, TEXT_COLOR)
    sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(sub_text, sub_rect)

def restart_game():
    global board, player, game_over
    draw_lines()
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False

# --- פונקציות בינה מלאכותית (רובוט) ---

def ai_move():
    """בינה מלאכותית חכמה: תוקפת, חוסמת ולוקחת את המרכז"""
    global player, game_over
    if game_over: return
    
    # 1. בדיקת מהלכי ניצחון של הרובוט (התקפה)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if is_square_available(row, col):
                board[row][col] = "O"  # סימולציה של מהלך
                if check_win("O"):
                    execute_ai_move(row, col)
                    return
                board[row][col] = " "  # ביטול סימולציה
                
    # 2. בדיקת מהלכי ניצחון של השחקן (הגנה וחסימה)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if is_square_available(row, col):
                board[row][col] = "X"  # סימולציה של מהלך השחקן
                if check_win("X"):
                    execute_ai_move(row, col)  # חסימה!
                    return
                board[row][col] = " "  # ביטול סימולציה

    # 3. אסטרטגיה: ניסיון לתפוס את מרכז הלוח (1,1)
    if is_square_available(1, 1):
        execute_ai_move(1, 1)
        return

    # 4. אם המרכז תפוס, ניסיון לתפוס פינות (0,0), (0,2), (2,0), (2,2)
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [c for c in corners if is_square_available(c[0], c[1])]
    if available_corners:
        row, col = random.choice(available_corners)
        execute_ai_move(row, col)
        return

    # 5. ברירת מחדל: בחירת משבצת פנויה אקראית שנשארה
    empty_squares = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if is_square_available(r, c)]
    if empty_squares:
        row, col = random.choice(empty_squares)
        execute_ai_move(row, col)

def execute_ai_move(row, col):
    """פונקציית עזר לביצוע המהלך שנבחר ועדכון מצב המשחק"""
    global player, game_over
    board[row][col] = "O"
    if check_win("O"):
        game_over = True
        draw_figures()
        draw_winner_text("The Robot Wins!")
    elif is_board_full():
        game_over = True
        draw_figures()
        draw_winner_text("Tie Game!")
    else:
        player = "X"
    draw_figures()

# --- פונקציות תפריט (Menu) ---

def draw_menu():
    """ציור מסך תפריט הפתיחה עם כפתורים אינטראקטיביים"""
    screen.fill(MENU_BG)
    
    # כותרת המשחק
    title_surf = font_large.render("Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_surf, title_rect)
    
    # מיקומי העכבר לצורך אפקט מעבר (Hover)
    mouse_pos = pygame.mouse.get_pos()
    
    # כפתור 1: שחקן נגד שחקן
    btn1_rect = pygame.Rect(WIDTH // 2 - 175, 220, 350, 60)
    color1 = BUTTON_HOVER if btn1_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color1, btn1_rect, border_radius=10)
    text1 = font_medium.render("1. Player vs Player (Regular)", True, TEXT_COLOR)
    screen.blit(text1, text1.get_rect(center=btn1_rect.center))
    
    # כפתור 2: שחקן נגד רובוט
    btn2_rect = pygame.Rect(WIDTH // 2 - 175, 340, 350, 60)
    color2 = BUTTON_HOVER if btn2_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color2, btn2_rect, border_radius=10)
    text2 = font_medium.render("2. Player vs Robot", True, TEXT_COLOR)
    screen.blit(text2, text2.get_rect(center=btn2_rect.center))
    
    return btn1_rect, btn2_rect


# --- הלולאה הראשית של המשחק ---
btn1_rect, btn2_rect = pygame.Rect(0,0,0,0), pygame.Rect(0,0,0,0)

while True:
    if game_state == "menu":
        btn1_rect, btn2_rect = draw_menu()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # לחיצות במסך התפריט
            if game_state == "menu":
                if btn1_rect.collidepoint(event.pos):
                    game_mode = "pvp"
                    game_state = "game"
                    restart_game()
                elif btn2_rect.collidepoint(event.pos):
                    game_mode = "ai"
                    game_state = "game"
                    restart_game()
            
            # לחיצות במהלך המשחק
            elif game_state == "game" and not game_over:
                # רק אם זה התור של השחקן האנושי (X) או במצב שני שחקנים
                if game_mode == "pvp" or (game_mode == "ai" and player == "X"):
                    clicked_row = mouse_y // SQUARE_SIZE
                    clicked_col = mouse_x // SQUARE_SIZE
                    
                    if is_square_available(clicked_row, clicked_col):
                        board[clicked_row][clicked_col] = player
                        draw_figures()
                        
                        if check_win(player):
                            game_over = True
                            draw_winner_text(f"Player {player} Wins!")
                        elif is_board_full():
                            game_over = True
                            draw_winner_text("Tie Game!")
                        else:
                            # החלפת תור
                            player = "O" if player == "X" else "X"

        # לחיצות מקלדת
        if event.type == pygame.KEYDOWN:
            # אתחול המשחק (Space)
            if event.key == pygame.K_SPACE and game_over:
                restart_game()
            # חזרה לתפריט הראשי (M)
            if event.key == pygame.K_m and game_state == "game":
                game_state = "menu"

    # מנגנון הפעלה אוטומטי של הרובוט
    if game_state == "game" and game_mode == "ai" and player == "O" and not game_over:
        pygame.time.delay(400) # השהייה קלה של 0.4 שניות כדי שהרובוט ירגיש אנושי
        ai_move()

    pygame.display.update()