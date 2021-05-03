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
fileName="a102_results"
fileExtension=".txt"

xData=[]
yData1=[]
yData2=[]

def landau(x):
    return np.exp(-(x+np.exp(-x))/2)
def scaled(x,amp,x0,sd):
    return amp*landau((x-x0)/sd)

with open (path+fileName+fileExtension, "r") as file:
    for i in range(9):
        file.readline()
    for line in file:
        line=line.split("\t")#line seperator
        #xData.append(float(line[xCol]))#x-zahlen
        xData.append(float(line[0].replace(",",".")))#x-tage
        #xError.append(float(line[1]))
        yData1.append(float(line[1].replace(",",".")))
        #yError.append(float(line[4]))     
        
xData=np.array(xData)
yData1=np.array(yData1)
yData2=np.array(yData2)


fitFunc=scaled

guess=[30,300,1]
popt, pcov = curve_fit(fitFunc, xData, yData1,guess)
#popt, pcov = curve_fit(fitFunc, xData, yData1)
pcov=np.sqrt(np.diag(pcov))


print("a1:", popt)
print("da1:", pcov)

#plt.errorbar(xData,yData,0.3,0.003,elinewidth=1,ls="none",label="daten")
plt.plot(xData, yData1, '.', label="daten")
xData=np.linspace(xData.min(),xData.max(),1000)
plt.plot(xData, fitFunc(xData, *popt), 'r-', label="fit")

plt.xlabel("Kanalnummer $k$")
plt.ylabel(r'Zählerstand $N_k$')
plt.title("Lebensdauer des Myons")
plt.legend()
