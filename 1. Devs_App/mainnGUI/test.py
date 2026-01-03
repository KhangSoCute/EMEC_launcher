import tkinter as tk

root = tk.Tk()

# create a label
label = tk.Label(root, text="Choose an option:")
label.pack()

# create a variable to store the selected option
selected_option = tk.StringVar()

# create an option list
option_list = ["Option 1", "Option 2", "Option 3"]

# create an OptionMenu widget
option_menu = tk.OptionMenu(root, selected_option, *option_list)
option_menu.pack()

root.mainloop()
