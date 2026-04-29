import customtkinter as ctk
from tkinter import ttk, messagebox
from app.utils.styles import FONTS
from app.services.student_service import StudentService

class StudentView(ctk.CTkFrame):
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
        
        ctk.CTkLabel(header_frame, text="Manage Students", font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(header_frame, text="Back to Dashboard", command=lambda: self.controller.show_frame("DashboardView"),
                      fg_color="transparent", border_width=1, text_color=("gray10", "gray90")).pack(side="right")

        # Form Frame
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)

        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Student Name", width=200)
        self.name_entry.grid(row=0, column=0, padx=20, pady=20)

        self.class_entry = ctk.CTkEntry(form_frame, placeholder_text="Class", width=150)
        self.class_entry.grid(row=0, column=1, padx=20, pady=20)

        self.age_entry = ctk.CTkEntry(form_frame, placeholder_text="Age", width=100)
        self.age_entry.grid(row=0, column=2, padx=20, pady=20)

        ctk.CTkButton(form_frame, text="Add", command=self.add_student, width=100).grid(row=0, column=3, padx=10)
        ctk.CTkButton(form_frame, text="Update", command=self.update_student, width=100, fg_color="#ffb900", hover_color="#cc9400", text_color="black").grid(row=0, column=4, padx=10)
        ctk.CTkButton(form_frame, text="Delete", command=self.delete_student, width=100, fg_color="#d83b01", hover_color="#a82d00").grid(row=0, column=5, padx=10)
        ctk.CTkButton(form_frame, text="Clear", command=self.clear_form, width=100, fg_color="gray", hover_color="darkgray").grid(row=0, column=6, padx=10)

        # Treeview (List)
        table_frame = ctk.CTkFrame(self, corner_radius=15)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(10, 30))
        table_frame.pack_propagate(False)

        # Style the ttk Treeview for CustomTkinter
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", font=FONTS["body"])

        columns = ("id", "name", "class", "age")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("class", text="Class")
        self.tree.heading("age", text="Age")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("class", width=150, anchor="center")
        self.tree.column("age", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = StudentService.get_all_students()
        for s in students:
            self.tree.insert("", "end", values=(s.id, s.name, s.student_class, s.age))
        self.clear_form()

    def add_student(self):
        name = self.name_entry.get().strip()
        student_class = self.class_entry.get().strip()
        age = self.age_entry.get().strip()

        if not name or not student_class or not age:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer")
            return

        success, msg = StudentService.add_student(name, student_class, age)
        if success:
            self.refresh()
            self.controller.frames["DashboardView"].update_dashboard()
        else:
            messagebox.showerror("Error", msg)

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update")
            return

        item = self.tree.item(selected[0])
        student_id = item['values'][0]
        
        name = self.name_entry.get().strip()
        student_class = self.class_entry.get().strip()
        age = self.age_entry.get().strip()

        if not name or not student_class or not age:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer")
            return

        success, msg = StudentService.update_student(student_id, name, student_class, age)
        if success:
            self.refresh()
        else:
            messagebox.showerror("Error", msg)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            item = self.tree.item(selected[0])
            student_id = item['values'][0]
            
            success, msg = StudentService.delete_student(student_id)
            if success:
                self.refresh()
                self.controller.frames["DashboardView"].update_dashboard()
            else:
                messagebox.showerror("Error", msg)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.clear_form()
            self.name_entry.insert(0, values[1])
            self.class_entry.insert(0, values[2])
            self.age_entry.insert(0, values[3])

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.class_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
