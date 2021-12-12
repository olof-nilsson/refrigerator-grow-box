import json
import os.path

class Settings:
    LightStartHour = 0
    LightStartMinute = 0
    LightOnHours = 0
    FanOnTemperature =  0
    FanOffTemperature = 0 
    FanOnHumidity =  0
    FanOffHumidity = 0 
    PID_Kp = 0
    PID_Ki = 0
    PID_Kd = 0
    PID_setpoint = 0
    __path_to_settingsfile = ""
    SettingsFile_mtime = ""
    def __init__(self,path_to_settingsfile):
        self.__path_to_settingsfile = path_to_settingsfile
        if (not os.path.isfile(path_to_settingsfile)):
            self.LightStartHour = 6
            self.LightStartMinute = 0
            self.LightOnHours = 8
            self.FanOnTemperature =  28
            self.FanOffTemperature = 24
            self.FanOnHumidity = 90
            self.FanOffHumidity = 50
            self.PID_Kp = 6
            self.PID_Ki = 3
            self.PID_Kd = 0
            self.PID_setpoint = 0
            self.Save()
            self.Load()
        else:
            self.Load()
        self.SettingsFile_mtime =  os.path.getmtime(path_to_settingsfile)            
    
    def Load(self):
        with open(self.__path_to_settingsfile) as json_file:
            data = json.load(json_file)
            if "LightStartHour" in data:
                self.LightStartHour = data['LightStartHour']
            if "LightStartMinute" in data:
                self.LightStartMinute = data['LightStartMinute']
            if "LightOnHours" in data:
                self.LightOnHours = data['LightOnHours']
            if "FanOnTemperature" in data:
                self.FanOnTemperature = data['FanOnTemperature']
            if "FanOffTemperature" in data:
                self.FanOffTemperature = data['FanOffTemperature']
            if "FanOnHumidity" in data:
                self.FanOnHumidity = data['FanOnHumidity']
            if "FanOffHumidity" in data:
                self.FanOffHumidity = data['FanOffHumidity']
            if "PID_setpoint" in data:
                self.PID_setpoint = data['PID_setpoint']
            if "PID_Kp" in data:
                self.PID_Kp = data['PID_Kp']
            if "PID_Ki" in data:
                self.PID_Ki = data['PID_Ki']
            if "PID_Kd" in data:
                self.PID_Kd = data['PID_Kd']                            

    def Save(self):
        with open( self.__path_to_settingsfile, 'w') as f:
                f.write(self.toJSON())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    
    def ReLoad(self):
        checkdate =  os.path.getmtime(self.__path_to_settingsfile)
        if (self.SettingsFile_mtime != checkdate):
            self.SettingsFile_mtime = checkdate
            self.Load()