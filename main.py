import json
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox

TASK_FILE = "tasks.json"

if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def suggest_task():
    for t in tasks:
        if t.get("priority") == "high":
            messagebox.showinfo("🤖 AI Suggestion", f"Do this first:\n\n{t['task']}")
            return
    if tasks:
        messagebox.showinfo("🤖 AI Suggestion", f"Try this:\n\n{tasks[0]['task']}")
    else:
        messagebox.showinfo("🤖 AI Suggestion", "No tasks available!")

def add_task():
    task_name = simpledialog.askstring("➕ Add Task", "Enter task name:")
    if task_name:
        priority = simpledialog.askstring("Priority", "Enter priority (low/medium/high):")
        if priority:
            tasks.append({"task": task_name, "priority": priority.lower()})
            save_tasks()
            messagebox.showinfo("TaskMate", "✅ Task added successfully!")

def view_tasks():
    if not tasks:
        messagebox.showinfo("📋 Your Tasks", "No tasks found.")
    else:
        task_list = "\n".join([f"{i+1}. {t['task']} [Priority: {t['priority']}]" for i, t in enumerate(tasks)])
        messagebox.showinfo("📋 Your Tasks", task_list)

def complete_task():
    if not tasks:
        messagebox.showinfo("TaskMate", "⚠ No tasks to complete.")
        return

    task_list = "\n".join([f"{i+1}. {t['task']} [Priority: {t['priority']}]" for i, t in enumerate(tasks)])
    task_index = simpledialog.askinteger("✅ Complete Task", f"Select task number to mark complete:\n\n{task_list}")

    if task_index and 1 <= task_index <= len(tasks):
        completed_task = tasks.pop(task_index - 1)
        save_tasks()
        messagebox.showinfo("TaskMate", f"🎉 Task '{completed_task['task']}' completed successfully!")
    else:
        messagebox.showwarning("TaskMate", "⚠ Invalid task number.")
root = ttk.Window(themename="flatly")  
root.title("TaskMate")
root.geometry("320x350")
root.resizable(False, False)
title_label = ttk.Label(root, text="📝 TaskMate", font=("Helvetica", 16, "bold"))
title_label.pack(pady=15)
ttk.Button(root, text="➕ Add Task", width=20, bootstyle=SUCCESS, command=add_task).pack(pady=8)
ttk.Button(root, text="📋 View Tasks", width=20, bootstyle=INFO, command=view_tasks).pack(pady=8)
ttk.Button(root, text="✅ Complete Task", width=20, bootstyle=PRIMARY, command=complete_task).pack(pady=8)
ttk.Button(root, text="🤖 AI Suggest Task", width=20, bootstyle=WARNING, command=suggest_task).pack(pady=8)
ttk.Button(root, text="❌ Exit", width=20, bootstyle=DANGER, command=root.quit).pack(pady=8)

root.mainloop()
