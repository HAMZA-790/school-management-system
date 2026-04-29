import customtkinter as ctk

# Configure CustomTkinter Appearance
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# We can still keep standard colors for custom drawing or standard tk fallback if needed
COLORS = {
    "primary": "#1f538d",
    "secondary": "#2cc985",
    "background": "#242424",
    "text": "#ffffff",
    "text_light": "#ffffff",
    "error": "#d83b01",
    "success": "#107c10",
    "warning": "#ffb900"
}

# Fonts for CTk widgets
FONTS = {
    "title": ("Roboto", 32, "bold"),
    "header": ("Roboto", 24, "bold"),
    "body": ("Roboto", 14),
    "button": ("Roboto", 14, "bold")
}
