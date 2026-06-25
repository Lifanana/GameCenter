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

        games_list = [
            {"name": "🐍 Snake Game", "command": lambda: self.launch_game("snake")},
            {"name": "🔢 2048", "command": lambda: self.launch_game("2048")},
            {"name": "❌ Tic Tac Toe", "command": lambda: self.launch_game("tictactoe")},
            {"name": "🤔 Guess The Number", "command": lambda: self.launch_game("guess")},
            {"name": "🐢 Turtle Control", "command": lambda: self.launch_game("turtle")}
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
                command=game["command"]
            )
            btn.pack(pady=8)  

    def launch_game(self, game_key):
        """מפעילה את פונקציות הרצת המשחקים דרך ה-manager"""
        print(f"Launching {game_key}...")
        if hasattr(self.app_manager, f"start_{game_key}"):
            getattr(self.app_manager, f"start_{game_key}")()