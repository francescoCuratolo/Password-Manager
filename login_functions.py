from criptography import generate_master_password, derive_key
from CTkMessagebox import CTkMessagebox
import json
import base64
from tkinter import *

class LoginFunctions():
    def init(app, filename="data.json"):

        try:
            with open(filename, mode="r") as f:
                data_json = json.load(f)
                
        except FileNotFoundError:
                app.stato = 0
                msg = CTkMessagebox(
                    title="First Time",
                    message="Inserisci una Master Password",
                    icon="warning",
                    option_1="Ok")
                msg.grab_set() 
                msg.focus_force()
                msg.bind("<Return>", lambda e: msg.button_1.invoke())

        else:
            if "master" in data_json:
                app.stato = 1

    def verify(app, win_login, filename="data.json", event=None):

        pwd = win_login.login_pwd_entry.get().strip()

        if len(pwd) == 0 and app.stato == 0:
            CTkMessagebox(
                title="Info",
                message="Questo campo non può essere vuoto!",
                icon="warning")
            
        elif len(pwd) < 5 and app.stato == 0:
            CTkMessagebox(
                title="Info",
                message="La password deve essere lunga almeno 5 caratteri!",
                icon="warning")
            win_login.login_pwd_entry.delete(0, END)

        else:
            match app.stato:

                case 0:
                    LoginFunctions.setup_master_password(win_login=win_login, master_password=pwd, app=app)

                    win_login.login_pwd_entry.delete(0, END)

                case 1:
                    with open(filename, mode="r") as f:
                        data_json = json.load(f)
        
                    salt = base64.b64decode(data_json["master"]["salt"])
                    stored_hash = base64.b64decode(data_json["master"]["hash"])

                    derived = derive_key(pwd, salt)
        
                    if derived != stored_hash:
                        CTkMessagebox(
                            title="Errore",
                            message="Password sbagliata, riprova",
                            icon="cancel")
                        win_login.login_pwd_entry.delete(0, END)
                    else:
                        app.aes_key = derived
                        win_login.login_pwd_entry.delete(0, END)
                        app.login_success()

    def setup_master_password(win_login, master_password: str, app, filename="data.json"):

        data = generate_master_password(master_password)
        app.stato = 1
        win_login.verify_login_button.configure(text="Login")

        with open(filename, mode="w") as f:
            data.update({"entries": {}})
            json.dump(data, f, indent=4)
        
        CTkMessagebox(
            title="Saved",
            message="Password memorizzata con successo!",
            icon="check")

