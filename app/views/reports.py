import customtkinter as ctk
from app.utils.styles import FONTS
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService

class ReportView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        ctk.CTkLabel(header_frame, text="System Reports", font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(header_frame, text="Back to Dashboard", command=lambda: self.controller.show_frame("DashboardView"),
                      fg_color="transparent", border_width=1, text_color=("gray10", "gray90")).pack(side="right")

        # Report Content
        self.report_frame = ctk.CTkFrame(self, corner_radius=20)
        self.report_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
        
        # Spacer
        ctk.CTkLabel(self.report_frame, text="").pack(pady=20)

        self.students_label = ctk.CTkLabel(self.report_frame, text="Total Enrolled Students: 0", font=FONTS["header"])
        self.students_label.pack(pady=20)

        self.teachers_label = ctk.CTkLabel(self.report_frame, text="Total Teachers: 0", font=FONTS["header"])
        self.teachers_label.pack(pady=20)

        self.fees_label = ctk.CTkLabel(self.report_frame, text="Total Fees Collected: $0.00", font=FONTS["header"], text_color="#2cc985")
        self.fees_label.pack(pady=20)

        ctk.CTkButton(self.report_frame, text="Refresh Data", font=FONTS["button"], command=self.refresh, width=200, height=45, corner_radius=10).pack(pady=40)

    def refresh(self):
        total_students = StudentService.get_total_students()
        total_teachers = TeacherService.get_total_teachers()
        total_fees = FeeService.get_total_fees()

        self.students_label.configure(text=f"Total Enrolled Students: {total_students}")
        self.teachers_label.configure(text=f"Total Teachers: {total_teachers}")
        self.fees_label.configure(text=f"Total Fees Collected: ${total_fees:,.2f}")
