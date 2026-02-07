import csv
#import serial
import os
import tkinter as tk
from tkinter import *
import time
import xlsxwriter
import threading
import schedule
from datetime import datetime
from eingabe import *

global userdata
file_lock = threading.Lock() #lock log file while writting log to log file to insure log file file log
try:
    with open("userdata.txt", "r") as file:
        userdata = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    input("ERROR keine werte gefunden bitte txt namens userdata.txt im selben ordner anlegen")


def userchanges():
    variables = [e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get(), e10.get(), e11.get(), e12.get(), e13.get()]
    print(variables)
    file = open("userdata.txt", "w")
    for variable in variables:
        file.write(variable + "\n")
    file.close()
    update()

def reset():
    file=open("userdata-STANDART.txt","r")
    fileContent=file.read()
    file.close()
    file=open("userdata.txt","w")
    file.write(fileContent)
    file.close()
    update()

def log(logM):
    print(logM)
    my_list = []
    for i in logM:
        my_list.append(i)
    with file_lock:
        with open("log-file.csv", "a", newline="") as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerows([my_list])

#funktionen haupt 
def luft():
    logM2 = "Luefter aus"
    logM1 = "Heizung Aus"
    if LuftTemp < float(userdata[0]):
        logM1 = "Heizung An"
    elif LuftTemp > float(userdata[1]):
        logM1 = "Heizung Aus"

    if LuftHUM < 95: #KOSNTANT
        logM2 = "Luefter ein"
    elif LuftHUM > 90: #KOSNTANT
        logM2 = "Luefter aus"
    now = datetime.now()
    logM = now.strftime("%H:%M:%S"), "Luft", logM1, logM2
    threading.Thread(target=log, args=(logM,)).start()

def wasser():
    logM1 = "Heizung Aus"
    logM2 = "Alle PH motoren aus"
    if WasserTemp < float(userdata[2]):
        logM1 = "Heizung An"
    elif WasserTemp > float(userdata[3]):
        logM1 = "Heizung Aus"

    if WasserPH <= float(userdata[4]):
            logM2 = "Laugenmotor ein"
    elif WasserPH >= float(userdata[5]):
            logM2 = "Laugenmotor aus"
    elif WasserPH >= float(userdata[6]):
            logM2 = "Säurenmotor ein"
    elif WasserPH <= float(userdata[7]):
            logM2 = "Säurenmotor aus"

    now = datetime.now()
    logM = now.strftime("%H:%M:%S"), "Wasser", logM1, logM2
    threading.Thread(target=log, args=(logM,)).start()

def erde():
    logM1 = "Heizung Aus"
    logM2 = "Duengerpumpe aus"
    if ErdTemp < float(userdata[10]):
        logM1 = "Heizung An"
    elif ErdTemp > float(userdata[11]):
        logM1 = "Heizung Aus"
    if ErdEC <= float(userdata[12]):
        logM2 = "Duengerpumpe An"
    elif  ErdEC >= 2:
        logM2 = "Duengerpumpe aus"

    now = datetime.now()
    logM = now.strftime("%H:%M:%S"), "Erde", logM1, logM2
    threading.Thread(target=log, args=(logM,)).start()

def licht(): #licht main
    now = datetime.now()
    Lstatus = 0 # anti log spamm
    while True:  #licht steurrung 1
        Htime = now.strftime("%H")
        if str(Htime).startswith('0'):
            Htime = int(str(Htime)[1:])

        if int(Htime) < 18 and int(Htime) >= 6:
            if Lumen <= float(userdata[8]) and Lstatus == 0: #ein

                logM = now.strftime("%H:%M:%S"), "Licht", "Licht ein"
                threading.Thread(target=log, args=(logM,)).start()
                Lstatus = 1
            elif Lumen >= float(userdata[9]) and Lstatus == 1: #aus

                logM = now.strftime("%H:%M:%S"), "Licht", "Licht aus"
                threading.Thread(target=log, args=(logM,)).start()
                Lstatus = 0

        time.sleep(1)

def licht2(status):
    now = datetime.now()
    if status == 0:
        logM = now.strftime("%H:%M:%S"), "Licht", "Licht aus"
        threading.Thread(target=log, args=(logM,)).start()
    elif status == 1:
        logM = now.strftime("%H:%M:%S"), "Licht", "Licht ein"
        threading.Thread(target=log, args=(logM,)).start()
