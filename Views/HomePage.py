import os
import sys
import subprocess
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# הגדרת עיצוב כללי
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameCenterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GameCenter")
        self.state("zoomed")  # מסך מלא בהפעלה
        
        # בניית פריים עמוד הבית הראשי
        self.main_menu_frame = MainMenuFrame(master=self, app_manager=self)
        self.main_menu_frame.pack(fill="both", expand=True)

    def confirm_exit(self):
        """שואל את המשתמש ומכבה את האפליקציה"""
        ans = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if ans: 
            self.destroy()


class MainMenuFrame(ctk.CTkFrame):
    """פריים עמוד הבית החדש שמכיל את המשחקים ב-2 עמודות"""
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager
        
        # 1. כותרת עמוד הבית
        self.title_label = ctk.CTkLabel(
            self, 
            text="Welcome to GameCenter!", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#EDC22E"  # צבע זהב חגיגי למשחקים
        )
        self.title_label.pack(pady=(30, 20))
        
        # 2. כותרת משנה
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Choose a game to play:",
            font=ctk.CTkFont(family="Arial", size=20, weight="normal"),
        )
        self.subtitle_label.pack(pady=(0, 20))

        # 3. מסגרת גריד מרכזית ל-2 עמודות
        self.grid_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both", padx=50, pady=10)
        
        # הגדרת 2 עמודות שוות משקל במרכז
        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)
        
        # חישוב נתיב תיקיית ה-Assets לתמונות
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  
        assets_dir = os.path.join(project_root, "Assets")

        # רשימת המשחקים: קובצי ריצה, שמות ותמונות תואמות
        games_list = [
            {"name": "🐍 Snake Game", "script": "Snake.py", "img_name": "Snake.png"},
            {"name": "🔢 2048", "script": "2048.py", "img_name": "2048.png"},
            {"name": "❌ Tic Tac Toe", "script": "XO.py", "img_name": "XO.png"},
            {"name": "🤔 Guess Number", "script": "GuessNumber.py", "img_name": "GuessNumber.png"},
            {"name": "🐢 Turtle Control", "script": "Turtle.py", "img_name": "Turtle.png"},
            {"name": "🏔 Icy Tower", "script": os.path.join("icytower1.3", "icytower13.exe"), "img_name": "IcyTower.png"},
            {"name": "Maze", "script": "Maze.py", "img_name": "Maze.png"},
            {"name": "Stanga", "script": "", "img_name": ""},
            {"name": "Maze", "script": "", "img_name": ""},
            {"name": "Maze", "script": "", "img_name": ""}
        ]

        # בניית ה-Grid ב-2 עמודות
        for index, game in enumerate(games_list):
            row = index // 2
            col = index % 2
            
            # פריים קטן לכל משחק שיחזיק את התמונה והכפתור צמודים
            game_card = ctk.CTkFrame(self.grid_frame, fg_color="#1E1E1E", corner_radius=12, border_width=1, border_color="#333333")
            game_card.grid(row=row, column=col, padx=25, pady=15, sticky="nsew")
            
            # עימוד פנימי בתוך כרטיס המשחק
            game_card.grid_columnconfigure(0, weight=0) # עבור התמונה
            game_card.grid_columnconfigure(1, weight=1) # עבור הכפתור שימתח
            
            # --- טעינת תמונת המשחק ---
            img_path = os.path.join(assets_dir, game["img_name"])
            try:
                pil_img = Image.open(img_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
                img_label = ctk.CTkLabel(game_card, image=ctk_img, text="")
                img_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
            except FileNotFoundError:
                # גיבוי במידה והתמונה לא קיימת בתיקייה
                fallback_label = ctk.CTkLabel(
                    game_card, text="No Image", width=100, height=100, 
                    fg_color="#2A2A2A", corner_radius=8, font=("Arial", 12)
                )
                fallback_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
            
            # --- כפתור הפעלת המשחק בצמוד לתמונה ---
            play_btn = ctk.CTkButton(
                game_card,
                text=f"Play {game['name']}",
                font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
                height=50,
                fg_color="#2B2B2B",
                hover_color="#3D3D3D",
                border_width=1,
                border_color="#555555",
                command=lambda g=game: self.launch_game(g["script"])
            )
            play_btn.grid(row=0, column=1, padx=(0, 20), pady=15, sticky="ew")

        # 4. מסגרת תחתונה לכפתור היציאה בלבד
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(pady=(20, 30))

        # כפתור Exit מעוצב
        self.btn_exit = ctk.CTkButton(
            self.buttons_frame, 
            text="🚪 Exit Game Center", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            fg_color="#A83232",       
            hover_color="#822121",   
            width=220,
            height=50,
            corner_radius=10,
            command=self.app_manager.confirm_exit  
        )
        self.btn_exit.pack()

    def launch_game(self, script_name):
        """פונקציה המפעילה את המשחק ומחזירה את עמוד הבית עם סגירתו"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # נתיב מלא לקובץ המשחק בתיקיית Games
        full_path = os.path.join(project_root, "Games", script_name)
        
        if os.path.exists(full_path):
            try:
                root = self.winfo_toplevel()
                root.withdraw()  # החבאת עמוד הבית בזמן המשחק
                
                game_dir = os.path.dirname(full_path)
                
                if full_path.endswith(".exe"):
                    subprocess.run([full_path], cwd=game_dir)
                else:
                    if hasattr(sys, '_MEIPASS'):
                        exe_dir = os.path.dirname(sys.executable)
                        internal_python = os.path.join(exe_dir, "python.exe")
                        
                        if os.path.exists(internal_python):
                            subprocess.run([internal_python, full_path], cwd=game_dir)
                        else:
                            subprocess.run(["python", full_path], cwd=game_dir)
                    else:
                        subprocess.run([sys.executable, full_path], cwd=game_dir)
                
                # החזרת חלון עמוד הבית לפעילות ברגע שהמשחק נסגר
                root.deiconify()
                
            except Exception as e:
                messagebox.showerror("Error", f"שגיאה בהפעלת המשחק:\n{e}")
                self.winfo_toplevel().deiconify()
        else:
            messagebox.showerror("Error", f"הקובץ לא נמצא בנתיב המבוקש:\n{full_path}")
            self.winfo_toplevel().deiconify()


if __name__ == "__main__":
    app = GameCenterApp()
    app.mainloop()