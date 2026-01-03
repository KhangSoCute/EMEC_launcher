import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def scan_ports():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        result_label.configure(text="No COM ports found")
    else:
        result_label.configure(text="Available COM ports:")
        for port in port_list:
            port_combobox['values'] = port_list

# Create the main window
window = tk.Tk()
window.title("COM Port Scanner")

# Create the GUI elements
label = ttk.Label(window, text="Click 'Scan' to find available COM ports")
label.pack(pady=10)

scan_button = ttk.Button(window, text="Scan", command=scan_ports)
scan_button.pack(pady=5)

result_label = ttk.Label(window, text="")
result_label.pack(pady=10)

port_combobox = ttk.Combobox(window, state="readonly")
port_combobox.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()
