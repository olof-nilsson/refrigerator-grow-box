import os
from tkinter import  ttk,Tk,IntVar,StringVar,Button,messagebox,PhotoImage,OptionMenu
from tkinter.messagebox import askyesno
import settings
import status
import matplotlib.pyplot as plt
import io
from PIL import ImageTk, Image
import threading
import time
import shutil
import Vkeyboard
import datetime

settings = settings.Settings(r'/boot/settings.json')
WIFI_ON_CONFIGURATION_FILE = r'/boot/config.txt_nowifi'
WIFI_OFF_CONFIGURATION_FILE = r'/boot/config.txt_wifi'
WIFI_CONFIGURATION_FILE = r'/boot/config.txt'
WPA_SUPPLICANT = r'/etc/wpa_supplicant/wpa_supplicant.conf'

gui = Tk(className='Refrigerator controller')
# set window size
gui.geometry("1024x600")
gui.attributes("-fullscreen", True) # run fullscreen
gui.wm_attributes("-topmost", True) # keep on top
FontLarge = ("Arial", 24)
button_width = 4
button_height = 2
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Ariel','18','normal') )

Notebook = ttk.Notebook(gui)
tabStatus = ttk.Frame(Notebook)
tabLight = ttk.Frame(Notebook)
tabFan = ttk.Frame(Notebook)
tabHeat = ttk.Frame(Notebook)
tabHistory = ttk.Frame(Notebook)
tabSystem = ttk.Frame(Notebook)
Notebook.add(tabStatus, text= f'{"Status": ^25s}')
Notebook.add(tabLight, text= f'{"Light": ^25s}')
Notebook.add(tabFan, text=f'{"Fan": ^25s}')
Notebook.add(tabHeat, text=f'{"Heating": ^25s}')
Notebook.add(tabHistory, text=f'{"History": ^25s}')
Notebook.add(tabSystem, text=f'{"System": ^25s}')


LightStartHour = IntVar()
LightStartHour.set(settings.LightStartHour)
LightStartHour.trace("w", lambda name, index, mode, LightStartHour=LightStartHour: UpdateSettings(LightStartHour,"LightStartHour"))
LightStartMinute = IntVar()
LightStartMinute.set(settings.LightStartMinute)
LightStartMinute.trace("w", lambda name, index, mode, LightStartMinute=LightStartMinute: UpdateSettings(LightStartMinute,"LightStartMinute"))
LightOnHours = IntVar()
LightOnHours.set(settings.LightOnHours)
LightOnHours.trace("w", lambda name, index, mode, LightOnHours=LightOnHours: UpdateSettings(LightOnHours,"LightOnHours"))
FanOnTemperature = IntVar()
FanOnTemperature.set(settings.FanOnTemperature)
FanOnTemperature.trace("w", lambda name, index, mode, FanOnTemperature=FanOnTemperature: UpdateSettings(FanOnTemperature,"FanOnTemperature"))
FanOffTemperature = IntVar()
FanOffTemperature.set(settings.FanOffTemperature)
FanOffTemperature.trace("w", lambda name, index, mode, FanOffTemperature=FanOffTemperature: UpdateSettings(FanOffTemperature,"FanOffTemperature"))
FanOnHumidity = IntVar()
FanOnHumidity.set(settings.FanOnHumidity)
FanOnHumidity.trace("w", lambda name, index, mode, FanOnHumidity=FanOnHumidity: UpdateSettings(FanOnHumidity,"FanOnHumidity"))
FanOffHumidity = IntVar()
FanOffHumidity.set(settings.FanOffHumidity)
FanOffHumidity.trace("w", lambda name, index, mode, FanOffHumidity=FanOffHumidity: UpdateSettings(FanOffHumidity,"FanOffHumidity"))

