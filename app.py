from criptography import encrypt_password, decrypt_password
from random import choice, randint, shuffle
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from autocomplete import *
from tkinter import *
import pyperclip
import json
import sys
import os

class MainApp(ctk.CTkToplevel):

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.app = app
        self.geometry(f"600x550+{self.centra_toplevel()["x"]}+{self.centra_toplevel()["y"]}")
        self.title("Password Manager")
        self.config(padx=50, pady=20)

        self.canvas = ctk.CTkCanvas(self, width=200, height=200, highlightthickness=0, bg="#242424")
        self.logo_img = PhotoImage(file=self.resource_path("lock.png"))
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(row=0, column=1, pady=20)

        self.website_label = ctk.CTkLabel(self, text="Website:")
        self.website_label.grid(row=1, column=0)
        self.email_label = ctk.CTkLabel(self, text="Email/Username:", width=120)
        self.email_label.grid(row=2, column=0)
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=3, column=0)

        self.website_entry = ctk.CTkEntry(self, width=250)
        self.after(200, lambda: self.website_entry.focus_force())
        self.website_entry.bind("<Return>", lambda event: self.find_password())
        self.website_entry.bind("<FocusOut>", lambda e: self.check_focus(self.website_autocomplete))
        self.website_entry.bind("<KeyRelease>", lambda e: self.website_autocomplete.update_suggestions(e))
        self.website_entry.bind("<Down>", lambda e: self.website_autocomplete.move_focus(e))
        self.website_entry.bind("<Up>", lambda e: self.website_autocomplete.move_focus(e))
        self.website_entry.grid(row=1, column=1)
        self.website_entry.focus()

        self.email_entry = ctk.CTkEntry(self, width=382)
        self.email_entry.bind("<Return>", lambda event: self.find_password())
        self.email_entry.bind("<FocusOut>", lambda e: self.check_focus(self.email_autocomplete))
        self.email_entry.bind("<KeyRelease>", lambda e: self.email_autocomplete.update_suggestions(e))
        self.email_entry.bind("<Down>", lambda e: self.email_autocomplete.move_focus(e))
        self.email_entry.bind("<Up>", lambda e: self.email_autocomplete.move_focus(e))
        self.email_entry.grid(row=2, column=1, columnspan=2)

        self.password_entry = ctk.CTkEntry(self, width=250)
        self.password_entry.bind("<Return>", lambda event: self.save())
        self.password_entry.grid(row=3, column=1)

        self.website_autocomplete = Autocomplete(app=self, entry=self.website_entry, parent_entry=None)
        self.email_autocomplete = Autocomplete(app=self, entry=self.email_entry, parent_entry=self.website_entry)
        
        self.gen_pass_button = ctk.CTkButton(self, text="Generate Password", width=125, command=self.generate_password)
        self.gen_pass_button.grid(row=3, column=2, pady=4, padx=4)

        self.add_button = ctk.CTkButton(self, text="Add", width=385, command=self.save)
        self.add_button.grid(row=4, column=1, columnspan=2, pady=4)

        self.delete_button = ctk.CTkButton(self, text="Delete", width=385, command=self.delete)
        self.delete_button.grid(row=5, column=1, columnspan=2, pady=4)

        self.search_button = ctk.CTkButton(self, text="Search", width=125, command=self.find_password)
        self.search_button.grid(row=1, column=2, pady=4)

        self.protocol("WM_DELETE_WINDOW", app.destroy)

    def check_focus(self, autocomplete):
        str_focused = str(self.focus_get())
        if str_focused.startswith(str(autocomplete)):
            pass
        else:
            autocomplete.place_forget()

    def centra_toplevel(self, larghezza=600, altezza=550):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (larghezza // 2)
        y = (screen_height // 2) - (altezza // 2)

        return {"x": x, "y": y}

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        self.password_entry.delete(0, END)

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)

    def find_password(self):
        website = self.website_entry.get()
        email = self.email_entry.get().strip()
        if website == "" and email == "":
            return

        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            CTkMessagebox(
                title="Error",
                message="No Data File Found.",
                icon="cancel")
        else:
            if website in data["entries"]:
                tutte_le_email = data["entries"][website]["email"]
                if isinstance(tutte_le_email, list) and email == "":
                    messaggio = ""
                    for i in range(len(tutte_le_email)):
                        email = tutte_le_email[i]
                        password = decrypt_password(
                            self.app.aes_key,
                            {
                                "password": data["entries"][website]["password"][i],
                                "nonce": data["entries"][website]["nonce"][i],
                            })
                        
                        messaggio += f"Email: {email}\nPassword: {password}\n\n"
                    msg = CTkMessagebox(
                        title=website, 
                        message=messaggio,
                        icon="check",
                        option_1="Ok")
                    msg.grab_set() 
                    msg.after(10, lambda: msg.focus_force())
                    msg.bind("<Return>", lambda e: msg.button_1.invoke())
                    
                elif isinstance(tutte_le_email, list) and email in tutte_le_email:
                    pos = data["entries"][website]["email"].index(email)
                    password = decrypt_password(
                        self.app.aes_key,
                        {
                            "password": data["entries"][website]["password"][pos],
                            "nonce": data["entries"][website]["nonce"][pos],
                        })
                    
                    msg = CTkMessagebox(
                        title=website, 
                        message=f"Email: {email}\nPassword: {password}",
                        icon="check",
                        option_1="Ok")
                    msg.grab_set() 
                    msg.after(10, lambda: msg.focus_force())
                    msg.bind("<Return>", lambda e: msg.button_1.invoke())
                    pyperclip.copy(password)

                elif isinstance(tutte_le_email, list) and email not in tutte_le_email:
                    msg = CTkMessagebox(
                        title="Oops", 
                        message=f"{email} entry does not exists for {website}.",
                        icon="warning",
                        option_1="Ok")
                    msg.grab_set() 
                    msg.after(10, lambda: msg.focus_force())
                    msg.bind("<Return>", lambda e: msg.button_1.invoke())
                    
                else:
                    email = data["entries"][website]["email"]
                    password = decrypt_password(self.app.aes_key, data["entries"][website])

                    msg = CTkMessagebox(
                        title=website, 
                        message=f"Email: {email}\nPassword: {password}",
                        icon="check",
                        option_1="Ok")
                    msg.grab_set() 
                    msg.after(10, lambda: msg.focus_force())
                    msg.bind("<Return>", lambda e: msg.button_1.invoke())
                    pyperclip.copy(password)
            else:
                msg = CTkMessagebox(
                    title="Error", 
                    message=f"No details for {website} exists.",
                    icon="warning",
                    option_1="Ok")
                msg.grab_set() 
                msg.after(10, lambda: msg.focus_force())
                msg.bind("<Return>", lambda e: msg.button_1.invoke())
        finally:
            self.website_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.after(200, lambda: self.website_entry.focus_force())

    def save(self):
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if len(website) == 0 or len(password) == 0:
            CTkMessagebox(
                title="Oops",
                message="Please don't leave any fields empty!",
                icon="warning")
        else:

            encrypted_object = encrypt_password(self.app.aes_key, password)
            new_data = {
                website: {
                    "email": email,
                    "password": encrypted_object["password"],
                    "nonce": encrypted_object["nonce"]
                }
            }

            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                if website in data["entries"]:
                    #Sito presente
                    entrate = data["entries"][website]["email"]
                    pwd_entrate = data["entries"][website]["password"]
                    nonce = data["entries"][website]["nonce"]

                    if isinstance(entrate, list):
                        #C'è già la tupla
                        if email not in entrate:
                            msg = self.add_entry(website, email, password)

                            if msg.get() == "Cancel":
                                return
                            
                            data["entries"][website]["email"] += (email,)
                            data["entries"][website]["password"] += (encrypted_object["password"],)
                            data["entries"][website]["nonce"] += (encrypted_object["nonce"],)

                        else:
                            msg = self.overwrite_entry()
                            
                            if msg.get() == "Cancel":
                                return
                            elif msg.get() == "Overwrite":
                                pos = entrate.index(email)
                                data["entries"][website]["email"][pos] = email
                                data["entries"][website]["password"][pos] = encrypted_object["password"]
                                data["entries"][website]["nonce"][pos] = encrypted_object["nonce"]
                        
                        with open("data.json", mode="w") as data_file:
                            json.dump(data, data_file, indent=4)
                        
                        self.entry_saved()                        
                        return
                    else:
                        #Non c'è già la tupla
                        if email != entrate:
                            msg = self.add_entry()
                            if msg.get() == "Cancel":
                                return
                            
                            data["entries"][website]["email"] = (entrate,)
                            data["entries"][website]["password"] = (pwd_entrate,)
                            data["entries"][website]["nonce"] = (nonce,)

                            data["entries"][website]["email"] += (email,)
                            data["entries"][website]["password"] += (encrypted_object["password"],)
                            data["entries"][website]["nonce"] += (encrypted_object["nonce"],)

                            with open("data.json", mode="w") as data_file:
                                json.dump(data, data_file, indent=4)

                            self.entry_saved()
                            
                            self.website_entry.delete(0, END)
                            self.after(200, lambda: self.website_entry.focus_force())
                            self.email_entry.delete(0, END)
                            self.password_entry.delete(0, END)
                            return
                        else:
                            msg = self.overwrite_entry()
                            
                            if msg.get() == "Cancel":
                                return
                            elif msg.get() == "Overwrite":
                                data["entries"].update(new_data)
                                with open("data.json", mode="w") as data_file:
                                    json.dump(data, data_file, indent=4)
                                self.entry_saved()
                                return
                #Sito non presente
                msg = self.add_entry(website, email, password)

                if msg.get() == "Cancel":
                    return
                
                data["entries"].update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            
                self.entry_saved()
                return

    def delete(self):
        website = self.website_entry.get()
        email = self.email_entry.get()

        if len(website) == 0 and len(email) == 0:
            return
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            CTkMessagebox(
                title="Oops",
                message="File does not exist.",
                icon="warning"
            )
        else:
            if website not in data["entries"]:
                CTkMessagebox(
                    title="Oops",
                    message="Entry does not exist in the file.",
                    icon="warning"
                )
                self.website_entry.delete(0, END)
                self.email_entry.delete(0, END)
                return
            elif website in data["entries"] and len(email) == 0:
                self.remove_all_entries(data, website)
                return
            
            elif website in data["entries"]:
                entrate = data["entries"][website]["email"]

                if isinstance(entrate, list) and len(entrate) > 1:
                    self.remove_one_entry(data, entrate, email, website)
                else:
                    self.remove_all_entries(data, website)

    def entry_saved(self):
        CTkMessagebox(
            title="Saved",
            message="Entry successfully saved!",
            icon="check")
        self.website_entry.delete(0, END)
        self.after(200, lambda: self.website_entry.focus_force())
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def add_entry(self, website, email, password):
        msg = CTkMessagebox(
            title="Save",
            message="Are you sure you want to add the following entry?\n" \
            f"Website: {website}\nEmail: {email}\nPassword: {password}",
            icon="question",
            option_1="Ok",
            option_2="Cancel")
        msg.grab_set() 
        msg.after(10, lambda: msg.focus_force())
        msg.bind("<Return>", lambda e: msg.button_1.invoke())
        return msg
    
    def overwrite_entry(self):
        msg = CTkMessagebox(
            title="Oops",
            message="User already present for this Website.\nWhat do you want to do?",
            icon="warning", 
            option_1="Cancel", 
            option_2="Overwrite")
        msg.grab_set() 
        msg.after(10, lambda: msg.focus_force())
        msg.bind("<Return>", lambda e: msg.button_2.invoke())
        return msg
    
    def entry_removed(self):
        CTkMessagebox(
            title="Deleted",
            message="Entry successfully removed!",
            icon="check"
        )
        self.website_entry.delete(0, END)
        self.website_entry.focus_force()
        self.email_entry.delete(0, END)

    def remove_all_entries(self, data, website):
        msg = CTkMessagebox(
            title="Alert",
            message="Are you sure you want to remove all entries from the list?",
            option_1="No",
            option_2="Yes",
            icon="warning"
        )

        if msg.get() == "No":
            self.website_entry.delete(0, END)
            self.website_entry.focus_force()
            self.email_entry.delete(0, END)
            return
        else:
            del data["entries"][website]
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
            self.entry_removed()

    def remove_one_entry(self, data, entrate, email, website):
        msg = CTkMessagebox(
            title="Alert",
            message=f"Are you sure you want to remove\n{email}\n from {website} entries?",
            option_1="No",
            option_2="Yes",
            icon="warning"
        )
        if msg.get() == "No":
            self.website_entry.delete(0, END)
            self.website_entry.focus_force()
            self.email_entry.delete(0, END)
            return
        else:
            try:
                pos = entrate.index(email)
            except ValueError:
                CTkMessagebox(
                    title="Oops",
                    message="Entry does not exist in the file.",
                    icon="warning"
                )
                return
            else:
                data["entries"][website]["email"].pop(pos)
                data["entries"][website]["password"].pop(pos)
                data["entries"][website]["nonce"].pop(pos)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
                self.entry_removed()
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

        