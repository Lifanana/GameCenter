import customtkinter as ctk
import turtle
import random
import sys

# הגדרת עיצוב כללי ל-customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# משתנה גלובלי שיעזור לנו לנהל את הניווט חזרה לתפריט
go_to_menu_flag = False

# --- מחלקת עמוד הפתיחה ב-CustomTkinter ---
class TurtleMenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Turtle Control - תפריט פתיחה")
        self.geometry("450x400")
        self.resizable(False, False)
        
        self.start_game_chosen = False

        # כותרת המשחק
        self.title_label = ctk.CTkLabel(
            self, 
            text="🐢 Turtle Control 🐢", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#50FA7B"  
        )
        self.title_label.pack(pady=(60, 20))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="שלטו בצב, שנו צבעים וציירו על המסך!", 
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
            text="⬅️ Back to Games Center",
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#A83232",
            hover_color="#822121",
            width=150,
            height=40,
            corner_radius=10,
             command=self.return_to_main_menu
        )
        self.btn_exit.pack(pady=(40, 10))

    def start_game(self):
        self.start_game_chosen = True
        self.destroy()

    def return_to_main_menu(self):
        """מסמן שרוצים לחזור לתפריט הראשי וסוגר את החלון"""
        self.back_to_games = True
        self.destroy()


# --- פונקציות המשחק ב-Turtle ---

def run_turtle_game():
    """הפעלת חלון המשחק והלוגיקה של Turtle"""
    global go_to_menu_flag
    go_to_menu_flag = False  # איפוס הדגל בכל הפעלה מחדש
    
    # אתחול מסך ה-Turtle
    screen = turtle.Screen()
    screen.title("GameCenter - Turtle Control")
    screen.bgcolor("white")
    screen.setup(width=600, height=600)

    # יצירת הצב (השחקן)
    player = turtle.Turtle()
    player.shape("turtle")
    player.color("blue")
    player.pensize(3)
    player.speed(0)

    # יצירת צב עזר לכתיבת ההוראות למעלה
    drawer = turtle.Turtle()
    drawer.speed(0)
    drawer.hideturtle()
    drawer.penup()
    drawer.goto(0, 260)
    drawer.color("gray")
    drawer.write("חצים: תנועה | רווח: צבע | C: ניקוי | M: חזרה לתפריט", align="center", font=("Arial", 11, "bold"))

    # פונקציות תנועה ושליטה
    def move_forward():
        player.forward(20)

    def move_backward():
        player.backward(20)

    def turn_left():
        player.left(15)

    def turn_right():
        player.right(15)

    def change_color_random():
        colors = ["red", "green", "blue", "purple", "orange", "magenta", "cyan"]
        player.color(random.choice(colors))

    def clear_screen():
        player.clear()

    def go_back_to_menu():
        """סוגר את חלון ה-turtle הנוכחי ומסמן שרוצים לחזור לתפריט"""
        global go_to_menu_flag
        go_to_menu_flag = True
        screen.bye()  # סוגר את חלון הטרטל ומסיים את ה-mainloop בצורה בטוחה

    # הגדרת ההקשבה למקלדת
    screen.listen()
    screen.onkeypress(move_forward, "Up")
    screen.onkeypress(move_backward, "Down")
    screen.onkeypress(turn_left, "Left")
    screen.onkeypress(turn_right, "Right")
    screen.onkeypress(change_color_random, "space")  
    screen.onkeypress(clear_screen, "c")             
    screen.onkeypress(go_back_to_menu, "m")  # הקשבה למקש M לחזרה לתפריט

    # השארת החלון פתוח ומניעת קריסה
    try:
        screen.mainloop()
    except (turtle.Terminator, _tkinter.TclError):
        pass


# --- ניהול הצימוד והריצה הראשי ---
def main():
    while True:
        # 1. הפעלת עמוד הפתיחה ב-CustomTkinter
        menu = TurtleMenuApp()
        menu.mainloop()

        # 2. אם המשתמש לחץ על כפתור ההתחלה, נעבור למשחק ה-Turtle
        if menu.start_game_chosen:
            run_turtle_game()
            
            # 3. ברגע שחלון ה-Turtle נסגר, בודקים אם זה קרה בגלל שלחצו על M
            if go_to_menu_flag:
                continue  # חוזר לתחילת הלולאה ומציג שוב את התפריט הראשי
            else:
                break  # אם החלון נסגר סתם ב-X, נצא מהלולאה ונסיים
        else:
            break


if __name__ == "__main__":
    main()