import customtkinter as ctk
import json

class Autocomplete(ctk.CTkScrollableFrame):

    def __init__(self, app, entry, parent_entry, *args, **kwargs):
        super().__init__(app, **kwargs)
        
        self.app = app
        self.entry = entry
        self.parent_entry = parent_entry
        self.position = -1
        self.sfondo_bottoni = None
        self.bordo_bottoni = None
        self.suggestions = None

    def get_siti(self):
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                siti = list(data["entries"].keys())
                return siti
        except FileNotFoundError:
            return
    
    def get_emails(self):
        sito = self.parent_entry.get()
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                
                if sito in data["entries"].keys():
                    emails = data["entries"][sito]["email"]
                    return emails
                else:
                    return []
        except FileNotFoundError:
            return
    
    def update_suggestions(self, event):
 
        if self.parent_entry == None:
            self.suggestions = self.get_siti()
        else:
            self.suggestions = self.get_emails()
        
        if not isinstance(self.suggestions, list):
            self.suggestions = [self.suggestions]
    
        typed = self.entry.get().lower()

        for widget in self.winfo_children():
            widget.destroy()
        
        if typed == "" or (typed in [s.lower() for s in self.suggestions]):
            self.place_forget()
            return
        
        self.position = -1
        
        filtered = [s for s in self.suggestions if typed in s.lower()]
        if len(filtered) == 0:
            self.place_forget()
            return
        
        self.entry.update_idletasks()
        self.configure(width=self.entry.winfo_width() - 20, height=150)
        self.place(in_=self.entry, relx=0, rely=1)
        self.lift()
    
        self._parent_canvas.yview_moveto(0)

        for item in filtered:
            btn = ctk.CTkButton(
                self,
                text=item,
                anchor="w",
                command=lambda val=item: self.select_item(val)
            )
            self.sfondo_bottoni = btn.cget("fg_color")
            self.bordo_bottoni = btn.cget("border_color")
            btn.pack(fill="x", padx=2, pady=2)
            btn.bind("<Return>", lambda e, val=item: self.select_item(val))
            btn.bind("<Down>", lambda e: self.move_focus(e))
            btn.bind("<Up>", lambda e: self.move_focus(e))

    def pulisci_listbox(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.after(200, self.grid_forget())
    
    def select_item(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.pulisci_listbox()
        self.entry.focus_set()

    def move_focus(self, event):
        lista = self.winfo_children()
        if len(lista) == 0:
            return
        for b in lista:
            b.configure(fg_color=self.sfondo_bottoni, border_width=0, border_color=self.bordo_bottoni)

        if event.keysym == "Up" and self.position <= 0:
            self.entry.focus_set()
            self.position = -1
            return
        elif event.keysym == "Up":
            self.position -= 1
        if event.keysym == "Down" and self.position == len(lista) - 1:
            self.position = 0
            self._parent_canvas.yview_moveto(0)
        elif event.keysym == "Down":
            self.position += 1
        
        lista[self.position].focus_set()
        self.entry.delete(0, "end")
        self.entry.insert(0, lista[self.position].cget("text"))
        lista[self.position].configure(fg_color="#7990aa", border_width=2, border_color="white")
        
        area_visibile_inizio, area_visibile_fine = self._parent_canvas.yview()
        pos_relativa_bottone = self.position / len(lista)
        margine = self.position / len(lista)

        if pos_relativa_bottone + margine > area_visibile_fine:
            self._parent_canvas.yview_moveto(pos_relativa_bottone - (area_visibile_fine - area_visibile_inizio) + margine)
        elif pos_relativa_bottone < area_visibile_inizio:
            self._parent_canvas.yview_moveto(pos_relativa_bottone)