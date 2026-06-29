import customtkinter as ctk
from PIL import Image
import os
from Games import GamesPage
from tkinter import messagebox  # ייבוא תיבת ההודעות של tkinter לטובת שאלת האישור
# ייבוא עמוד ההגדרות מהקובץ השני
from Settings import SettingsPage

# הגדרת עיצוב כללי
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameCenterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GameCenter")
        self.geometry("650x650")
        
        # בניית העמודים (פריימים) בתוך אותו החלון
        self.main_menu_frame = MainMenuFrame(master=self, app_manager=self)
        self.settings_frame = SettingsPage(master=self, app_manager=self)
        self.games_frame = GamesPage(master=self, app_manager=self)

        # הצגת עמוד הבית בהתחלה
        self.show_main_menu()

    def hide_all_frames(self):
        """פונקציית עזר פרטית שמסתירה את כל הפריימים לפני שמציגים פריים חדש"""
        self.main_menu_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.games_frame.pack_forget()

    def show_main_menu(self):
        """מעבר לעמוד הראשי"""
        self.hide_all_frames()
        self.main_menu_frame.pack(fill="both", expand=True)  # מציג את עמוד הבית 

    def show_settings(self):
        """מעבר לעמוד ההגדרות"""
        self.hide_all_frames()
        self.settings_frame.pack(fill="both", expand=True)  # מציג את ההגדרות

    def show_games(self):
        """מעבר לעמוד המשחקים (פותר את ה-AttributeError)"""
        self.hide_all_frames()
        self.games_frame.pack(fill="both", expand=True)  # מציג את עמוד המשחקים

    def confirm_exit(self):
        """פונקציה ששואלת את המשתמש אם הוא בטוח וסוגרת את האפליקציה"""
        ans = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if ans: 
            self.destroy()


class MainMenuFrame(ctk.CTkFrame):
    """פריים עמוד הבית"""
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager
        
        # 1. כותרת עליונה
        self.title_label = ctk.CTkLabel(
            self, 
            text="Welcome to GameCenter!", 
            font=ctk.CTkFont(family="Arial", size=32, weight="bold")
        )
        self.title_label.pack(pady=(30, 20))
        
        # 2. יצירת מסגרת פנימית לשישיית התמונות (Grid)
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=10)
        
        # --- חישוב הנתיב לתיקיית Assets ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  
        assets_dir = os.path.join(project_root, "Assets")
        
        # רשימת שמות קבצי החתולים
        cat_images = ["Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png", "Cat5.png", "Cat6.png"]
        
        # טעינת התמונות והצגתן במבנה של 2 שורות ו-3 עמודות
        for index, img_name in enumerate(cat_images):
            row = index // 3  
            col = index % 3   
            
            full_img_path = os.path.join(assets_dir, img_name)
            
            try:
                pil_img = Image.open(full_img_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(150, 150))
                
                img_label = ctk.CTkLabel(self.grid_frame, image=ctk_img, text="")
                img_label.grid(row=row, column=col, padx=15, pady=15)
            except FileNotFoundError:
                fallback_label = ctk.CTkLabel(
                    self.grid_frame, 
                    text=f"[חתול {index+1}\nלא נמצא ב-Assets]", 
                    width=150, 
                    height=150, 
                    fg_color="#333333",
                    corner_radius=10,
                    font=ctk.CTkFont(family="Arial", size=11)
                )
                fallback_label.grid(row=row, column=col, padx=15, pady=15)
        
        # 3. יצירת מסגרת תחתונה לכפתורים
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(pady=(30, 20))

        # כפתור Settings
        self.btn_settings = ctk.CTkButton(
            self.buttons_frame, 
            text="⚙️ Settings", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            width=160,
            height=45,
            corner_radius=8,
            command=self.app_manager.show_games
        )
        self.btn_settings.pack(side="left", padx=10)

        # כפתור Exit
        self.btn_exit = ctk.CTkButton(
            self.buttons_frame, 
            text="🚪 Exit", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            fg_color="#A83232",       
            hover_color="#822121",   
            width=160,
            height=45,
            corner_radius=8,
            command=self.app_manager.confirm_exit  
        )
        self.btn_exit.pack(side="left", padx=10)


if __name__ == "__main__":
    app = GameCenterApp()
    app.mainloop()