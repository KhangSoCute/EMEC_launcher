import socket
import concurrent.futures

def get_device_name(ip_address):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout value of 1 second
            sock.connect((ip_address, 80))
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
    except (socket.herror, socket.timeout):
        return "Unknown"

# Example IP range to scan
ip_range = "172.18.10."
start_ip = 1
end_ip = 10

with concurrent.futures.ThreadPoolExecutor() as executor:
    ip_addresses = [ip_range + str(i) for i in range(start_ip, end_ip + 1)]
    results = executor.map(get_device_name, ip_addresses)

for ip, result in zip(ip_addresses, results):
    print(f"Device name for {ip}: {result}")
