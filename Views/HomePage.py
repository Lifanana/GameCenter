import os
import sys
import subprocess
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import pygame

# הגדרת עיצוב כללי
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameCenterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GameCenter & Joystick Launcher")
        self.state("zoomed")  # מסך מלא בהפעלה
        
        # אתחול Pygame עבור הג'ויסטיק
        pygame.init()
        pygame.joystick.init()

        # תפיסת אירוע סגירת החלון
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        
        # בניית פריים עמוד הבית הראשי
        self.main_menu_frame = MainMenuFrame(master=self, app_manager=self)
        self.main_menu_frame.pack(fill="both", expand=True)

        # התחלת לולאת בדיקת סטטוס הג'ויסטיק בזמן אמת
        self.update_joystick_status()

    def update_joystick_status(self):
        """בדיקת חיבור/ניתוק של ג'ויסטיק בזמן אמת"""
        pygame.joystick.quit()
        pygame.joystick.init()

        count = pygame.joystick.get_count()

        if count > 0:
            js = pygame.joystick.Joystick(0)
            js.init()
            name = js.get_name()
            self.main_menu_frame.status_label.configure(
                text=f"🎮 Connected: {name}", 
                text_color="#4ade80"
            )
        else:
            self.main_menu_frame.status_label.configure(
                text="❌ No Joystick Detected", 
                text_color="#f87171"
            )

        self.after(1000, self.update_joystick_status)

    def confirm_exit(self):
        """אישור יציאה מהאפליקציה"""
        ans = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if ans: 
            self.destroy()
            pygame.quit()
            sys.exit()


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master)
        self.app_manager = app_manager
        
        # 1. אינדיקטור ג'ויסטיק (בצד ימין למעלה)
        self.status_label = ctk.CTkLabel(
            self, 
            text="Checking Joystick...", 
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            anchor="e"
        )
        self.status_label.pack(side="top", anchor="ne", padx=25, pady=(15, 0))

        # 2. כותרת ראשית של עמוד הבית
        self.title_label = ctk.CTkLabel(
            self, 
            text="Welcome to GameCenter!", 
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#EDC22E"
        )
        self.title_label.pack(pady=(10, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Choose a game to play:",
            font=ctk.CTkFont(family="Arial", size=18, weight="normal"),
        )
        self.subtitle_label.pack(pady=(0, 15))

        # 3. אזור נגלל ראשי למשחקים
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(expand=True, fill="both", padx=40, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        # נתיבים לתמונות
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  
        assets_dir = os.path.join(project_root, "Assets")

        # --- רשימת משחקים רגילים ---
        standard_games = [
            {"name": "🐍 Snake Game", "script": os.path.join("RegularGames", "Snake.py"), "img_name": "Snake.png"},
            {"name": "🔢 2048", "script": os.path.join("RegularGames", "2048.py"), "img_name": "2048.png"},
            {"name": "❌ Tic Tac Toe", "script": os.path.join("RegularGames", "XO.py"), "img_name": "XO.png"},
            {"name": "🤔 Guess Number", "script": os.path.join("RegularGames", "GuessNumber.py"), "img_name": "GuessNumber.png"},
            {"name": "🐢 Turtle Control", "script": os.path.join("RegularGames", "Turtle.py"), "img_name": "Turtle.png"},
            {"name": "🏔 Icy Tower", "script": os.path.join("icytower1.3", "icytower13.exe"), "img_name": "IcyTower.png"},
            {"name": "Maze", "script": os.path.join("RegularGames", "Maze.py"), "img_name": "Maze.png"},
            {"name": "⚽ Stanga", "script": os.path.join("RegularGames", "Stanga.py"), "img_name": "Stanga.png"},
            {"name": "🧱 DX Ball", "script": os.path.join("DX-Ball 2", "DXBall2.exe"), "img_name": "DXBall.png"},
            {"name": "🐦 Flabby Bird", "script": os.path.join("RegularGames", "FlabbyBird.py"), "img_name": "FlabbyBird.png"},
            {"name": "🧠 Simon Says", "script": os.path.join("RegularGames", "SimonSays.py"), "img_name": "SimonSays.png"},
            {"name": "🃏 Memory Game", "script": os.path.join("RegularGames", "MemoryGame.py"), "img_name": "MemoryGame.png"},
            {"name": "🪵 Hangman", "script": os.path.join("RegularGames", "Hangman.py"), "img_name": "Hangman.png"},
            {"name": "🟡 Pac-Man", "script": os.path.join("RegularGames", "PacMan.py"), "img_name": "PacMan.png"},
            {"name": "🏓 Ping Pong", "script": os.path.join("RegularGames", "PingPong.py"), "img_name": "PingPong.png"}
        ]

        # --- רשימת משחקי ג'ויסטיק ---
        joystick_games = [
            {"name": "✈️ Flight Simulator", "script": os.path.join("JoystickGames", "FlightSimulator.py"), "img_name": "FlightSimulator.png"},
            {"name": "💥 RoboticArm", "script": os.path.join("JoystickGames", "RoboticArm.py"), "img_name": "AlphaStrike.png"},
            {"name": "🌌 SpaceSimulator", "script": os.path.join("JoystickGames", "SpaceSimulator.py"), "img_name": "NebulaRacing.png"},
            {"name": "🌊 HoverCraft", "script": os.path.join("JoystickGames", "HoverCraft.py"), "img_name": "DeepSea.png"},
            {"name": "⚓ RacingCars", "script": os.path.join("JoystickGames", "RacingCars.py"), "img_name": "SubmarineHunt.png"},
            {"name": "🛡️ BalanceMaze", "script": os.path.join("JoystickGames", "BalanceMaze.py"), "img_name": "TurretDefense.png"},
            {"name": "🚀 MechaPilot", "script": os.path.join("JoystickGames", "MechaPilot.py"), "img_name": "MoonLander.png"},
            {"name": "🪂 Wingsuit Pro", "script": os.path.join("JoystickGames", ""), "img_name": "WingsuitPro.png"},
            {"name": "🕹️ Retro Arcade", "script": os.path.join("JoystickGames", ""), "img_name": "RetroArcade.png"},
            {"name": "🪐 Space Voyager", "script":os.path.join("JoystickGames", ""), "img_name": "SpaceVoyager.png"}
        ]

        # 4. רינדור משחקים רגילים
        current_row = 0
        current_row = self.render_game_section(
            games_list=standard_games, 
            assets_dir=assets_dir, 
            start_row=current_row
        )

        # 5. כותרת הפרדה למשחקי ג'ויסטיק
        section_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="🎮 Joystick Games",
            font=ctk.CTkFont(family="Arial", size=26, weight="bold"),
            text_color="#38bdf8"
        )
        section_label.grid(row=current_row, column=0, columnspan=2, pady=(30, 15), sticky="ew")
        current_row += 1

        # 6. רינדור משחקי ג'ויסטיק
        self.render_game_section(
            games_list=joystick_games, 
            assets_dir=assets_dir, 
            start_row=current_row
        )

        # 7. כפתור יציאה בתחתית
        self.btn_exit = ctk.CTkButton(
            self, 
            text="🚪 Exit Game Center", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            fg_color="#A83232",       
            hover_color="#822121",   
            width=220,
            height=45,
            corner_radius=10,
            command=self.app_manager.confirm_exit  
        )
        self.btn_exit.pack(pady=15)

    def render_game_section(self, games_list, assets_dir, start_row):
        """פונקציית עזר ליצירת כרטיסי המשחק ב-Grid"""
        for index, game in enumerate(games_list):
            row = start_row + (index // 2)
            col = index % 2

            game_card = ctk.CTkFrame(
                self.scrollable_frame, 
                fg_color="#1E1E1E", 
                corner_radius=12, 
                border_width=1, 
                border_color="#333333"
            )
            game_card.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

            game_card.grid_columnconfigure(0, weight=0)
            game_card.grid_columnconfigure(1, weight=1)

            # טעינת תמונה
            img_path = os.path.join(assets_dir, game.get("img_name", ""))
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(80, 80))
                    img_label = ctk.CTkLabel(game_card, image=ctk_img, text="")
                    img_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")
                except Exception:
                    self.show_fallback_img(game_card)
            else:
                self.show_fallback_img(game_card)

            # כפתור הפעלה
            play_btn = ctk.CTkButton(
                game_card,
                text=f"Play {game['name']}",
                font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
                height=45,
                fg_color="#2B2B2B",
                hover_color="#3D3D3D",
                border_width=1,
                border_color="#555555",
                command=lambda g=game: self.launch_game(g["script"])
            )
            play_btn.grid(row=0, column=1, padx=(0, 15), pady=12, sticky="ew")

        # מחזיר את השורה הבאה הפנויה ב-Grid
        return start_row + ((len(games_list) + 1) // 2)

    def show_fallback_img(self, parent_frame):
        fallback_label = ctk.CTkLabel(
            parent_frame, text="No Image", width=80, height=80, 
            fg_color="#2A2A2A", corner_radius=8, font=("Arial", 11)
        )
        fallback_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")

    def launch_game(self, script_name):
        """הפעלת המשחק והחזרת עמוד הבית עם סגירתו"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        full_path = os.path.join(project_root, "Games", script_name)
        
        if os.path.exists(full_path):
            try:
                root = self.winfo_toplevel()
                root.withdraw()
                
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