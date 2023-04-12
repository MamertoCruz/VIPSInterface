from tkinter import *
import serial.tools.list_ports
import threading
import time
import csv
#import pandas as pd
#import numpy as np
#import array

class Graphics():
    pass

def connect_menu_init():
    global root, connect_btn, refresh_btn, graph
    root = Tk()
    root.title("VIPS Pressure Readings")
    root.geometry("500x500")
    root.config(bg="white")

    port_label = Label(root, text = "Available Port(s): ", bg="white")
    port_label.grid(column = 1, row = 2, pady = 20, padx = 10)

    port_bd = Label(root, text = "Baude Rate: ", bg="white")
    port_bd.grid(column = 1, row = 3, pady = 20, padx = 10)

    refresh_btn = Button(root, text = "Refresh", height = 2, width = 10, command = update_coms)
    refresh_btn.grid(column = 3, row = 2, padx=(0,20))

    connect_btn = Button(root, text = "Connect", height = 2, 
                            width = 10, state = "disabled", command = connection)
    connect_btn.grid(column=3,row=4, padx=(0,20))
    baud_select()
    update_coms()

    graph = Graphics()

    graph.canvas = Canvas(root, width = 450, height = 300, bg="white", highlightthickness=0)
    graph.canvas.grid(row = 5, columnspan = 4, padx=25, pady=10)
    #Static Text
    graph.inlet = graph.canvas.create_text(110,100, anchor = CENTER, font = ("Helvetica", "18"), text = "Inlet Pressure: ")
    graph.outlet = graph.canvas.create_text(110,200, anchor = CENTER, font = ("Helvetica", "18"), text = "Outlet Pressure: ")

    #Dynamic Text
    graph.p1Box = graph.canvas.create_rectangle(225,75,325,125,fill="white")
    graph.p2Box = graph.canvas.create_rectangle(225,175,325,225,fill="white")
    graph.p1 = graph.canvas.create_text(275,100, anchor = CENTER, font = ("Helvetica", "20"), text = "---")
    graph.p2 = graph.canvas.create_text(275,200, anchor = CENTER, font = ("Helvetica", "20"), text = "---")

    #Label Text
    graph.p1Label = graph.canvas.create_text(400,100, anchor = CENTER, font = ("Helvetica", "18"), text = "mmHg")
    graph.p2Label = graph.canvas.create_text(400,200, anchor = CENTER, font = ("Helvetica", "18"), text = "mmHg")

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

def readSerial():
    global serialData, p1, p2, graph
    global tArray, inlet, outlet
    tArray = []
    t = 0;
    inlet = []
    outlet = []
    while serialData:
            data = ser.readline()
            data = str(data,'utf-8')
            try:
                p1, p2 = data.split(';')
                p1 = float(p1)
                p2 = float(p2)
                t +=1
                tArray.append(t)
                inlet.append(p1)
                outlet.append(p2)
                graph.canvas.itemconfig(graph.p1, text= p1)
                graph.canvas.itemconfig(graph.p2, text= p2)
                change_color(float(p1), float(p2))
            except:
                pass

def connection():
    global ser, serialData, tArray, inlet, outlet
    if connect_btn["text"] in "Disconnect":
        serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"
        ser.close()
        graph.canvas.itemconfig(graph.p1Box, fill= "white")
        graph.canvas.itemconfig(graph.p2Box, fill= "white")
        graph.canvas.itemconfig(graph.p1, text= "---")
        graph.canvas.itemconfig(graph.p2, text= "---")
        #inlet = np.array(inlet)
        #outlet = np.array(outlet)
        #output = np.column_stack(inlet.flatten(), outlet.flatten())
        #np.savetxt("pressure.csv", output, delimiter=" ", fmt="% 5d")
        #print(inlet)
        #print(outlet)
        #used for validation purposes to be able to record inlet and outlet pressure values
        with open("pressure.csv", "w", newline="") as infile:
            writer = csv.writer(infile)
            writer.writerow(["Time", "Inlet", "Outlet"])
            for i in zip(tArray, inlet, outlet):
                writer.writerow(i)
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

#used to visualize a pressure difference
def change_color(a, b):
    if abs((a - b))  > 1 or abs((b-a)) > 1:
        graph.canvas.itemconfig(graph.p1Box, fill= "red")
        graph.canvas.itemconfig(graph.p2Box, fill= "red")
    else:
        #graph.canvas.configure(bg="green")
        graph.canvas.itemconfig(graph.p1Box, fill= "green")
        graph.canvas.itemconfig(graph.p2Box, fill= "green")

connect_menu_init()

root.mainloop()