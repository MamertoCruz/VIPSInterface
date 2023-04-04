from tkinter import *
import serial.tools.list_ports
import threading
import time

def connect_menu_init():
    global root, connect_btn, refresh_btn
    root = Tk()
    root.title("VIPS Pressure Readings")
    root.geometry("500x500")
    #root.config(bg="white")
    bg = PhotoImage(file = "VIPS_Logo.png")
    bg_label = Label(root, image=bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    port_label = Label(root, text = "Available Port(s): ", bg="white")
    port_label.grid(column = 1, row = 2, pady = 20, padx = 10)

    port_bd = Label(root, text = "Baude Rate: ", bg="white")
    port_bd.grid(column = 1, row = 3, pady = 20, padx = 10)

    refresh_btn = Button(root, text = "R", height = 2, width = 10, command = update_coms)
    refresh_btn.grid(column = 3, row = 2)

    connect_btn = Button(root, text = "Connect", height = 2, 
                         width = 10, state = "disabled", command = connection)
    connect_btn.grid(column=3,row=4)
    baud_select()
    update_coms()

def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"

def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-",
           "300",
           "600",
           "1200",
           "2400",
           "4800",
           "9600",
           "14400",
           "19200",
           "28800",
           "38400",
           "56000",
           "57600",
           "115200",
           "128000",
           "256000"]
    clicked_bd.set(bds[6])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command = connect_check)
    drop_bd.config(width = 20)
    drop_bd.grid(column = 2, row = 3, padx = 50)

def update_coms():
    global clicked_com, drop_COM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0,"-")
    
    try:
        drop_COM.destroy()
    except:
        pass

    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_COM = OptionMenu(root, clicked_com, *coms, command = connect_check)
    drop_COM.config(width = 20)
    drop_COM.grid(column = 2, row = 2, padx = 50)
    connect_check(0)

#def readSerial():
#    global serialData
#    while serialData:
#        data = ser.readline()
        #needles = re.match("(\d+);(\d+)",data)
        #if needles:
        #    print("Got: {} {} {}".format(needles[0], needles[1]))
        #if len(data) > 0:
#        try:
#            sensor = data.decode('ascii')
#            print(sensor)
#            print("hi")
#        except:
#            pass

#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
serBuffer = ""

def readSerial():
    global p1, p2
    while serialData:
            data = ser.readline()
            data = str(data,'utf-8')
            p1, p2 = data.split(';')
            p1 = float(p1)
            p2 = float(p2)
            print(p1, end=' ')
            print(p2)

def connection():
    global ser, serialData
    if connect_btn["text"] in "Disconnect":
        serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"
    else:
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disabled"
        drop_bd["state"] = "disabled"
        drop_COM["state"] = "disabled"
        port = clicked_com.get()
        baud = clicked_bd.get()
        try:
            ser = serial.Serial(port, baud, timeout=10)
            time.sleep(2)
        except:
            pass
        t1 = threading.Thread(target = readSerial)
        t1.deamon = True
        t1.start()


connect_menu_init()

root.mainloop()