import os
import subprocess
import time
from datetime import datetime

class SeegeneLauncherLogController:
    def __init__(self, seegene_launcher_path, log_directory):
        self.seegene_launcher_path = seegene_launcher_path
        self.log_directory = log_directory
        self.script_start_time = None
        self.launcher_process = None

    def start_launcher(self):
        self.script_start_time = datetime.now()
        self.launcher_process = subprocess.Popen([self.seegene_launcher_path])
        print(f"Seegene Launcher started at {self.script_start_time}")

    def wait_for_launcher(self):
        if self.launcher_process:
            self.launcher_process.wait()
        print("Seegene Launcher closed.")

    def read_log_and_save_output(self, output_file_path='output.txt'):
        output_lines = []
        log_file_path = os.path.join(self.log_directory, 'Launcherlog.log')

        try:
            with open(log_file_path, 'r') as log_file:
                for line in log_file:
                    if line and line[:23] != '':
                        try:
                            timestamp_str = line[:23]
                            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')

                            if timestamp >= self.script_start_time:
                                output_lines.append(line)
                        except ValueError:
                            pass
        except FileNotFoundError:
            print(f"Log file not found: {log_file_path}")

        with open(output_file_path, 'w') as output_file:
            output_file.writelines(output_lines)
        print(f"Output saved to {output_file_path}")

    def keyword_checking(self):
        output_file_path = 'output.txt'
        keyword = "Method Complete"

        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as output_file:
                for line in output_file:
                    if keyword in line:
                        print("Method Complete found.")
                        return True
                else:
                    print("Method Complete not found.")
                    # Add additional actions or raise an exception if needed.
                    return False
        else:
            print("Output file not found.")
            return False
        
