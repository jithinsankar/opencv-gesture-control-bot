# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:00:03 2019

@author: ADITYA
"""

import cv2 as cv
import numpy as np

video = cv.VideoCapture(0)
frame2 = None
cv.waitKey(5)
x2 = y2 = None
while True:
    ret,frame= video.read() 
    if frame2 is None:          #Reference Frame Initialisation (keep glove wearing hand out of frame)'''
        frame2=frame 
    d = cv.absdiff(frame,frame2)
    gray = cv.cvtColor(d,cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lr = np.array([110,50,50])
    ur= np.array([130,255,255])
    mask= cv.inRange(hsv, lr, ur) #color detection (blue)'''
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret, th = cv.threshold(blur,20,255,cv.THRESH_BINARY)
    frame3 = cv.bitwise_and(th,mask, mask= mask) # intersection of color detection and object detection'''
    dilated = cv.dilate(frame3, np.ones((3,3),np.uint8),iterations=1)
    
    c ,h = cv.findContours(dilated, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for contour in c:
        if cv.contourArea(contour)<5000: #area threshold'''
            continue
        x,y,w,h = cv.boundingRect(contour)
        x1 = x+w/2 # to find the centroid of hand'''
        y1 = y+h/2
        cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)
        if x2 is None or y2 is None:
            x2 = x1 #initial storing of centroid to be compared with next frame'''
            y2 = y1
            continue
        if x2-x1 > 20:
            print("Right")
        if x1-x2 > 20:
            print("Left")
        if y2-y1 > 20:
            print("Forward")
        if y1-y2 > 20:
            print("Reverse")
        #print(x1,y1)    
        x2 = x1 
        y2 = y1
        break
            
        
    
    #cv.drawContours(frame1, c, -1, (0,255,0),2)
    cv.imshow('frame',frame)
    cv.imshow('frame3',dilated)
    frame1=frame
    if cv.waitKey(1)==27:
        break
video.release()
cv.destroyAllWindows()   