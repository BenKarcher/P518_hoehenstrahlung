#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:35:22 2020

@author: ben
"""
import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)

import numpy as np
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad

path="/home/ben/Documents/Praktikum5/Strahlung/"
fileName="data3"
fileExtension=".txt"

xData=[]
yData1=[]
yData2=[]

def taylor(x,a,b,c,d,e,f,g):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5+g*x**6#+h*x**7#+i*x**8

with open (path+fileName+fileExtension, "r") as file:
    for line in file:
        line=line.split("\t")#line seperator
        #xData.append(float(line[xCol]))#x-zahlen
        xData.append(float(line[1].replace(",",".")))#x-tage
        #xError.append(float(line[1]))
        yData1.append(float(line[4].replace(",",".")))
        #yData2.append(float(line[2].replace(",",".")))
        #yError.append(float(line[4]))
        
def deriveTaylor(arr):
    result=[]
    for i in range(1,len(arr)):
        result.append(i*arr[i])
    result.append(0)
    return result
        
        
xData=np.array(xData)
yData1=np.array(yData1)
yData2=np.array(yData2)


fitFunc=taylor

#guess=[]
#popt, pcov = curve_fit(fitFunc, xData, yData, guess)
popt, pcov = curve_fit(fitFunc, xData, yData1)
pcov=np.sqrt(np.diag(pcov))
deriv=deriveTaylor(popt)

print("a1:", popt)
print("da1:", pcov)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel("negative Spannung [mV]")
ax1.set_ylabel(r"$N_{mes}/N_{monitor}$", color=color)
ax1.plot(xData, yData1, '.', label="daten",color=color)
xData=np.linspace(xData.min(),xData.max(),1000)
ax1.plot(xData, fitFunc(xData, *popt), 'r-', label="fit")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(r"$N_{mes}/N_{monitor}/U\quad[1/mV]$", color=color)  # we already handled the x-label with ax1
ax2.plot(xData, -fitFunc(xData, *deriv), 'b-', label="-ableitung")
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title(r"Schwellenkurve von $Z_{12}$ mit Koinzidenz")
plt.show()
