import tkinter as tk
from tkinter import messagebox

class AppController:
    def __init__(self, master):
        self.master = master
        self.master.title("Seegene Launcher Controller")

        # Create radio buttons for method selection
        self.method_var = tk.StringVar(value="None")  # Default selection
        self.create_radio_buttons()

        # Create Start button
        start_button = tk.Button(self.master, text="Start", command=self.start_sequence)
        start_button.pack(pady=10)

    def create_radio_buttons(self):
        methods = ["HBV", "HCV", "HIV", "None"]  # Updated methods list
        for method in methods:
            method_radio = tk.Radiobutton(self.master, text=method, variable=self.method_var, value=method)
            method_radio.pack(anchor="w")

    def start_sequence(self):
        # Display selected method
        selected_method = self.method_var.get()
        messagebox.showinfo("Selected Method", f"Selected Method: {selected_method}")

        # Run the sequence based on the selected method
        if selected_method == "None":
            print("No method selected.")
            # Handle the case where no method is selected
        else:
            print(f"Running sequence for {selected_method}...")
            # Call run_seegene_launcher_sequence with the appropriate parameters

# # Create the main window
# root = tk.Tk()
# app = AppController(root)
# root.mainloop()
