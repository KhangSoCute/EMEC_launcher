from tkinter import *
import tkinter
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
from cv2 import mean
from matplotlib import image
import numpy as np
import customtkinter
import threading
import time

# -------- LOADING SCREEN --------------
def task():
    # The window will stay open until this function call ends.
    time.sleep(2)
    root.destroy()

WIDTH_GUI_LOADING = 600
HEIGHT_GUI_LOADING = 400

root = customtkinter.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI_LOADING/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI_LOADING/2))
customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light

root.geometry("{}x{}+{}+{}".format(WIDTH_GUI_LOADING,HEIGHT_GUI_LOADING,x_cordinate,y_cordinate))
root.overrideredirect(True)

#Draw from here
logo_bme = ImageTk.PhotoImage(Image.open('logo_PD-removebg.png').resize((100, 100), Image.Resampling.LANCZOS))
label_logo_bme = customtkinter.CTkLabel(master=root,text="")
label_logo_bme.grid(row=0, column=0)
label_logo_bme.place(relx=0.5,rely=0.2,anchor='center')
label_logo_bme.configure(image=logo_bme)

title_text = customtkinter.CTkLabel(master=root,text='EASTERN',font=("Roboto Bold", -48),text_color='black')
title_text.grid(row=0, column=0)
title_text.place(relx=0.5, rely=0.5,anchor='center')

root.after(200, task)
root.mainloop()

# -------- MAIN SCREEN --------------
root = customtkinter.CTk()
customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light
customtkinter.set_default_color_theme('green') #green,dark-blue,white

WIDTH_GUI = 800
HEIGHT_GUI = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI/2))

root.geometry("{}x{}+{}+{}".format(WIDTH_GUI,HEIGHT_GUI,x_cordinate,y_cordinate))

# Set GUI
root.title("APP NAME")

# Logo
photo = PhotoImage(file = "logo_PD-removebg.png")
root.iconphoto(False, photo)



root.mainloop()





