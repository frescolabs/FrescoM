# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 21:36:57 2019

@author: tonza
"""

from tkinter import *
import serial
import time

class FrankieGui():
    
    
    
    def __init__(self, master):
        

        self.numWells = [12, 8]
        self.bottomLeft = [-28612, -15412]
        self.topRight = [-8863, -3173]
        self.currentPosition = [0, 0]

        self.aserial = serial.Serial('COM10', 250000)
        self.master = master
        master.title("Frankie")

        
        self.xIncrement = Button(master, text="X Increment")
        self.xIncrement.bind("<Button-1>", self.xIncrementPressed)
        self.xIncrement.bind("<ButtonRelease-1>", self.xIncrementReleased)
        self.xIncrement.pack(side = TOP)

        self.xDecrement = Button(master, text="X Decrement")
        self.xDecrement.bind("<Button-1>", self.xDecrementPressed)
        self.xDecrement.bind("<ButtonRelease-1>", self.xDecrementReleased)
        self.xDecrement.pack(side = TOP)
        
        self.yIncrement = Button(master, text="Y Increment")
        self.yIncrement.bind("<Button-1>", self.yIncrementPressed)
        self.yIncrement.bind("<ButtonRelease-1>", self.yIncrementReleased)
        self.yIncrement.pack(side = TOP)
        
        self.yDecrement = Button(master, text="Y Decrement")
        self.yDecrement.bind("<Button-1>", self.yDecrementPressed)
        self.yDecrement.bind("<ButtonRelease-1>", self.yDecrementReleased)
        self.yDecrement.pack(side = TOP)
        
        self.zeroButton = Button(master, text="Zero", command=self.toZero)
        self.zeroButton.pack(side = TOP)
        
        self.xPosEntry = Entry(master)
        self.xPosEntry.pack (side = TOP)
        
        self.xToButton = Button(master, text="xPos", command=self.xToPos)
        self.xToButton.pack(side = TOP)
        
        self.yPosEntry = Entry(master)
        self.yPosEntry.pack (side = TOP)
        
        self.yToButton = Button(master, text="yPos", command=self.yToPos)
        self.yToButton.pack(side = TOP)
        
        self.setTopRightButton = Button(master, text = "Set Top Right", command = self.setTopRight)
        self.setTopRightButton.pack(side = TOP)
        
        self.setBottomLeftButton = Button(master, text = "Set Bottom Left", command = self.setBottomLeft)
        self.setBottomLeftButton.pack(side = TOP)
        
        self.startButton = Button (master, text = "START", command = self.start)
        self.startButton.pack(side = LEFT)
       
        

    def __del__(self):
         self.aserial.close()
         
    def xIncrementPressed(self, event):
        print ("ixincpressed")
        
        message =  bytearray('M000 -1' +'\n', 'utf8')
        self.aserial.write(message)
        
    def xIncrementReleased(self, event):
        print ("x inc released")
        message =  bytearray('S000' +'\n', 'utf8')
        self.aserial.write(message)
    
    def xDecrementPressed (self, event):
        print ("x dec pressed")
        message =  bytearray('M000 1' +'\n', 'utf8')
        self.aserial.write(message)
        
    def xDecrementReleased (self, event):
        print ("x dec released")
        message =  bytearray('S000' +'\n', 'utf8')
        self.aserial.write(message) 
        
    def yIncrementPressed(self, event):
        print ("y inc pressed")
        message =  bytearray('M001 -1' +'\n', 'utf8')
        self.aserial.write(message)
    
    def yIncrementReleased(self, event):    
        print ("y inc released")
        message =  bytearray('S001' +'\n', 'utf8')
        self.aserial.write(message)
    
    def yDecrementPressed(self, event): 
        print ("y dec pressed")
        message =  bytearray('M001 1' +'\n', 'utf8')
        self.aserial.write(message)
    
    def yDecrementReleased(self, event):  
        print ("y dec released")
        message =  bytearray('S001' +'\n', 'utf8')
        self.aserial.write(message)
        
    def toZero(self):    
        message =  bytearray('Z', 'utf8')
        self.aserial.write(message)
        self.currentPosition = [0, 0]
        
    def xToPos(self):    
        message =  bytearray('P000 ' +self.xPosEntry.get() +'\n', 'utf8')
        print('P000 ' +self.xPosEntry.get() +'\n')
        self.aserial.write(message)
    
    def yToPos(self):    
        message =  bytearray('P001 ' +self.yPosEntry.get() +'\n', 'utf8')
        print('P001 ' +self.yPosEntry.get() +'\n')
        self.aserial.write(message)
    
    def setTopRight(self):
        message =  bytearray('X000'  +'\n', 'utf8') 
        self.aserial.write(message)
        time.sleep(0.1)
        self.topRight[0] = int(self.aserial.readline()[:-2])

        message =  bytearray('X001'  +'\n', 'utf8') 
        self.aserial.write(message)
        time.sleep(0.1)
        self.topRight[1] = int(self.aserial.readline()[:-2])
        print (self.topRight)
    def setBottomLeft(self):
        message =  bytearray('X000'  +'\n', 'utf8') 
        self.aserial.write(message)
        time.sleep(0.1)
        self.bottomLeft[0] = int(self.aserial.readline()[:-2])
        
        message =  bytearray('X001'  +'\n', 'utf8') 
        self.aserial.write(message)
        time.sleep(0.1)
        self.bottomLeft[1] = int(self.aserial.readline()[:-2])
        print (self.bottomLeft)
        
    def recalculateWells(self):
        print ("position recalculation")
        # ith, jth well is [(i+1)*(topleftX-bottmrightX)/(totalX-1)][(j+1)*(topleftY-bottmrightY)/(totalY-1)]
        
    def goToWell(self, wellNumberX, wellNumberY):
        print("gotowell")
        print (self.topRight)
        print (self.bottomLeft)
        newPosition = self.topRight[0] - wellNumberX*(self.topRight[0]-self.bottomLeft[0])/(self.numWells[0]-1)
        deltaX = newPosition - self.currentPosition[0]
        message =  bytearray('P000 ' +str(deltaX) +'\n', 'utf8')
        self.aserial.write(message)
        self.currentPosition[0] = newPosition
        
        while  int(self.aserial.readline()[:-2])!= -1:
            time.sleep(0.1)
        
        
        
        print ("passed")
        newPosition = self.topRight[1] - wellNumberY*(self.topRight[1]-self.bottomLeft[1])/(self.numWells[1]-1)
        deltaY = newPosition - self.currentPosition[1]
        message =  bytearray('P001 ' +str(deltaY) +'\n', 'utf8')
        self.aserial.write(message)
        self.currentPosition[1] = newPosition
        
        while  int(self.aserial.readline()[:-2])!= -1:
            time.sleep(0.1)
        
    def apply(self, pump, number):
        print ("apply")
        
    def takeFrame (self):
        print ("takeFrame")
        
    def movePump(self, steps):
        message =  bytearray('P002 ' +str(steps) +'\n', 'utf8')
        self.aserial.write(message)
        while  int(self.aserial.readline()[:-2])!= -1:
            time.sleep(0.1)
            
    def start(self):
        print ("start")
        self.toZero()
        time.sleep(2)
        for i in range (12):
            for j in range(8):
                self.goToWell(i, j)
                self.movePump(5000)
                time.sleep(1)
                self.movePump(-5000)
    def autoFocus(self):
        print("autofocus")
        
root = Tk()
my_gui = FrankieGui(root)
root.mainloop()
del my_gui