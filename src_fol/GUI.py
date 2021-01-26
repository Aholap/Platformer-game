from PyQt5 import QtWidgets, QtCore, QtGui
from platform import Platform
from Player import Player
from random import randint
from lava import Lava
from background import Background

class GUI(QtWidgets.QMainWindow):
    try:
        
        def __init__(self, app, specs):
            super().__init__()
            
            self.application = app
            self.death_text = None
            self.win_text = None
            self.application_running = True
            self.window_width = 800
            self.window_height = 600
            self.setGeometry(300, 300, self.window_width, self.window_height)
            self.setWindowTitle('Tasohyppely')
            self.show()
            self.game_running = False
            
            self.test_player = Player(specs[0])
            self.player_specs = specs[0]
            self.enemy_specs = specs[1]
            self.platform_specs = specs[2]
            
            self.test_platform = Platform(0,300,self.window_width - 100,40)
            self.test_platform_2 = Platform(self.window_width - 50, 320, 100, 35)
            self.rightKeydown = False
            self.leftKeydown = False
            self.enemies = []
            self.bottom_lava = Lava(-1, self.window_height - 50, self.window_width + 1, 51)
            
            self.reRun = False
            self.completion = 0
            
            self.platforms = []
            self.counter = 0
            
            self.backGround = Background(-1,-1, self.window_width + 1, self.window_height + 1)
            
            
            self.skyObject = self.backGround.skyObj
            'self.label.setPixmap(self.pxmap)'
            
            'Scene'
            self.Scen = QtWidgets.QGraphicsScene()
            self.scene = QtWidgets.QGraphicsScene()
            self.init_start_screen()
            self.goal_added = False
            'Add player'
            
            'self.player  = QtWidgets.QGraphicsRectItem(100,300,300,100)'
            'self.scene.addItem(self.player)'
            
            
            'scene view'
            if self.game_running:
                self.view = QtWidgets.QGraphicsView(self.scene, self)
            else:
                self.view = QtWidgets.QGraphicsView(self.Scen, self) 
            
            self.view.setVerticalScrollBarPolicy(1)
            self.view.setHorizontalScrollBarPolicy(1)
            self.view.adjustSize()
            self.view.show()
            
            self.scene.keyPressEvent = self.keyPressEvent
            
            self.init_game_screen()
            
            'Game timer ie. loop'
            
            'called in the loop constanly'
            
            
               
            def generate_platforms():
                
                try:
                    if self.completion < 100:
                        
                        player_x = self.test_player.x()
                        
                        free_to_spawn = True
                        
                        platforms_to_add = []
                        
                        num_to_spawn = randint(2,10)
                        counter = 0
                        
                        for p in self.platforms:
                            if player_x + self.window_width/4 < p.x < player_x + self.window_width:
                                free_to_spawn = False
                        
                        if free_to_spawn:
                            
                            while counter < num_to_spawn:
                                can_be_added = True
                                
                                platform_to_add = Platform(randint(player_x + self.window_width/2, player_x + self.window_width/2 + 150), randint(100, 500), int(self.platform_specs[0]), int(self.platform_specs[1]), self.enemy_specs)
                                
                                if self.rightKeydown:
                                    platform_to_add.set_x_velocity(-self.test_player.speed)
                                
                                
                                for plat in platforms_to_add:
                                    if -40 < platform_to_add.x - plat.x < 40 or -80 < platform_to_add.y - plat.y < 80:
                                        can_be_added = False
                                        
                                if can_be_added:    
                                    platforms_to_add.append(platform_to_add)
                                    if platform_to_add.enemy != None:
                                        self.enemies.append(platform_to_add.enemy)
                                    
                                counter = counter + 1
                            for p in platforms_to_add:
                                
                                self.platforms.append(p)
                                self.scene.addItem(p)
                                if p.health_package != None:
                                    self.scene.addItem(p.health_package)
                                
                            for e in self.enemies:
                                if self.rightKeydown:
                                    e.x_velocity = -int(self.test_player.speed)
                                e.set_p_speed(self.test_player.speed)
                                self.scene.addItem(e)
                    
                    else:
                        if not self.goal_added:
                            
                            goalPost1 = Platform(self.window_width + 600,300 - 60,20,60)
                            goalPost2 = Platform(self.window_width + 700,300 - 60,20,60)
                            goalBar = Platform(self.window_width + 600,300- 70,120,20)
                            
                            goalPost1.goal = True
                            goalPost2.goal = True
                            goalBar.goal = True
                            
                            plat_to_add = Platform(self.window_width,300,800,25) 
                            plat_to_add.setBrush(QtGui.QBrush( QtGui.QColor(214,255,48), QtCore.Qt.SolidPattern))           
                            
                            goalPost1.setBrush(QtGui.QBrush( QtGui.QColor(196,255,0), QtCore.Qt.SolidPattern))
                            goalPost2.setBrush(QtGui.QBrush( QtGui.QColor(196,255,0), QtCore.Qt.SolidPattern))
                            goalBar.setBrush(QtGui.QBrush( QtGui.QColor(196,255,0), QtCore.Qt.SolidPattern))
                            if self.rightKeydown:
                                goalPost1.set_x_velocity(-self.test_player.speed)
                                goalPost2.set_x_velocity(-self.test_player.speed)
                                goalBar.set_x_velocity(-self.test_player.speed)
                                plat_to_add.set_x_velocity(-self.test_player.speed)
                            self.scene.addItem(plat_to_add)
                            self.scene.addItem(goalPost1)
                            self.scene.addItem(goalPost2)
                            self.scene.addItem(goalBar)
                            self.platforms.append(goalPost1)
                            self.platforms.append(goalPost2)
                            self.platforms.append(goalBar)
                            self.platforms.append(plat_to_add)
                            self.goal_added = True
                except Exception as e:
                    print(e)
        
            def update_obj_pos():
                
                if self.rightKeydown:
                    self.completion = self.completion + 0.01
                
                if self.test_player.projectile != None:
                    self.test_player.update_projectile(self.window_width)
                else:
                    
                    self.scene.removeItem(self.test_player.projectile)
                try:
                    if self.test_player.health <= 0 or self.test_player.collidesWithItem(self.bottom_lava):
                        self.die()
                    
                    self.backGround.move_s()
                    self.backGround.update_bg_color()
                    self.bottom_lava.update_color()
                    
                    self.test_player.update_y()  
                    self.test_player.update_x(self.leftKeydown, self.rightKeydown)
            
                    for i in self.enemies:
                        
                        if self.test_player.projectile != None:
                            if i.collidesWithItem(self.test_player.projectile):
                                i.take_damage()
                        if not i.alive:
                            self.scene.removeItem(i)
                            if i.projectile != None:
                                self.scene.removeItem(i.projectile)
                            self.enemies.remove(i)
                        
                        if i.armed and i.x <= self.window_width + 100:
                        
                            i.shoot(self.test_player, self.rightKeydown)
                            if not i.proj_added:
                                self.scene.addItem(i.projectile)
                                
                                i.proj_added = True
                            if i.proj_x <= self.test_player.x() and not i.proj_added:
                                self.scene.removeItem(i.projectile)
                        
                            
                             
                
                        
                        if self.test_player.collidesWithItem(i):
                            self.test_player.take_damage()
                
                    
                    if self.test_player.x() >= self.window_width/2:
                        self.test_player.scrolling = True
                        generate_platforms()
                        
                    else:
                        self.test_player.scrolling = False
                        
                    
                    "print('keydown:l:r:',self.leftKeydown, self.rightKeydown, self.test_player.x_velocity)"
                    self.test_player.y_on_platform = False
                    
                    
                    
                    for e in self.enemies:
                        e.update_x(self.rightKeydown, self.test_player.scrolling)
                        if self.test_player.collidesWithItem(e) or self.test_player.collidesWithItem(e.projectile):
                            self.test_player.take_damage()
                            
                    try:
                        for p in self.platforms:
                            
                            p.update_x(self.rightKeydown, self.test_player.scrolling)
                            if p.health_package != None:
                                if self.test_player.collidesWithItem(p.health_package) and not p.health_used:
                                    self.test_player.gain_health()
                                    p.set_health_as_used()
                                    self.scene.removeItem(p.health_package)
                            
                            if self.goal_added:
                                if self.test_player.collidesWithItem(p) and p.goal:
                                    self.win_game()       
                            
                            
                            if p.x + p.width <= 0:
                                
                                self.scene.removeItem(p)
                                
                                self.platforms.remove(p)
                                if p.enemy != None:
                                    self.scene.removeItem(p.enemy)
                                    self.enemies.remove(p.enemy)
                            
                                
                            if self.test_player.y() + 20 >= p.y and (self.test_player.x() + 5 > p.x and self.test_player.x() + 5 < p.x +  + p.width ) :
                                if (p.y - self.test_player.y()) > 10 and self.test_player.y_velocity >= 0:
                                    self.test_player.setY(p.y - 20) 
                                    self.test_player.y_on_platform = True
                    except Exception as d:
                        print(d, 'aha')                
                except Exception as e:
                    print(e, 'AAAAAAAAAAA')            
            try:
                
            
                self.game_timer = QtCore.QTimer(self)
            
                self.game_timer.timeout.connect(update_obj_pos)
            except Exception as e:
                print(e)
            
        
        
        def die(self):
            self.game_timer.stop()
            text = QtWidgets.QGraphicsTextItem('YOU DIED!')
            text.moveBy(300,50)
            text.setFont(QtGui.QFont("Helvetica [Cronyx]", 20))
            self.death_text = text
            self.Scen.addItem(text)
            self.view.setScene(self.Scen)
            
            self.reRun = True
            
         
        def win_game(self):
            self.game_timer.stop()
            
            text = QtWidgets.QGraphicsTextItem('YOU WIN!')
            text.moveBy(300,50)
            text.setFont(QtGui.QFont("Helvetica [Cronyx]", 20))
            self.Scen.addItem(text)
            self.win_text = text
            self.view.setScene(self.Scen)
        
            self.reRun = True
        
        def start(self):
            self.game_running = True
            self.application.exec_()
             
         
            
            
        'To be run when the start-button is clicked'
        def init_game_screen(self):
            
            self.scene.clear()
            self.enemies.clear()
            self.platforms.clear()
            
            try:
                self.scene.addItem(self.backGround)
            except Exception as e:
                print('VI')
            self.scene.addItem(self.skyObject)
            
            self.scene.addItem(self.bottom_lava)
            self.scene.addItem(self.test_player.health_bar)
            self.scene.addItem(self.test_player.health_bar_condition)
            
            self.scene.addItem(self.test_player)
            self.scene.addItem(self.test_platform)
            self.scene.addItem(self.test_platform_2)
            
            self.test_player.setRect(0, 0, self.test_player.size,self.test_player.size)
            self.platforms.append(self.test_platform)
            self.platforms.append(self.test_platform_2)
            
            "self.game_timer.start(10)"
            
        def start_game(self):
            try:
                
                if self.reRun:
                    if self.death_text != None:
                        self.Scen.removeItem(self.death_text)
                        self.death_text = None
                    if self.win_text != None:
                        self.Scen.removeItem(self.win_text)
                        self.win_text = None
                    self.test_player.setY(-60)
                    self.test_player = Player(self.player_specs)
                    self.backGround = Background(-1,-1, self.window_width + 1, self.window_height + 1)
                    self.skyObject = self.backGround.skyObj
                    self.bottom_lava = Lava(-1, self.window_height - 50, self.window_width + 1, 51)
                    self.test_platform = Platform(0,300,self.window_width - 100,40)
                    self.test_platform_2 = Platform(self.window_width - 50, 320, 100, 35)
                    self.init_game_screen()
                    self.completion = 0
                    self.goal_added = False
                    
                    
                self.view.setScene(self.scene)
                
                
                
                self.game_timer.start(10)
            except Exception as r:
                print('JJJJJJJJ')
         
        def exit_game(self):
            self.application_running = False
            self.application.exit()
                
        def init_start_screen(self):
        
            painter = QtGui.QPainter(self)
            background_brush = QtGui.QBrush( QtGui.QColor(203,58,58), QtCore.Qt.SolidPattern)
            painter.setBrush(background_brush)
            
            
            
            'Widget for the layout'
            widget = QtWidgets.QWidget()
            
            'Layout for buttons'
            layout = QtWidgets.QVBoxLayout()
            widget.setLayout(layout)
            
            
            
            'Buttons'
            self.start_button = QtWidgets.QPushButton('START')
            self.exit_button = QtWidgets.QPushButton('EXIT')
            
            self.start_button.clicked.connect(self.start_game)
            self.exit_button.clicked.connect(self.exit_game)
            'EXIT GAME:'
            'self.exit_button.clicked.connect(self.sc)'
            
            
            
            'Buttons to layout'
            layout.addWidget(self.start_button)
            layout.addWidget(self.exit_button)
            
            widget.move(325,200)
            
            'r - painted rect'
            r = QtWidgets.QGraphicsRectItem(0,0,self.window_width,self.window_height)
            r.setBrush(background_brush)
            
            'Adding items to scene'
            self.Scen.addItem(r)
            self.Scen.addWidget(widget)
            
        
        
        def keyPressEvent(self, key):
            
            if(key.key() == 87 and not key.isAutoRepeat()):
                
                self.test_player.jump()
                
                
            if(key.key() == 68 ):
                if not key.isAutoRepeat():
                
                    self.test_player.x_velocity = self.test_player.speed
                    for p in self.platforms:
                        p.set_x_velocity(-self.test_player.speed)
                        
                        if p.enemy != None:
                            p.set_x_velocity(-self.test_player.speed)
                    self.rightKeydown = True
        
            
            if(key.key() == 65 and not key.isAutoRepeat()):
                
                self.test_player.set_x_velocity(-self.test_player.speed)
                
                self.leftKeydown = True
            
            if key.key() == 32 and not key.isAutoRepeat():
                self.test_player.shoot(self.rightKeydown)
                self.scene.addItem(self.test_player.projectile)
            
        def keyReleaseEvent(self, key):
            
           
                
            if(key.key() == 68 and not key.isAutoRepeat()):
               
                self.rightKeydown = False
                
            
            
            if(key.key() == 65 and not key.isAutoRepeat()):
                
                self.leftKeydown = False
    except Exception as e:
        print(e)    
