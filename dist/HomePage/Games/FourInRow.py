import customtkinter as ctk
from tkinter import messagebox
import random

# הגדרת עיצוב כללי
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FourInRowGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Four In A Row - ארבע בשורה")
        self.geometry("650x700")
        
        # הגדרות לוח המשחק (6 שורות, 7 עמודות)
        self.ROWS = 6
        self.COLS = 7
        self.board = []
        self.current_player = 1  # 1 = אדום, 2 = צהוב (שחקן 2 או רובוט)
        self.is_vs_robot = False
        
        # טעינת מסך בחירת המצב (שחקן נגד שחקן או נגד רובוט) בהתחלה
        self.show_mode_selection()

    def show_mode_selection(self):
        """מסך בחירת מצב משחק (PVP או נגד רובוט)"""
        # ניקוי ווידג'טים קודמים אם קיימים
        for widget in self.winfo_children():
            widget.destroy()

        # כותרת עיקרית
        self.title_label = ctk.CTkLabel(
            self, text="🔵 Four In A Row 🔴", font=("Arial", 36, "bold")
        )
        self.title_label.pack(pady=(80, 40))

        self.subtitle_label = ctk.CTkLabel(
            self, text="בחר מצב משחק / Select Game Mode:", font=("Arial", 20)
        )
        self.subtitle_label.pack(pady=10)

        # כפתור שחקן נגד שחקן
        self.btn_pvp = ctk.CTkButton(
            self,
            text="👥 Player vs Player",
            font=("Arial", 18, "bold"),
            width=280,
            height=55,
            corner_radius=10,
            command=lambda: self.start_game(vs_robot=False)
        )
        self.btn_pvp.pack(pady=15)

        # כפתור שחקן נגד רובוט
        self.btn_pve = ctk.CTkButton(
            self,
            text="🤖 Player vs Robot",
            font=("Arial", 18, "bold"),
            width=280,
            height=55,
            corner_radius=10,
            command=lambda: self.start_game(vs_robot=True)
        )
        self.btn_pve.pack(pady=15)

        # כפתור סגירה
        self.btn_close = ctk.CTkButton(
            self,
            text="🚪 Exit Game",
            font=("Arial", 14),
            fg_color="#A83232",
            hover_color="#822121",
            width=150,
            height=40,
            command=self.destroy
        )
        self.btn_close.pack(pady=(60, 10))

    def start_game(self, vs_robot):
        """איפוס המטריצה והצגת לוח המשחק האקטיבי"""
        self.is_vs_robot = vs_robot
        self.current_player = 1
        
        # יצירת לוח וירטואלי ריק (0 מסמל תא ריק)
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # ניקוי המסך
        for widget in self.winfo_children():
            widget.destroy()

        # אינדיקטור תור נוכחי
        self.turn_label = ctk.CTkLabel(
            self, text="🔴 Player 1's Turn (Red) 🔴", font=("Arial", 22, "bold"), text_color="#FF4444"
        )
        self.turn_label.pack(pady=15)

        # מסגרת לרשת הכפתורים (הלוח הכחול המסורתי)
        self.grid_frame = ctk.CTkFrame(self, fg_color="#1E1E2E", padding=15, corner_radius=15)
        self.grid_frame.pack(pady=10)

        # יצירת כפתורי הלוח כעיגולים
        self.buttons_grid = []
        for r in range(self.ROWS):
            row_buttons = []
            for c in range(self.COLS):
                btn = ctk.CTkButton(
                    self.grid_frame,
                    text="",
                    width=50,
                    height=50,
                    corner_radius=25,  # הופך את הכפתור לעיגול מושלם
                    fg_color="#333344",  # צבע חור ריק
                    hover_color="#444455",
                    command=lambda col=c: self.make_move(col)
                )
                btn.grid(row=r, column=c, padx=8, pady=8)
                row_buttons.append(btn)
            self.buttons_grid.append(row_buttons)

        # כפתור כניעה / חזרה לבחירה
        self.btn_reset = ctk.CTkButton(
            self, text="🏳️ Surrender / Reset", font=("Arial", 14), fg_color="#A83232", hover_color="#822121",
            command=self.show_mode_selection
        )
        self.btn_reset.pack(pady=20)

    def make_move(self, col):
        """ביצוע מהלך בעמודה שנבחרה"""
        # מציאת השורה הפנויה התחתונה ביותר בעמודה הזו (חוקי כוח המשיכה של המשחק)
        for r in reversed(range(self.ROWS)):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                
                # צביעת העיגול בלוח בהתאם לשחקן
                color = "#FF4444" if self.current_player == 1 else "#FFCC00"
                self.buttons_grid[r][col].configure(fg_color=color, hover_color=color)
                
                # בדיקת ניצחון
                if self.check_winner(r, col):
                    p_name = "Player 1 (Red)" if self.current_player == 1 else ("Robot" if self.is_vs_robot else "Player 2 (Yellow)")
                    messagebox.showinfo("Game Over", f"🎉 {p_name} Wins!")
                    self.show_mode_selection()
                    return
                
                # בדיקת תיקו (אם השורה העליונה מלאה לחלוטין)
                if all(self.board[0][c] != 0 for c in range(self.COLS)):
                    messagebox.showinfo("Game Over", "🤝 It's a Tie!")
                    self.show_mode_selection()
                    return

                # החלפת תורות
                self.current_player = 2 if self.current_player == 1 else 1
                self.update_turn_label()

                # אם נבחר מצב רובוט והתור שלו - הפעלת הרובוט בעיכוב קל לחוויית משחק טבעית
                if self.is_vs_robot and self.current_player == 2:
                    self.after(500, self.robot_move)
                return
                
        # התראה אם העמודה כבר מלאה עד הסוף
        messagebox.showwarning("Invalid Move", "העמודה הזו מלאה! בחר עמודה אחרת.")

    def robot_move(self):
        """בינה מלאכותית בסיסית: מחפשת ניצחון, חוסמת הפסד, או בוחרת אקראית"""
        valid_cols = [c for c in range(self.COLS) if self.board[0][c] == 0]
        if not valid_cols:
            return

        # 1. בדיקה: האם הרובוט יכול לנצח כבר עכשיו?
        for c in valid_cols:
            for r in reversed(range(self.ROWS)):
                if self.board[r][c] == 0:
                    self.board[r][c] = 2
                    if self.check_winner(r, c):
                        self.board[r][c] = 0
                        self.make_move(c)
                        return
                    self.board[r][c] = 0
                    break

        # 2. בדיקה: האם צריך לחסום את השחקן האנושי מניצחון בטוח?
        for c in valid_cols:
            for r in reversed(range(self.ROWS)):
                if self.board[r][c] == 0:
                    self.board[r][c] = 1
                    if self.check_winner(r, c):
                        self.board[r][c] = 0
                        self.make_move(c)
                        return
                    self.board[r][c] = 0
                    break

        # 3. אם אין מהלך קריטי - בחירה אקראית מעמודה פנויה
        chosen_col = random.choice(valid_cols)
        self.make_move(chosen_col)

    def update_turn_label(self):
        """עדכון ויזואלי של טקסט התור בראש המסך"""
        if self.current_player == 1:
            self.turn_label.configure(text="🔴 Player 1's Turn (Red) 🔴", text_color="#FF4444")
        else:
            if self.is_vs_robot:
                self.turn_label.configure(text="🤖 Robot is thinking... 🤖", text_color="#FFCC00")
            else:
                self.turn_label.configure(text="🟡 Player 2's Turn (Yellow) 🟡", text_color="#FFCC00")

    def check_winner(self, row, col):
        """סריקת 4 כיוונים לבדיקת רצף של 4 דיסקיות מאותו צבע"""
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # אופקי, אנכי, אלכסון חיובי, אלכסון שלילי

        for dr, dc in directions:
            count = 1
            # סריקה קדימה בכיוון הוקטור
            r, c = row + dr, col + dc
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # סריקה אחורה בכיוון ההפוך לוקטור
            r, c = row - dr, col - dc
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
                
            if count >= 4:
                return True
        return False

if __name__ == "__main__":
    app = FourInRowGame()
    app.mainloop()