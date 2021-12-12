import json
import os.path

class Status:
    Light = 0
    Heat = 0
    Fan = 0
    Temperature =  0
    TemperatureHistoryRows = 0
    temperatureHistory = {}
    Humidity =  0
    humidityHistory = {}
    HumidityHistoryRows = 0
    __path_to_statusfile = ""
    StatusFile_mtime = ""
    def __init__(self,__path_to_statusfile):
        self.__path_to_statusfile = __path_to_statusfile
        self.Light = 0
        self.Heat = 0
        self.Fan = 0
        self.Temperature =  0
        self.TemperatureHistoryRows = 144
        self.temperatureHistory = {}
        self.Humidity = 0
        self.humidityHistory = {}
        self.HumidityHistoryRows = 144
        if (not os.path.isfile(__path_to_statusfile)):
            self.Save()
        self.Load()
    
    def Load(self):
        with open(self.__path_to_statusfile, 'r') as f:
            data=f.read()
       
        obj = json.loads(data)
        self.Light = obj['Light']
        self.Heat = obj['Heat']
        self.Fan = obj['Fan']
        self.Temperature =  obj['Temperature']
        self.temperatureHistory = obj['temperatureHistory']
        self.Humidity =  obj['Humidity']
        self.humidityHistory = obj['humidityHistory']

    def Save(self):
        with open(self.__path_to_statusfile, 'w') as f:
                f.write(self.toJSON())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)  

    def AddTemperatureToHistory(self,key,temperature):
        self.temperatureHistory[key] = temperature
        if (len(self.temperatureHistory)>self.TemperatureHistoryRows):
            self.temperatureHistory.pop(next(iter(self.temperatureHistory)))        

    def AddhumidityHistory(self,key,humidity):
        self.humidityHistory[key] = humidity
        if (len(self.humidityHistory)>self.TemperatureHistoryRows):
            self.humidityHistory.pop(next(iter(self.humidityHistory)))              

    def ReLoad(self):
        checkdate =  os.path.getmtime(self.__path_to_statusfile)
        if (self.StatusFile_mtime != checkdate):
            self.StatusFile_mtime = checkdate
            self.Load()            