PID_Kp = IntVar()
PID_Kp.set(settings.PID_Kp)
PID_Kp.trace("w", lambda name, index, mode, PID_Kp=PID_Kp: UpdateSettings(PID_Kp,"PID_Kp"))
PID_Ki = IntVar()
PID_Ki.set(settings.PID_Ki)
PID_Ki.trace("w", lambda name, index, mode, PID_Ki=PID_Ki: UpdateSettings(PID_Ki,"PID_Ki"))
PID_Kd = IntVar()
PID_Kd.set(settings.PID_Kd)
PID_Kd.trace("w", lambda name, index, mode, PID_Kd=PID_Kd: UpdateSettings(PID_Kd,"PID_Kd"))
PID_setpoint = IntVar()
PID_setpoint.set(settings.PID_setpoint)
PID_setpoint.trace("w", lambda name, index, mode, PID_setpoint=PID_setpoint: UpdateSettings(PID_setpoint,"PID_setpoint"))

WIFI_SSID = StringVar()
WIFI_PASSWORD = StringVar()

def UpdateSettings(var,settingname):
    try:
        res = var.get()
    except Exception as e:
        return
    
    if res is not None and isinstance(res, int):
        if (settingname == "LightStartHour"):
                settings.LightStartHour = res
        if (settingname == "LightStartMinute"):
                settings.LightStartMinute = res
        if (settingname == "LightOnHours"):
                settings.LightOnHours = res
        if (settingname == "FanOnTemperature"):
                settings.FanOnTemperature = res
        if (settingname == "FanOffTemperature"):
                settings.FanOffTemperature = res
        if (settingname == "FanOnHumidity"):
                settings.FanOnHumidity = res
        if (settingname == "FanOffHumidity"):
                settings.FanOffHumidity = res
        if (settingname == "PID_Kp"):
                settings.PID_Kp = res
        if (settingname == "PID_Ki"):
                settings.PID_Ki = res
        if (settingname == "PID_Kd"):
                settings.PID_Kd = res                                                                
        if (settingname == "PID_setpoint"):
                settings.PID_setpoint = res                                                                


def Save(s):
    s.Save()
    messagebox.showinfo("Information","Settings saved to disk!")

def IncOrDecLightTimer(part = 0,IncOrDec = 1):
    if (part==0):
        if (IncOrDec == 1):
            h =  LightStartHour.get() + 1
            if (h>23):
                h=0
        else:
            h =  LightStartHour.get() - 1
            if (h<0):
                h=23           
        settings.LightStartHour = h
        LightStartHour.set(h)    
    else:
        if (IncOrDec == 1):
            m =  LightStartMinute.get() + 1
            if (m>59):
                m=0
        else:
            m =  LightStartMinute.get() - 1
            if (m<0):
                m=59        
        settings.LightStartMinute = m
        LightStartMinute.set(m)    
  

def IncOrDecLightonHours(IncOrDec = 1):
    if (IncOrDec == 1):
        h =  LightOnHours.get() + 1
        if (h>23):
            h=0
    else:
        h =  LightOnHours.get() - 1
        if (h<0):
            h=23            
    settings.LightOnHours = h
    LightOnHours.set(h)    

def IncOrDecFan(part = 0,IncOrDec = 1):
    if (part==0):
        if (IncOrDec == 1):
            ton =  FanOnTemperature.get() + 1
            if (ton>34):
                ton=35
        else:
            ton =  FanOnTemperature.get() - 1
            if (ton<11):
                ton=10           
        settings.FanOnTemperature = ton
        FanOnTemperature.set(ton)    
    elif part==1:
        if (IncOrDec == 1):
            ton =  FanOnTemperature.get()
            toff =  FanOffTemperature.get() + 1
            if (toff>ton-2):
                toff = ton-2
        else:
            ton =  FanOnTemperature.get()
            toff =  FanOffTemperature.get() - 1
            if (toff<ton-10):
                toff=ton-10        
        settings.FanOffTemperature = toff
        FanOffTemperature.set(toff)        
    elif part==2:
        if (IncOrDec == 1):
            fon =  FanOnHumidity.get() + 1
            if (fon>99):
                fon=100
        else:
            fon =  FanOnHumidity.get() - 1
            if (fon<2):
                fon=1           
        settings.FanOnHumidity = fon
        FanOnHumidity.set(fon) 
    elif part==3:           
        if (IncOrDec == 1):
            fon =  FanOnHumidity.get()
            foff =  FanOffHumidity.get() + 1
            if (foff>fon-2):
                foff = fon-2
        else:
            fon =  FanOnHumidity.get()
            foff =  FanOffHumidity.get() - 1
            if (foff<fon-10):
                foff=fon-10        
        settings.FanOffHumidity = foff
        FanOffHumidity.set(foff)             

