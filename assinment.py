import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json

# ==========================================
#        SHARED DATA & CONFIGURATION
# ==========================================

# Shared Data Storage
grocery_list = []
budget_expenses = []

# Styles for Chore App
COLOR_BG = "#f0f2f5"
COLOR_WHITE = "#ffffff"
COLOR_PRIMARY = "#6366f1"  # Indigo
COLOR_PRIMARY_HOVER = "#4f46e5"
COLOR_SUCCESS = "#10b981"  # Emerald
COLOR_TEXT_MAIN = "#1e293b"
COLOR_TEXT_SUB = "#64748b"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")
FONT_SMALL = ("Helvetica", 9)

# ==========================================
#          DATA MODELS (Chore App)
# ==========================================

class Member:
    def __init__(self, name, xp=0, color="#3b82f6"):
        self.name = name
        self.xp = xp
        self.color = color

class Chore:
    def __init__(self, title, assignee_name, points, due_date, category):
        self.title = title
        self.assignee = assignee_name
        self.points = points
        self.due_date = due_date
        self.category = category
        self.completed = False

# ==========================================
#            APP 1: GROCERY LIST
# ==========================================

class GroceryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Grocery List Manager")
        self.window.geometry("500x600")
        self.window.config(bg="#ffffff")
        
        # Proper window close handling
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        title_label = tk.Label(
            window, text="🛒 Grocery List Manager",
            font=("Arial", 18, "bold"), bg="#ffffff", fg="#4CAF50"
        )
        title_label.pack(pady=15)
        
        button_frame = tk.Frame(window, bg="#ffffff")
        button_frame.pack(pady=10)
        
        btn_add = tk.Button(
            button_frame, text="➕ Add Item",
            font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
            width=15, height=2, command=self.add_item
        )
        btn_add.grid(row=0, column=0, padx=5, pady=5)
        
        btn_update = tk.Button(
            button_frame, text="✏️ Update Item",
            font=("Arial", 11), bg="#2196F3", fg="white",
            width=15, height=2, command=self.update_item
        )
        btn_update.grid(row=0, column=1, padx=5, pady=5)
        
        btn_delete = tk.Button(
            button_frame, text="🗑️ Delete Item",
            font=("Arial", 11), bg="#f44336", fg="white",
            width=15, height=2, command=self.delete_item
        )
        btn_delete.grid(row=1, column=0, padx=5, pady=5)
        
        btn_back = tk.Button(
            button_frame, text="Close",
            font=("Arial", 11), bg="#9E9E9E", fg="white",
            width=15, height=2, command=self.on_closing
        )
        btn_back.grid(row=1, column=1, padx=5, pady=5)
        
        list_label = tk.Label(window, text="Your Grocery Items:", 
                             font=("Arial", 12, "bold"), bg="#ffffff")
        list_label.pack(pady=10)
        
        list_frame = tk.Frame(window, bg="#ffffff")
        list_frame.pack(pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame, font=("Arial", 11), width=50, height=15,
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.listbox.yview)
        
        self.refresh_list()
    
    def on_closing(self):
        """Properly close the window"""
        self.window.destroy()
    
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        if len(grocery_list) == 0:
            self.listbox.insert(tk.END, "No items yet. Click 'Add Item' to start!")
        else:
            for i, item in enumerate(grocery_list, 1):
                display_text = f"{i}. {item['name']} - Quantity: {item['quantity']}"
                self.listbox.insert(tk.END, display_text)
    
    def add_item(self):
        item_name = simpledialog.askstring("Add Item", "Enter item name (letters only):", parent=self.window)
        if not item_name or item_name.strip() == "":
            return
        
        if any(char.isdigit() for char in item_name):
            messagebox.showerror("Invalid Input", "Item name cannot contain numbers!")
            return
        
        if not item_name.replace(" ", "").isalpha():
            messagebox.showerror("Invalid Input", "Item name should only contain letters!")
            return
        
        quantity = simpledialog.askinteger("Add Item", f"Enter quantity for '{item_name}':", 
                                         parent=self.window, minvalue=1)
        if quantity is None:
            return
        
        item = {"name": item_name.strip(), "quantity": quantity}
        grocery_list.append(item)
        self.refresh_list()
        messagebox.showinfo("Success", f"'{item_name}' added to your list!")
    
    def update_item(self):
        if len(grocery_list) == 0:
            messagebox.showwarning("Empty List", "No items to update!")
            return
        
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to update.")
            return
        
        index = selection[0]
        current_item = grocery_list[index]
        
        new_name = simpledialog.askstring("Update Item", 
                                         f"Current: {current_item['name']}\nEnter new name:", 
                                         parent=self.window)
        if new_name is None:
            return
        if new_name.strip() != "":
            if any(char.isdigit() for char in new_name):
                messagebox.showerror("Invalid Input", "Item name cannot contain numbers!")
                return
            if not new_name.replace(" ", "").isalpha():
                messagebox.showerror("Invalid Input", "Item name should only contain letters!")
                return
            current_item['name'] = new_name.strip()
        
        new_quantity = simpledialog.askinteger("Update Item", 
                                              f"Current quantity: {current_item['quantity']}\nEnter new quantity:", 
                                              parent=self.window, minvalue=1)
        if new_quantity is not None:
            current_item['quantity'] = new_quantity
        
        self.refresh_list()
        messagebox.showinfo("Success", "Item updated!")
    
    def delete_item(self):
        if len(grocery_list) == 0:
            messagebox.showwarning("Empty List", "No items to delete!")
            return
        
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to delete.")
            return
        
        index = selection[0]
        item_to_delete = grocery_list[index]
        
        if messagebox.askyesno("Confirm Delete", f"Delete '{item_to_delete['name']}'?"):
            grocery_list.pop(index)
            self.refresh_list()
            messagebox.showinfo("Success", f"'{item_to_delete['name']}' deleted!")


