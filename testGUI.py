# testGUI.py

import PySimpleGUI as sg

layout = [[sg.Text("Inlet Pressure")]]

sg.Window(title="Pressure Readings", layout=[[]], margins=(100, 50)).read()
