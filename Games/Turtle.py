import turtle
import random

# 1. הגדרת מסך המשחק והחלון
screen = turtle.Screen()
screen.title("GameCenter - Turtle Control")
screen.bgcolor("white")
screen.setup(width=600, height=600)  # קיבוע גודל החלון כדי שהכפתורים יהיו מדויקים

# 2. יצירת הצב (השחקן)
player = turtle.Turtle()
player.shape("turtle")
player.color("blue")
player.pensize(3)
player.speed(0)
player.hideturtle()  # נסתיר אותו במסך הפתיחה

def change_color_random():
    """שינוי צבע הצב לצבע אקראי"""
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]
    player.color(random.choice(colors))

# יצירת צב עזר מיוחד לציור הכפתורים והטקסטים
drawer = turtle.Turtle()
drawer.speed(0)
drawer.hideturtle()

# משתנה גלובלי שעוקב אחרי מצב המשחק ("menu" או "game")
game_state = "menu"

# --- פונקציות תנועה ושליטה בצב ---
def move_forward():
    if game_state == "game":
        player.forward(20)

def move_backward():
    if game_state == "game":
        player.backward(20)

def turn_left():
    if game_state == "game":
        player.left(15)

def turn_right():
    if game_state == "game":
        player.right(15)

def change_color_red():
    if game_state == "game": player.color("red")

def change_color_green():
    if game_state == "game": player.color("green")

def change_color_blue():
    if game_state == "game": player.color("blue")

def clear_screen():
    if game_state == "game": player.clear()

# --- פונקציות ניהול מסכים וכפתורים ---

def draw_button(x, y, width, height, text, color):
    """פונקציית עזר לציור כפתור מלבני עם טקסט במרכזו"""
    drawer.penup()
    drawer.goto(x - width/2, y - height/2)
    drawer.pendown()
    drawer.color(color)
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(width)
        drawer.left(90)
        drawer.forward(height)
        drawer.left(90)
    drawer.end_fill()
    
    # כתיבת הטקסט במרכז הכפתור
    drawer.penup()
    drawer.goto(x, y - 10)  # התאמה קלה שיהיה במרכז לגובה
    drawer.color("white")
    drawer.write(text, align="center", font=("Arial", 14, "bold"))

def show_menu():
    """הצגת מסך הפתיחה"""
    global game_state
    game_state = "menu"
    
    player.hideturtle()  # הסתרת השחקן
    player.penup()       # מניעת ציור בזמן שהשחקן חוזר למרכז
    player.goto(0, 0)
    
    drawer.clear()       # ניקוי מסך הפתיחה הקודם
    screen.bgcolor("lightblue")  # רקע לתפריט
    
    # כותרת המשחק
    drawer.penup()
    drawer.goto(0, 150)
    drawer.color("navy")
    drawer.write("ברוכים הבאים למשחק הצב!", align="center", font=("Arial", 24, "bold"))
    
    # ציור כפתור "שחק" (במרכז המסך בקואורדינטות 0,0)
    draw_button(0, 0, 150, 50, "שחק (Play)", "green")

def start_game():
    """מעבר למצב משחק"""
    global game_state
    game_state = "game"
    
    drawer.clear()  # מחיקת כפתורי התפריט
    screen.bgcolor("white")  # רקע המשחק
    
    # הוראות קטנות בחלק העליון שיראו תמיד
    drawer.penup()
    drawer.goto(0, 260)
    drawer.color("gray")
    drawer.write("לחץ על M כדי לחזור לתפריט הראשי | C כדי לנקות", align="center", font=("Arial", 10, "normal"))
    
    player.pendown()  # החזרת היכולת לצייר
    player.showturtle()  # הצגת הצב שוב

def check_click(x, y):
    """פונקציה שבודקת איפה המשתמש לחץ עם העכבר"""
    global game_state
    if game_state == "menu":
        # בדיקה האם הלחיצה הייתה בתוך גבולות כפתור "שחק"
        # הכפתור נמצא ב-X בין 75- ל-75, וב-Y בין 25- ל-25
        if -75 < x < 75 and -25 < y < 25:
            start_game()

def go_back_to_menu():
    """פונקציה שמופעלת בלחיצה על המקלדת ומחזירה לתפריט"""
    if game_state == "game":
        player.clear()  # מוחק את הציורים הקודמים
        show_menu()

# --- 5. הגדרת ההקשבה למקלדת ולעכבר ---
screen.listen()

# זיהוי לחיצת עכבר על המסך
screen.onclick(check_click)

# קישור מקשי החיצים לתנועה
screen.onkeypress(move_forward, "Up")
screen.onkeypress(move_backward, "Down")
screen.onkeypress(turn_left, "Left")
screen.onkeypress(turn_right, "Right")

# קישור מקשים נוספים לשינוי צבע וניקוי
screen.onkeypress(change_color_random, "space")  # מקש רווח - צבע אקראי 
screen.onkeypress(clear_screen, "c")       # מקש C - מחיקת הציור

# מקש חזרה לתפריט (M)
screen.onkeypress(go_back_to_menu, "m")

# הפעלה ראשונית של תפריט המשחק
show_menu()

# השארת החלון פתוח
screen.mainloop()