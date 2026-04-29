import tkinter as tk
import os
import sys

# Ensure the app can import its modules when run as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.views.student import StudentView
from app.views.teacher import TeacherView
from app.views.attendance import AttendanceView
from app.views.fees import FeeView
from app.views.reports import ReportView

class SchoolManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("800x600")
        
        # Center window
        self.eval('tk::PlaceWindow . center')

        # Container to hold all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Initialize all views
        for F in (LoginView, DashboardView, StudentView, TeacherView, AttendanceView, FeeView, ReportView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with Login
        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = SchoolManagementApp()
    app.mainloop()
