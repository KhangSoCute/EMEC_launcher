import tkinter as tk
import serial
import threading
import pandas as pd
import os
import subprocess
import shutil
from tkinter import messagebox
import serial.tools.list_ports
from tkinter import filedialog

class SampleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sample GUI")
        
        self.baudrate = 9600
        self.timeout = 0.2
        self.variable = tk.StringVar()
        self.variable.set("")
        
        self.com_ports = [port.device for port in serial.tools.list_ports.comports()]
        
        print(self.com_ports)

        # Create the label and entry widget for number of samples
        self.num_samples_label = tk.Label(master, text="Enter number of samples:")
        self.num_samples_label.pack()

        self.num_samples_entry = tk.Entry(master)
        self.num_samples_entry.pack()

        # Create the check button for barcode scanner
        self.use_scanner = tk.BooleanVar()
        self.use_scanner.set(False)
        self.use_scanner_button = tk.Checkbutton(master, text="Use barcode scanner", variable=self.use_scanner,
                                                 command=self.toggle_scanner_options)
        self.use_scanner_button.pack()

        # Create the "Enter" button
        self.enter_button = tk.Button(master, text="Enter", command=self.show_sample_input)
        self.enter_button.pack()

        # Initialize scanner options
        self.ser = None
        self.scanner_options_window = None
        self.com_port_entry = None
        self.baudrate_entry = None
        self.timeout_entry = None

    def toggle_scanner_options(self):
        # Show/hide scanner options window based on check button status
        if self.use_scanner.get():
            self.show_scanner_options()
        else:
            self.hide_scanner_options()

    def show_scanner_options(self):
        # Create a new window for scanner options
        self.scanner_options_window = tk.Toplevel(self.master)
        self.scanner_options_window.title("Scanner Options")

        # Create the label and entry widgets for COM port, baudrate, and timeout
        self.com_port_label = tk.Label(self.scanner_options_window, text="COM Port:")
        self.com_port_label.pack()

        self.com_port_option_menu = tk.OptionMenu(self.scanner_options_window,self.variable, *self.com_ports)
        self.com_port_option_menu.pack()

        self.baudrate_label = tk.Label(self.scanner_options_window, text="Baudrate:")
        self.baudrate_label.pack()

        self.baudrate_entry = tk.Entry(self.scanner_options_window)
        self.baudrate_entry.pack()
        self.baudrate_entry.insert(0,str(self.baudrate))

        self.timeout_label = tk.Label(self.scanner_options_window, text="Timeout:")
        self.timeout_label.pack()

        self.timeout_entry = tk.Entry(self.scanner_options_window)
        self.timeout_entry.pack()
        self.timeout_entry.insert(0,str(self.timeout))

        # Create the "Connect" button
        connect_button = tk.Button(self.scanner_options_window, text="Connect", command=self.connect_to_scanner)
        connect_button.pack()
        
        # Set the focus to the COM port option menu
        self.com_port_option_menu.focus()

    def hide_scanner_options(self):
        # Destroy the scanner options window and close the serial port if it was opened
        if self.scanner_options_window is not None:
            self.scanner_options_window.destroy()
        if self.ser is not None:
            self.ser.close()
            self.ser = None

    def connect_to_scanner(self):
        # Connect to the scanner using the specified serial port, baudrate, and timeout
        try:
            com_port = self.variable.get()
            baudrate = int(self.baudrate_entry.get())
            timeout = float(self.timeout_entry.get())
            self.ser = serial.Serial(com_port, baudrate=baudrate, timeout=timeout)
        except serial.SerialException:
            print("Error connecting to scanner")
        
        messagebox.showinfo("Success", "COM available.")
        self.scanner_options_window.destroy()
        
    def show_sample_input(self):
        # Check that the number of samples is valid
        try:
            num_samples = int(self.num_samples_entry.get())
            if num_samples <= 0:
                raise ValueError
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Check if the scanner is being used
        if self.use_scanner.get() and self.ser is None:
            messagebox.showerror("Error", "Barcode scanner not connected")
            return
        
        # Create a new window for sample input
        sample_input_window = tk.Toplevel(self.master)
        sample_input_window.title("Sample Input")
        
        def insert_text(text):
            current_widget = sample_input_window.focus_get()
            # print(current_widget)    
            current_pos = current_widget.index(tk.INSERT)
            current_widget.insert(current_pos, text)
        
        self.is_running = False
        
        def read_from_scanner():
            # This function continuously reads input from the serial port
            while self.is_running:
                data = self.ser.readline().decode('utf-8').strip()
                if data:
                    insert_text(data)
                else:
                    pass
        
        self.thread = None
        
        if self.use_scanner.get():
            self.is_running = True
            self.thread = threading.Thread(target=read_from_scanner, daemon=True)
            self.thread.start()

        # Create a list to store sample data
        sample_data = []
        no_column = 20
        stt_row = 0
        stt_column = 0

        for i in range(num_samples):
            # Create the label and entry widget for each sample
            sample_label = tk.Label(sample_input_window, text="Sample {}".format(i + 1))
            sample_label.grid(row=stt_row, column=stt_column)

            sample_entry = tk.Entry(sample_input_window)
            sample_entry.grid(row=stt_row, column=stt_column+1)
        
            stt_row+=1
            if i >= no_column:
                no_column+=10
                stt_row = 0
                stt_column+=2
                
            # Add the sample data to the list
            sample_data.append(sample_entry)

        # Create the "Save" button
        def save_data():
            # Get the sample data from the entry fields and print it out
            data = [entry.get() for entry in sample_data]
            
            if self.use_scanner and self.thread != None:
                if self.thread.is_alive():
                    self.is_running = False
                    self.thread.join() 

            # Close the sample input window
            sample_input_window.destroy()
            
            self.after_have_data(data)
            
        save_button = tk.Button(sample_input_window, text="Save", command=save_data)
        save_button.grid(row=num_samples, column=1)
        
    def after_have_data(self,data):
        num_cols = ["No.Sample"]
        arr_barcord = data
        
        num_sample = int(self.num_samples_entry.get())
        arr_barcord.insert(0, num_sample)
        
        for i in range(num_sample):
            num = f"No.{i+1}"
            num_cols.append(num)

        df = pd.DataFrame([num_cols,arr_barcord])
        df.to_excel("input.xls", index=False,header=False) #TODO: ignore openyxl
        
        self.insert_to_template(num_sample,data)
        
        messagebox.showinfo("Succeed","Created excel")
        
        self.choose_med_file()
        

    def insert_to_template(self,num_sample,data):
        try:
            if (len(data)-1) != num_sample:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "length of data not equal number of sample")
            return
        keys = ["A","B","C","D","E","F","G","H"]
        
        # Load the template excel file
        template = pd.read_excel('LIMS_HBV_template.xlsx', engine='openpyxl',header=None)
        
        # Create a copy of the template
        output = template.copy()
        
        row_index = 22
        count = 0
        
        # Loop through the number of samples and key values
        for i in range(num_sample):
            for j, key in enumerate(keys):
                if i == 0 and j < 6:
                    pass
                else:
                    output.iloc[row_index,0] = f'{key}0{i+1}'
                    output.iloc[row_index,1] = "FAM"
                    output.iloc[row_index,2] = "HEX"
                    output.iloc[row_index,7] = "Unknown"
                    output.iloc[row_index,9] = "HBV"
                    output.iloc[row_index,10] = "IC"
                    output.iloc[row_index,8] = data[count+1]
                    count+=1
                    row_index+=1
                    if count == num_sample:
                        break
                    
            if count == num_sample:
                break
        
        # Save the output to a new excel file
        output.to_excel('LIMS_HBV_output.xlsx', index=False,header=False)
        
        # Convert PLRN
        # Get the base filename without extension
        filename_base = os.path.splitext('LIMS_HBV_output.xlsx')[0]
        
        # Set the new extension
        new_extension = ".plrn"
        
        # Create the new file name with the new extension
        new_filename = filename_base + new_extension
        
        # Rename the file
        shutil.copyfile('LIMS_HBV.xlsx', new_filename)

    def choose_med_file(self):
        input_med_window = tk.Toplevel(self.master)
        input_med_window.title(".MED")
        
        def choose_path():
            file_path = ""
            file_path = filedialog.askopenfilename()
            if file_path:
                text_box.config(state="normal")
                text_box.delete("1.0", tk.END)
                text_box.insert("1.0", file_path)
                text_box.config(state="disabled")
                check_file_existence(file_path)
        
        def run_med_file(text_box):
            path_exe = "C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe"
            path_med = text_box.get("1.0","end").rstrip().replace("/", "\\")

            try:
                if os.path.isfile(path_exe) or os.path.isfile("C:\Program Files\HAMILTON\Bin\HxRun.exe"):
                    pass
                else:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error running", "You had not install Hamilton Method yet")
                return
            
            try:
                # Construct the command string using string formatting
                command = r'"{}" "{}" /t'.format(path_exe,path_med)
                print(command)
                subprocess.run(command)
            except ValueError as e:
                messagebox.showerror("Error running", e.message)
                return
        
        # function to check if file exists
        def check_file_existence(file_path):
            if os.path.isfile(file_path):
                messagebox.showinfo("File!","File exists!")
                button_med = tk.Button(input_med_window,text="RUN",command = lambda: run_med_file(text_box))
                button_med.grid(row=3,column=0)
            else:
                messagebox.showinfo("File!","File does not exist!")
                text_box.delete("0.0", tk.END)
                for widget in input_med_window.winfo_children():
                    if isinstance(widget, tk.Button) and widget['text'] == "RUN":
                        widget.destroy()
        
        label = tk.Label(input_med_window,text=" choose .med file path")
        label.grid(row=0,column=0)
        med_button = tk.Button(input_med_window,text="Browsers",command = lambda: choose_path()) 
        med_button.grid(row=1,column=0)
        text_box = tk.Text(input_med_window,height=1,state="disabled")
        text_box.grid(row=2,column=0)
         
# Create the main window and run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    sample_gui = SampleGUI(root)
    root.mainloop()