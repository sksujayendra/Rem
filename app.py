import tkinter as tk
from tkinter import messagebox
import threading 
from tkinter import ttk
from database import create_table, add_reminder, get_all_reminders, delete_reminder
from notifier import check_reminders

create_table()

root = tk.Tk()
root.title("Rem")
root.geometry("500x600")
reminder_ids = []

# ---------------- FUNCTIONS ----------------

def refresh_list():
    tree.get_children()
    for item in tree.get_children():
         tree.delete(item)
    reminder_ids.clear()
    reminders = get_all_reminders()
    for rem in reminders:
        reminder_ids.append(rem[0])
        tree.insert("", tk.END, values=(rem[1], rem[2], rem[3]))

def open_add_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add Reminder")
    add_window.geometry("500x600")

    tk.Label(add_window, text="Reminder Title").pack(pady=5)
    title_entry = tk.Entry(add_window)
    title_entry.pack(pady=5)

    tk.Label(add_window, text="Date (YYYY-MM-DD)").pack(pady=5)
    date_entry = tk.Entry(add_window)
    date_entry.pack(pady=5)

    tk.Label(add_window, text="Time (HH:MM)").pack(pady=5)
    time_entry = tk.Entry(add_window)
    time_entry.pack(pady=5)

    def save_reminder():
        add_reminder(
            title_entry.get(),
            date_entry.get(),
            time_entry.get()
        )
        messagebox.showinfo("Saved", "Reminder added")
        add_window.destroy()
        refresh_list()
    

    tk.Button(add_window, text="Save", command=save_reminder).pack(pady=15)

def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("NO selection", "please select a reminder to delete")
            return
        index = tree.index(selected[0])
        reminder_id = reminder_ids[index]
        
        confirm = messagebox.askyesno("confirm delete", "are you sure you want to delete this reminder?")

        if confirm:
            delete_reminder(reminder_id)
            refresh_list()

# ---------------- UI ----------------

root.config(bg="#4863A0")

tk.Label(root, text="YOUR REMINDERS", font=("TkDefaultFont", 20), bg="#4863A0").pack(pady=10)
tk.Label(root, text="its now or never!!!", font=("italic", 15), bg="#4863A0", fg="white").pack(pady=10)

columns = ("title", "date", "time")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("date", text="DATE", anchor="center")
tree.heading("title", text="TITLE", anchor="center")
tree.heading("time", text="TIME", anchor="center")

tree.column("title",width=200, anchor="center")
tree.column("date", width=100, anchor="center")
tree.column("time", width=80, anchor="center")
tree.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
button_frame.config(bg="#4863A0")

tk.Button(button_frame, text="Add Reminder", width=15, command=open_add_window, relief="raised", font=("Segoe UI", 10), bg="#00FF00").grid(row=0, column=0, padx=10, pady=10) 
tk.Button(button_frame, text="Delete Reminder", width=15, command=delete_selected, relief="raised", font=("Segoe UI", 10), bg="#E2F516").grid(row=0, column=1, padx=10, pady=10)


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", background="#00BCD4", foreground="black", font=("Arial", 10, "bold"))
style.configure("Treeview", background="#E0F7FA", foreground="black", rowheight=25, font=("Arial", 10))

# -----------------------------------------------------

refresh_list()

threading.Thread(target=check_reminders, daemon=True).start()

root.mainloop()
