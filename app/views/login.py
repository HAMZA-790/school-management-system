import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import AuthService
from app.utils.styles import COLORS, FONTS

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["background"])

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="School Management System", font=FONTS["title"], bg=COLORS["background"], fg=COLORS["primary"])
        title_label.pack(pady=(50, 20))

        # Login Frame
        login_frame = tk.Frame(self, bg=COLORS["background"])
        login_frame.pack(pady=20)

        # Username
        tk.Label(login_frame, text="Username:", font=FONTS["body"], bg=COLORS["background"], fg=COLORS["text"]).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(login_frame, font=FONTS["body"])
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password
        tk.Label(login_frame, text="Password:", font=FONTS["body"], bg=COLORS["background"], fg=COLORS["text"]).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(login_frame, font=FONTS["body"], show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        login_btn = tk.Button(login_frame, text="Login", font=FONTS["button"], bg=COLORS["primary"], fg=COLORS["text_light"], command=self.handle_login, width=15)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        user, message = AuthService.login(username, password)
        if user:
            messagebox.showinfo("Success", message)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            # Make sure DashboardView is loaded when app starts
            self.controller.frames["DashboardView"].update_dashboard()
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Error", message)
