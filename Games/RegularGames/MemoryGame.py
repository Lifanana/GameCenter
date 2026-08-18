import os
import sys
import time
import random
import customtkinter as ctk
import pygame

# ==========================================
# 1. חלון התחלה באמצעות CustomTkinter
# ==========================================
class MemoryStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Memory Game - Start Menu")
        self.geometry("500x480")
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        # כותרת ראשית צבעונית
        self.title_label = ctk.CTkLabel(
            self, 
            text="🃏 MEMORY GAME 🃏", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#9B59B6"
        )
        self.title_label.pack(pady=(30, 20))
        
        # שם שחקן
        self.name_label = ctk.CTkLabel(self, text="Enter Your Name:", font=("Arial", 16))
        self.name_label.pack(pady=5)
        self.name_input = ctk.CTkEntry(self, placeholder_text="Player", width=200)
        self.name_input.insert(0, "Player 1")
        self.name_input.pack(pady=5)

        # בחירת רמת קושי (זמן הצגת קלפים לא תואמים לפני סגירה)
        self.difficulty_label = ctk.CTkLabel(self, text="Select Difficulty:", font=("Arial", 16))
        self.difficulty_label.pack(pady=(15, 5))
        self.difficulty_combo = ctk.CTkComboBox(
            self, 
            values=["Easy (Show longer)", "Medium (Normal)", "Hard (Fast close)"],
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
            border_color="#9B59B6",
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
            height=50,
            command=self.return_to_main_menu
        )
        self.btn_back.pack(pady=30)

        self.player_name = "Player"
        self.reveal_delay_ms = 1000  # ברירת מחדל
        self.should_start = False

    def return_to_main_menu(self):
          """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
          self.back_to_games = True
          self.destroy()
        
     

    def launch_game(self):
        self.player_name = self.name_input.get().strip() or "Player"
        diff = self.difficulty_combo.get()
        if "Easy" in diff:
            self.reveal_delay_ms = 1500
        elif "Hard" in diff:
            self.reveal_delay_ms = 500
        else:
            self.reveal_delay_ms = 1000
            
        self.should_start = True
        self.destroy()


# ==========================================
# 2. קוד המשחק באמצעות Pygame
# ==========================================
def run_memory_game(player_name, reveal_delay):
    pygame.init()
    
    # מימדי חלון
    WIDTH, HEIGHT = 600, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    
    # פונטים
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 42, bold=True)
    symbol_font = pygame.font.SysFont("Segoe UI Symbol", 45) # תמיכה באמוג'י / סמלים מובנים
    
    # צבעים
    BG_COLOR = (34, 40, 49)
    CARD_BACK_COLOR = (46, 204, 113) # ירוק כשהקלף סגור
    CARD_FRONT_COLOR = (236, 240, 241) # לבן-אפרפר כשהוא פתוח
    CARD_BORDER = (40, 40, 60)
    
    # 8 זוגות של סמלים/צורות צבעוניים
    SHAPES = [
        {"char": "⭐", "color": (241, 196, 15)},  # כוכב זהב
        {"char": "❤️", "color": (231, 76, 60)},   # לב אדום
        {"char": "🎈", "color": (230, 126, 34)},  # בלון כתום
        {"char": "🍀", "color": (46, 204, 113)},  # תלתן ירוק
        {"char": "💎", "color": (52, 152, 219)},  # יהלום כחול
        {"char": "🔮", "color": (155, 89, 182)},  # כדור בדולח סגול
        {"char": "🐱", "color": (243, 156, 18)},  # חתול כתום
        {"char": "🦊", "color": (211, 84, 0)}     # שועל
    ] * 2  # מכפילים ליצירת זוגות (סה"כ 16)

    # ערבוב הקלפים
    random.shuffle(SHAPES)
    
    # בניית מבנה הקלפים (מטריצה של 4x4)
    COLS, ROWS = 4, 4
    CARD_SIZE = 100
    GAP = 20
    
    # חישוב אופסט כדי למרכז את הלוח במסך
    board_width = (COLS * CARD_SIZE) + ((COLS - 1) * GAP)
    board_height = (ROWS * CARD_SIZE) + ((ROWS - 1) * GAP)
    START_X = (WIDTH - board_width) // 2
    START_Y = ((HEIGHT - board_height) // 2) + 40

    cards = []
    for i in range(16):
        r = i // COLS
        c = i % COLS
        x = START_X + c * (CARD_SIZE + GAP)
        y = START_Y + r * (CARD_SIZE + GAP)
        cards.append({
            "rect": pygame.Rect(x, y, CARD_SIZE, CARD_SIZE),
            "shape": SHAPES[i]["char"],
            "color": SHAPES[i]["color"],
            "revealed": False,
            "matched": False
        })

    # משתני משחק
    flipped_indices = []
    waiting_timer = 0
    turns = 0
    matches_found = 0
    game_over = False

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        screen.fill(BG_COLOR)

        # קבלת אירועים
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # מניעת קליקים בזמן שהמשחק מציג זוג לא תואם לפני סגירתו
                if len(flipped_indices) < 2 and current_time > waiting_timer:
                    mouse_pos = event.pos
                    for idx, card in enumerate(cards):
                        if not card["revealed"] and not card["matched"]:
                            if card["rect"].collidepoint(mouse_pos):
                                card["revealed"] = True
                                flipped_indices.append(idx)
                                
                                # אם הפכנו שני קלפים
                                if len(flipped_indices) == 2:
                                    turns += 1
                                    idx1, idx2 = flipped_indices
                                    
                                    # בדיקה אם יש התאמה
                                    if cards[idx1]["shape"] == cards[idx2]["shape"]:
                                        cards[idx1]["matched"] = True
                                        cards[idx2]["matched"] = True
                                        flipped_indices = []
                                        matches_found += 1
                                        if matches_found == 8:
                                            game_over = True
                                    else:
                                        # אם אין התאמה, נקבע טיימר לסגירה אוטומטית
                                        waiting_timer = current_time + reveal_delay

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True

                if game_over:
                    if event.key == pygame.K_x:  # התחלה מחדש
                        random.shuffle(SHAPES)
                        for idx, card in enumerate(cards):
                            card["shape"] = SHAPES[idx]["char"]
                            card["color"] = SHAPES[idx]["color"]
                            card["revealed"] = False
                            card["matched"] = False
                        flipped_indices = []
                        turns = 0
                        matches_found = 0
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:  # יציאה
                        running = False

        # סגירת הקלפים הלא תואמים לאחר סיום הטיימר
        if len(flipped_indices) == 2 and current_time > waiting_timer and waiting_timer != 0:
            idx1, idx2 = flipped_indices
            cards[idx1]["revealed"] = False
            cards[idx2]["revealed"] = False
            flipped_indices = []
            waiting_timer = 0

        # --- ציור המסך ---

        # בר מידע עליון
        pygame.draw.rect(screen, (23, 28, 36), (0, 0, WIDTH, 70))
        name_lbl = font.render(f"👤 {player_name}", True, (255, 255, 255))
        turns_lbl = font.render(f"Turns: {turns}", True, (241, 196, 15))
        
        # חישוב אחוז דיוק
        accuracy = int((matches_found / turns) * 100) if turns > 0 else 100
        accuracy_lbl = font.render(f"Accuracy: {accuracy}%", True, (155, 89, 182))

        screen.blit(name_lbl, (25, 22))
        screen.blit(turns_lbl, (WIDTH // 2 - turns_lbl.get_width() // 2, 22))
        screen.blit(accuracy_lbl, (WIDTH - accuracy_lbl.get_width() - 25, 22))

        # ציור הקלפים
        for card in cards:
            if card["revealed"] or card["matched"]:
                # קלף פתוח
                pygame.draw.rect(screen, CARD_FRONT_COLOR, card["rect"], border_radius=12)
                pygame.draw.rect(screen, CARD_BORDER, card["rect"], width=3, border_radius=12)
                
                # ציור האייקון/סמל במרכז
                shape_text = symbol_font.render(card["shape"], True, card["color"])
                text_x = card["rect"].x + (CARD_SIZE - shape_text.get_width()) // 2
                text_y = card["rect"].y + (CARD_SIZE - shape_text.get_height()) // 2
                screen.blit(shape_text, (text_x, text_y))
            else:
                # קלף סגור
                pygame.draw.rect(screen, CARD_BACK_COLOR, card["rect"], border_radius=12)
                pygame.draw.rect(screen, CARD_BORDER, card["rect"], width=3, border_radius=12)
                
                # סימן שאלה במרכז הקלף הסגור
                q_text = font.render("?", True, (255, 255, 255))
                text_x = card["rect"].x + (CARD_SIZE - q_text.get_width()) // 2
                text_y = card["rect"].y + (CARD_SIZE - q_text.get_height()) // 2
                screen.blit(q_text, (text_x, text_y))

        # מסך סיום המשחק
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title_txt = large_font.render("WELL DONE!", True, (46, 204, 113))
            summary_txt = font.render(f"Cleared in {turns} turns with {accuracy}% accuracy!", True, (255, 255, 255))
            restart_txt = font.render("Press 'X' to Play Again", True, (200, 200, 200))
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
# ==========================================
# 3. ניתוב הפעלה ראשי
# ==========================================
if __name__ == "__main__":
    while True:
        menu = MemoryStartWindow()
        menu.mainloop()
        
        # אם המשתמש לחץ על כפתור חזרה ל-Games Center
        if menu.back_to_games:
            break
            
        # אם המשתמש לחץ על כפתור התחלת משחק
        if menu.should_start:
            # מריצים את המשחק ושומרים את הערך המוחזר (True ל-ESC, False ליציאה)
            should_return_to_menu = run_memory_game(menu.player_name, menu.reveal_delay_ms)
            
            # אם לא לחצו ESC (למשל סגרו את החלון ב-X), נצא מהלולאה
            if not should_return_to_menu:
                break
            # אם לחצו ESC, הלולאה תמשיך ותפתח שוב את חלון ה-MemoryStartWindow
        else:
            break