import os
import sys
import random
import customtkinter as ctk
import pygame

# English Only Word Bank
WORD_BANK = {
    "Animals": ["LION", "ELEPHANT", "GIRAFFE", "DOLPHIN", "TIGER", "PANDA", "MONKEY", "RABBIT"],
    "Countries": ["ISRAEL", "ITALY", "FRANCE", "JAPAN", "CANADA", "BRAZIL", "SPAIN", "EGYPT"],
    "Foods": ["PIZZA", "BURGER", "SUSHI", "PASTA", "CHOCOLATE", "BANANA", "SALAD", "BREAD"],
    "General": ["COMPUTER", "PHONE", "FRIEND", "FAMILY", "SCHOOL", "KEYBOARD", "SKY", "FLOWER"]
}

# ==========================================
# 1. Start Window (CustomTkinter)
# ==========================================
class HangmanStartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Hangman - Start Menu")
        self.geometry("500x480")
        self.resizable(False, False)
        self.back_to_games = False  # משתנה שבודק אם ביקשנו לחזור ל-Games Center
        ctk.set_appearance_mode("dark")
        
        # Colorful Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="🪵 HANGMAN 🪵", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#3498DB"
        )
        self.title_label.pack(pady=(30, 20))
        
        # Player Name
        self.name_label = ctk.CTkLabel(self, text="Enter Your Name:", font=("Arial", 16))
        self.name_label.pack(pady=5)
        self.name_input = ctk.CTkEntry(self, placeholder_text="Player", width=200)
        # שומרים את השם הקודם אם קיים (למקרה של חזרה מתפריט)
        old_name = os.environ.get("HANGMAN_PLAYER_NAME", "Player 1")
        self.name_input.insert(0, old_name)
        self.name_input.pack(pady=5)

        # Category Selection
        self.category_label = ctk.CTkLabel(self, text="Select Category:", font=("Arial", 16))
        self.category_label.pack(pady=(15, 5))
        self.category_combo = ctk.CTkComboBox(self, values=list(WORD_BANK.keys()), width=200)
        
        # שומרים את הקטגוריה הקודמת אם קיימת
        old_cat = os.environ.get("HANGMAN_LAST_CAT", "Animals")
        if old_cat in WORD_BANK:
            self.category_combo.set(old_cat)
        else:
            self.category_combo.set("Animals")
        self.category_combo.pack(pady=5)

        # Start Button
        self.start_btn = ctk.CTkButton(
            self,
            text="🎮 Play Game 🎮",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            fg_color="#2B2B2B",
            hover_color="#444444",
            border_width=2,
            border_color="#3498DB",
            height=50,
            command=self.launch_game
        )
        self.start_btn.pack(pady=35)
        
        self.player_name = "Player"
        self.selected_category = ""
        self.should_start = False

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

    def return_to_main_menu(self):
        """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
        self.back_to_games = True
        self.destroy()

    def launch_game(self):
        self.player_name = self.name_input.get().strip() or "Player"
        self.selected_category = self.category_combo.get()
        # שומרים את הנתונים בסביבה למקרה של הפעלה מחדש
        os.environ["HANGMAN_PLAYER_NAME"] = self.player_name
        os.environ["HANGMAN_LAST_CAT"] = self.selected_category
        self.should_start = True
        self.destroy()


# ==========================================
# 2. Game Code (Pygame)
# ==========================================
# הפונקציה עכשיו מחזירה True אם צריך לחזור לתפריט, ו-False אם צריך לצאת לגמרי
def run_hangman_game(player_name, category):
    pygame.init()
    
    WIDTH, HEIGHT = 700, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman")
    clock = pygame.time.Clock()
    
    # Fonts
    font = pygame.font.SysFont("Arial", 22, bold=True)
    large_font = pygame.font.SysFont("Arial", 38, bold=True)
    letter_font = pygame.font.SysFont("Arial", 32, bold=True)
    
    # Colors
    BG_COLOR = (44, 62, 80)
    WOOD_COLOR = (139, 69, 19)
    ROPE_COLOR = (245, 222, 179)
    WHITE = (255, 255, 255)
    RED = (231, 76, 60)
    GREEN = (46, 204, 113)

    # Pick secret word
    secret_word = random.choice(WORD_BANK[category]).upper()
    guessed_letters = set()
    wrong_attempts = 0
    max_attempts = 6
    game_over = False
    win = False

    # Draw gallows and stickman
    def draw_hangman(attempts):
        pygame.draw.rect(screen, WOOD_COLOR, (80, 480, 200, 20), border_radius=5)
        pygame.draw.rect(screen, WOOD_COLOR, (120, 150, 20, 330), border_radius=5)
        pygame.draw.rect(screen, WOOD_COLOR, (120, 150, 150, 20), border_radius=5)
        pygame.draw.line(screen, ROPE_COLOR, (240, 170), (240, 210), width=4)
        
        if attempts >= 1: pygame.draw.circle(screen, WHITE, (240, 240), 30, width=4)
        if attempts >= 2: pygame.draw.line(screen, WHITE, (240, 270), (240, 370), width=4)
        if attempts >= 3: pygame.draw.line(screen, WHITE, (240, 300), (200, 330), width=4)
        if attempts >= 4: pygame.draw.line(screen, WHITE, (240, 300), (280, 330), width=4)
        if attempts >= 5: pygame.draw.line(screen, WHITE, (240, 370), (200, 420), width=4)
        if attempts >= 6: pygame.draw.line(screen, WHITE, (240, 370), (280, 420), width=4)

    running = True
    return_to_menu = False # משתנה חדש שקובע אם לחזור לתפריט

    while running:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return_to_menu = False # סגירת חלון = יציאה מוחלטת

            # קליטת ESC בכל שלב במשחק
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return_to_menu = True # לחיצה על ESC = חזרה לתפריט
                
            if event.type == pygame.KEYDOWN and not game_over:
                char = event.unicode.upper()
                if char.isalpha() and char != "":
                    if char not in guessed_letters:
                        guessed_letters.add(char)
                        if char not in secret_word:
                            wrong_attempts += 1
                            if wrong_attempts >= max_attempts:
                                game_over = True
                                win = False
                        
                        if all(letter in guessed_letters or letter == " " for letter in secret_word):
                            game_over = True
                            win = True
            
            # Post-game control (רק X, כי ESC מטופל למעלה)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_x:  # Restart
                    secret_word = random.choice(WORD_BANK[category]).upper()
                    guessed_letters = set()
                    wrong_attempts = 0
                    game_over = False
                    win = False

        # --- Render ---
        pygame.draw.rect(screen, (32, 44, 57), (0, 0, WIDTH, 70))
        name_lbl = font.render(f"👤 {player_name}", True, WHITE)
        category_lbl = font.render(f"Category: {category}", True, (241, 196, 15))
        attempts_lbl = font.render(f"Attempts Left: {max_attempts - wrong_attempts}", True, RED if wrong_attempts > 4 else WHITE)
        screen.blit(name_lbl, (25, 22))
        screen.blit(category_lbl, (WIDTH // 2 - category_lbl.get_width() // 2, 22))
        screen.blit(attempts_lbl, (WIDTH - attempts_lbl.get_width() - 25, 22))

        draw_hangman(wrong_attempts)

        display_word = ""
        for letter in secret_word:
            if letter == " ": display_word += "   "
            elif letter in guessed_letters: display_word += f" {letter} "
            else: display_word += " _ "
        word_lbl = letter_font.render(display_word, True, WHITE)
        screen.blit(word_lbl, (320, 240))

        letters_text = "Tried: " + ", ".join(sorted(list(guessed_letters)))
        letters_lbl = font.render(letters_text, True, (149, 165, 166))
        screen.blit(letters_lbl, (320, 360))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            if win:
                title_txt = large_font.render("YOU WIN! 🎉", True, GREEN)
                summary_text = f"Amazing job! You guessed the word: {secret_word}"
            else:
                title_txt = large_font.render("GAME OVER 💀", True, RED)
                summary_text = f"The word was: {secret_word}"
            summary_txt = font.render(summary_text, True, WHITE)
            restart_txt = font.render("Press 'X' to Play Again", True, (200, 200, 200))
            exit_txt = font.render("Press 'ESC' to return to Category Menu", True, (34, 152, 219)) # טקסט מעודכן

            screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(summary_txt, (WIDTH // 2 - summary_txt.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 30))
            screen.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return return_to_menu # מחזירים את ההחלטה


# ==========================================
# 3. Main Executable Entry (מעודכן)
# ==========================================
if __name__ == "__main__":
    # לולאה אינסופית שמאפשרת חזרה לתפריט
    while True:
        menu = HangmanStartWindow()
        menu.mainloop()
        
        if menu.should_start:
            # מריצים את המשחק ובודקים מה הוא החזיר
            should_return = run_hangman_game(menu.player_name, menu.selected_category)
            
            # אם הוא החזיר False (סגירת חלון), יוצאים מהלולאה האינסופית
            if not should_return:
                break
            # אם הוא החזיר True (ESC), הלולאה ממשיכה ופותחת מחדש את HangmanStartWindow
        else:
            # אם חלון התפריט נסגר בלי ללחוץ על Play
            break