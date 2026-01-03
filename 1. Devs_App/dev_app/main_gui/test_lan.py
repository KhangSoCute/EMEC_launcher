import tkinter as tk
from tkinter import ttk
import socket

def scan_ports():
    port_list = []
    num_ports = int(port_entry.get())
    for port in range(1, num_ports + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((host_entry.get(), port))
        if result == 0:
            port_list.append(port)
        sock.close()
    
    if len(port_list) == 0:
        result_label.configure(text="No open ports found")
    else:
        result_label.configure(text="Open ports:")
        port_combobox['values'] = port_list

# Create the main window
window = tk.Tk()
window.title("LAN Port Scanner")

# Create the GUI elements
host_label = ttk.Label(window, text="Enter the host (e.g., IP address or domain name) to scan:")
host_label.pack(pady=10)

host_entry = ttk.Entry(window)
host_entry.pack(pady=5)

port_label = ttk.Label(window, text="Enter the number of ports to scan (e.g., 100):")
port_label.pack(pady=10)

port_entry = ttk.Entry(window)
port_entry.pack(pady=5)

scan_button = ttk.Button(window, text="Scan", command=scan_ports)
scan_button.pack(pady=5)

result_label = ttk.Label(window, text="")
result_label.pack(pady=10)

port_combobox = ttk.Combobox(window, state="readonly")
port_combobox.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()