# ==========================================
#            APP 2: BUDGET TRACKER
# ==========================================

class BudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.categories = ["Food", "Transport", "Entertainment", "Utilities", "Other"]
        self.expenses = budget_expenses
        
        # Proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
    
    def on_closing(self):
        """Properly close the window"""
        self.root.destroy()
    
    def create_widgets(self):
        self.root.title("Budget Tracker")
        self.root.geometry("450x600")
        
        title = tk.Label(self.root, text="💰 Budget Tracker", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Add Expense Section
        add_frame = tk.LabelFrame(self.root, text="Add New Expense", padx=15, pady=15)
        add_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(add_frame, text="Category:").grid(row=0, column=0, sticky="w", pady=8)
        self.category = tk.StringVar()
        category_menu = tk.OptionMenu(add_frame, self.category, *self.categories)
        category_menu.grid(row=0, column=1, sticky="ew", pady=8, padx=10)
        self.category.set(self.categories[0])
        
        tk.Label(add_frame, text="Amount ($):").grid(row=1, column=0, sticky="w", pady=8)
        self.amount_entry = tk.Entry(add_frame)
        self.amount_entry.grid(row=1, column=1, sticky="ew", pady=8, padx=10)
        
        tk.Label(add_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=8)
        self.desc_entry = tk.Entry(add_frame)
        self.desc_entry.grid(row=2, column=1, sticky="ew", pady=8, padx=10)
        
        btn_frame = tk.Frame(add_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        add_btn = tk.Button(btn_frame, text="Add Expense", command=self.add_expense, 
                           bg="lightgreen", font=("Arial", 10))
        add_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(btn_frame, text="Reset All", command=self.reset_all,
                            bg="lightcoral", font=("Arial", 10))
        reset_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(btn_frame, text="Close", command=self.on_closing,
                           bg="lightblue", font=("Arial", 10))
        back_btn.pack(side="left", padx=5)
        
        # View Expenses Section
        view_frame = tk.LabelFrame(self.root, text="View Expenses", padx=15, pady=15)
        view_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        view_all_btn = tk.Button(view_frame, text="View All Expenses", 
                                command=self.view_all, font=("Arial", 10))
        view_all_btn.pack(pady=8)
        
        self.display = tk.Text(view_frame, height=12, width=50, font=("Consolas", 9), state="disabled")
        self.display.pack(pady=10, fill="both", expand=True)
        
        self.view_all()
    
    def add_expense(self):
        category = self.category.get()
        amount_text = self.amount_entry.get()
        description = self.desc_entry.get()
        
        if not amount_text:
            messagebox.showerror("Error", "Please enter amount!")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return
        
        self.expenses.append({
            'category': category,
            'amount': amount,
            'description': description if description else "No description"
        })
        
        messagebox.showinfo("Success", f"Added ${amount:.2f} to {category}!")
        self.clear_entries()
        self.view_all()
    
    def view_all(self):
        self.display.config(state="normal")  # Enable editing temporarily
        self.display.delete(1.0, tk.END)
        
        if not self.expenses:
            self.display.insert(tk.END, "No expenses recorded yet.\nAdd some expenses above!")
            self.display.config(state="disabled")  # Disable editing
            return
        
        total = 0
        self.display.insert(tk.END, "Your Expenses:\n" + "="*30 + "\n")
        
        for i, exp in enumerate(self.expenses, 1):
            self.display.insert(tk.END, f"{i}. {exp['category']}: ${exp['amount']:.2f}\n")
            self.display.insert(tk.END, f"   Description: {exp['description']}\n\n")
            total += exp['amount']
        
        self.display.insert(tk.END, "="*30 + f"\nTOTAL: ${total:.2f}")
        self.display.config(state="disabled")  # Disable editing
    
    def reset_all(self):
        if messagebox.askyesno("Confirm Reset", "Delete ALL expenses?"):
            self.expenses.clear()
            self.clear_entries()
            self.view_all()
            messagebox.showinfo("Reset", "All expenses cleared!")
    
    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)


# ==========================================
#          APP 3: CHORE SCHEDULER
# ==========================================

class ChoreSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HomeSync - Chore Scheduler")
        self.root.geometry("900x650")
        self.root.configure(bg=COLOR_BG)
        
        # Proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initial Data
        self.members = {
            "Alex": Member("Alex", 120, "#3b82f6"),
            "Sam": Member("Sam", 85, "#10b981"),
            "Jordan": Member("Jordan", 200, "#a855f7"),
            "Taylor": Member("Taylor", 50, "#f97316"),
        }
        
        self.chores = []

        self.setup_styles()
        self.create_layout()
        self.refresh_ui()
    
    def on_closing(self):
        """Properly close the window"""
        self.root.destroy()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # General Frame Styles
        style.configure("Card.TFrame", background=COLOR_WHITE, relief="flat")
        style.configure("Main.TFrame", background=COLOR_BG)
        
        # Button Styles
        style.configure("Primary.TButton", 
                        background=COLOR_PRIMARY, 
                        foreground=COLOR_WHITE, 
                        font=FONT_BOLD, 
                        borderwidth=0, 
                        padding=10)
        style.map("Primary.TButton", background=[('active', COLOR_PRIMARY_HOVER)])
        
        style.configure("Action.TButton", 
                        background="#e2e8f0", 
                        foreground=COLOR_TEXT_MAIN, 
                        font=FONT_SMALL,
                        borderwidth=0)

    def create_layout(self):
        # -- Sidebar (Left) --
        sidebar = tk.Frame(self.root, bg=COLOR_WHITE, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # App Logo/Title
        tk.Label(sidebar, text="HomeSync", bg=COLOR_WHITE, fg=COLOR_PRIMARY, 
                 font=("Helvetica", 22, "bold")).pack(pady=(30, 40))
        
        # Exit Button in Sidebar
        exit_btn = tk.Button(sidebar, text="Back to Main Menu", bg="#f44336", fg="white",
                             font=("Helvetica", 9), borderwidth=0, padx=10, pady=5,
                             command=self.on_closing)
        exit_btn.pack(side="bottom", pady=20)

        # -- Main Content (Right) --
        content_area = tk.Frame(self.root, bg=COLOR_BG)
        content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(content_area, bg=COLOR_BG)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="Chore Dashboard", bg=COLOR_BG, fg=COLOR_TEXT_MAIN, 
                 font=("Helvetica", 24, "bold")).pack(side="left")

        add_btn = ttk.Button(header_frame, text="+ New Task", style="Primary.TButton", 
                             command=self.open_add_task_window)
        add_btn.pack(side="right")

        # Scrollable Task List Area
        self.canvas = tk.Canvas(content_area, bg=COLOR_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(content_area, orient="vertical", command=self.canvas.yview)
        self.task_list_frame = tk.Frame(self.canvas, bg=COLOR_BG)

        self.task_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw", width=640)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def refresh_ui(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        if not self.chores:
            tk.Label(self.task_list_frame, text="No chores assigned! Relax.", bg=COLOR_BG, fg=COLOR_TEXT_SUB).pack(pady=50)

        for chore in self.chores:
            self.create_chore_card(chore)

    def create_chore_card(self, chore):
        # Card Container
        card = tk.Frame(self.task_list_frame, bg=COLOR_WHITE, padx=20, pady=15)
        card.pack(fill="x", pady=8)
        
        # Status Color Indicator strip
        status_color = COLOR_SUCCESS if chore.completed else "#e2e8f0"
        tk.Frame(card, bg=status_color, width=5).pack(side="left", fill="y", padx=(0, 15))

        # Text Info
        info_frame = tk.Frame(card, bg=COLOR_WHITE)
        info_frame.pack(side="left", fill="both", expand=True)

        title_style = ("Helvetica", 12, "overstrike") if chore.completed else ("Helvetica", 12, "bold")
        title_fg = COLOR_TEXT_SUB if chore.completed else COLOR_TEXT_MAIN
        
        tk.Label(info_frame, text=chore.title, font=title_style, bg=COLOR_WHITE, fg=title_fg).pack(anchor="w")
        
        meta_text = f"Assigned to: {chore.assignee}  •  {chore.category}  •  {chore.points} XP"
        tk.Label(info_frame, text=meta_text, font=FONT_SMALL, bg=COLOR_WHITE, fg=COLOR_TEXT_SUB).pack(anchor="w", pady=(4, 0))

        # Action Button
        if not chore.completed:
            btn = tk.Button(card, text="Complete", bg=COLOR_SUCCESS, fg="white", font=FONT_BOLD, 
                            relief="flat", padx=10, pady=5, cursor="hand2",
                            command=lambda c=chore: self.mark_completed(c))
            btn.pack(side="right")
        else:
            tk.Label(card, text="Done ✓", fg=COLOR_SUCCESS, bg=COLOR_WHITE, font=FONT_BOLD).pack(side="right", padx=10)

    def mark_completed(self, chore):
        chore.completed = True
        if chore.assignee in self.members:
            self.members[chore.assignee].xp += chore.points
        self.refresh_ui()

    def open_add_task_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Task")
        top.geometry("400x450")
        top.configure(bg=COLOR_WHITE)
        
        # Make dialog modal
        top.transient(self.root)
        top.grab_set()

        tk.Label(top, text="New Chore", font=("Helvetica", 18, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN).pack(pady=20)

        def create_field(label):
            tk.Label(top, text=label, bg=COLOR_WHITE, fg=COLOR_TEXT_SUB, font=FONT_BOLD).pack(anchor="w", padx=40, pady=(10, 5))
            entry = ttk.Entry(top, width=40)
            entry.pack(padx=40)
            return entry

        title_entry = create_field("Task Title")
        assignee_entry = create_field("Assign To (Name)")
        points_entry = create_field("XP Points (e.g. 10, 20)")
        cat_entry = create_field("Category (e.g. Kitchen)")

        def save_task():
            title = title_entry.get().strip()
            points_str = points_entry.get().strip()
            assignee = assignee_entry.get().strip()
            category = cat_entry.get().strip()

            if not title or not points_str or not assignee:
                messagebox.showerror("Error", "Please fill in Title, Assignee, and Points!")
                return
            
            try:
                points = int(points_str)
                if points <= 0:
                    messagebox.showerror("Error", "Points must be a positive number!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Points must be a valid number!")
                return
            
            new_chore = Chore(title, assignee, points, datetime.now().strftime("%Y-%m-%d"), category if category else "General")
            self.chores.append(new_chore)
            self.refresh_ui()
            top.destroy()

        submit_btn = tk.Button(top, text="Assign Task", bg=COLOR_PRIMARY, fg="white", font=FONT_BOLD, 
                               relief="flat", pady=10, command=save_task)
        submit_btn.pack(fill="x", padx=40, pady=30)


# ==========================================
#              MAIN MENU
# ==========================================

class MainMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Household Management System")
        self.root.geometry("400x480")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f0f0")
        
        # Proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)
        
        # Title
        title_label = tk.Label(
            root, text="🏠 HOUSEHOLD MANAGER",
            font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333"
        )
        title_label.pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Grocery List Button
        btn_grocery = tk.Button(
            button_frame, text="🛒 Grocery List Manager",
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
            width=28, height=2, command=self.open_grocery_app
        )
        btn_grocery.pack(pady=12)
        
        # Budget Tracker Button
        btn_budget = tk.Button(
            button_frame, text="💰 Budget Tracker", 
            font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
            width=28, height=2, command=self.open_budget_app
        )
        btn_budget.pack(pady=12)
        
        # Chore Scheduler Button
        btn_chore = tk.Button(
            button_frame, text="🧹 Chore Scheduler",
            font=("Arial", 12, "bold"), bg=COLOR_PRIMARY, fg="white",
            width=28, height=2, command=self.open_chore_app
        )
        btn_chore.pack(pady=12)
        
        # Exit button
        btn_exit = tk.Button(
            button_frame, text="❌ Exit Program",
            font=("Arial", 12), bg="#f44336", fg="white",
            width=28, height=2, command=self.exit_program
        )
        btn_exit.pack(pady=12)
    
    def open_grocery_app(self):
        grocery_window = tk.Toplevel(self.root)
        GroceryApp(grocery_window)
    
    def open_budget_app(self):
        budget_window = tk.Toplevel(self.root)
        BudgetTrackerGUI(budget_window)
    
    def open_chore_app(self):
        chore_window = tk.Toplevel(self.root)
        ChoreSchedulerApp(chore_window)
    
    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
            self.root.destroy()

# ==========================================
#              ENTRY POINT
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenuApp(root)
    root.mainloop()