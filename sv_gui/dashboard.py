import customtkinter as ctk
from sv_core.db import connect
import os

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # ================= SIDEBAR =================
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar,
            text="🔐 SecureVault",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        self.nav_btn(sidebar, "🏠 Dashboard", app.show_dashboard)
        self.nav_btn(sidebar, "🔑 Passwords", app.show_passwords)
        self.nav_btn(sidebar, "📁 File Vault", app.show_vault)
        self.nav_btn(sidebar, "🚪 Logout", app.show_login)

        # ================= MAIN AREA =================
        main = ctk.CTkFrame(self)
        main.pack(side="right", fill="both", expand=True)

        # ===== Header =====
        header = ctk.CTkFrame(main, height=80)
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(
            header,
            text="Overview of your secure vault",
            font=("Arial", 14)
        ).pack(anchor="w", padx=10)

        # ===== Content Area =====
        content = ctk.CTkFrame(main)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Grid layout
        content.grid_columnconfigure((0, 1), weight=1)

        # ===== Cards =====
        self.create_card(
            content, "🔑 Saved Passwords",
            self.count_passwords(), 0, 0
        )

        self.create_card(
            content, "📁 Vault Files",
            self.count_files(), 0, 1
        )

        self.create_card(
            content, "🔒 Security Status",
            "Active", 1, 0
        )

        self.create_card(
            content, "⏱ Auto Lock",
            "Enabled", 1, 1
        )

    # ---------- NAV BUTTON ----------
    def nav_btn(self, parent, text, command):
        ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=180,
            height=40
        ).pack(pady=6)

    # ---------- CARD ----------
    def create_card(self, parent, title, value, row, col):
        frame = ctk.CTkFrame(parent, height=120)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 14)
        ).pack(anchor="w", padx=15, pady=10)

        ctk.CTkLabel(
            frame,
            text=str(value),
            font=("Arial", 28, "bold")
        ).pack(anchor="w", padx=15)

    # ---------- COUNT PASSWORDS ----------
    def count_passwords(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vault")
        count = cur.fetchone()[0]
        conn.close()
        return count

    # ---------- COUNT FILES ----------
    def count_files(self):
        path = os.path.join(os.getenv("APPDATA"), "SecureVault", "files")
        if os.path.exists(path):
            return len(os.listdir(path))
        return 0