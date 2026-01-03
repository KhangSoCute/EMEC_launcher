import tkinter as tk
import serial
import socket
import threading
import serial.tools.list_ports

window = tk.Tk()
window.title("HL7 Data Capture")

label = tk.Label(window, text="Captured Data:")
label.pack()

text_box = tk.Text(window, height=10, width=50)
text_box.pack()

option_var = tk.StringVar()
option_var.set("COM")  # Default option is COM port

option_frame = tk.Frame(window)
option_frame.pack()

port_list = list(serial.tools.list_ports.comports())

com_label = tk.Label(option_frame, text="COM Port:")
com_label.pack(side=tk.LEFT)

com_option = tk.OptionMenu(option_frame, option_var, *port_list, command=lambda x: port_selected(x))
com_option.pack(side=tk.LEFT)

lan_label = tk.Label(option_frame, text="LAN IP:")
lan_entry = tk.Entry(option_frame)
lan_label.pack(side=tk.LEFT)
lan_entry.pack(side=tk.LEFT)

port_label = tk.Label(option_frame, text="Port:")
port_entry = tk.Entry(option_frame)
port_label.pack(side=tk.LEFT)
port_entry.pack(side=tk.LEFT)

monitoring = False  # Variable to track monitoring status
selected_port = None  # Variable to store selected COM port
selected_ip = None  # Variable to store entered IP address
selected_port_num = None  # Variable to store entered port number

def capture_data_from_com():
    ser = serial.Serial(selected_port.device, baudrate=9600, timeout=1)  # Adjust baudrate and timeout as per your needs
    
    while monitoring:
        captured_data = ser.readline().decode().strip()  # Read data line by line
        text_box.insert(tk.END, captured_data + "\n")  # Append the captured data to the text box
        text_box.see(tk.END)  # Scroll to the end of the text box

def capture_data_from_lan():
    ip_address = selected_ip
    port = selected_port_num
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, port))

    while monitoring:
        captured_data = sock.recv(1024).decode().strip()  # Receive data
        text_box.insert(tk.END, captured_data + "\n")  # Append the captured data to the text box
        text_box.see(tk.END)  # Scroll to the end of the text box

def toggle_monitoring():
    global monitoring
    
    if monitoring:
        monitoring = False
        start_button.config(text="Start Monitoring")
    else:
        monitoring = True
        start_button.config(text="Stop Monitoring")
        
        selected_option = option_var.get()

        if selected_option == "COM":
            com_thread = threading.Thread(target=capture_data_from_com)
            com_thread.daemon = True
            com_thread.start()
        elif selected_option == "LAN":
            lan_thread = threading.Thread(target=capture_data_from_lan)
            lan_thread.daemon = True
            lan_thread.start()

def port_selected(selected):
    global selected_port
    selected_port = selected

def start_capture():
    global selected_ip, selected_port_num

    selected_option = option_var.get()

    if selected_option == "LAN":
        selected_ip = lan_entry.get()
        selected_port_num = int(port_entry.get())
        
        if not selected_ip or not selected_port_num:
            return

    toggle_monitoring()

start_button = tk.Button(option_frame, text="Start Monitoring", command=start_capture)
start_button.pack(side=tk.LEFT)

option_menu = tk.OptionMenu(option_frame, option_var, "COM", "LAN", command=lambda x: option_selected(x))
option_menu.pack(side=tk.LEFT)

def option_selected(selected):
    if selected == "COM":
        com_label.pack(side=tk.LEFT)
        com_option.pack(side=tk.LEFT)
        lan_label.pack_forget()
        lan_entry.pack_forget()
        port_label.pack_forget()
        port_entry.pack_forget()
    elif selected == "LAN":
        com_label.pack_forget()
        com_option.pack_forget()
        lan_label.pack(side=tk.LEFT)
        lan_entry.pack(side=tk.LEFT)
        port_label.pack(side=tk.LEFT)
        port_entry.pack(side=tk.LEFT)

option_selected(option_var.get())

window.mainloop()
