
import customtkinter as ctk
from tkinter import PhotoImage
from login_functions import *
import sys
import os

class LoginApp(ctk.CTkToplevel):
    
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.title("Password Manager - Login")
        self.config(padx=25, pady=50)
        self.geometry(f"450x400+{self.centra_toplevel()["x"]}+{self.centra_toplevel()["y"]}")
        self.label_bottone_login = "Save" if app.stato == 0 else "Login"
        
        self.canvas = ctk.CTkCanvas(self, width=200, height=200, highlightthickness=0, bg="#242424")
        self.logo_img = PhotoImage(file=self.resource_path("lock.png"))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(row=0, column=1, pady=20)

        self.enter_pwd_label = ctk.CTkLabel(self, text="Enter Password:")
        self.enter_pwd_label.grid(row=1, column=0)

        self.login_pwd_entry = ctk.CTkEntry(self, width=200)
        self.login_pwd_entry.grid(row=1, column=1, padx=10)
        self.after(200, lambda: self.login_pwd_entry.focus_force())
        self.login_pwd_entry.bind("<Return>", lambda event: LoginFunctions.verify(app=app, win_login=self))

        self.verify_login_button = ctk.CTkButton(self, text=self.label_bottone_login, width=100, command=lambda: LoginFunctions.verify(app=app, win_login=self))
        self.verify_login_button.grid(row=1, column=3)

        self.protocol("WM_DELETE_WINDOW", app.destroy)

    def centra_toplevel(self, larghezza=600, altezza=550):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (larghezza // 2)
        y = (screen_height // 2) - (altezza // 2)

        return {"x": x, "y": y}
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

        