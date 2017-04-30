class Appliance:

#Defines various appliances and equipment that would use the power
#generated by a solar panel,
#an appliance is defined by it's name it's peak power consumtion and it's priority to the user
#and it's on/off status
#priority is defined by n => 1 where 1 is the highest priority and every larger number is lower priority


  def __init__(self, App_name, peakPowerCon, priority, status=True):
    self.App_name = App_name
    self.status = status
    self.peakPowerCon = peakPowerCon
    self.priority = priority


  def appliance_out(self):
      print("Name: ",self.App_name, ", Peak Power Consumption: ", self.peakPowerCon," Priority: ", self.priority, " Status: ", self.status )

  