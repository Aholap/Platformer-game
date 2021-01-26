'''
Created on Apr 2, 2020

@author: Pate
'''
from PyQt5 import QtCore, QtWidgets, QtGui
from random import randint
from enemy import Enemy

class Platform(QtWidgets.QGraphicsRectItem):
    
    
    def __init__(self, x, y, width, heigth,e_specs = None):
        
        super(Platform, self).__init__(x,y, width, heigth)
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        
        self.enemy_on_top = randint(0,6)
        self.health_on_top = randint(0,5)
        self.x_velocity = 0
        self.health_package = None
        self.enemy = None
        self.health_used = False
        self.goal = False
        platform_brush = QtGui.QBrush( QtGui.QColor(100,50,100), QtCore.Qt.SolidPattern)
        enemy_platform_brush = QtGui.QBrush(QtGui.QColor(50,200,180), QtCore.Qt.SolidPattern)
        health_package_brush = QtGui.QBrush(QtGui.QColor(43,255,0), QtCore.Qt.SolidPattern)
        
        if self.enemy_on_top != 6 or e_specs == None:
            self.setBrush(platform_brush)
            if self.health_on_top == 5:
                self.health_package = QtWidgets.QGraphicsRectItem(self.x + self.width/2, self.y, 20,10)
                self.health_package.setBrush(health_package_brush)
            
        else:
            if e_specs != None:
                self.enemy = Enemy(self.x , self.y - 30, int(e_specs[0]),int(e_specs[0]),self,e_specs)
                self.setBrush(enemy_platform_brush)
        
        
    def update_x(self,rkeydown, scrolling):
    
        slow_constant = -1
        
        'Movement left to create the illusion of the player moving right'
        
        
        if scrolling:
                  
            if self.x_velocity < 0 and rkeydown:
                
                self.x = self.x + self.x_velocity
                self.setRect(self.x, self.y, self.width, self.height)
                if self.health_package != None:
                    
                    self.health_package.setRect(self.x + self.width/2, self.y- self.height/2, 20,10)
                'self.setX(self.x + self.x_velocity)'
            else:
                if self.x_velocity < 0:
                    self.x_velocity = self.x_velocity - slow_constant
               

    def set_x_velocity(self, velocity):
        self.x_velocity = velocity   
    
    def set_health_as_used(self):
        self.health_used = True
        
        