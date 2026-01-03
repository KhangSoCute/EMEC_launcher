import tkinter as tk
from ping3 import ping
import socket
import json


CONFIG_FILE = "config.json"  # Configuration file name


def save_config():
    config = {
        "ip_addresses": [ip_box.get() for ip_box in ip_boxes],
        "delay": delay_entry.get()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        ip_addresses = config.get("ip_addresses", [])
        delay = config.get("delay", "")
        delay_entry.delete(0, tk.END)
        delay_entry.insert(tk.END, delay)
        for ip in ip_addresses:
            create_ip_box(ip)
    except FileNotFoundError:
        pass


def create_ip_box(ip=""):
    ip_box = tk.Entry(root)
    ip_box.pack()
    ip_box.insert(tk.END, ip)
    ip_boxes.append(ip_box)


def delete_ip_box():
    if ip_boxes:
        ip_box = ip_boxes[-1]
        ip_box.pack_forget()  # Remove from the GUI
        ip_boxes.remove(ip_box)


def check_status():
    result_text.delete(1.0, tk.END)  # Clear previous results
    
    for ip_box in ip_boxes:
        ip = ip_box.get()
        
        if not ip:
            continue  # Skip empty IP boxes
        
        try:
            socket.inet_pton(socket.AF_INET, ip)
        except socket.error:
            result = f"Invalid IP format: {ip}\n"
            result_text.insert(tk.END, result)
            continue  # Skip invalid IP formats

        response = ping(ip)
        if response is not None:
            result = f"IP: {ip} is reachable with round-trip time: {response} ms\n"
        else:
            result = f"IP: {ip} is unreachable\n"
        result_text.insert(tk.END, result)
    
    # Schedule the next check after the specified delay (in milliseconds)
    delay = int(delay_entry.get()) * 1000  # Convert delay to milliseconds
    root.after(delay, check_status)


def exit_program():
    save_config()
    root.destroy()


root = tk.Tk()
root.title("IP Status Checker")

# IP Entry Field
ip_label = tk.Label(root, text="Enter IP addresses:")
ip_label.pack()

ip_boxes = []  # List to store IP entry boxes

add_button = tk.Button(root, text="Add IP", command=create_ip_box)
add_button.pack()

delete_button = tk.Button(root, text="Delete IP", command=delete_ip_box)
delete_button.pack()

# Delay Entry Field
delay_label = tk.Label(root, text="Enter delay in seconds:")
delay_label.pack()

delay_entry = tk.Entry(root)
delay_entry.pack()

# Load Configuration
load_config()

# Check Status Button
check_button = tk.Button(root, text="Check Status", command=check_status)
check_button.pack()

# Result Text
result_text = tk.Text(root)
result_text.pack()

# Exit Button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

# Save Configuration on exit
root.protocol("WM_DELETE_WINDOW", exit_program)

root.mainloop()
