import customtkinter as ctk
import time
from sv_core.db import setup
from sv_gui.login import LoginFrame
from sv_gui.dashboard import Dashboard
from sv_gui.password_ui import PasswordUI
from sv_gui.vault_ui import VaultUI

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SecureVault")
        self.geometry("900x600")

        setup()
        self.password=None
        self.frame=None

        self.last_activity=time.time()
        self.bind_all("<Any-KeyPress>", self.reset_timer)
        self.check_timeout()

        self.show_login()

    def reset_timer(self,e=None):
        self.last_activity=time.time()

    def check_timeout(self):
        if self.password and time.time()-self.last_activity>60:
            self.password=None
            self.show_login()
        self.after(5000,self.check_timeout)

    def switch(self,frame):
        if self.frame:
            self.frame.destroy()
        self.frame=frame(self,self)
        self.frame.pack(fill="both",expand=True)

    def show_login(self):
        self.switch(LoginFrame)

    def login_success(self,p):
        self.password=p
        self.show_dashboard()

    def show_dashboard(self):
        self.switch(Dashboard)

    def show_passwords(self):
        self.switch(PasswordUI)

    def show_vault(self):
        self.switch(VaultUI)

if __name__=="__main__":
    app=App()
    app.mainloop()