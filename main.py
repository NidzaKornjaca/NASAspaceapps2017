"""
high level support for doing this and that.
"""
#!/usr/bin/env python 
from tkinter import *
from Appliances import * 
from SolarPanels import *
from tkinter import messagebox


fields = "Model Name", "Surface Size", "Tilt Degree", "Short Circuit Current", "Open Circuit Voltage", "Test Surface", "Test Flux", "Appliance Name", "Appliance Peak Power Consumption", "Appliance Priority", "Power Output", "Total Power Consumption"
apps = []
x = solarPanel()
calc = 0 
def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print('%s: "%s"' % (field, text)) 

def findLowestPriority_HighestConsumtipon(entries):
   global apps
   i = 0
   k = 1
   p = 0
   for app in apps:
       if app.priority > k:
           if app.peakPowerCon > apps[i].peakPowerCon:
               k = app.priority
               p = i
       i += 1
   messagebox.showinfo("Turn off", "We suggest you turn off: " + apps[p].App_name)


 
#########################################
def makeform(root, fields):
    entries = {}
    for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
    return entries
 ################################   
def CalcPowCons(entries):
    global calc
    for app in apps:
        if (app.status == True): 
             calc += app.peakPowerCon 
    entries["Total Power Consumption"].delete(0,END)
    #apps[findLowestPriority_HighestConsumtipon(apps)].appliance_out()
    entries["Total Power Consumption"].insert(0, calc)
##################################
def CalcPout(entries):
    global x
    x.model_Name = entries["Model Name"].get()
    x.surface_Size = float(entries["Surface Size"].get())
    x.tilt_Degree = float(entries["Tilt Degree"].get())
    x.shortCircuitCurrent = float(entries["Short Circuit Current"].get())
    x.openCircuitVoltage = float(entries["Open Circuit Voltage"].get())
    x.test_Surface = float(entries["Test Surface"].get())
    x.test_Flux = float(entries["Test Flux"].get())
    #x = solarPanel(mn, ss, td, Isc, Voc, ts, tf)
    entries["Power Output"].delete(0, END)
    p = x.powerOutput(20000)
    entries["Power Output"].insert(0,p )
    if p < calc: 
       messagebox.showwarning("Power Warning", "Warning, power consumption exceeded power ")
###############################################
def addAppliance(entries):   
    global apps 
    App_name1 = entries["Appliance Name"].get()
    peakPowerCon1 = float(entries["Appliance Peak Power Consumption"].get())
    priority1 = int(entries["Appliance Priority"].get())
    a = Appliance(App_name1, peakPowerCon1, priority1)
    apps.append(a)    
 ###################################################       
if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)
    root.bind(lambda event, e=ents: fetch(e))   
    b1 = Button(root, text='Calculate Total Power Consumption',
                command=(lambda e=ents: CalcPowCons(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Power Output',
               command=(lambda e=ents: CalcPout(e)))
    b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(root, text='Add Appliance',
               command=(lambda e=ents: addAppliance(e)))
    b3.pack(side=LEFT, padx=5, pady=5)
    b4 = Button(root, text='What should i turn off', 
               command=(lambda e=ents: findLowestPriority_HighestConsumtipon(e)))
    b4.pack(side=LEFT, padx=5, pady=5)
    b5 = Button(root, text='Quit', command=root.quit)
    b5.pack(side=LEFT, padx=5, pady=5)
    #k = findLowestPriority_HighestConsumtipon(apps)
    #if x.powerOutput(5) < calc: 
      # messagebox.showinfo("Power Warning", "Warning, power consumption exceeded power ")
    root.mainloop()