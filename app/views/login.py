import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from app.services.auth_service import AuthService
from app.utils.styles import FONTS

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Grid configuration to split screen
        self.grid_columnconfigure(0, weight=1) # Image side
        self.grid_columnconfigure(1, weight=1) # Form side
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # 1. Image Side (Left)
        image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "login_bg.png")
        try:
            # Load image using CTkImage for scaling support
            bg_image = ctk.CTkImage(light_image=Image.open(image_path),
                                    dark_image=Image.open(image_path),
                                    size=(500, 700))
            image_label = ctk.CTkLabel(self, text="", image=bg_image)
            image_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        except Exception as e:
            # Fallback if image not found
            image_label = ctk.CTkLabel(self, text="School Management System\nProfessional Edition", font=FONTS["title"])
            image_label.grid(row=0, column=0, sticky="nsew")

        # 2. Login Form Side (Right)
        form_frame = ctk.CTkFrame(self, corner_radius=20)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 40), pady=40)
        form_frame.grid_rowconfigure(0, weight=1)
        form_frame.grid_rowconfigure(6, weight=1)

        # Welcome Text
        ctk.CTkLabel(form_frame, text="Welcome Back!", font=FONTS["title"]).grid(row=1, column=0, pady=(40, 10))
        ctk.CTkLabel(form_frame, text="Please login to your account", font=FONTS["body"], text_color="gray").grid(row=2, column=0, pady=(0, 40))

        # Inputs
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Username", width=300, height=45, font=FONTS["body"])
        self.username_entry.grid(row=3, column=0, pady=(0, 20))

        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Password", width=300, height=45, show="*", font=FONTS["body"])
        self.password_entry.grid(row=4, column=0, pady=(0, 30))

        # Login Button
        login_btn = ctk.CTkButton(form_frame, text="LOGIN", font=FONTS["button"], width=300, height=45, corner_radius=8, command=self.handle_login)
        login_btn.grid(row=5, column=0, pady=(0, 40))

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return

        user, message = AuthService.login(username, password)
        if user:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.controller.frames["DashboardView"].update_dashboard()
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Error", message)
