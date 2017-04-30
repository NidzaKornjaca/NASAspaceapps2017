"""
even higher level support for doing this and that.
"""
#!/usr/bin/env python 
import tkinter as tk
from solarRadiationPredictor import read_spaceapps_data, plot_predictor

def plot_commmand():
    x_pre, y = read_spaceapps_data("SpaceAppsData.csv")
    plot_predictor(x_pre, y, 20, 0.5)



root = tk.Tk()

b4 =tk.Button(root, text='Plot', command=plot_commmand())
b4.tk.pack(side=tk.LEFT, padx=5, pady=5)
root.mainloop()