from seegene_launcher_log_controller import SeegeneLauncherLogController
from med_file_controller import MedFileController
from app_controller import AppController


# Set paths
seegene_launcher_path = r'C:\Seegene\Seegene Launcher IVD V6\Seegene Launcher IVD V6.exe'
log_directory = r'C:\Seegene\Seegene Launcher IVD V6\log\syslog'
hxrun_executable = r'C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe'
med_file_path = r'C:\Users\Admin\OneDrive - CONG TY TNHH THIET BI Y TE PHUONG DONG\5. EMEC Launcher\2. Hamilton edit method\HAMILTON_STARLET\Methods\EMEC Launcher\STARlet_v6.1 - EMEC Launcher - v1.med'

# Initialize controllers
seegene_controller = SeegeneLauncherLogController(seegene_launcher_path, log_directory)
med_file_controller = MedFileController(hxrun_executable)

# Function containing the sequence of commands
def run_seegene_launcher_sequence():
    # Step 1: Start Seegene Launcher
    seegene_controller.start_launcher()

    # Step 2: Wait for Seegene Launcher to close
    seegene_controller.wait_for_launcher()

    # Step 3: Read log and save output
    seegene_controller.read_log_and_save_output()

    # Step 4: Check for "Method Complete"
    if seegene_controller.keyword_checking():
        # Step 5: Open .med file
        med_file_controller.open_med_file(med_file_path)

        # Wait for user to close HxRun manually
        input("Press Enter when you have finished with HxRun...")

        # Close .med file
        med_file_controller.close_med_file()
    else:
        print("Seegene Launcher method did not complete successfully.")

run_seegene_launcher_sequence();

# # Create an instance of AppController
# app_controller = AppController(run_seegene_launcher_sequence)

# # Run the GUI
# app_controller.run_gui()