def IncOrDecPID(part = 0,IncOrDec = 1):
    #Setpoint
    if (part==0):
        if (IncOrDec == 1):
            t_settpoint =  PID_setpoint.get() + 1
            if (t_settpoint>29):
                t_settpoint=30
        else:
            t_settpoint =  PID_setpoint.get() - 1
            if (t_settpoint<1):
                t_settpoint=0           
        settings.PID_setpoint = t_settpoint
        PID_setpoint.set(t_settpoint)  
    #Kp
    if (part==1):
        if (IncOrDec == 1):
            kp =  PID_Kp.get() + 1
        else:
            kp =  PID_Kp.get() - 1
            if (kp<1):
                kp=0           
        settings.PID_Kp = kp
        PID_Kp.set(kp)                   
    #Kb
    if (part==2):
        if (IncOrDec == 1):
            kd =  PID_Kd.get() + 1
        else:
            kd =  PID_Kd.get() - 1
            if (kd<1):
                kd=0           
        settings.PID_Kd = kd
        PID_Kd.set(kd)         
    #Ki
    if (part==3):
        if (IncOrDec == 1):
            ki =  PID_Ki.get() + 1
        else:
            ki =  PID_Ki.get() - 1
            if (ki<1):
                ki=0           
        settings.PID_Kd = ki
        PID_Ki.set(ki)     

def plothist():
    global s,plt,histlabel,gui
    now = datetime.datetime.now().strftime('%H:%M')
    pastlisty=[]
    pastlisty2=[]
    pastlistx=[]
    pastlistx2=[]
    for e in s.temperatureHistory:
       if (now>e):
          pastlistx.append(e)
          pastlisty.append(s.temperatureHistory[e])
       if (now<e):
          pastlistx2.append(e)
          pastlisty2.append(s.temperatureHistory[e])
    y = pastlisty2 + pastlisty
    x = pastlistx2 + pastlistx
    labels=[]
    i=0
    for l in x:
        i=i + 1
        if (i==4):
            labels.append(l[:5])
            i=0
        else:
            labels.append("")
    plt.clf()
    f = plt.figure()
    f.set_figwidth(7)
    f.set_figheight(5)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Temperature', fontsize=12)
    plt.xticks(rotation=90)
    plt.xticks(fontsize=8 )
    plt.plot(x,y)
    plt.xticks(ticks = x, labels = labels)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight',dpi=120)
    img2 = ImageTk.PhotoImage(Image.open(img_buf))
    histlabel.image = img2  # <== this is were we anchor the img object    
    histlabel.configure(image=img2)
    gui.update()
#--------------------------------------------------------Status
img_light_on=PhotoImage(file=r'/usr/local/refrigurator/light_on.png')        
img_light_off=PhotoImage(file=r'/usr/local/refrigurator/light_off.png')        
img_fan_on=PhotoImage(file=r'/usr/local/refrigurator/fan_on.png')        
img_fan_off=PhotoImage(file=r'/usr/local/refrigurator/fan_off.png')        
img_temp=PhotoImage(file=r'/usr/local/refrigurator/temp.png')      
img_humidity=PhotoImage(file=r'/usr/local/refrigurator/humidity.png')      
img_heat_on=PhotoImage(file=r'/usr/local/refrigurator/heat_on.png')      
img_heat_off=PhotoImage(file=r'/usr/local/refrigurator/heat_off.png')      

