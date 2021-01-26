'''
Created on 30.4.2020

@author: Pate

'''

from PyQt5 import QtWidgets, QtGui, QtCore

class Background(QtWidgets.QGraphicsRectItem):
    
    
    def __init__(self, x, y, width, heigth):
        
        super(Background, self).__init__(x,y, width, heigth)
        
        self.R = 0
        self.G = 0
        self.B = 0
        
        self.color = QtGui.QBrush(QtGui.QColor(self.R,self.G,self.B), QtCore.Qt.SolidPattern)
        self.setBrush(self.color)
        
        self.time = 'Night'
        
        self.moon_color = QtGui.QBrush(QtGui.QColor(220,220,220), QtCore.Qt.SolidPattern)
        self.skyObj = QtWidgets.QGraphicsEllipseItem(-350,400,350,350)
        self.skyObj.setBrush(self.moon_color)
        
        self.sun_color = QtGui.QBrush(QtGui.QColor(255,255,0), QtCore.Qt.SolidPattern)
        self.skyObj.moon = True
        self.skyObj.rising = True
        
        self.skyObj.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        
    def move_s(self):
        
        
        if self.skyObj.x() < 800 + 350: 
            self.skyObj.setX(self.skyObj.x() + 0.15)
            if self.skyObj.rising:
                self.skyObj.setY(self.skyObj.y() - 0.05)
            else:
                self.skyObj.setY(self.skyObj.y() + 0.05)
            if self.skyObj.x() >= 600:
                self.skyObj.rising = False
            else:
                self.skyObj.rising = True
            
        else:
            if self.skyObj.moon:
                self.skyObj.moon = False  
                self.skyObj.setBrush(self.sun_color)
                self.time = 'Day'
            else:
                self.skyObj.moon = True
                self.skyObj.setBrush(self.moon_color)
                self.time = 'Night'
            self.skyObj.setX(-50)
            self.skyObj.setY(0)
    
    def update_bg_color(self):
        
        if self.skyObj.x() >= 800:
            
            if self.time=='Night':
                self.R = self.R + 0.132/2
                self.G = self.G + 0.1
                self.B = self.B + 0.216/2
            elif self.time=='Day':
                self.R = self.R - 0.132/2
                self.G = self.G - 0.1
                self.B = self.B - 0.216/2
               
        self.color = QtGui.QBrush(QtGui.QColor(self.R,self.G,self.B), QtCore.Qt.SolidPattern)
        self.setBrush(self.color)
        
        
        
         
        