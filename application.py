import os
import json

tasks = []

def tasks_menu():
    while True:
        print("\nTask Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Task Complete")
        print("5. Save")
        print("6. Exit")

        choice = input("Option 1-6: ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            task_complete()
        elif choice == '5':
            save_task()
        elif choice == '6':
            print("Goodbye.")
        else:
            print("Invalid. Please try again.")

def add_task():
    title = input("Enter task")
    if not title:
        print("Do not leave blank.")
        return
    tasks.append({"title": title, "completed": False})
    print(f'task "{title}" added.')

def view_tasks():
    if not tasks:
        print("No tasks available.")
        return
    print("\nTasks:")
    for idx, task in enumerate(tasks, start=1):
        status = "[x] " if task.get("completed") else "[ ] "
        desc = f" - {task['description']}" if task.get('description') else ""
        print(f"{idx}. {status}{task['title']}{desc}")

def delete_task():
    if not tasks:
        print("No tasks to delete.")
        return
    view_tasks()
    choice = input("Enter the number of the task to delete: ").strip()
    try:
        idx = int(choice)
        if 1 <= idx <= len(tasks):
            removed = tasks.pop(idx - 1)
            print(f"Removed task: '{removed['title']}'")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def task_complete():
    if not tasks:
        print("No tasks to mark complete.")
        return
    view_tasks()
    choice = input("Enter the number of the task to mark complete: ").strip()
    try:
        idx = int(choice)
        if 1 <= idx <= len(tasks):
            tasks[idx - 1]['completed'] = True
            print(f"Marked task '{tasks[idx - 1]['title']}' as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def save_task():
    import json, os
    out_path = os.path.join(os.path.dirname(__file__), "tasks.json")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"Tasks saved to {out_path}")
    except Exception as e:
        print(f"Failed to save tasks: {e}")

def refresh_listbox(lb):
    lb.delete(0, "end")
    for task in tasks:
        status = "[x] " if task.get("completed") else "[ ] "
        desc = f" - {task['description']}" if task.get('description') else ""
        lb.insert("end", f"{status}{task['title']}{desc}")

def add_task_gui(title_var, desc_var, lb):
    title = title_var.get().strip()
    if not title:
        try:
            from tkinter import messagebox
            messagebox.showwarning("Input error", "Task title cannot be empty.")
        except Exception:
            print("Task title cannot be empty.")
        return
    description = desc_var.get().strip()
    tasks.append({"title": title, "description": description, "completed": False})
    title_var.set("")
    desc_var.set("")
    refresh_listbox(lb)

def delete_task_gui(lb):
    sel = lb.curselection()
    if not sel:
        try:
            from tkinter import messagebox
            messagebox.showinfo("Info", "No task selected.")
        except Exception:
            print("No task selected.")
        return
    idx = sel[0]
    removed = tasks.pop(idx)
    refresh_listbox(lb)
    try:
        from tkinter import messagebox
        messagebox.showinfo("Deleted", f"Removed task: '{removed['title']}'")
    except Exception:
        print(f"Removed task: '{removed['title']}'")

def run_gui():
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("To-Do List")

    mainframe = ttk.Frame(root, padding="12")
    style = ttk.Style()
    style.configure("Pink.TFrame", background="pink")
    mainframe.configure(style="Pink.TFrame")
    mainframe.grid(row=0, column=0, sticky="nsew")

    # Listbox
    lb_frame = ttk.Frame(mainframe)
    lb_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
    lb = tk.Listbox(lb_frame, height=30, width=50)
    sb = ttk.Scrollbar(lb_frame, orient="vertical", command=lb.yview)
    lb.configure(yscrollcommand=sb.set)
    lb.grid(row=0, column=0, sticky="nsew")
    sb.grid(row=0, column=1, sticky="ns")

    # Title and description entries
    ttk.Label(mainframe, text="Title:").grid(row=1, column=0, sticky="w", pady=(8,0))
    title_var = tk.StringVar()
    title_entry = ttk.Entry(mainframe, textvariable=title_var, width=40)
    title_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(8,0))

    ttk.Label(mainframe, text="Description:").grid(row=2, column=0, sticky="w")
    desc_var = tk.StringVar()
    desc_entry = ttk.Entry(mainframe, textvariable=desc_var, width=40)
    desc_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

    # Buttons
    add_btn = ttk.Button(mainframe, text="Add", command=lambda: add_task_gui(title_var, desc_var, lb))
    add_btn.grid(row=3, column=0, pady=10, sticky="ew")
    view_btn = ttk.Button(mainframe, text="View", command=lambda: refresh_listbox(lb))
    view_btn.grid(row=3, column=1, pady=10, sticky="ew")
    del_btn = ttk.Button(mainframe, text="Delete", command=lambda: delete_task_gui(lb))
    del_btn.grid(row=3, column=1, pady=10, sticky="ew")
    task_complete_btn = ttk.Button(mainframe, text="Complete", command=lambda: mark_task_complete_gui(lb))
    task_complete_btn.grid(row=4, column=0, pady=10, sticky="ew")
    save_btn = ttk.Button(mainframe, text="Save", command=save_task)
    save_btn.grid(row=4, column=1, pady=10, sticky="ew")
    exit_btn = ttk.Button(mainframe, text="Exit", command=root.destroy)
    exit_btn.grid(row=5, column=0, pady=10, sticky="ew")

    # Make resizing reasonable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1)
    mainframe.rowconfigure(0, weight=1)

    refresh_listbox(lb)
    root.mainloop()

if __name__ == "__main__":
    try:
        run_gui()
    except Exception:
        tasks_menu()