s = status.Status(r'/mnt/ramdisk/status.json')

Lightlabelvar = StringVar()
if (s.Light):
    Lightlabelvar.set(f"Light on")
else:
    Lightlabelvar.set(f"Light off")

lightLabel = ttk.Label(tabStatus,text="Light", image=img_light_on)  
lightLabel.grid(row = 1, column=1,padx=50, pady=30, sticky = "w")

ttk.Label(tabStatus,textvariable=Lightlabelvar,font=FontLarge).grid(row = 1, column=2,padx=2, pady=30, sticky = "w")

fanLabel = ttk.Label(tabStatus,text="Fan is off", image=img_fan_on)
fanLabel.grid(row = 2, column=1,padx=50, pady=0,sticky = "w" )
Fanlabelvar = StringVar()
if (s.Fan):
    Fanlabelvar.set(f"Fan on")
else:
    Fanlabelvar.set(f"Fan off")

ttk.Label(tabStatus,textvariable=Fanlabelvar,font=FontLarge).grid(row = 2, column=2,padx=2, pady=0, sticky = "w")

Temperaturelabelvar = StringVar()    
Temperaturelabelvar.set(f"Temperature {s.Temperature} C")
ttk.Label(tabStatus,text = "Temperature", image=img_temp).grid(row = 1, column=3,padx=100, pady=30, sticky = "w")
ttk.Label(tabStatus,textvariable = Temperaturelabelvar,font=FontLarge).grid(row = 1, column=4,padx=2, pady=30, sticky = "w")

Humiditylabelvar = StringVar()
Humiditylabelvar.set(f"Humidity {s.Humidity}%")
ttk.Label(tabStatus,text="Humidity", image=img_humidity).grid(row = 2, column=3,padx=100, pady=10, sticky = "w")
ttk.Label(tabStatus,textvariable=Humiditylabelvar,font=FontLarge).grid(row = 2, column=4,padx=2, pady=10, sticky = "w")

Heatlabelvar = StringVar()
Heatlabelvar.set(f"Heat {s.Heat}")
heatLabel = ttk.Label(tabStatus,text="Heat", image=img_heat_on)
heatLabel.grid(row = 3, column=1,padx=50, pady=30, sticky = "w")
ttk.Label(tabStatus,textvariable=Heatlabelvar,font=FontLarge).grid(row = 3, column=2,padx=2, pady=10, sticky = "w")

#--------------------------------------------------------Light
ttk.Label(tabLight,text ="Start time",font=FontLarge).grid(row = 2, column=1,padx=2, pady=40, sticky = "w")
ttk.Entry(tabLight, textvariable=str(LightStartHour), width=3,  font=FontLarge).grid(row = 2, column=2,padx=4, pady=0)    
Button(tabLight, text='+', command=lambda:IncOrDecLightTimer(0,1), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=3,padx=0, pady=0)
Button(tabLight, text='-', command=lambda:IncOrDecLightTimer(0,0), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=4,padx=0, pady=0)
Button(tabLight, text='Save', command=lambda:Save(settings), width = 6, height = 2,font=FontLarge).place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")

ttk.Label(tabLight,text ="hour",font=FontLarge).grid(row = 2, column=5,padx=0, pady=0)

ttk.Entry(tabLight, textvariable=str(LightStartMinute), width=3,  font=FontLarge).grid(row = 2, column=6,padx=4, pady=0)    
Button(tabLight, text='+', command=lambda:IncOrDecLightTimer(1,1), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=7,padx=0, pady=0)
Button(tabLight, text='-', command=lambda:IncOrDecLightTimer(1,0), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=8,padx=0, pady=0)
ttk.Label(tabLight,text ="minute",font=FontLarge).grid(row = 2, column=9,padx=0, pady=0)

