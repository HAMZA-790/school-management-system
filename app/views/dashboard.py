import tkinter as tk
from app.utils.styles import COLORS, FONTS
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["background"])

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=60)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Dashboard", font=FONTS["header"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(pady=15)

        # Metrics Frame
        self.metrics_frame = tk.Frame(self, bg=COLORS["background"])
        self.metrics_frame.pack(pady=20, fill=tk.X, padx=20)

        self.total_students_label = tk.Label(self.metrics_frame, text="Total Students: 0", font=FONTS["body"], bg=COLORS["background"])
        self.total_students_label.grid(row=0, column=0, padx=20)

        self.total_teachers_label = tk.Label(self.metrics_frame, text="Total Teachers: 0", font=FONTS["body"], bg=COLORS["background"])
        self.total_teachers_label.grid(row=0, column=1, padx=20)

        self.total_fees_label = tk.Label(self.metrics_frame, text="Total Fees: $0.00", font=FONTS["body"], bg=COLORS["background"])
        self.total_fees_label.grid(row=0, column=2, padx=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg=COLORS["background"])
        nav_frame.pack(pady=30)

        buttons = [
            ("Manage Students", "StudentView"),
            ("Manage Teachers", "TeacherView"),
            ("Mark Attendance", "AttendanceView"),
            ("Manage Fees", "FeeView"),
            ("Reports", "ReportView"),
            ("Logout", "LoginView")
        ]

        for i, (text, view_name) in enumerate(buttons):
            btn = tk.Button(nav_frame, text=text, font=FONTS["button"], bg=COLORS["secondary"], fg=COLORS["text_light"], width=20, command=lambda v=view_name: self.navigate(v))
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)

    def update_dashboard(self):
        # Update metrics dynamically
        total_students = StudentService.get_total_students()
        total_teachers = TeacherService.get_total_teachers()
        total_fees = FeeService.get_total_fees()

        self.total_students_label.config(text=f"Total Students: {total_students}")
        self.total_teachers_label.config(text=f"Total Teachers: {total_teachers}")
        self.total_fees_label.config(text=f"Total Fees: ${total_fees:.2f}")

    def navigate(self, view_name):
        if view_name in self.controller.frames and hasattr(self.controller.frames[view_name], 'refresh'):
            self.controller.frames[view_name].refresh()
        self.controller.show_frame(view_name)
