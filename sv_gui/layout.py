import customtkinter as ctk

class AppLayout(ctk.CTkFrame):
    def __init__(self, master, app, title=""):
        super().__init__(master)
        self.app = app

        # ===== Sidebar =====
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar, text="🔐 SecureVault",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        self.nav_btn(sidebar, "🏠 Dashboard", app.show_dashboard)
        self.nav_btn(sidebar, "🔑 Passwords", app.show_passwords)
        self.nav_btn(sidebar, "📁 File Vault", app.show_vault)
        self.nav_btn(sidebar, "🚪 Logout", app.show_login)

        # ===== Main Area =====
        self.main = ctk.CTkFrame(self)
        self.main.pack(side="right", fill="both", expand=True)

        # ===== Header =====
        header = ctk.CTkFrame(self.main, height=80)
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            header, text=title,
            font=("Arial", 28, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # ===== Content =====
        self.content = ctk.CTkFrame(self.main)
        self.content.pack(fill="both", expand=True, padx=20, pady=10)

    def nav_btn(self, parent, text, command):
        ctk.CTkButton(parent, text=text, command=command, width=180)\
            .pack(pady=6)