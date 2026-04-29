import customtkinter as ctk
from tkinter import ttk, messagebox
from app.utils.styles import FONTS
from app.services.attendance_service import AttendanceService
from app.services.student_service import StudentService

class AttendanceView(ctk.CTkFrame):
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
        
        ctk.CTkLabel(header_frame, text="Mark Attendance", font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(header_frame, text="Back to Dashboard", command=lambda: self.controller.show_frame("DashboardView"),
                      fg_color="transparent", border_width=1, text_color=("gray10", "gray90")).pack(side="right")

        # Form Frame
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)

        self.student_combo = ctk.CTkComboBox(form_frame, values=[], width=250)
        self.student_combo.grid(row=0, column=0, padx=20, pady=20)

        self.date_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", width=150)
        self.date_entry.grid(row=0, column=1, padx=20, pady=20)

        self.status_combo = ctk.CTkComboBox(form_frame, values=["Present", "Absent", "Late"], width=150)
        self.status_combo.set("Present")
        self.status_combo.grid(row=0, column=2, padx=20, pady=20)

        ctk.CTkButton(form_frame, text="Mark", command=self.mark_attendance, width=150, fg_color="#107c10", hover_color="#0b5a0b").grid(row=0, column=3, padx=20)

        # Treeview
        table_frame = ctk.CTkFrame(self, corner_radius=15)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(10, 30))
        table_frame.pack_propagate(False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", font=FONTS["body"])

        columns = ("id", "student_name", "date", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("student_name", text="Student Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("student_name", width=250)
        self.tree.column("date", width=150, anchor="center")
        self.tree.column("status", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def refresh(self):
        # Update student list
        students = StudentService.get_all_students()
        self.student_mapping = {f"{s.id} - {s.name}": s.id for s in students}
        
        keys = list(self.student_mapping.keys())
        if keys:
            self.student_combo.configure(values=keys)
            self.student_combo.set(keys[0])
        else:
            self.student_combo.configure(values=[])
            self.student_combo.set("")

        # Update attendance list
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = AttendanceService.get_attendance()
        for r in records:
            self.tree.insert("", "end", values=(r['id'], r['student_name'], r['date'], r['status']))

    def mark_attendance(self):
        selection = self.student_combo.get()
        if not selection:
            messagebox.showerror("Error", "Please select a student")
            return
        
        student_id = self.student_mapping[selection]
        date = self.date_entry.get().strip()
        status = self.status_combo.get()

        if not date:
            messagebox.showerror("Error", "Date is required")
            return

        success, msg = AttendanceService.mark_attendance(student_id, date, status)
        if success:
            self.refresh()
        else:
            messagebox.showerror("Error", msg)
