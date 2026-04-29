import customtkinter as ctk
from app.utils.styles import FONTS
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # 1. Sidebar (Navigation)
        sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_rowconfigure(7, weight=1) # Push logout to bottom

        logo_label = ctk.CTkLabel(sidebar_frame, text="Admin Panel", font=FONTS["header"])
        logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        buttons = [
            ("Manage Students", "StudentView", 1),
            ("Manage Teachers", "TeacherView", 2),
            ("Mark Attendance", "AttendanceView", 3),
            ("Manage Fees", "FeeView", 4),
            ("System Reports", "ReportView", 5),
        ]

        for text, view_name, r in buttons:
            btn = ctk.CTkButton(sidebar_frame, text=text, command=lambda v=view_name: self.navigate(v), 
                                width=200, height=40, anchor="w", fg_color="transparent", 
                                text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
            btn.grid(row=r, column=0, padx=20, pady=10)

        # Logout Button
        logout_btn = ctk.CTkButton(sidebar_frame, text="Logout", command=lambda: self.controller.show_frame("LoginView"),
                                   width=200, height=40, fg_color="#d83b01", hover_color="#a82d00")
        logout_btn.grid(row=8, column=0, padx=20, pady=30)

        # 2. Main Content Area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)

        header = ctk.CTkLabel(self.main_frame, text="Dashboard Overview", font=FONTS["title"])
        header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 30))

        # Metric Cards
        self.students_card, self.students_val = self.create_metric_card(self.main_frame, "Total Students", "0", 0, 0)
        self.teachers_card, self.teachers_val = self.create_metric_card(self.main_frame, "Total Teachers", "0", 0, 1)
        self.fees_card, self.fees_val = self.create_metric_card(self.main_frame, "Fees Collected", "$0", 0, 2)

    def create_metric_card(self, parent, title, value, row, col):
        card = ctk.CTkFrame(parent, corner_radius=15)
        card.grid(row=row+1, column=col, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(card, text=title, font=FONTS["body"], text_color="gray").pack(pady=(20, 5))
        val_label = ctk.CTkLabel(card, text=value, font=("Roboto", 36, "bold"))
        val_label.pack(pady=(0, 20))
        return card, val_label

    def update_dashboard(self):
        total_students = StudentService.get_total_students()
        total_teachers = TeacherService.get_total_teachers()
        total_fees = FeeService.get_total_fees()

        self.students_val.configure(text=str(total_students))
        self.teachers_val.configure(text=str(total_teachers))
        self.fees_val.configure(text=f"${total_fees:,.2f}")

    def navigate(self, view_name):
        if view_name in self.controller.frames and hasattr(self.controller.frames[view_name], 'refresh'):
            self.controller.frames[view_name].refresh()
        self.controller.show_frame(view_name)
