import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.styles import COLORS, FONTS
from app.services.student_service import StudentService

class StudentView(tk.Frame):
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
        tk.Label(header_frame, text="Manage Students", font=FONTS["header"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)

        # Form Frame
        form_frame = tk.Frame(self, bg=COLORS["background"])
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Name:", bg=COLORS["background"]).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Class:", bg=COLORS["background"]).grid(row=0, column=2, padx=5, pady=5)
        self.class_entry = tk.Entry(form_frame)
        self.class_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Age:", bg=COLORS["background"]).grid(row=0, column=4, padx=5, pady=5)
        self.age_entry = tk.Entry(form_frame)
        self.age_entry.grid(row=0, column=5, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLORS["background"])
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", command=self.add_student, bg=COLORS["success"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Update", command=self.update_student, bg=COLORS["warning"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete", command=self.delete_student, bg=COLORS["error"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=10)

        # Treeview (List)
        columns = ("id", "name", "class", "age")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("class", text="Class")
        self.tree.heading("age", text="Age")
        
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("class", width=100)
        self.tree.column("age", width=50)

        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = StudentService.get_all_students()
        for s in students:
            self.tree.insert("", tk.END, values=(s.id, s.name, s.student_class, s.age))
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
            messagebox.showinfo("Success", msg)
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
            messagebox.showinfo("Success", msg)
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
                messagebox.showinfo("Success", msg)
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
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
