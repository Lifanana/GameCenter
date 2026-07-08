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
        self.geometry("950x700")
        
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
        """מעבר לעמוד הגדרות"""
        self.hide_all_frames()
        self.settings_frame.pack(fill="both", expand=True)  # מציג את ההגדרות

    def show_games(self):
        """מעבר לעמוד המשחקים"""
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
        self.title_label.pack(pady=(20, 10))
        
        # 2. יצירת מסגרת פנימית לכל האלמנטים הגרפיים (רצועות משחקים + חתולים)
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=10, pady=10)
        
        # הגדרת חלוקת המשקל של העמודות
        self.grid_frame.grid_columnconfigure(0, weight=0) 
        self.grid_frame.grid_columnconfigure(1, weight=1) 
        self.grid_frame.grid_columnconfigure(2, weight=1) 
        self.grid_frame.grid_columnconfigure(3, weight=1) 
        self.grid_frame.grid_columnconfigure(4, weight=0) 
        
        # --- חישוב הנתיב לתיקיית Assets ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  
        assets_dir = os.path.join(project_root, "Assets")
        
        # ==========================================
        # א. טור שמאל - רצועת 2048 (מוצמדת לשמאל, ונמתחת אנכית)
        # ==========================================
        left_path = os.path.join(assets_dir, "Row1.png")
        try:
            pil_img_left = Image.open(left_path)
            # הגדלנו את הגובה ל-480 כדי למלא את הפער
            ctk_img_left = ctk.CTkImage(light_image=pil_img_left, dark_image=pil_img_left, size=(130, 480))
            left_label = ctk.CTkLabel(self.grid_frame, image=ctk_img_left, text="")
            # sticky="wns" מצמיד לשמאל (w) ומוערך מלמעלה למטה (ns)
            left_label.grid(row=0, column=0, rowspan=2, sticky="wns", padx=(0, 10), pady=0)
        except FileNotFoundError:
            fallback_left = ctk.CTkLabel(
                self.grid_frame, text="[Row1.png\nלא נמצא]", 
                width=130, height=480, fg_color="#333333", corner_radius=10
            )
            fallback_left.grid(row=0, column=0, rowspan=2, sticky="wns", padx=(0, 10), pady=0)

        # ==========================================
        # ב. מרכז - ששת החתולים (עמודות 1, 2, 3)
        # ==========================================
        cat_images = ["Cat1.png", "Cat2.png", "Cat3.png", "Cat4.png", "Cat5.png", "Cat6.png"]
        
        for index, img_name in enumerate(cat_images):
            row = index // 3  
            col = (index % 3) + 1  
            
            full_img_path = os.path.join(assets_dir, img_name)
            
            try:
                pil_img = Image.open(full_img_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(140, 140))
                
                img_label = ctk.CTkLabel(self.grid_frame, image=ctk_img, text="")
                img_label.grid(row=row, column=col, padx=10, pady=25) # הגדלנו מעט את ה-pady כדי להתאים לגובה החדש של הרצועות
            except FileNotFoundError:
                fallback_label = ctk.CTkLabel(
                    self.grid_frame, 
                    text=f"[חתול {index+1}\nלא נמצא]", 
                    width=140, 
                    height=140, 
                    fg_color="#333333",
                    corner_radius=10,
                    font=ctk.CTkFont(family="Arial", size=11)
                )
                fallback_label.grid(row=row, column=col, padx=10, pady=25)

        # ==========================================
        # ג. טור ימין - רצועת האיש התלוי (מוצמדת לימין, ונמתחת אנכית)
        # ==========================================
        right_path = os.path.join(assets_dir, "Row2.png")
        try:
            pil_img_right = Image.open(right_path)
            # הגדלנו את הגובה ל-480
            ctk_img_right = ctk.CTkImage(light_image=pil_img_right, dark_image=pil_img_right, size=(130, 480))
            right_label = ctk.CTkLabel(self.grid_frame, image=ctk_img_right, text="")
            # sticky="ens" מצמיד לימין (e) ומוערך מלמעלה למטה (ns)
            right_label.grid(row=0, column=4, rowspan=2, sticky="ens", padx=(10, 0), pady=0)
        except FileNotFoundError:
            fallback_right = ctk.CTkLabel(
                self.grid_frame, text="[Row2.png\nלא נמצא]", 
                width=130, height=480, fg_color="#333333", corner_radius=10
            )
            fallback_right.grid(row=0, column=4, rowspan=2, sticky="ens", padx=(10, 0), pady=0)
        
        # 3. יצירת מסגרת תחתונה לכפתורים
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(pady=(20, 10))

        # כפתור Settings
        self.btn_settings = ctk.CTkButton(
            self.buttons_frame, 
            text="⚙️ Settings", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            width=160,
            height=45,
            corner_radius=8,
            command=self.app_manager.show_settings
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