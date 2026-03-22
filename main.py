from tkinter import *
import customtkinter as ctk
from login_functions import *
from window_login import *
from app import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.logged = False
        self.stato = None #[0: First Time, 1: Login]
        self.aes_key = None
        self.withdraw()

        LoginFunctions.init(app=self)
        self.login_app = LoginApp(app=self)

    def login_success(self):
        self.logged = True
        self.login_app.destroy()
        MainApp(app=self)



if __name__ == "__main__":
    app = App()
    app.mainloop()