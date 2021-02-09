# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 10:19:12 2021

@author: IU
"""

import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime
rm = pyvisa.ResourceManager()
devices = rm.list_resources()
dev_objs=[]
dev_names=[]
c =0
for i in devices:
    dev_objs.append(rm.open_resource(i))
    dev_names.append(dev_objs[c].query('*IDN?'))
    print("Detected Device",c, " : ",dev_names[c])
    c=c+1
    
mode_valid =False
while not mode_valid:
    mode = int(input("Select Measurement Mode\n 0: V\n 1: I\n 2: V-I\n"))
    if mode>-1 and mode<3:
        mode_valid=True


if mode==0 or mode==2:
    indexValid = False
    while not(indexValid):
        indV = int(input('Enter DMM index for Voltage Measurement: '))
        if indV<c:
            indexValid=True
            print(dev_names[indV],"is selected as Voltage DMM.")
        else:
            print("Index not valid, try again...")

if mode==1 or mode==2:
    indexValid = False
    while not(indexValid):
        indC = int(input('Enter DMM index for Current Measurement: '))
        if indC<c:
            indexValid=True
            print(dev_names[indC],"is selected as Current DMM.")
        else:
            print("Index not valid, try again...")
        
MeasPeriod= int(input("Enter measurment interval in seconds: "))
Points= int(input("Enter measurment points: "))
VectorV = []
VectorI = []
Vectort =[0]
timeV = 0



    
    
    
def StartRecording():
    global dev_names,dev_objs,indV,indC,timer1
    if mode==0 or mode==2:
        dev_objs[indV].timeout=5000
        dev_objs[indV].write('CONF:VOLT:DC 10,DEF')
    if mode==1 or mode==2:
        dev_objs[indC].timeout=5000
        dev_objs[indC].write('CONF:CURR:DC 100m')
    
    
    print("Timeouts and Ranges are SET..")
    time.sleep(5)
    #dev_objs[indV].write('CONF:VOLT:DC')
    #dev_objs[indC].write('CONF:CURR:DC')
    

StartRecording()
fname='RECORDING-'+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"+'.txt')
recfile = open(fname,'w')
time.sleep(1)
print("Openning file for recording...")
if mode==0:
    recfile.write('Time,Voltage\n')
elif mode==1:
    recfile.write('Time,Current\n')
elif mode==2:
    recfile.write('Time,Voltage,Current\n')


for measurements in range(Points):
    if mode==0:
        V = dev_objs[indV].query('READ?')
        print(measurements, "- V: ", V[:-1])
        recfile.write('%d,%2.6f,%2.6f\n' % (timeV, float(V)))
    elif mode==1:
        I = dev_objs[indC].query('READ?')
        print(measurements, "- I: ", I[:-1])
        recfile.write('%d,%2.6f\n' % (timeV,float(I)))
    elif mode==2:
        V = dev_objs[indV].query('READ?')
        I = dev_objs[indC].query('READ?')
        print(measurements, "- V: ", V[:-1],", I: ",I[:-1])
        recfile.write('%d,%2.6f,%2.6f\n' % (timeV, float(V),float(I)))
    timeV +=MeasPeriod
    time.sleep(MeasPeriod)

print("Recording completed...")
recfile.close()



























    
    
    