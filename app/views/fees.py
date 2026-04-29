import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.styles import COLORS, FONTS
from app.services.fee_service import FeeService
from app.services.student_service import StudentService

class FeeView(tk.Frame):
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
        tk.Label(header_frame, text="Manage Fees", font=FONTS["header"], bg=COLORS["primary"], fg=COLORS["text_light"]).pack(side=tk.LEFT, padx=20, pady=15)

        # Form Frame
        form_frame = tk.Frame(self, bg=COLORS["background"])
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Student:", bg=COLORS["background"]).grid(row=0, column=0, padx=5, pady=5)
        self.student_combo = ttk.Combobox(form_frame, state="readonly", width=25)
        self.student_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Amount:", bg=COLORS["background"]).grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame, width=10)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg=COLORS["background"]).grid(row=0, column=4, padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.insert(0, "2023-01-01")
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(form_frame, text="Add Fee", command=self.add_fee, bg=COLORS["success"], fg=COLORS["text_light"]).grid(row=0, column=6, padx=15)

        # Treeview
        columns = ("id", "student_name", "amount", "date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("student_name", text="Student Name")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("date", text="Date")
        
        self.tree.column("id", width=50)
        self.tree.column("student_name", width=200)
        self.tree.column("amount", width=100)
        self.tree.column("date", width=100)

        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    def refresh(self):
        # Update student list
        students = StudentService.get_all_students()
        self.student_mapping = {f"{s.id} - {s.name}": s.id for s in students}
        self.student_combo['values'] = list(self.student_mapping.keys())
        if self.student_mapping:
            self.student_combo.current(0)

        # Update fees list
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = FeeService.get_fees()
        for r in records:
            self.tree.insert("", tk.END, values=(r['id'], r['student_name'], f"${r['amount']:.2f}", r['date']))

    def add_fee(self):
        selection = self.student_combo.get()
        if not selection:
            messagebox.showerror("Error", "Please select a student")
            return
        
        student_id = self.student_mapping[selection]
        amount_str = self.amount_entry.get().strip()
        date = self.date_entry.get()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        success, msg = FeeService.add_fee(student_id, amount, date)
        if success:
            messagebox.showinfo("Success", msg)
            self.amount_entry.delete(0, tk.END)
            self.refresh()
            self.controller.frames["DashboardView"].update_dashboard()
        else:
            messagebox.showerror("Error", msg)
