from tkinter import *

gui = Tk()

gui.geometry("500x200")

bg= PhotoImage(file = "VIPS_Logo.png")

label1= Label(gui, image = bg)
label1.place(x = 0, y = 0)

label2 = Label(gui, text = "Welcome", bg = "#88cffa")
label2.pack(pady = 50)

frame1 = Frame(gui, bg = "#88cffa")
frame1.pack(pady = 20)

gui.mainloop()