ttk.Label(tabLight,text ="Number of hours",font=FontLarge).grid(row = 3, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabLight, textvariable=str(LightOnHours), width=3,  font=FontLarge).grid(row = 3, column=2,padx=4, pady=0)    
Button(tabLight, text='+', command=lambda:IncOrDecLightonHours(1), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=3,padx=0, pady=0)
Button(tabLight, text='-', command=lambda:IncOrDecLightonHours(0), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=4,padx=0, pady=0)

#--------------------------------------------------------FAN
ttk.Label(tabFan,text ="Fan on temperature",font=FontLarge).grid(row = 2, column=1,padx=2, pady=40, sticky = "w")
ttk.Entry(tabFan, textvariable=str(FanOnTemperature), width=3,  font=FontLarge).grid(row = 2, column=2,padx=4, pady=0)    
Button(tabFan, text='+', command=lambda:IncOrDecFan(0,1), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=3,padx=0, pady=0)
Button(tabFan, text='-', command=lambda:IncOrDecFan(0,0), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=4,padx=0, pady=0)
Button(tabFan, text='Save', command=lambda:Save(settings), width = 6, height = 2,font=FontLarge).place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")

ttk.Label(tabFan,text ="Fan off temperature",font=FontLarge).grid(row = 3, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabFan, textvariable=str(FanOffTemperature), width=3,  font=FontLarge).grid(row = 3, column=2,padx=4, pady=0)    
Button(tabFan, text='+', command=lambda:IncOrDecFan(1,1), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=3,padx=0, pady=0)
Button(tabFan, text='-', command=lambda:IncOrDecFan(1,0), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=4,padx=0, pady=0)

ttk.Label(tabFan,text ="Fan on humidity",font=FontLarge).grid(row = 4, column=1,padx=2, pady=40, sticky = "w")
ttk.Entry(tabFan, textvariable=str(FanOnHumidity), width=3,  font=FontLarge).grid(row = 4, column=2,padx=4, pady=0)    
Button(tabFan, text='+', command=lambda:IncOrDecFan(2,1), width = button_width, height = button_height,font=FontLarge).grid(row = 4, column=3,padx=0, pady=0)
Button(tabFan, text='-', command=lambda:IncOrDecFan(2,0), width = button_width, height = button_height,font=FontLarge).grid(row = 4, column=4,padx=0, pady=0)

ttk.Label(tabFan,text ="Fan off humidity",font=FontLarge).grid(row = 5, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabFan, textvariable=str(FanOffHumidity), width=3,  font=FontLarge).grid(row = 5, column=2,padx=4, pady=0)    
Button(tabFan, text='+', command=lambda:IncOrDecFan(3,1), width = button_width, height = button_height,font=FontLarge).grid(row = 5, column=3,padx=0, pady=0)
Button(tabFan, text='-', command=lambda:IncOrDecFan(3,0), width = button_width, height = button_height,font=FontLarge).grid(row = 5, column=4,padx=0, pady=0)

Button(tabFan, text='Save', command=lambda:Save(settings), width = 6, height = 2,font=FontLarge).place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")
#--------------------------------------------------------Heating
ttk.Label(tabHeat,text ="Setpoint",font=FontLarge).grid(row = 2, column=1,padx=2, pady=40, sticky = "w")
ttk.Entry(tabHeat, textvariable=str(PID_setpoint), width=3,  font=FontLarge).grid(row = 2, column=2,padx=4, pady=0)    
Button(tabHeat, text='+', command=lambda:IncOrDecPID(0,1), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=3,padx=0, pady=0)
Button(tabHeat, text='-', command=lambda:IncOrDecPID(0,0), width = button_width, height = button_height,font=FontLarge).grid(row = 2, column=4,padx=0, pady=0)
Button(tabHeat, text='Save', command=lambda:Save(settings), width = 6, height = 2,font=FontLarge).place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")

