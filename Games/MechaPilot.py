import math
import sys
import pygame

# אתחול Pygame
pygame.init()

# הגדרות חלון
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tracking Algorithm Simulator (Dummy Camera)")
clock = pygame.time.Clock()

# צבעים
BLACK = (15, 15, 15)
RED = (255, 60, 60)
GREEN = (0, 255, 120)
WHITE = (200, 200, 200)

# --- משתני הסימולציה ---

# 1. מיקום המטרה (Target)
target_pos = [200.0, 150.0]
target_angle = 0.0
target_speed = 0.03

# 2. מיקום הכוונת/המצלמה (Tracker)
tracker_pos = [400.0, 300.0]

# 3. הפרמטרים של אלגוריתם העקיבה
KP = 0.08  # מקדם הגבר העקיבה (Proportional Gain) - ככל שגבוה יותר העקיבה מהירה יותר
MAX_TRACKER_SPEED = 5.0  # מהירות מקסימלית של הכוונת


def update_target():
    """מעדכן את מיקום המטרה - תנועה מעגלית אוטומטית."""
    global target_angle
    target_angle += target_speed

    # תנועה במסלול שמונה (Lissajous curve) ליצירת אתגר עקיבה
    center_x, center_y = WIDTH / 2, HEIGHT / 2
    target_pos[0] = center_x + math.sin(target_angle) * 250
    target_pos[1] = center_y + math.sin(target_angle * 2) * 150


def track_target():
    """אלגוריתם העקיבה: מחשב שגיאה ומזיז את הכוונת אל המטרה."""
    # חישוב השגיאה (Error) - המרחק בצירים X ו-Y
    error_x = target_pos[0] - tracker_pos[0]
    error_y = target_pos[1] - tracker_pos[1]

    # חישוב התיקון הנדרש (Proportional Control)
    vel_x = error_x * KP
    vel_y = error_y * KP

    # הגבלת מהירות מקסימלית של הכוונת
    speed = math.hypot(vel_x, vel_y)
    if speed > MAX_TRACKER_SPEED:
        vel_x = (vel_x / speed) * MAX_TRACKER_SPEED
        vel_y = (vel_y / speed) * MAX_TRACKER_SPEED

    # עדכון מיקום הכוונת
    tracker_pos[0] += vel_x
    tracker_pos[1] += vel_y


# --- לולאת המשחק/הסימולציה ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. עדכון מנוע הסימולציה והאלגוריתם
    update_target()
    track_target()

    # 2. ציור על המסך
    screen.fill(BLACK)

    # ציור המטרה (עיגול אדום)
    pygame.draw.circle(
        screen, RED, (int(target_pos[0]), int(target_pos[1])), 12
    )

    # ציור הכוונת העוקבת (צלב ירוק)
    tx, ty = int(tracker_pos[0]), int(tracker_pos[1])
    pygame.draw.circle(screen, GREEN, (tx, ty), 18, 2)
    pygame.draw.line(screen, GREEN, (tx - 25, ty), (tx + 25, ty), 1)
    pygame.draw.line(screen, GREEN, (tx, ty - 25), (tx, ty + 25), 1)

    # ציור קו שגיאה (Vector) בין הכוונת למטרה
    pygame.draw.line(
        screen,
        WHITE,
        (tx, ty),
        (int(target_pos[0]), int(target_pos[1])),
        1,
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()