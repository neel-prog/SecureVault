import customtkinter as ctk
from sv_core.db import connect
from sv_core.crypto import hash_password, verify_password
import hashlib

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Secure Vault 🔐", font=("Arial", 24)).pack(pady=40)

        self.entry = ctk.CTkEntry(self, placeholder_text="Master Password", show="*")
        self.entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        pwd = self.entry.get()
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM master")
        data = cur.fetchone()

        if data is None:
            # Fresh setup — store as PBKDF2
            cur.execute("INSERT INTO master VALUES(?)", (hash_password(pwd),))
            conn.commit()
            self.app.login_success(pwd)

        elif "$" not in data[0]:
            # Old SHA-256 hash — migrate on successful login
            if hashlib.sha256(pwd.encode()).hexdigest() == data[0]:
                cur.execute("UPDATE master SET password=?", (hash_password(pwd),))
                conn.commit()
                self.app.login_success(pwd)

        else:
            # New PBKDF2 hash
            if verify_password(pwd, data[0]):
                self.app.login_success(pwd)

        conn.close()