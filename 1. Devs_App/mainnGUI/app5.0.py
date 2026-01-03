import tkinter as tk

class SampleInputGUI:
    def __init__(self):
        self.samples = []

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Sample Input GUI")

        # Create the sample input frame
        self.sample_frame = tk.Frame(self.root)
        self.sample_label = tk.Label(self.sample_frame, text="Number of Samples:")
        self.sample_entry = tk.Entry(self.sample_frame)
        self.sample_button = tk.Button(self.sample_frame, text="Enter", command=self.on_sample_button_click)
        self.sample_label.pack(side=tk.LEFT)
        self.sample_entry.pack(side=tk.LEFT)
        self.sample_button.pack(side=tk.LEFT)

        # Create the input value frame
        self.input_frame = tk.Frame(self.root)
        self.input_label = tk.Label(self.input_frame, text="Input Value:")
        self.input_entry = tk.Entry(self.input_frame)
        self.input_button = tk.Button(self.input_frame, text="Enter", command=self.on_input_button_click)
        self.input_label.pack(side=tk.LEFT)
        self.input_entry.pack(side=tk.LEFT)
        self.input_button.pack(side=tk.LEFT)

        # Create the display frame
        self.display_frame = tk.Frame(self.root)
        self.display_button = tk.Button(self.display_frame, text="Display", command=self.on_display_button_click)
        self.display_button.pack()

        # Pack the frames
        self.sample_frame.pack()
        self.input_frame.pack()
        self.display_frame.pack()

    def on_sample_button_click(self):
        # Get the number of samples from the entry widget
        num_samples = int(self.sample_entry.get())

        # Create a new window for the sample values
        self.sample_window = tk.Toplevel(self.root)
        self.sample_window.title("Sample Values")

        # Create a listbox to display the sample values
        self.sample_listbox = tk.Listbox(self.sample_window)
        for i in range(1, num_samples + 1):
            self.samples.append("Sample {}".format(i))
            self.sample_listbox.insert(tk.END, "Sample {}".format(i))
        self.sample_listbox.pack()

        # Set the focus to the input entry widget
        self.input_entry.focus()

    def on_input_button_click(self):
        # Get the input value from the entry widget
        value = self.input_entry.get()

        # Add the input value to the list of input values
        if hasattr(self, "values"):
            self.values.append(value)
        else:
            self.values = [value]

        # Clear the input entry widget
        self.input_entry.delete(0, tk.END)

    def on_display_button_click(self):
        # Create a new window for the input values
        self.display_window = tk.Toplevel(self.root)
        self.display_window.title("Input Values")

        # Create a listbox to display the input values
        self.display_listbox = tk.Listbox(self.display_window)
        for i in range(len(self.samples)):
            sample = self.samples[i]
            if i < len(self.values):
                value = self.values[i]
            else:
                value = ""
            self.display_listbox.insert(tk.END, "{:<20}{}".format(sample, value))
        self.display_listbox.pack()

sample_input_gui = SampleInputGUI()
sample_input_gui.root.mainloop()
