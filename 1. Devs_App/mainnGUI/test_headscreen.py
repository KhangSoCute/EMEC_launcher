from tkinter import *
import tkinter
import tkinter as tk
import customtkinter
import time
from PIL import Image, ImageTk

WIDTH_GUI_LOADING = 600
HEIGHT_GUI_LOADING = 400

root = customtkinter.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI_LOADING/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI_LOADING/2))
customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light,Blue

root.geometry("{}x{}+{}+{}".format(WIDTH_GUI_LOADING,HEIGHT_GUI_LOADING,x_cordinate,y_cordinate))
root.overrideredirect(True)

logo_image = customtkinter.CTkImage(Image.open('logo_PD-removebg.png'), size=(100, 100))
label_logo_bme = customtkinter.CTkLabel(root,image=logo_image)
label_logo_bme.grid(row=0, column=0)

time.sleep(3)

root.mainloop()