ttk.Label(tabHeat,text ="Kp",font=FontLarge).grid(row = 3, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabHeat, textvariable=str(PID_Kp), width=3,  font=FontLarge).grid(row = 3, column=2,padx=4, pady=0)    
Button(tabHeat, text='+', command=lambda:IncOrDecPID(1,1), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=3,padx=0, pady=0)
Button(tabHeat, text='-', command=lambda:IncOrDecPID(1,0), width = button_width, height = button_height,font=FontLarge).grid(row = 3, column=4,padx=0, pady=0)

ttk.Label(tabHeat,text ="Kd",font=FontLarge).grid(row = 4, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabHeat, textvariable=str(PID_Kd), width=3,  font=FontLarge).grid(row = 4, column=2,padx=4, pady=0)    
Button(tabHeat, text='+', command=lambda:IncOrDecPID(2,1), width = button_width, height = button_height,font=FontLarge).grid(row = 4, column=3,padx=0, pady=0)
Button(tabHeat, text='-', command=lambda:IncOrDecPID(2,0), width = button_width, height = button_height,font=FontLarge).grid(row = 4, column=4,padx=0, pady=0)

ttk.Label(tabHeat,text ="Ki",font=FontLarge).grid(row = 5, column=1,padx=2, pady=0, sticky = "w")
ttk.Entry(tabHeat, textvariable=str(PID_Ki), width=3,  font=FontLarge).grid(row = 5, column=2,padx=4, pady=0)    
Button(tabHeat, text='+', command=lambda:IncOrDecPID(3,1), width = button_width, height = button_height,font=FontLarge).grid(row = 5, column=3,padx=0, pady=0)
Button(tabHeat, text='-', command=lambda:IncOrDecPID(3,0), width = button_width, height = button_height,font=FontLarge).grid(row = 5, column=4,padx=0, pady=0)
#--------------------------------------------------------History
histlabel = ttk.Label(tabHistory,text="Temperature history")
histlabel.grid(row = 1, column=1, sticky = "nw") 
plothist()
#--------------------------------------------------------System
def Wifi_clicked(entry):
    key = Tk()  # key window name
    key.title('Virtual keyboard')  # title Name
    #key.wm_attributes("-topmost", True) # keep on top
    key.geometry('%dx%d+%d+%d' % (520, 220, gui.winfo_x(),(gui.winfo_y() + gui.winfo_height())-220 ))
    key.maxsize(width=520, height=220)      # maximum size
    key.minsize(width= 520 , height = 220)     # minimum size
    #key.attributes('-toolwindow', True)
    Vkeyboard.createKeyBoard(key,2,1,("Arial", 16),entry,False)

def SaveWIFI(username,password,entry):
    entry.delete(0, 'end')
    file = open(WPA_SUPPLICANT,mode='r')
    text = file.read()
    file.close()    
    start_index = text.find("ssid=")
    if start_index>0:
        start_index += 6
        new_text=text[:start_index] + username
        stop_index = text[start_index:].find('"')
        if stop_index>0:
            text = new_text + text[start_index+ stop_index:]
            start_index = text.find("psk=")
            if start_index>0:
                start_index += 5
                new_text=text[:start_index] + password
                stop_index = text[start_index:].find('"')
                if stop_index>0:
                    new_text = new_text + text[start_index + stop_index:]
                    with open(WPA_SUPPLICANT,'w') as f:
                            f.write(new_text)
def ExecuteCommand(command):
    if (command == 'Save SSID & Password'):
        SaveWIFI(WIFI_SSID.get(),WIFI_PASSWORD.get(),SSID_Password_Entry)
        messagebox.showinfo("Information","SSID & password saved!")
    elif (command == 'Shutdown'):
         Shutdown()
    elif (command == 'Restart enable WIFI'):
        WIFI(1)
    elif (command == 'Restart disable WIFI'):
        WIFI(0)

ttk.Label(tabSystem,text ="SSID",font=FontLarge).grid(row = 1, column=1,padx=20, pady=20, sticky = "w")
SSID_Entry = ttk.Entry(tabSystem, textvariable=WIFI_SSID, width=20,  font=FontLarge)
SSID_Entry.grid(row = 1, column=2,padx=4, pady=20)    
SSID_Entry.bind("<Button-1>", lambda event, entry = SSID_Entry: Wifi_clicked(entry))

