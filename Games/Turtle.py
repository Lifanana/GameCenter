import turtle

# 1. הגדרת מסך המשחק
screen = turtle.Screen()
screen.title("GameCenter - Turtle Control")
screen.bgcolor("white")  # צבע רקע

# 2. יצירת הצב (השחקן)
player = turtle.Turtle()
player.shape("turtle")  # משנה את הצורה מחץ לצב קלאסי
player.color("blue")    # צבע התחלתי
player.pensize(3)       # עובי הקו שהצב מצייר
player.speed(0)         # מהירות האנימציה (הכי מהיר)

# 3. פונקציות תנועה והיגוי
def move_forward():
    player.forward(20)  # זז קדימה 20 פיקסלים

def move_backward():
    player.backward(20)  # זז אחורה 20 פיקסלים

def turn_left():
    player.left(15)  # מסובב את החץ/צב 15 מעלות שמאלה

def turn_right():
    player.right(15)  # מסובב את החץ/צב 15 מעלות ימינה

# 4. פונקציות בונוס לשליטה במשחק
def change_color_red():
    player.color("red")

def change_color_green():
    player.color("green")

def change_color_blue():
    player.color("blue")

def clear_screen():
    player.clear()  # מוחק את כל הציורים שהצב עשה עד עכשיו

# 5. הגדרת ההקשבה למקלדת (Key Binding)
screen.listen()  # אומר למסך להתחיל להקשיב ללחיצות

# קישור מקשי החיצים לפונקציות התנועה
screen.onkeypress(move_forward, "Up")      # חץ למעלה - זז קדימה
screen.onkeypress(move_backward, "Down")  # חץ למטה - זז אחורה
screen.onkeypress(turn_left, "Left")       # חץ שמאלה - מסתובב שמאלה
screen.onkeypress(turn_right, "Right")     # חץ ימינה - מסתובב ימינה

# קישור מקשים נוספים לשינוי צבע וניקוי
screen.onkeypress(change_color_red, "r")   # מקש R - צבע אדום
screen.onkeypress(change_color_green, "g") # מקש G - צבע ירוק
screen.onkeypress(change_color_blue, "b")  # מקש B - צבע כחול
screen.onkeypress(clear_screen, "c")       # מקש C - מחיקת הציור

# השארת החלון פתוח
screen.mainloop()