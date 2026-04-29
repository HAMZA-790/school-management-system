import tkinter as tk
from app.utils.styles import COLORS, FONTS
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService

class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["background"])
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=60)
        header_frame.pack(fill=tk.X)
        tk.Button(header_frame, text="Back", command=lambda: self.controller.show_frame("DashboardView")).pack(side=tk.LEFT, padx=10, pady=15)
        tk.Label(header_frame, text="System Reports", font=FONTS["header"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)

        # Report Content
        self.report_frame = tk.Frame(self, bg=COLORS["background"])
        self.report_frame.pack(pady=40)

        self.students_label = tk.Label(self.report_frame, text="Total Enrolled Students: 0", font=FONTS["header"], bg=COLORS["background"])
        self.students_label.pack(pady=10)

        self.teachers_label = tk.Label(self.report_frame, text="Total Teachers: 0", font=FONTS["header"], bg=COLORS["background"])
        self.teachers_label.pack(pady=10)

        self.fees_label = tk.Label(self.report_frame, text="Total Fees Collected: $0.00", font=FONTS["header"], bg=COLORS["background"], fg=COLORS["success"])
        self.fees_label.pack(pady=10)

        tk.Button(self.report_frame, text="Refresh Data", font=FONTS["button"], command=self.refresh, bg=COLORS["secondary"], fg=COLORS["text_light"]).pack(pady=30)

    def refresh(self):
        total_students = StudentService.get_total_students()
        total_teachers = TeacherService.get_total_teachers()
        total_fees = FeeService.get_total_fees()

        self.students_label.config(text=f"Total Enrolled Students: {total_students}")
        self.teachers_label.config(text=f"Total Teachers: {total_teachers}")
        self.fees_label.config(text=f"Total Fees Collected: ${total_fees:.2f}")
