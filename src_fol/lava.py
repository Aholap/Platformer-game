'''
Created on 30.4.2020

@author: Pate
'''
from PyQt5 import QtWidgets, QtGui, QtCore

class Lava(QtWidgets.QGraphicsRectItem):
    
    
    def __init__(self, x, y, width, heigth):
        
        super(Lava, self).__init__(x,y, width, heigth)
        
        self.rgb_G = 0
        self.rgb_up = True
        
        
        self.color = QtGui.QBrush(QtGui.QColor(255,self.rgb_G,0), QtCore.Qt.SolidPattern)
        self.setBrush(self.color)
    
    def update_color(self):
        
        if self.rgb_up:
            if self.rgb_G < 200:
                self.rgb_G = self.rgb_G + 1
            else:
                self.rgb_up = False
        else:
            if self.rgb_G > 0:
                self.rgb_G = self.rgb_G - 1
            else:
                self.rgb_up = True
        
        self.color = QtGui.QBrush(QtGui.QColor(255,self.rgb_G,0), QtCore.Qt.SolidPattern)
        self.setBrush(self.color)
    
   
        
        