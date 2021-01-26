'''
Created on 29.4.2020

@author: Pate
'''
from PyQt5 import QtWidgets, QtGui, QtCore
from random import randint

class Enemy(QtWidgets.QGraphicsRectItem):
    
    def __init__(self, x, y, width, heigth, parentPlatform,specs,type = None):
        
        super(Enemy, self).__init__(x,y,width,heigth)
        self.specs = specs
        self.enemy_platform_brush = QtGui.QBrush(QtGui.QColor(50,200,180), QtCore.Qt.SolidPattern)
        self.setBrush(self.enemy_platform_brush)
        self.projectile_brush = QtGui.QBrush(QtGui.QColor(255,255,255), QtCore.Qt.SolidPattern)
        self.projectile_brush_2 = QtGui.QBrush(QtGui.QColor(255,0,0), QtCore.Qt.SolidPattern)
        self.armed_enemy_brush = QtGui.QBrush(QtGui.QColor(230,255,10), QtCore.Qt.SolidPattern)
        
        self.health = 100
        self.x_velocity = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = heigth
        self.parent = parentPlatform
        self.on_plat_move_speed = int(specs[1])
        self.projectile = None
        self.proj_y = 0
        self.proj_x = 0
        self.proj_added = False
        self.proj_brush1 = True
        self.damage = 100
        rng = randint(0,1);
        self.player_speed = 0
        self.alive = True
        if (rng == 1 or type == 1) and (type != 0):
            
            self.armed = False
            self.setBrush(self.enemy_platform_brush)
        
        else:
            self.armed = True
            self.setBrush(self.armed_enemy_brush)
    
    
    def update_projectile(self, rkeydown,player):
        
        
        if self.proj_x >= -200:
            
            if self.proj_brush1:
                self.projectile.setBrush(self.projectile_brush_2)
                self.proj_brush1 = False
            else:
                self.projectile.setBrush(self.projectile_brush)
                self.proj_brush1 = True
                
            
            if rkeydown and player.scrolling:
                self.proj_x = self.proj_x - 7
            else:
                self.proj_x = self.proj_x - 5
            
            if self.proj_x >= player.x():
                    
                if self.proj_y > player.y():
                    self.proj_y = self.proj_y - 3
                else:
                    self.proj_y = self.proj_y + 3
            self.projectile.setRect(self.proj_x, self.proj_y, 30, 10)
        else:
            
            self.projectile = None 
    
    def set_health(self, val):
        self.health = val             
        
    def set_p_speed(self,val):
        self.player_speed = val 
            
    
    def take_damage(self):
        
        self.set_health(self.health - 5)
        if self.health <= 0:
            self.alive = False
          
    
    
        
    def shoot(self, player, rkeydown):
        
        if self.x >= player.x():
            
            if self.projectile == None:
                self.proj_added = False
                
                self.proj_y = self.y
                self.proj_x = self.x
                self.projectile = QtWidgets.QGraphicsRectItem(self.proj_x, self.proj_y, 30,10);
                self.projectile.setBrush(self.projectile_brush)
                
                
         
        if self.projectile != None:      
           
            self.update_projectile(rkeydown, player)
            
                
        
    
        
    def update_x(self, rkeydown, scrolling):
        
        
        'Movement left to create the illusion of the player moving right'
        
        
        if self.x <= self.parent.x:
            self.on_plat_move_speed = int(self.specs[1])
        elif self.x >= self.parent.x + self.parent.width:
            self.on_plat_move_speed = -int(self.specs[1])
        
        if rkeydown and scrolling:
            self.x = self.x + self.on_plat_move_speed - self.player_speed
            self.setRect(self.x, self.y, self.width, self.height)
        else:
            self.x = self.x + self.on_plat_move_speed
            self.setRect(self.x, self.y, self.width, self.height)
               
        
                       
        
            
    def set_x_velocity(self, velocity):
        self.x_velocity = velocity        
      
    def set_x(self, val):
        self.x = val  
        