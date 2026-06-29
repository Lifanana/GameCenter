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

        # כפתור הגדרות
        self.settings_btn = ctk.CTkButton(
            self.menu_frame,
            text="Settings",
            font=("Arial", 16, "bold"),
            width=140,
            height=40,
            command=self.app_manager.show_settings  
        )
        self.settings_btn.pack(side="left", padx=10)

        # כפתור יציאה
        self.exit_btn = ctk.CTkButton(
            self.menu_frame,
            text="Exit",
            font=("Arial", 16, "bold"),
            fg_color="#A83232",
            hover_color="#822121",
            width=140,
            height=40,
            command=self.app_manager.confirm_exit
        )
        self.exit_btn.pack(side="left", padx=10)

        # --- 3. אזור רשימת המשחקים (מתחת לתפריט) ---
        
        self.games_container = ctk.CTkFrame(self, fg_color="transparent")
        self.games_container.pack(pady=30, padx=20, fill="both", expand=True)

        self.select_label = ctk.CTkLabel(
            self.games_container,
            text="Choose a game to play:",
            font=("Arial", 18, "bold"),
        )
        self.select_label.pack(pady=(0, 15))

        # Added "filename" to map each option to its actual script file
        games_list = [
            {"name": "🐍 Snake Game", "script": "Snake.py"},
            {"name": "🔢 2048", "script": "2048.py"},
            {"name": "❌ Tic Tac Toe", "script": "XO.py"},
            {"name": "🤔 Guess The Number", "script": "GuessNumber.py"},
            {"name": "🐢 Turtle Control", "script": "Turtle.py"}
        ]

        for game in games_list:
            # FIX: game=game passes the current loop state safely to the lambda function
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
        full_path = os.path.join("Games", script_name)
        
        if os.path.exists(full_path):
            try:
                # 1. מוצאים את החלון הראשי ביותר (ה-root של האפליקציה)
                root = self.winfo_toplevel()
                
                # 2. מחביאים את החלון הראשי
                root.withdraw()
                
                # 3. מריצים את המשחק ומחכים שהוא יסתיים (run במקום Popen)
                # שימו לב: זה יקפיא את תהליך הרקע של התפריט, וזה מצוין כי הוא מוחבא ממילא
                subprocess.run([sys.executable, full_path])
                
                # 4. ברגע שהמשחק נסגר (והשורה למעלה מסיימת), מחזירים את החלון הראשי
                root.deiconify()
                
            except Exception as e:
                print(f"Error launching {script_name}: {e}")
                # במקרה של שגיאה, נדאג שהחלון יחזור ולא ייעלם לתמיד
                self.winfo_toplevel().deiconify()
        else:
            print(f"Error: Could not find '{full_path}'.")