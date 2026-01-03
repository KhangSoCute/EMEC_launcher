import tkinter as tk
import serial.tools.list_ports
import winreg

com_ports = [port.device for port in serial.tools.list_ports.comports()]
print("Available COM ports:", com_ports)

# Get the device name for each COM port
com_ports_with_names = []
for port in com_ports:
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fr"SYSTEM\CurrentControlSet\Enum\{port}") as key:
            device_name = winreg.QueryValueEx(key, "FriendlyName")[0]
            com_ports_with_names.append(f"{port} ({device_name})")
    except FileNotFoundError:
        com_ports_with_names.append(port)

print(com_ports_with_names)

