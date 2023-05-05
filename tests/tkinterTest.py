from tkinter import *
import ImageTk

gui = Tk()

gui.geometry("600x400")
gui.title("Test")

frame = Frame(gui)
frame.pack()

canvas = Canvas(frame, bg="black", width=500, height=500)
canvas.pack()

photoimage = ImageTk.PhotoImage(file="VIP_Logo.png")
canvas.create_image(600, 400, image=photoimage)

#t.mainloop()

#ibg= PhotoImage(file = "VIPS_Logo.png")

#canvas1 = Canvas( gui, width = 400,
#                 height = 400)
  
#canvas1.pack(fill = "both", expand = True)
  
# Display image
#canvas1.create_image( 0, 0, image = ibg, 
                   #  anchor = "nw")
  
#gui['bg']='green'

# Add Text
#canvas1.create_text( 200, 250, text = "Welcome")
  
#label1= Label(gui, image = bg)
#label1.place(x = 0, y = 0)

#label2 = Label(gui, text = "Welcome", bg = "#88cffa")
#label2.pack(pady = 50)

#frame1 = Frame(gui, bg = "#88cffa")
#frame1.pack(pady = 20)

gui.mainloop()

