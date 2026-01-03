import tkinter as tk
from tkinter import messagebox

def on_button_click():
    user_input = entry.get()
    messagebox.showinfo("Message", f"Hello, {user_input}!")

# Create the main window
window = tk.Tk()
window.title("Simple GUI App")

# Create and add a label
label = tk.Label(window, text="Enter your name:")
label.pack()

# Create and add an entry widget
entry = tk.Entry(window)
entry.pack()

# Create and add a button with a callback function
button = tk.Button(window, text="Say Hello", command=on_button_click)
button.pack()

# Run the main loop
window.mainloop()