#GUI
def new_window():
    global window
    window = Tk()
    window.title("Hello Garden")
    window.geometry("1200x800")
    bg = PhotoImage(file="bild.gif")
    my_label = Label(window, image=bg)
    window.resizable(False, False)

    global e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13

    # CANVAS stuff.. ich hasse es

    my_canvas = Canvas(window, width=1200, height=800, bd=0, highlightthickness=0)
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(0, 0, image=bg, anchor="nw")

    my_canvas.create_text(150, 30, text="Luft", fill="red", font=('Arial', 25))
    my_canvas.create_text(450, 30, text="Wasser", fill="red", font=('Arial', 25))
    my_canvas.create_text(750, 30, text="Erde", fill="red", font=('Arial', 25))
    my_canvas.create_text(1050, 30, text="Licht", fill="red", font=('Arial', 25))
    my_canvas.create_text(75, 70, text="Temp. Heizung ein unter", fill="blue", font=('Arial', 10)) #x - 75 y + 10
    my_canvas.create_text(75, 110, text="Temp. Heizung aus über", fill="blue", font=('Arial', 10))

    my_canvas.create_text(375, 70, text="Temp. Heizung ein unter", fill="blue", font=('Arial', 10))
    my_canvas.create_text(375, 110, text="Temp. Heizung aus über", fill="blue", font=('Arial', 10))
    my_canvas.create_text(375, 150, text="PH Laugenmotor ein", fill="blue", font=('Arial', 10))
    my_canvas.create_text(375, 190, text="PH Laugenmotor aus", fill="blue", font=('Arial', 10))
    my_canvas.create_text(375, 230, text="PH Säurenmotor ein", fill="blue", font=('Arial', 10))
    my_canvas.create_text(375, 270, text="PH Säurenmotor aus", fill="blue", font=('Arial', 10))

    my_canvas.create_text(675, 70, text="Temp. Heizung ein unter", fill="blue", font=('Arial', 10))
    my_canvas.create_text(675, 110, text="Temp. Heizung aus über", fill="blue", font=('Arial', 10))
    my_canvas.create_text(675, 150, text="EC Düngerpumpe ein", fill="blue", font=('Arial', 10))

    my_canvas.create_text(1000, 70, text="Lumen licht ein", fill="blue", font=('Arial', 10))
    my_canvas.create_text(1000, 110, text="Lumen licht aus", fill="blue", font=('Arial', 10))



    e1 = Entry(window, fg="black", bd=0)
    e2 = Entry(window, fg="black", bd=0)
    e3 = Entry(window, fg="black", bd=0)
    e4 = Entry(window, fg="black", bd=0)
    e5 = Entry(window, fg="black", bd=0)
    e6 = Entry(window, fg="black", bd=0)
    e7 = Entry(window, fg="black", bd=0)
    e8 = Entry(window, fg="black", bd=0)
    e9 = Entry(window, fg="black", bd=0)
    e10 = Entry(window, fg="black", bd=0)
    e11 = Entry(window, fg="black", bd=0)
    e12 = Entry(window, fg="black", bd=0)
    e13 = Entry(window, fg="black", bd=0)

    e1.insert(0, userdata[0])
    e2.insert(0, userdata[1])
    e3.insert(0, userdata[2])
    e4.insert(0, userdata[3])
    e5.insert(0, userdata[4])
    e6.insert(0, userdata[5])
    e7.insert(0, userdata[6])
    e8.insert(0, userdata[7])
    e9.insert(0, userdata[8])
    e10.insert(0, userdata[9])
    e11.insert(0, userdata[10])
    e12.insert(0, userdata[11])
    e13.insert(0, userdata[12])

    e1_w = my_canvas.create_window(150, 60, anchor="nw", window=e1)
    e2_w = my_canvas.create_window(150, 100, anchor="nw", window=e2)
    e3_w = my_canvas.create_window(450, 60, anchor="nw", window=e3)
    e4_w = my_canvas.create_window(450, 100, anchor="nw", window=e4)
    e5_w = my_canvas.create_window(450, 140, anchor="nw", window=e5)
    e6_w = my_canvas.create_window(450, 180, anchor="nw", window=e6)
    e7_w = my_canvas.create_window(450, 220, anchor="nw", window=e7)
    e8_w = my_canvas.create_window(450, 260, anchor="nw", window=e8) 
    e9_w = my_canvas.create_window(1050, 60, anchor="nw", window=e9) 
    e10_w = my_canvas.create_window(1050, 100, anchor="nw", window=e10) 
    e11_w = my_canvas.create_window(750, 60, anchor="nw", window=e11) 
    e12_w = my_canvas.create_window(750, 100, anchor="nw", window=e12) 
    e13_w = my_canvas.create_window(750, 140, anchor="nw", window=e13) 


    button1 = Button(window, text='Save', bd=0, bg="black", fg="white", height= 3, width=15, command=userchanges)
    button2 = Button(window, text='Reset all', bd=0, bg="black", fg="white", height=3, width=15, command=reset) 

    button1 = my_canvas.create_window(500, 700, anchor="nw", window=button1)
    button1 = my_canvas.create_window(700, 700, anchor="nw", window=button2)

    window.mainloop()

def update():
    global userdata
    try:
        window.destroy()
        with open("userdata.txt", "r") as file:
            userdata = [line.strip() for line in file.readlines()]
        print(userdata)
    except Exception as e:
        print(e)

    now = datetime.now()
    print("hello garden, starting window")
    new_window()

def main():
    while True:
            #
               #implimentieren von abrufen aktueller werte aus eingabe.py und werte per arg weiter geben
        print("sim werte check")
            #
        wasser()
        erde()
        luft()
        time.sleep(300) #5 minuten update circle = 300, "time.sleep kann nach wochen langem betrieb den thread beenden"


threading.Thread(target=main).start()
threading.Thread(target=licht).start()
schedule.every().day.at("18:00").do(licht2,1) #06:00
schedule.every().day.at("20:00").do(licht2,0) #20:00
schedule.run_pending()
update()