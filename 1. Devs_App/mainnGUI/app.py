from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter
import time
import subprocess
from tkinter import filedialog
import serial.tools.list_ports

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Eastern Launcher")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("logo_PD-removebg.ico")
        
        self.browse_label = customtkinter.CTkLabel(master=self,
                                        text='Choose path to .med',
                                        font=("Roboto Medium", -12))
        self.browse_label.grid(row=0, column=0, pady=0, padx=0, sticky='w')

        self.browse_button = customtkinter.CTkButton(master=self,
                                        text="Browsers",
                                        command = lambda: self.choose_path(),
                                        font=("Roboto Bold", -12))
        self.browse_button.grid(row=1, column=0, pady=10, padx=10,sticky='w')
        
        self.textbox_browser = customtkinter.CTkTextbox(self, width=500,height=20,wrap="none")
        self.textbox_browser.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        
        self.sample_input = customtkinter.CTkLabel(master=self,
                                        text='Number of samples',
                                        font=("Roboto Medium", -12))
        self.sample_input.grid(row=3, column=0, pady=0, padx=0, sticky='w')
        
        self.entry_sample = customtkinter.CTkEntry(self, width=100, validate="key",validatecommand=(self.register(self.validate_number), '%P'))     
        self.entry_sample.grid(row=4, column=0, pady=0, padx=0, sticky='w')
        
        self.com_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.variable = customtkinter.StringVar()
        self.variable.set("")
        
        self.optionmenu_tk = customtkinter.CTkOptionMenu(self, variable=self.variable, values=self.com_ports, command=self.select_com)
        self.optionmenu_tk.grid(row=5, column=0, pady=0, padx=0, sticky='w')
        
        self.run_button = customtkinter.CTkButton(master=self,
                                        text="RUN",
                                        command = lambda: self.run(),
                                        font=("Roboto Bold", -12))
        self.run_button.grid(row=6, column=0, pady=10, padx=10,sticky='w')
    
    def choose_path(self):
        self.file_path = ""
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.textbox_browser.delete("0.0", customtkinter.END)
            self.textbox_browser.insert("0.0", self.file_path)

    def validate_number(self,new_value):
        if new_value.isdigit() or new_value == "":
            return True
        return False
    
    def select_com(self,choice):
        pass
        
    def run(self):
        self.loading_window = Toplevel()
        self.loading_window.geometry("300x100")
        self.loading_window.title("Loading")
        self.loading_window.resizable(False, False)
        self.loading_label = Label(self.loading_window, text="Running function...")
        self.loading_label.pack(pady=20)
        self.loading_window.update()
        
        # run the actual function
        time.sleep(3)  
        
        self.loading_window.destroy()
        messagebox.showinfo("Completed", "Function has been completed.")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()