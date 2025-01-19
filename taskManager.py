import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
import hashlib

# data storage files
CREDENTIALS_FILE = "users.txt"
TASKS_FILE = "tasks.csv"

# Predefined categories
CATEGORIES = ["Education", "Health", "Work", "Sports", "Other"]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and hash_password(password) == stored_password:
                    return True
    return False

def register_user(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "w"):
            pass
    with open(CREDENTIALS_FILE, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(",")
            if username == stored_username:
                return False  # Username already exists
    with open(CREDENTIALS_FILE, "a") as file:
        file.write(f"{username},{hash_password(password)}\n")
    return True

def save_task(username, description, category, deadline, status="Pending"):
    task_id = f"{username}_{int(datetime.now().timestamp())}"
    with open(TASKS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([task_id, username, description, category, deadline, status, datetime.now().strftime("%Y-%m-%d")])
    return task_id

def get_tasks(username):
    """Retrieves all tasks for the logged-in user."""
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username:
                    tasks.append(row)
    return tasks

def update_task_status(task_id, new_status):
    tasks = []
    with open(TASKS_FILE, "r") as file:
        reader = csv.reader(file)
        tasks = list(reader)
    with open(TASKS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for task in tasks:
            if task[0] == task_id:
                task[5] = new_status
            writer.writerow(task)

def delete_task(task_id):
    tasks = []
    with open(TASKS_FILE, "r") as file:
        reader = csv.reader(file)
        tasks = list(reader)
    with open(TASKS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for task in tasks:
            if task[0] != task_id:
                writer.writerow(task)

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1000x700")
        self.username = None

        # UI Initialization
        self.create_login_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Task Manager - Login", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 14), bg="blue", fg="white").pack(pady=20)
        tk.Button(self.root, text="Register", command=self.create_register_screen, font=("Arial", 14)).pack(pady=5)

    def create_register_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Task Manager - Register", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register, font=("Arial", 14), bg="green", fg="white").pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen, font=("Arial", 14)).pack(pady=5)

    def create_task_manager_screen(self):
        self.clear_frame()

        tk.Label(self.root, text=f"Welcome to Gargi's Task Manager, {self.username}", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.root, text="Add Task", command=self.create_add_task_screen, font=("Arial", 14), bg="lightblue").pack(pady=10)
        tk.Button(self.root, text="View Tasks", command=self.create_view_tasks_screen, font=("Arial", 14), bg="lightblue").pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 14), bg="red", fg="white").pack(pady=10)

    def create_add_task_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Add a Task", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Task Description:").pack(pady=5)
        self.task_description_entry = tk.Entry(self.root, font=("Arial", 14))
        self.task_description_entry.pack(pady=5)

        tk.Label(self.root, text="Category:").pack(pady=5)
        self.task_category_combobox = ttk.Combobox(self.root, values=CATEGORIES, font=("Arial", 14))
        self.task_category_combobox.pack(pady=5)

        tk.Label(self.root, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        self.task_deadline_entry = tk.Entry(self.root, font=("Arial", 14))
        self.task_deadline_entry.pack(pady=5)

        tk.Button(self.root, text="Add Task", command=self.add_task, font=("Arial", 14), bg="green", fg="white").pack(pady=20)
        tk.Button(self.root, text="Back", command=self.create_task_manager_screen, font=("Arial", 14)).pack(pady=5)

    def create_view_tasks_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Your Tasks", font=("Arial", 24)).pack(pady=20)

        tasks = get_tasks(self.username)

        columns = ("ID","user", "Description", "Category", "Deadline", "Status", "Date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=20, fill="both", expand=True)

        for task in tasks:
            self.tree.insert("", "end", values=task)

        tk.Button(
            self.root,
            text="Mark as Completed",
            command=self.mark_task_completed,
            font=("Arial", 14),
            bg="green",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Delete Task",
            command=self.delete_selected_task,
            font=("Arial", 14),
            bg="red",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Back",
            command=self.create_task_manager_screen,
            font=("Arial", 14)
        ).pack(pady=10)

    def mark_task_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, "values")[0]
            update_task_status(task_id, "Completed")
            messagebox.showinfo("Success", "Task marked as completed.")
            self.create_view_tasks_screen()  # Refresh the tasks list
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_selected_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_id = self.tree.item(selected_item, "values")[0]
            delete_task(task_id)
            messagebox.showinfo("Success", "Task deleted.")
            self.create_view_tasks_screen()  # Refresh the tasks list
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def add_task(self):
        description = self.task_description_entry.get()
        category = self.task_category_combobox.get()
        deadline = self.task_deadline_entry.get()

        if not description or not category or not deadline:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        task_id = save_task(self.username, description, category, deadline)
        messagebox.showinfo("Success", f"Task added with ID: {task_id}")
        self.create_task_manager_screen()  # Go back to the task manager screen

    def login(self):
        """Handles user login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Please enter both username and password!")
            return

        if authenticate(username, password):
            self.username = username
            self.create_task_manager_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def register(self):
        """Handles user registration."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Please fill out all fields!")
            return

        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password must be at least 6 characters long!")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists! Please choose a different username.")

    def logout(self):
        """Logs the user out and redirects to the login screen."""
        self.username = None
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
