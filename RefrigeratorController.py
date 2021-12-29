import settings
import status
import datetime
import threading
import time
from simple_pid import PID
from os import path
import smbus
import sys
import getopt

bus = smbus.SMBus(1)  # New Rev 2 board 
address = 0x20 # I2C address of MCP23008, change this accordingly
bus.write_byte_data(0x20,0x00,0x00) # Set all to outputs, change this accordingly

settings = settings.Settings(r'/boot/settings.json')
status = status.Status(r'/mnt/ramdisk/status.json')

Light_Relay = 16
Fan_Relay = 128
Heat_Relay = 8

def TurnOnRelay(relay):
    global address
    global bus
    current_val = bus.read_byte_data(address,0x09)
    if(current_val & relay):
      return
    bus.write_byte_data(address,0x09,current_val + relay)

def TurnOffRelay(relay):
    global address
    global bus
    current_val = bus.read_byte_data(address,0x09)
    if(current_val & relay):
      bus.write_byte_data(address,0x09,current_val - relay)

def IsRelayOn(relay):
    global address
    global bus
    return bus.read_byte_data(address,0x09) & relay

def LightThreadFunction():
    global status
    global Light_Relay
    status.Light = IsRelayOn(Light_Relay)
    while (1==1):
        now = datetime.datetime.now()
        h = settings.LightStartHour + settings.LightOnHours
        if (status.Light):
            if (now.hour>h or (now.hour==h and now.minute>=settings.LightStartMinute)):
                TurnOffRelay(Light_Relay)
                status.Light=0
                status.Save()
        else:
               if (now.hour>h or (now.hour==h and now.minute>=settings.LightStartMinute)):
                   pass
               else:
                   if (now.hour>settings.LightStartHour or (now.hour==settings.LightStartHour and now.minute>=settings.LightStartMinute)):
                       TurnOnRelay(Light_Relay)
                       status.Light=1    
                       status.Save()    
        time.sleep(60)       

def FanThreadFunction():
    global humidity
    global temperature
    global settings
    global status
    global Fan_Relay
    if (IsRelayOn(Fan_Relay)):
        FanOn = True
    else:
        FanOn = False
    FanOnTempOrHumidity = 1
    while (1==1):
        while (temperature == -99):
          print("Temperature error!")
          time.sleep(1)
        if (FanOn == False):
            if (status.Temperature>=settings.FanOnTemperature):
                TurnOnRelay(Fan_Relay)
                status.Fan = 1
                status.Save()
                FanOn = True
                FanOnTempOrHumidity = 1
            else:
                if (status.Humidity >= settings.FanOnHumidity):
                    TurnOnRelay(Fan_Relay)
                    status.Fan = 1
                    status.Save()                    
                    FanOn = True
                    FanOnTempOrHumidity = 2
        else:
            if (FanOnTempOrHumidity == 1):
                if (status.Temperature<=settings.FanOffTemperature):
                    TurnOffRelay(Fan_Relay)
                    status.Fan = 0
                    status.Save()                    
                    FanOn = False
                    FanOnTempOrHumidity=0
            else:
                print(status.Humidity)
                print(settings.FanOffHumidity)
                if (status.Humidity <= settings.FanOffHumidity):
                    TurnOffRelay(Fan_Relay)
                    status.Fan = 0
                    status.Save()                    
                    FanOn = False
                    FanOnTempOrHumidity = 0
        time.sleep(10)

def SensorThreadFunction():
    global status
    global humidity
    global temperature
    global temperatureHistory
    global humidityHistory
    upordown=1
    hcounter=0
    while (1==1):
        try:
            with open(r'/proc/am2301') as file:
                data = file.read()
                if ("ok" in data):
                    humidity = float(data[0:data.find("RH")])
                    temperature= float(data[data.find(",")+1:data.find("C")])
        except:
            temperature = -99
            humidity = -99
        now = datetime.datetime.now()
        status.Temperature = temperature
        status.Humidity = humidity
        status.Save()
        hcounter=hcounter+1
        if (hcounter == 10):
            hcounter=0
            status.AddTemperatureToHistory(now.strftime("%H:%M:%S"),temperature)
            status.AddhumidityHistory(now.strftime("%H:%M:%S"),humidity)
            status.Save()
        time.sleep(60)

def PIDThreadFunction():
    global settings
    global status
    global Heat_Relay
    #Kp, Ki, Kd
    #settings.PID_setpoint
    pid = PID(settings.PID_Kp, settings.PID_Ki, settings.PID_Kd, settings.PID_setpoint)
    
    WindowSize = 5000
    pid.output_limits = (0, WindowSize) 
    windowStartTime = int(round(time.time() * 1000))
    state = 2
    pretemperature=0
    premillis=0
    status_on = 0
    pre_status_on = 0
    while (1==1):
        if (settings.PID_setpoint != pid.setpoint):
          pid.setpoint = settings.PID_setpoint
        if (settings.PID_Kp != pid.Kp):
          pid.Kp = settings.PID_Kp
        if (settings.PID_Ki != pid.setpoint):
          pid.Ki = settings.PID_Ki
        if (settings.PID_Kd != pid.setpoint):
          pid.Kd = settings.PID_Kd

        while (temperature == -99):
          print("Temperature error!")
          time.sleep(1)
        if (temperature!=pretemperature):
            pretemperature = temperature
        output = pid(temperature)
        if (output>0):
            status_on = round((output/WindowSize)*100.0)
            if (status_on != pre_status_on):
                status.Heat = status_on                
                status.Save()                
                pre_status_on = status_on
        else:
            status.Heat = 0
            status.Save()            
        millis = int(round(time.time() * 1000))
        if (millis - windowStartTime > WindowSize):
            windowStartTime += WindowSize

        if (output < millis - windowStartTime):
            if (state!=1):                
                TurnOffRelay(Heat_Relay)
                premillis = millis
                state = 1
        else:
            if (state!=0): 
                TurnOnRelay(Heat_Relay)
                premillis = millis
                state = 0
        time.sleep(0.1)

def StatusThreadFunction():
    while (1==1):
        status.ReLoad()
        time.sleep(1)

humidity = 50
temperature = 18
temperatureHistory = {}
humidityHistory = []

x = threading.Thread(target=LightThreadFunction, args=())
x.start()

x2 = threading.Thread(target=SensorThreadFunction, args=())
x2.start()

x3 = threading.Thread(target=PIDThreadFunction, args=())
x3.start()

x4 = threading.Thread(target=StatusThreadFunction, args=())
x4.start()

x5 = threading.Thread(target=FanThreadFunction, args=())
x5.start()

while (1==1):
    settings.ReLoad()
    time.sleep(60)
