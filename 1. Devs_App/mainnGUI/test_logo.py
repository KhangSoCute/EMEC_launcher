# Importing Tkinter module
from tkinter import *
from tkinter.ttk import *
  
# Creating master Tkinter window
master = Tk()
  
# Setting icon of master window
master.iconphoto(False, 'logo_PD-removebg.png')
  
# Creating button
b = Button(master, text = 'Click me !')
b.pack(side = TOP)
  
# Infinite loop can be terminated by
# keyboard or mouse interrupt
# or by any predefined function (destroy())
mainloop()