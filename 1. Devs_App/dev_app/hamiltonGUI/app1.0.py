import tkinter as tk
from tkinter import messagebox

def on_sample_finish_button_click():
    # Do something with the sample inputs
    sample_inputs = [sample_input.get() for sample_input in sample_inputs_list]
    print(sample_inputs)

    # Close the sample input window
    sample_window.destroy()

def on_back_button_click():
    # Close the sample input window
    sample_window.destroy()

def focus_next_entry(event):
    generate_input_box()

def generate_input_box():
    global current_sample
    global sample_inputs_list
    global num_samples

    if current_sample < num_samples:
        current_sample += 1
        sample_label = tk.Label(sample_window, text=f"Sample {current_sample}:")
        sample_label.grid(row=current_sample, column=0)

        sample_input = tk.Entry(sample_window)
        sample_input.grid(row=current_sample, column=1)
        print(sample_input.get())
        sample_input.bind('<Return>', focus_next_entry)
    else:
        pass

def on_finish_button_click():
    global num_samples
    try:
        num_samples = int(num_samples_input.get())
        if num_samples < 1:
            raise ValueError("Number of samples must be greater than 0")

        # Create the new window
        global sample_window
        sample_window = tk.Toplevel(root)
        sample_window.title("Sample Input")

        # Create the input boxes and buttons in the new window
        global current_sample
        current_sample = 0
        generate_input_box()

        finish_button = tk.Button(sample_window, text="Finish", command=on_sample_finish_button_click)
        finish_button.grid(row=num_samples+1, column=0)

        back_button = tk.Button(sample_window, text="Back", command=on_back_button_click)
        back_button.grid(row=num_samples+1, column=1)

    except ValueError:
        messagebox.showerror("Invalid input", "Number of samples must be a positive integer")

root = tk.Tk()
root.title("Sample Input App")

num_samples_label = tk.Label(root, text="Number of samples:")
num_samples_label.grid(row=0, column=0)

num_samples_input = tk.Entry(root)
num_samples_input.grid(row=0, column=1)

finish_button = tk.Button(root, text="Enter", command=on_finish_button_click)
finish_button.grid(row=0, column=2)

num_samples = 0
current_sample = 0
sample_inputs_list = []

root.mainloop()