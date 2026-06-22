import pygame
import random
import sys

# אתחול pygame
pygame.init()

# הגדרת קבועים
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20  # גודל של כל ריבוע במשחק (הנחש והאוכל)

# צבעים (RGB)
COLOR_BACKGROUND = (40, 42, 54)   # דרקולה כהה
COLOR_SNAKE_HEAD = (80, 250, 123)  # ירוק בהיר
COLOR_SNAKE_BODY = (64, 210, 100)  # ירוק כהה יותר
COLOR_FOOD = (255, 85, 85)         # אדום
COLOR_TEXT = (248, 248, 242)       # לבן-אפרפר

# הגדרת המסך והשעון
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("GameCenter - Snake Game")
clock = pygame.time.Clock()


def generate_food(snake):
    """מייצר מיקום חדש לאוכל שלא נמצא על הנחש"""
    while True:
        x = random.randint(0, (WINDOW_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (WINDOW_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake:
            return x, y


def main():
    # מיקום התחלתי של הנחש (רשימת קואורדינטות)
    snake = [
        (100, 100),  # ראש
        (80, 100),   # גוף
        (60, 100)    # זנב
    ]

    # כיוון תנועה התחלתי (ימינה)
    # קואורדינטות התנועה: (x, y)
    direction = (GRID_SIZE, 0)

    # יצירת האוכל הראשון
    food = generate_food(snake)

    score = 0
    game_over = False

    # לולאת המשחק הראשית
    while not game_over:
        
        # 1. טיפול באירועים (קלט מהמשתמש)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                # שינוי כיוון, תוך מניעה מהנחש לחזור ישירות אחורה לתוך עצמו
                if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                    direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                    direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                    direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                    direction = (GRID_SIZE, 0)

        # 2. עדכון מיקום הנחש
        # חישוב המיקום החדש של הראש
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # בדיקת התנגשות בקירות
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
            game_over = True
            continue

        # בדיקת התנגשות בגוף של עצמו
        if new_head in snake:
            game_over = True
            continue

        # הוספת הראש החדש לפנים
        snake.insert(0, new_head)

        # בדיקה אם הנחש אכל את האוכל
        if new_head == food:
            score += 1
            food = generate_food(snake)
        else:
            # אם הוא לא אכל, מוחקים את האיבר האחרון כדי לשמור על האורך
            snake.pop()

        # 3. ציור על המסך
        screen.fill(COLOR_BACKGROUND)

        # ציור האוכל
        pygame.draw.rect(screen, COLOR_FOOD, pygame.Rect(food[0], food[1], GRID_SIZE, GRID_SIZE))

        # ציור הנחש
        for i, segment in enumerate(snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2))

        # הצגת הניקוד
        font = pygame.font.SysFont("arial", 24)
        score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_text, (10, 10))

        # עדכון המסך
        pygame.display.flip()

        # הגדרת מהירות המשחק (Frames Per Second) - ככל שהמספר גבוה, הנחש מהיר יותר
        clock.tick(10)

    # מסך Game Over קצר
    print(f"Game Over! Your final score is: {score}")
    pygame.quit()


if __name__ == "__main__":
    main()