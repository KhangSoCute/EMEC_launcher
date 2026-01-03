import tkinter as tk
from tkinter import messagebox

class SampleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sample GUI")

        # Create the label and entry widget for number of samples
        self.num_samples_label = tk.Label(master, text="Enter number of samples:")
        self.num_samples_label.pack()

        self.num_samples_entry = tk.Entry(master)
        self.num_samples_entry.pack()

        # Create the "Enter" button
        self.enter_button = tk.Button(master, text="Enter", command=self.show_sample_input)
        self.enter_button.pack()

    def show_sample_input(self):
        # Check if the number of samples is positive and not empty
        try:
            num_samples = int(self.num_samples_entry.get())
            if num_samples <= 0:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Number of samples must be a positive integer")
            return

        # Create a new window for sample input
        self.sample_input_window = tk.Toplevel(self.master)
        self.sample_input_window.title("Sample Input")

        # Create a label and entry widget for each sample
        self.sample_entries = []
        for i in range(num_samples):
            sample_label = tk.Label(self.sample_input_window, text=f"Enter value for sample {i+1}:")
            sample_label.pack()

            sample_entry = tk.Entry(self.sample_input_window)
            sample_entry.pack()

            self.sample_entries.append(sample_entry)

        # Create a "Save" button and a "Back" button
        save_button = tk.Button(self.sample_input_window, text="Save", command=self.save_samples)
        save_button.pack()

        back_button = tk.Button(self.sample_input_window, text="Back", command=self.back_to_main_window)
        back_button.pack()

    def back_to_main_window(self):
        # Destroy the sample input window and return to the main window
        self.sample_input_window.destroy()

    def save_samples(self):
        # Get the values of each sample and check that they are valid
        sample_values = []
        for entry in self.sample_entries:
            try:
                value = float(entry.get())
            except ValueError:
                messagebox.showerror("Error", "Sample values must be numeric")
                return

            sample_values.append(value)

        # Print the sample values
        print(sample_values)

        # Destroy the sample input window and return to the main window
        self.sample_input_window.destroy()


# Create the main window and run the GUI
root = tk.Tk()
sample_gui = SampleGUI(root)
root.mainloop()
