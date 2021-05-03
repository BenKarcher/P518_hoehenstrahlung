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
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad

path="/home/ben/Documents/Praktikum5/Strahlung/"
fileName="winkelData"
fileExtension=".txt"

xData=[]
yData1=[]

def cos2(x,amp,phase):
    return amp*np.cos(np.radians(x+phase))**2

def cosn(x,amp,phase,c,offset):
    return amp*np.power(np.abs(np.cos(np.radians(x+phase))),c)+offset


with open (path+fileName+fileExtension, "r") as file:
    for line in file:
        line=line.split("\t")#line seperator
        #xData.append(float(line[xCol]))#x-zahlen
        xData.append(float(line[0].replace(",",".")))#x-tage
        #xError.append(float(line[1]))
        yData1.append(float(line[1].replace(",",".")))
        #yError.append(float(line[4]))     
        
xData=np.array(xData)
yData1=np.array(yData1)-514

xDataFixed=np.delete(xData,5)
yDataFixed=np.delete(yData1,5)

fitFunc=cosn

guess=[5000,0,2,0]
popt, pcov = curve_fit(fitFunc, xDataFixed, yDataFixed,guess)
#popt, pcov = curve_fit(fitFunc, xData, yData1)
pcov=np.sqrt(np.diag(pcov))


print("a1:", popt)
print("da1:", pcov)

#plt.errorbar(xData,yData,0.3,0.003,elinewidth=1,ls="none",label="daten")
plt.plot(xData, yData1, '.', label="daten")
xData=np.linspace(xData.min(),xData.max(),1000)
plt.plot(xData, fitFunc(xData, *popt), 'r-', label="fit")

plt.xlabel("Winkel [grad]")
plt.ylabel('Ereignisse')
plt.title("Winkelverteilung")
plt.legend()
