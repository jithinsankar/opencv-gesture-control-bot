# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:00:03 2019

@author: ADITYA
"""

import cv2 as cv
import numpy as np
import time
f = open("text.txt",'w')

video = cv.VideoCapture(0)
frame2 = None
cv.waitKey(5)
x2 = y2 = None
while True:
    f.seek(0,0)
    ret,frame= video.read() 
    if frame2 is None:          #Reference Frame Initialisation (keep glove wearing hand out of frame)'''
        frame2=frame 
    d = cv.absdiff(frame,frame2)
    gray = cv.cvtColor(d,cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lr = np.array([40,50,50])
    ur= np.array([80,255,255])
    mask= cv.inRange(hsv, lr, ur) #color detection (blue)'''
    blur = cv.GaussianBlur(gray,(5,5),0)
    blur = cv.GaussianBlur(blur,(5,5),0)
    ret, th = cv.threshold(blur,20,255,cv.THRESH_BINARY)
    frame3 = cv.bitwise_and(th,mask, mask= mask) # intersection of color detection and object detection'''
    dilated = cv.dilate(frame3, np.ones((3,3),np.uint8),iterations=5)
    
    c ,h = cv.findContours(dilated, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for contour in c:
        if cv.contourArea(contour)<5000: #area threshold'''
            continue
        x,y,w,h = cv.boundingRect(contour)
        x1 = x+w/2 # to find the centroid of hand'''
        y1 = y+h/2
        cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)
        if (w*h)<5000:
            continue
        if x2 is None or y2 is None:
            x2 = x1 #initial storing of centroid to be compared with next frame'''
            y2 = y1
            continue
        if x2-x1 > 25:
            print("Right")
            f.seek(0,0)
            f.write('6')
        if x1-x2 > 25:
            print("Left")
            f.seek(0,0)
            f.write('4')
        if y2-y1 > 25:
            print("Forward")
            f.seek(0,0)
            f.write('8')
        if y1-y2 > 25:
            print("Reverse")
            f.seek(0,0)
            f.write('2')
        if (h*w)<10000:
            print('stop')
            f.seek(0,0)
            f.write('5')    
        #print(h*w)    
        #print(x1,y1)    
        x2 = x1 
        y2 = y1
        break
            
        
    
    #cv.drawContours(frame1, c, -1, (0,255,0),2)
    cv.imshow('frame',frame)
    cv.imshow('frame3',dilated)

    frame1=frame
    if cv.waitKey(10)==27:
        break
video.release()
f.seek(0,0)
f.write('5')
cv.destroyAllWindows()   
