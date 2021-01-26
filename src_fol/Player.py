'''
Created on Mar 24, 2020

@author: Pate
'''
from PyQt5 import QtWidgets, QtGui, QtCore


class Player(QtWidgets.QGraphicsEllipseItem):
    
    
    def __init__(self, specs):
        super(Player, self).__init__()
        self.y_velocity = 0
        self.y_on_platform = False
        self.x_velocity = 0
        self.jumps_used = 0
        self.scrolling = False
        self.health = 150
        
        
        
        self.size = int(specs[0])
        self.speed = int(specs[1])
        
        self.health_bar = QtWidgets.QGraphicsRectItem(500,20,self.health,20)
        self.projectile = None
         
        self.health_bar_brush = QtGui.QBrush(QtGui.QColor(220,220,220), QtCore.Qt.SolidPattern)
        self.health_bar.setBrush(self.health_bar_brush)
        
        self.health_bar_condition = QtWidgets.QGraphicsRectItem(500,20,self.health,20)
        self.health_brush = QtGui.QBrush( QtGui.QColor(0,255,0), QtCore.Qt.SolidPattern)
        self.health_bar_condition.setBrush((self.health_brush))
        
        player_brush = QtGui.QBrush( QtGui.QColor(0,255,30), QtCore.Qt.SolidPattern)
        
        self.setBrush(player_brush)
        self.projectile_shot = False
        self.projectile_brush = QtGui.QBrush( QtGui.QColor(0,255,255), QtCore.Qt.SolidPattern)
        self.projectile_brush2 = QtGui.QBrush( QtGui.QColor(0,0,102), QtCore.Qt.SolidPattern)
        self.proj_cur_brush = self.projectile_brush
        self.projectile_rKey = False
        
        
    def take_damage(self):
        self.health = self.health - 1   
        if self.health > 0:
            self.health_bar_condition.setRect(500, 20, self.health, 20)
            
    
    def update_y(self):
        g_end = 6
        gravity = 1
        
        if (self.y_on_platform == False):
          
            self.y_velocity = self.y_velocity + gravity
            
            if(self.y_velocity > g_end):
                self.y_velocity = g_end
            
            self.setY(self.y() + self.y_velocity)
        
         
        else:
            self.y_velocity = 0
            self.jumps_used = 0
        
    
    def update_x(self, lkeydown,rkeydown):
        
        slow_constant = -1
        
        'case right'
        if not self.scrolling:
            
            if self.x_velocity > 0 and rkeydown:
                
                self.setX(self.x() + self.x_velocity)
                
            else:
                if self.x_velocity > 0:
                    self.x_velocity = self.x_velocity + slow_constant
                
        'case left'
        if self.x() > 0:
            
            if self.x_velocity < 0 and lkeydown:
                self.setX(self.x() + self.x_velocity)
            else:
                if self.x_velocity < 0:
                    self.x_velocity = self.x_velocity - slow_constant
                    
        
            
        
        if self.x_velocity == 0:
            
            self.x_velocity = 0
            

        
        
    def jump(self):
        "self.y_on_platform and "
        
        if (self.y_on_platform and self.jumps_used < 2):
            
            self.y_on_platform = False
            self.setY_velocity(-24)
            
            self.jumps_used = self.jumps_used + 1
            
        elif (not self.y_on_platform and self.jumps_used < 2):
            
            self.y_on_platform = False
            self.setY_velocity(-24)
            
            self.jumps_used = self.jumps_used + 1
        
        elif self.y_on_platform:
            
            self.jumps_used = 0
            self.y_on_platform = False
            self.setY_velocity(-24)
            
            self.jumps_used = self.jumps_used + 1
        
    def set_x_velocity(self, vel):
        self.x_velocity = vel
        
        
    def update_projectile(self,win_width):
        if self.projectile != None:
            if self.proj_cur_brush == self.projectile_brush:
                self.projectile.setBrush(self.projectile_brush2)
                self.proj_cur_brush = self.projectile_brush2
            else:
                self.projectile.setBrush(self.projectile_brush)
                self.proj_cur_brush = self.projectile_brush
            
            
            if self.projectile_rKey:
                self.projectile_x = self.projectile.x()
                self.projectile.setX(self.projectile_x + 7)
            else:
                self.projectile_x = self.projectile.x()
                self.projectile.setX(self.projectile_x + 5)
        if (self.projectile.x() ) > (win_width - self.temp_x):
            self.projectile = None
        
            
    def shoot(self, rightKey):
        if self.projectile == None:
            self.projectile = QtWidgets.QGraphicsEllipseItem(self.x(), self.y(), 20,20)
            self.projectile.setBrush(self.projectile_brush)
            self.temp_x = self.x()
            self.projectile_rKey = rightKey
    
    def set_health(self, health):
        self.health = health
        
    def setY_velocity(self, vel):
        self.y_velocity = vel
       
    
    def gain_health(self):
        
        if self.health <= 150-12:
            
            self.health = self.health + 12
        else:
            self.health = 150
        self.health_bar_condition.setRect(500, 20, self.health, 20)
        