import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    """פריים עמוד ההגדרות"""
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager

        # כותרת (בתוך הפריים הנוכחי)
        self.title_label = ctk.CTkLabel(
            self,
            text="Game Center - Settings",
            font=("Arial", 30, "bold")
        )
        self.title_label.pack(pady=20)

        # תפריט כפתורים צדי
        self.menu_frame = ctk.CTkFrame(self, width=200)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        # כפתור חזרה הביתה (משתמש ב-app_manager שקיבלנו)
        self.home_btn = ctk.CTkButton(
            self.menu_frame,
            text="Home",
            command=self.app_manager.show_main_menu
        )
        self.home_btn.pack(pady=10, padx=10)

        self.games_btn = ctk.CTkButton(
            self.menu_frame,
            text="Games"
        )
        self.games_btn.pack(pady=10, padx=10)

        # כפתור יציאה שסוגר את כל האפליקציה
        self.exit_btn = ctk.CTkButton(
            self.menu_frame,
            text="Exit",
            command=self.app_manager.destroy
        )
        self.exit_btn.pack(pady=10, padx=10)