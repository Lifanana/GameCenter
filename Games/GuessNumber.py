import customtkinter as ctk
import random

# הגדרת עיצוב כללי
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GuessNumberGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Guess The Number - נחש את המספר")
        self.geometry("500x550")
        self.resizable(False, False)
        
        # משתני המשחק
        self.secret_number = 0
        self.attempts = 0
        
        # טעינת מסך הפתיחה בהתחלה
        self.show_menu_screen()

    def show_menu_screen(self):
        """מציג את מסך הפתיחה של המשחק"""
        self.clear_screen()

        # כותרת המשחק
        self.title_label = ctk.CTkLabel(
            self, 
            text="🤔 Guess The Number 🤔", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#EDC22E"
        )
        self.title_label.pack(pady=(60, 10))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="האם תצליחו לנחש את המספר הסודי בין 1 ל-100?", 
            font=ctk.CTkFont(family="Arial", size=15)
        )
        self.subtitle_label.pack(pady=(0, 40))

        # כפתור מעבר למשחק
        self.btn_start = ctk.CTkButton(
            self,
            text="🎮 התחל משחק / Start Game",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            width=260,
            height=55,
            corner_radius=10,
            command=self.start_game
        )
        self.btn_start.pack(pady=15)

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
        self.btn_exit.pack(pady=(50, 10))

    def start_game(self):
        """מאתחל משחק חדש ומציג את מסך לוח המשחק"""
        self.clear_screen()
        
        # הגרלת מספר חדש ואיפוס ניסיונות
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # כותרת עליונה
        self.game_title = ctk.CTkLabel(
            self, text="נחש את המספר (1-100)", font=("Arial", 24, "bold")
        )
        self.game_title.pack(pady=(30, 20))

        # תווית להצגת רמזים והודעות למשתמש
        self.feedback_label = ctk.CTkLabel(
            self, 
            text="הכנס מספר ולחץ על 'בדוק' כדי להתחיל!", 
            font=("Arial", 16),
            text_color="#A0A0A0"
        )
        self.feedback_label.pack(pady=15)

        # תיבת קלט להכנסת המספר
        self.guess_entry = ctk.CTkEntry(
            self,
            placeholder_text="המספר שלך...",
            font=("Arial", 20),
            width=180,
            height=45,
            justify="center"
        )
        self.guess_entry.pack(pady=15)
        
        # מאפשר ללחוץ על Enter במקלדת כדי לבדוק
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        # כפתור בדיקה
        self.btn_check = ctk.CTkButton(
            self,
            text="🔍 בדוק / Check",
            font=("Arial", 16, "bold"),
            width=180,
            height=45,
            command=self.check_guess
        )
        self.btn_check.pack(pady=10)

        # תווית המציגה את כמות הניסיונות הנוכחית
        self.attempts_label = ctk.CTkLabel(
            self, text="ניסיונות: 0", font=("Arial", 14), text_color="#888888"
        )
        self.attempts_label.pack(pady=20)

    def check_guess(self):
        """בודק את הניחוש של המשתמש ומעדכן את הממשק"""
        user_input = self.guess_entry.get().strip()
        
        # בדיקה שהקלט הוא אכן מספר תקין
        if not user_input.isdigit():
            self.feedback_label.configure(text="❌ אנא הכנס מספר שלם תקין!", text_color="#FF5555")
            return
        
        guess = int(user_input)
        self.attempts += 1
        self.attempts_label.configure(text=f"ניסיונות: {self.attempts}")
        
        # ניקוי תיבת הקלט לתור הבא
        self.guess_entry.delete(0, 'end')

        if guess < self.secret_number:
            self.feedback_label.configure(text=f"📈 {guess} הוא נמוך מדי! נסה גבוה יותר.", text_color="#38BDF8")
        elif guess > self.secret_number:
            self.feedback_label.configure(text=f"📉 {guess} הוא גבוה מדי! נסה נמוך יותר.", text_color="#FB923C")
        else:
            # ניצחון! מעבר למסך סיום
            self.show_game_over_screen()

    def show_game_over_screen(self):
        """מסך סיום חגיגי שמציג את התוצאה"""
        self.clear_screen()

        self.win_title = ctk.CTkLabel(
            self, text="🎉 כל הכבוד! 🎉", font=("Arial", 36, "bold"), text_color="#50FA7B"
        )
        self.win_title.pack(pady=(50, 10))

        self.result_label = ctk.CTkLabel(
            self, 
            text=f"ניחשתם נכון את המספר: {self.secret_number}\nזה לקח לכם בדיוק {self.attempts} ניסיונות!",
            font=("Arial", 18),
            justify="center"
        )
        self.result_label.pack(pady=30)

        # כפתור לשחק מחדש
        self.btn_restart = ctk.CTkButton(
            self,
            text="🔄 לשחק מחדש / Restart",
            font=("Arial", 15, "bold"),
            fg_color="#50FA7B",
            hover_color="#40D268",
            text_color="#1E1E2E",
            width=240,
            height=45,
            command=self.start_game
        )
        self.btn_restart.pack(pady=10)

        # כפתור חזרה לתפריט הפתיחה
        self.btn_menu = ctk.CTkButton(
            self,
            text="🏠 תפריט ראשי / Main Menu",
            font=("Arial", 15, "bold"),
            fg_color="#444444",
            hover_color="#333333",
            width=240,
            height=45,
            command=self.show_menu_screen
        )
        self.btn_menu.pack(pady=10)

    def clear_screen(self):
        """פונקציית עזר המנקה את כל הרכיבים מהמסך הנוכחי"""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = GuessNumberGame()
    app.mainloop()