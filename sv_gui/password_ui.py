import customtkinter as ctk
from sv_gui.layout import AppLayout
from sv_core.db import connect
from sv_core.crypto import encrypt, decrypt
from sv_core.utils import generate_password, check_strength
import pyperclip
from tkinter import messagebox

class PasswordUI(AppLayout):
    def __init__(self, master, app):
        super().__init__(master, app, title="Password Manager")

        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", pady=10)

        self.site = ctk.CTkEntry(form, placeholder_text="Website")
        self.user = ctk.CTkEntry(form, placeholder_text="Username")
        self.pwd = ctk.CTkEntry(form, placeholder_text="Password", show="*")

        self.site.grid(row=0, column=0, padx=5)
        self.user.grid(row=0, column=1, padx=5)
        self.pwd.grid(row=0, column=2, padx=5)

        ctk.CTkButton(form, text="Save", command=self.save)\
            .grid(row=0, column=3, padx=5)

        ctk.CTkButton(form, text="Generate", command=self.generate)\
            .grid(row=1, column=2, pady=5)

        self.strength = ctk.CTkLabel(form, text="Strength:")
        self.strength.grid(row=1, column=1)

        self.pwd.bind("<KeyRelease>", self.update_strength)

        self.container = ctk.CTkScrollableFrame(self.content)
        self.container.pack(fill="both", expand=True)

        self.load()

    def generate(self):
        self.pwd.delete(0, "end")
        self.pwd.insert(0, generate_password())

    def update_strength(self, e=None):
        self.strength.configure(text=f"Strength: {check_strength(self.pwd.get())}")

    def save(self):
        conn = connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO vault(website,username,password) VALUES(?,?,?)",
                    (self.site.get(), self.user.get(),
                     encrypt(self.pwd.get(), self.app.password)))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Saved!")
        self.load()

    def load(self):
        for w in self.container.winfo_children():
            w.destroy()

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vault")

        for row in cur.fetchall():
            self.create_row(row)

        conn.close()

    def create_row(self, row):
        id, site, user, p = row
        pwd = decrypt(p, self.app.password)

        f = ctk.CTkFrame(self.container)
        f.pack(fill="x", pady=5)

        show = ctk.StringVar(value="••••")

        ctk.CTkLabel(f, text=site, width=120).pack(side="left")
        ctk.CTkLabel(f, text=user, width=120).pack(side="left")
        ctk.CTkLabel(f, textvariable=show, width=120).pack(side="left")

        def toggle():
            show.set(pwd if show.get() == "••••" else "••••")

        ctk.CTkButton(f, text="👁", width=30, command=toggle).pack(side="left")
        ctk.CTkButton(f, text="📋", width=30,
                      command=lambda: pyperclip.copy(pwd)).pack(side="left")

        ctk.CTkButton(f, text="🗑", width=30,
                      command=lambda: self.delete(id)).pack(side="left")

    def delete(self, id):
        conn = connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM vault WHERE id=?", (id,))
        conn.commit()
        conn.close()
        self.load()