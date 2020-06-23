# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:46:27 2019

@author: tonza
"""


#to do:
# test for params or rather save params in a separate file
# normalization
# saving imaging data in a file (including brightness of the LED?)
# C2_PVCAM_ALREADY_INITED  issue
# 
#
#
#
#
#
#
#
#
#




#from tkinter import Tk, Label, Button
from tkinter import *
from PIL import Image, ImageTk
from pyvcam import pvc 
from pyvcam.camera import Camera   
import cv2
import serial
import numpy

class MyFirstGUI:
    def __init__(self, master):
        try:
            pvc.init_pvcam()                   # Initialize PVCAM 
        except:
            print ("pvc exception")
            
        self.pumpPort = 'COM3'
        self.LEDPort = 'COM5'
        self.cameraType = 2# 1 no camera, 2 PVCam, 3 - BlackFly
        self.isLiveImaging = False
        self.isRecording = False
        
        self.master = master
        master.title("Mini Microscope Imager")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.live_button = Button(master, text="Live", command=self.live)
        self.live_button.pack(side = TOP)

        self.record_button = Button(master, text="Record", command=self.record)
        self.record_button.pack(side = TOP)
       
        self.labelfps = Label(master, text = 'Frames per second:')
        self.labelfps.pack(side = TOP)
        
        self.fps_entry = Entry(master)
        self.fps_entry.pack (side = TOP)
        
        self.labelExposure = Label(master, text = 'Exposure in ms:')
        self.labelExposure.pack(side = TOP)
        
        self.exp_entry = Entry(master)
        self.exp_entry.pack (side = TOP)
        
        self.labelnframes = Label(master, text = 'Number of frames:')
        self.labelnframes.pack(side = TOP)
        
        self.nframes_entry = Entry(master)
        self.nframes_entry.pack (side = TOP)
        
        self.labelbin = Label(master, text = 'binning:')
        self.labelbin.pack(side = TOP)
        
        self.bin_entry = Entry(master)
        self.bin_entry.pack (side = TOP)
        
    
    def getImage(self):
        if self.cameraType == 1:
            
            image = cv2.imread ('IMG_1573.JPG')
            
        else:
            message =  bytearray('1' +'\n', 'utf8')
            cam = next(Camera.detect_camera()) # Use generator to find first camera.
            cam.open()                         # Open the camera.
            self.aserial.write(message)
            #first switch the LED on
             
           
            image = cam.get_frame(exp_time=int(self.exp_entry.get()))
            
            message =  bytearray('0' +'\n', 'utf8')
            self.aserial.write(message)
            cam.close()
            
            #switch the LED off
        return image
    
    def live(self):
       
       
       self.getallparams()
       self.aserial = serial.Serial(self.LEDPort, 9600)
       # A camera object named cam has already been created
       a = 0
       while True:
           
           frame = self.getImage()
           resized = cv2.resize(frame, (300, 300), interpolation = cv2.INTER_AREA)
           resized = numpy.array(resized, dtype = numpy.uint8)
           cv2.imshow('miniImage', resized)
           key = cv2.waitKey(int((1000/self.framesperseconds)-self.exptime))
           if key == 27:#if ESC is pressed, exit loop
              cv2.destroyAllWindows()
              break
       self.aserial.close()
       
       
    def record(self):
        self.getallparams()
        self.aserial = serial.Serial(self.LEDPort, 9600)
        #aserial2 = serial.Serial(self.pumpPort, 9600)
        #aserial2.write(str.encode('A'))
        #aserial2.close()
        for a in range (1,self.numFr):
            image = self.getImage()
            resized = cv2.resize(image, (300, 300), interpolation = cv2.INTER_AREA)
            resized = numpy.array(resized, dtype = numpy.uint8)
            cv2.imshow('miniImage', resized)
            name = 'Image'+str(a)+'.tif'
            print (name)
            cv2.imwrite(name, image)
            key = cv2.waitKey(int((1000/self.framesperseconds)-self.exptime))
            if key == 27:#if ESC is pressed, exit loop
              cv2.destroyAllWindows()
              break
        
        self.aserial.close() 
            
    def getallparams(self):
        self.numFr = int(self.nframes_entry.get())
        self.exptime = int(self.exp_entry.get())
        self.framesperseconds = float(self.fps_entry.get())
        self.binning = int(self.bin_entry.get())
        
root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()