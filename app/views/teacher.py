import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.styles import COLORS, FONTS
from app.services.teacher_service import TeacherService

class TeacherView(tk.Frame):
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
        tk.Label(header_frame, text="Manage Teachers", font=FONTS["header"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)

        # Form Frame
        form_frame = tk.Frame(self, bg=COLORS["background"])
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Name:", bg=COLORS["background"]).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Subject:", bg=COLORS["background"]).grid(row=0, column=2, padx=5, pady=5)
        self.subject_entry = tk.Entry(form_frame)
        self.subject_entry.grid(row=0, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=COLORS["background"])
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", command=self.add_teacher, bg=COLORS["success"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Update", command=self.update_teacher, bg=COLORS["warning"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete", command=self.delete_teacher, bg=COLORS["error"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=10)

        # Treeview
        columns = ("id", "name", "subject")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("subject", text="Subject")
        
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("subject", width=150)

        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        teachers = TeacherService.get_all_teachers()
        for t in teachers:
            self.tree.insert("", tk.END, values=(t.id, t.name, t.subject))
        self.clear_form()

    def add_teacher(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()

        if not name or not subject:
            messagebox.showerror("Error", "All fields are required")
            return

        success, msg = TeacherService.add_teacher(name, subject)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh()
            self.controller.frames["DashboardView"].update_dashboard()
        else:
            messagebox.showerror("Error", msg)

    def update_teacher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a teacher to update")
            return

        item = self.tree.item(selected[0])
        teacher_id = item['values'][0]
        
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()

        if not name or not subject:
            messagebox.showerror("Error", "All fields are required")
            return
        
        success, msg = TeacherService.update_teacher(teacher_id, name, subject)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh()
        else:
            messagebox.showerror("Error", msg)

    def delete_teacher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a teacher to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this teacher?"):
            item = self.tree.item(selected[0])
            teacher_id = item['values'][0]
            
            success, msg = TeacherService.delete_teacher(teacher_id)
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
            self.subject_entry.insert(0, values[2])

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
