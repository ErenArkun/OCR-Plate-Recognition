import serial.tools.list_ports
from tkinter.ttk import *
from tkinter import *
import tkinter as tk
import serial

# Serial Port seçim butonlarını oluştur
serial_ports = serial.tools.list_ports.comports()
port_buttons = []

serial_port = serial.Serial()

root = tk.Tk()
root.state("zoomed")

myfont = ("Helvetica", 16, "bold")

lists = Frame(root, bg="lightgray")
lists.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.15)

def connect(port):
    global serial_port
    # Daha önceki bir seri bağlantı varsa kapat
    if serial_port is not None:
        serial_port.close()
    try:
        serial_port.port = port
        serial_port.baudrate = 9600
        serial_port.open()
        print("baglandi")
    except:
        print("baglanmadi")

def upgrade_list():
    for widg in lists.winfo_children():
        widg.destroy()

    serial_ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(serial_ports):


        b = tk.Button(lists, font=("Helvetica", "15"), text="{} \n{}".format(port, desc), command=lambda port=port: connect(port), height=4)
        b.pack(padx=2, pady=5)
        port_buttons.append(b)

def on():
    serial_port.write(b'H')
    print("led acik")

led_on = Button(root, text="ON", font=myfont, command=on)
led_on.place(relx=0.4, rely=0.85, relwidth=0.07, relheight=0.07)
def page2():
    for widget in root.winfo_children():
        widget.destroy()
def off():
    serial_port.write(b'L')
    print("led kapali")
    page2()

led_off = Button(root, text="OFF", font=myfont, command=off)
led_off.place(relx=0.5, rely=0.85, relwidth=0.07, relheight=0.07)

rst_btn = Button(root, text="Yenile", font=myfont, command=upgrade_list)
rst_btn.place(relx=0.85, rely=0.85, relwidth=0.07, relheight=0.07)





root.mainloop()