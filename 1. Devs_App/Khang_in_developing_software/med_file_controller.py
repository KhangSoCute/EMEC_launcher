import subprocess

class MedFileController:
    def __init__(self, hxrun_executable):
        self.hxrun_executable = hxrun_executable
        self.process = None

    def open_med_file(self, med_file_path):
        if self.hxrun_executable:
            self.process = subprocess.Popen([self.hxrun_executable, med_file_path])
            print(f"Opening .med file: {med_file_path}")
        else:
            print("HxRun executable not provided. Cannot open .med file.")

    def close_med_file(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            print("Closed .med file.")

# Save this code in 'med_file_controller.py'
