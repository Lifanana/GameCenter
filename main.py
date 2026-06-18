import customtkinter as ctk

app=ctk.CTk()
ctk.set_appearance_mode("dark")
app.title("Game Center")
app.geometry("1000*600")

#title
title=ctk.CTkLabel(
    app,
    text="Game Center",
    font=("Arial",30,"bold")
)
title.pack(pady=20)

#Frame Buttons
menu_frame=ctk.CTkFrame(app,width=200)
menu_frame.pack(side="left",fill="y",padx=10,pady=10)

#Buttons
home_btn=ctk.CTkButton(
    menu_frame,
    text="Home"
)
home_btn.pack(pady=10,padx=10)

games_btn=ctk.CTkButton(
    menu_frame,
    text="Games"
)
games_btn.pack(pady=10,padx=10)

exit_btn=ctk.CTkButton(
    menu_frame,
    text="Exit",
    command=app.destroy
)
exit_btn.pack(pady=10,padx=10)

app.mainloop()