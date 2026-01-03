import tkinter as tk

root = tk.Tk()
root.title("RealNet")

def event_after_selected(*args):
    selected_option = option_var.get()
    print(selected_option)

option_var = tk.StringVar(value="")
option_var.trace("w",event_after_selected)

option_menu = tk.OptionMenu(root, option_var, "COM", "LAN")
option_menu.pack(pady=10)

root.mainloop()