ttk.Label(tabSystem,text ="WIFI password",font=FontLarge).grid(row = 2, column=1,padx=20, pady=20, sticky = "w")
SSID_Password_Entry= ttk.Entry(tabSystem, textvariable=WIFI_PASSWORD, width=20,  font=FontLarge)
SSID_Password_Entry.grid(row = 2, column=2,padx=4, pady=20)    
SSID_Password_Entry.bind("<Button-1>", lambda event, entry = SSID_Password_Entry: Wifi_clicked(entry))
RestartVar = StringVar(tabSystem)
RestartVar.set("Save SSID & Password") # default value
ttk.Label(tabSystem,text ="Command",font=FontLarge).grid(row = 3, column=1,padx=20, pady=20, sticky = "w")
OM = OptionMenu(tabSystem, RestartVar, "Save SSID & Password", "Shutdown", "Restart enable WIFI", "Restart disable WIFI")
OM.grid(row = 3, column=2,padx=20, pady=20, sticky = "w")
OM.config(font=FontLarge,bg = "WHITE")
menu = tabSystem.nametowidget(OM.menuname)
menu.config(font=FontLarge,bg = "WHITE")  
Button(tabSystem, text='Execute', command=lambda:ExecuteCommand(RestartVar.get()),font=FontLarge).grid(row = 3, column=3,padx=20, pady=20, sticky = "w")

def Shutdown():
    os.system("shutdown now -h")

def WIFI(enable):
    if (enable):
        shutil.copyfile(WIFI_ON_CONFIGURATION_FILE, WIFI_CONFIGURATION_FILE)
    else:
        shutil.copyfile(WIFI_OFF_CONFIGURATION_FILE, WIFI_CONFIGURATION_FILE)
    Restart()

def Restart():
    answer = askyesno("Restart", "Do you want to restart server?")
    if (answer):
        os.system("shutdown now -r")

def UpdateStatus():
    global s
    global Lightlabelvar, Fanlabelvar, Temperaturelabelvar, Humiditylabelvar
    global lightLabel, fanLabel, heatLabel
    global img_light_on,img_light_off,img_fan_on,img_fan_off, img_heat_on, img_heat_off
    plotcounter=0
    while (1==1):
        plotcounter += 1
        if (plotcounter==600):
            plotcounter=0
            try:
                plothist()
            except:
                pass
        try:
            s.ReLoad()
        except:
            pass
        if (s.Light):
            Lightlabelvar.set(f"Light on")
            lightLabel.configure(image=img_light_on)
            lightLabel.image = img_light_on
        else:
            Lightlabelvar.set(f"Light off")
            lightLabel.configure(image=img_light_off)
            lightLabel.image = img_light_off           

        if (s.Fan):
            Fanlabelvar.set(f"Fan on")
            fanLabel.configure(image=img_fan_on)
            fanLabel.image = img_fan_on
        else:
            Fanlabelvar.set(f"Fan off")
            fanLabel.configure(image=img_fan_off)
            fanLabel.image = img_fan_off

        if (s.Heat>0):
            Heatlabelvar.set(f"Heat on " + str(s.Heat) + "%")
            heatLabel.configure(image=img_heat_on)
            heatLabel.image = img_heat_on
        else:
            Heatlabelvar.set(f"Heat off")            
            heatLabel.configure(image=img_heat_off)
            heatLabel.image = img_heat_off

        Temperaturelabelvar.set(f"Temperature {s.Temperature} C")
        Humiditylabelvar.set(f"Humidity {s.Humidity}%")
        time.sleep(1)


x1 = threading.Thread(target=UpdateStatus, args=())
x1.start()

Notebook.pack(expand = 1, fill ="both")
gui.mainloop() 
	
