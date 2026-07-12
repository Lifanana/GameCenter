import subprocess
import sys
import os
import customtkinter as ctk

class GamesPage(ctk.CTkFrame):
    """פריים עמוד המשחקים"""
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager

        # 1. כותרת (בראש העמוד)
        self.title_label = ctk.CTkLabel(
            self,
            text="Game Center - Arcade Games",
            font=("Arial", 30, "bold"),
            text_color="#EDC22E"  # גוון זהב מעניין למשחקים
        )
        self.title_label.pack(pady=(20, 10))

        # 2. מסגרת לכפתורי הניווט העליוניים
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(pady=10)

        # כפתור בית
        self.home_btn = ctk.CTkButton(
            self.menu_frame,
            text="Home",
            font=("Arial", 16, "bold"),
            width=140,
            height=40,
            command=self.app_manager.show_main_menu
        )
        self.home_btn.pack(side="left", padx=10)

        # כפתור משחקים (עמוד נוכחי - צבע מודגש)
        self.games_btn = ctk.CTkButton(
            self.menu_frame,
            text="Games",
            font=("Arial", 16, "bold"),
            width=140,
            height=40,
            fg_color="#1F538D",  # גוון כחול כהה שמסמן "לשונית פעילה"
            hover_color="#14375E",
            command=lambda: None  # לא עושה כלום כי אנחנו כבר כאן
        )
        self.games_btn.pack(side="left", padx=10)

        # --- 3. אזור רשימת המשחקים (מתחת לתפריט) ---
        self.games_container = ctk.CTkFrame(self, fg_color="transparent")
        self.games_container.pack(pady=30, padx=20, fill="both", expand=True)

        self.select_label = ctk.CTkLabel(
            self.games_container,
            text="Choose a game to play:",
            font=("Arial", 18, "bold"),
        )
        self.select_label.pack(pady=(0, 15))

        # נתיבי המשחקים יחסית לתיקיית Games הראשי
        games_list = [
            {"name": "🐍 Snake Game", "script": "Snake.py"},
            {"name": "🔢 2048", "script": "2048.py"},
            {"name": "❌ Tic Tac Toe", "script": "XO.py"},
            {"name": "🤔 Guess The Number", "script": "GuessNumber.py"},
            {"name": "🐢 Turtle Control", "script": "Turtle.py"},
           {"name": "🏔 Icy Tower", "script": os.path.join("icytower1.3", "icytower13.exe")}
        ]

        for game in games_list:
            btn = ctk.CTkButton(
                self.games_container,
                text=game["name"],
                font=("Arial", 16, "bold"),
                width=300,
                height=45,
                fg_color="#2B2B2B",          
                hover_color="#3D3D3D",
                border_width=1,
                border_color="#555555",
                command=lambda g=game: self.launch_game(g["script"])
            )
            btn.pack(pady=8)  

    def launch_game(self, script_name):
        """מפעילה את המשחק, מחביאה את התפריט הראשי ומחזירה אותו כשהמשחק נסגר"""
        
        # 1. חישוב דינמי של תיקיית השורש (עובד גם בריצה רגילה וגם בתוך ה-exe)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # נתיב מלא לקובץ המשחק או ה-exe
        full_path = os.path.join(project_root, "Games", script_name)
        
        if os.path.exists(full_path):
            try:
                root = self.winfo_toplevel()
                root.withdraw()  # מחביאים את התפריט הראשי
                
                game_dir = os.path.dirname(full_path)
                
                # 2. בדיקה האם מדובר בקובץ הרצה חיצוני (exe) כמו Icy Tower
                if full_path.endswith(".exe"):
                    subprocess.run([full_path], cwd=game_dir)
                else:
                    # בדיקה האם האפליקציה רצה כקובץ קומפילציה (EXE של PyInstaller)
                    if hasattr(sys, '_MEIPASS'):
                        # בתוך ה-EXE, אין לנו מפרש פייתון חיצוני, לכן נריץ את קובץ ה-py 
                        # באמצעות פקודת המערכת הכללית של ווינדוס (cmd /c) שמפעילה קבצי פייתון
                        subprocess.run(["cmd", "/c", sys.executable, full_path], cwd=game_dir)
                    else:
                        # ריצה רגילה בזמן פיתוח ב-VS Code
                        subprocess.run([sys.executable, full_path], cwd=game_dir)
                
                # ברגע שהמשחק נסגר, מחזירים את החלון הראשי
                root.deiconify()
                
            except Exception as e:
                print(f"Error launching {script_name}: {e}")
                self.winfo_toplevel().deiconify()
        else:
            # במקום רק להדפיס, נקפיץ הודעה למסך כדי שתראה בדיוק איזה נתיב התוכנה חיפשה ולא מצאה
            from tkinter import messagebox
            messagebox.showerror("Error", f"הקובץ לא נמצא בנתיב המבוקש:\n{full_path}")
            self.winfo_toplevel().deiconify()