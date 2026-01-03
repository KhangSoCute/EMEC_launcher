import customtkinter
import os
from tkinter import filedialog

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("500x500")
app.title("Main screen")

def save_info():
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected directory:", file_path)
    

# USER INPUT
frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

patient_name = customtkinter.CTkLabel(master=frame_1,
                                        text='Enter path to .med',
                                        font=("Roboto Medium", -12))
patient_name.grid(row=2, column=0, pady=0, padx=0, sticky='w')

# entry_name =  customtkinter.CTkEntry(master=frame_1,
#                                     width=50,
#                                     placeholder_text="Enter path to .med")
# entry_name.grid(row=3, column=0, columnspan=2, pady=0, padx=10, sticky="we")

save_button = customtkinter.CTkButton(master=frame_1,
                                        text="Browsers",
                                        command = lambda: save_info(),
                                        font=("Roboto Bold", -12))
save_button.grid(row=8, column=0, pady=10, padx=10,sticky='w')

app.mainloop()