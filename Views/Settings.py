import customtkinter as ctk
from Games import GamesPage

class SettingsPage(ctk.CTkFrame):
    """פריים עמוד ההגדרות"""
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager

        # 1. כותרת (בראש העמוד)
        self.title_label = ctk.CTkLabel(
            self,
            text="Game Center - Settings",
            font=("Arial", 30, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # 2. מסגרת לכפתורים - ממוקמת מתחת לכותרת (בלי side="left" לפריים עצמו)
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(pady=10)

        # 3. הכפתורים - כולם עם side="left" כדי שיוצגו אחד ליד השני בתוך המסגרת
        self.home_btn = ctk.CTkButton(
            self.menu_frame,
            text="Home",
            font=("Arial", 16, "bold"),
            width=140,
            height=40,
            command=self.app_manager.show_main_menu
        )
        self.home_btn.pack(side="left", padx=10)

        self.games_btn = ctk.CTkButton(
            self.menu_frame,
            text="Games",
            font=("Arial", 16, "bold"),
            width=140,
            height=40,
            command=self.app_manager.show_games
        )
        self.games_btn.pack(side="left", padx=10)

        self.exit_btn = ctk.CTkButton(
            self.menu_frame,
            text="Exit",
            font=("Arial", 16, "bold"),
            fg_color="#A83232",       # צבע אדום תואם ליציאה
            hover_color="#822121",
            width=140,
            height=40,
            command=self.app_manager.confirm_exit  # משתמש בפונקציית האישור עם השאלה שיצרנו ב-HomePage
        )
        self.exit_btn.pack(side="left", padx=10)