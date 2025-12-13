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
            print("Bye.")
            break
        else:
            print("Invalid. Please try again.")
