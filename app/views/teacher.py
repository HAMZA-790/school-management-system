import customtkinter as ctk
from tkinter import ttk, messagebox
from app.utils.styles import FONTS
from app.services.teacher_service import TeacherService

class TeacherView(ctk.CTkFrame):
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
        
        ctk.CTkLabel(header_frame, text="Manage Teachers", font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(header_frame, text="Back to Dashboard", command=lambda: self.controller.show_frame("DashboardView"),
                      fg_color="transparent", border_width=1, text_color=("gray10", "gray90")).pack(side="right")

        # Form Frame
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=10)

        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Teacher Name", width=200)
        self.name_entry.grid(row=0, column=0, padx=20, pady=20)

        self.subject_entry = ctk.CTkEntry(form_frame, placeholder_text="Subject", width=200)
        self.subject_entry.grid(row=0, column=1, padx=20, pady=20)

        ctk.CTkButton(form_frame, text="Add", command=self.add_teacher, width=100).grid(row=0, column=2, padx=10)
        ctk.CTkButton(form_frame, text="Update", command=self.update_teacher, width=100, fg_color="#ffb900", hover_color="#cc9400", text_color="black").grid(row=0, column=3, padx=10)
        ctk.CTkButton(form_frame, text="Delete", command=self.delete_teacher, width=100, fg_color="#d83b01", hover_color="#a82d00").grid(row=0, column=4, padx=10)
        ctk.CTkButton(form_frame, text="Clear", command=self.clear_form, width=100, fg_color="gray", hover_color="darkgray").grid(row=0, column=5, padx=10)

        # Treeview
        table_frame = ctk.CTkFrame(self, corner_radius=15)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(10, 30))
        table_frame.pack_propagate(False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", font=FONTS["body"])

        columns = ("id", "name", "subject")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("subject", text="Subject")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=300)
        self.tree.column("subject", width=300)

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        teachers = TeacherService.get_all_teachers()
        for t in teachers:
            self.tree.insert("", "end", values=(t.id, t.name, t.subject))
        self.clear_form()

    def add_teacher(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()

        if not name or not subject:
            messagebox.showerror("Error", "All fields are required")
            return

        success, msg = TeacherService.add_teacher(name, subject)
        if success:
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
        self.name_entry.delete(0, 'end')
        self.subject_entry.delete(0, 'end')
