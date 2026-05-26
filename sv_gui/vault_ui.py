import customtkinter as ctk
from sv_gui.layout import AppLayout
from tkinter import filedialog, messagebox
from sv_core.file_vault import encrypt_file, decrypt_file, list_files, delete_file
import os

class VaultUI(AppLayout):
    def __init__(self, master, app):
        super().__init__(master, app, title="File Vault")

        ctk.CTkButton(self.content, text="Add File", command=self.add)\
            .pack(pady=10)

        self.container = ctk.CTkScrollableFrame(self.content)
        self.container.pack(fill="both", expand=True)

        self.load()

    def add(self):
        path = filedialog.askopenfilename()
        if path:
            success, msg = encrypt_file(path, self.app.password)
            if success:
                messagebox.showinfo("Success", "Encrypted!")
                self.load()
            else:
                messagebox.showerror("Error", msg)

    def load(self):
        for w in self.container.winfo_children():
            w.destroy()

        for f in list_files():
            self.row(f)

    def row(self, file):
        fr = ctk.CTkFrame(self.container)
        fr.pack(fill="x", pady=5)

        ctk.CTkLabel(fr, text=file).pack(side="left", padx=10)

        ctk.CTkButton(fr, text="Decrypt",
            command=lambda f=file: self.decrypt(f)).pack(side="right")

        ctk.CTkButton(fr, text="🗑",
            command=lambda f=file: self.delete(f)).pack(side="right")

    def decrypt(self, file):
        path = filedialog.asksaveasfilename(
            initialfile=file.replace(".enc", "")
        )

        if not path:
            return

        success, msg = decrypt_file(file, self.app.password, path)

        if success:
            messagebox.showinfo("Success", "Decrypted!")
            try:
                os.startfile(path)
            except:
                pass
        else:
            messagebox.showerror("Error", msg)

    def delete(self, file):
        if messagebox.askyesno("Confirm", "Delete file?"):
            delete_file(file)
            self.load()