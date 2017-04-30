import numpy as np
#this class is for various solar panels 
#the important atritbutes for a solar panel are it's model, 
# the surface size of the panel and it's tilt expressed in 
#

class solarPanel:
  
    thermalVoltage = 25
    optimalVoltage = 450 
    def __init__(self, model_Name = "test model", surface_Size = 0.0000023895, tilt_Degree = 0, shortCircuitCurrent = 0.875, openCircuitVoltage = 0.612, test_Surface = 0.0000023895, test_Flux = 1000):
        self.model_Name = model_Name
        self.surface_Size = surface_Size
        self.tilt_Degree = tilt_Degree
        self.shortCircuitCurrent = shortCircuitCurrent
        self.openCircuitVoltage = openCircuitVoltage
        self.test_Surface = test_Surface 
        self.test_Flux = test_Flux



   #methods
    def Ksol(self):
        return self.shortCircuitCurrent / (self.test_Surface * self.test_Flux)

    def idealSolarPanelCurrent(self, flux):
        return self.Ksol() * self.surface_Size * flux * np.cos(self.tilt_Degree)

    def diodeParam(self):
        return self.shortCircuitCurrent / (np.exp(self.openCircuitVoltage / self.thermalVoltage)-1)
  
    def powerOutput(self, flux):
        CVchar = self.diodeParam()*(np.exp(self.optimalVoltage/self.thermalVoltage) - 1)
        p = self.idealSolarPanelCurrent(flux) - self.diodeParam() * CVchar
        return p
    

   
     

