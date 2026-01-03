import tkinter as tk
import serial
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

        # Open the serial port for the barcode scanner
        self.ser = serial.Serial('COM3', 9600, timeout=0.2)

    def show_sample_input(self):
        # Check if the number of samples is positive and not empty
        try:
            num_samples = int(self.num_samples_entry.get())
            if num_samples <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of samples must be a positive integer")
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

        # Start listening for barcode scans
        self.sample_input_window.after(100, self.listen_for_scans)

    def listen_for_scans(self):
        # Read a barcode scan from the serial port and fill in the corresponding sample entry field
        try:
            scan = self.ser.readline().decode().strip()
        except serial.SerialException:
            messagebox.showerror("Error", "Barcode scanner not detected")
            return

        for i, entry in enumerate(self.sample_entries):
            if scan == f"Sample {i+1}":
                entry.insert(0, "Scanned")
                break

        # Continue listening for scans
        self.sample_input_window.after(100, self.listen_for_scans)

    def back_to_main_window(self):
        # Close the serial port and destroy the sample input window
        self.sample_input_window.destroy()
        self.ser.close()

    def save_samples(self):
        # Get the values of each sample and check that they are valid
        sample_values = []
        for entry in self.sample_entries:
            value = entry.get().strip()

            # Check if the value was entered from the keyboard or the barcode scanner
            if value == "Scanned":
                scan = self.ser.readline().decode().strip()
                if scan.startswith("Value"):
                    value = scan.split(":")[1].strip()

            try:
                value = float(value)
            except ValueError:
                tk.messagebox.showerror("Error", "Sample values must be numeric")
                return

            sample_values.append(value)

        # Print the sample values
        print(sample_values)

        # Close the serial port and destroy the
