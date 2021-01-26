'''
Created on 6.5.2020

@author: Pate
'''
import unittest
import sys
from Player import Player
from platform import Platform
from enemy import Enemy
from PyQt5 import QtWidgets, QtTest
from GUI import GUI
import threading
import time

class TestClassesAndFunctions(unittest.TestCase):

    def test_player_health(self):
        self.specs = [[30,3],[25,4],[100,30]]
        "Class objects"
        test_player = Player(self.specs[0])
        
        self.assertEqual(test_player.health, 150, "Wrong amount of health")
        
        "Health in middle"
        test_player.set_health(100)
        self.assertEqual(test_player.health, 100, "Health setting not working")
        
        test_player.take_damage()
        self.assertEqual(test_player.health, 99, "Damage working")
        
        test_player.gain_health()
        self.assertEqual(test_player.health, 99 + 12, "Health gain not working")
        
        "Health almost max"
        test_player.set_health(149.7)
        test_player.gain_health()
        self.assertEqual(test_player.health, 150, "Health gain not working when health almost at max")
        
        'Health reducing at low health reduces health possibly to under 0, but the GUI class handles the dying'
        
    def test_player_xy_updates(self):
        self.specs = [[30,3],[25,4],[100,30]]
        test_player = Player(self.specs[0])
        
        test_player.set_x_velocity(2)
        self.assertEqual(test_player.x_velocity, 2, 'X-velocity setting not working correctly')
        
        "movement Left"
        test_player.update_x(True, False)
        self.assertEqual(test_player.x(), 0, "Player should not move left at x = 0")
        
        'Moving left should reduce movement speed to right (2)'
        self.assertEqual(test_player.x_velocity, 1, "Moving left with positive x vel does not reduce x velocity")
        
        'Right'
        
        test_player.update_x(False,True)
        
        self.assertEqual(test_player.x(), 1, "Moving right should change player increase player x with x_vel")
        
        'Player slow down when no keys are pressed, but x vel > 0 or < 0'
        
        test_player.update_x(False,False)
        self.assertEqual(test_player.x_velocity, 0, 'Movement speed of 1 should be zero')
        
        
        
        "Y movement when not on a platform"
        init_y = test_player.y()
        test_player.update_y()
        self.assertGreater(test_player.y(), init_y, "Y should increase")
        
        "Y movement on plaform"
        test_player.y_on_platform = True
        init_y = test_player.y()
        test_player.update_y()
        self.assertEqual(init_y, test_player.y(), "Player should not fall when on platform")
        'Jumping'
        test_player.y_on_platform = True
        test_player.jump()
        test_player.update_y()
        self.assertGreater(init_y,test_player.y(),"Jumping should reduce player y value")
        
    def test_player_shooting(self):
        self.specs = [[30,3],[25,4],[100,30]]
        test_player = Player(self.specs[0])
        self.assertEqual(test_player.projectile, None)
        
        'Shooting'
        test_player.shoot(False)
        self.assertNotEqual(test_player.projectile, None, "shooting doesnt create a graphicitem projectile")
        
        test_player.update_projectile(600)
        self.assertGreater(test_player.projectile.x(), test_player.x(), 'Updating projectile moves it right')
        
    
    def test_platform_and_enemy(self):
        self.specs = [[30,3],[25,4],[100,30]]
        "PLATFORM"
        
        test_platform = Platform(100,100,100,100)
        
        init_x = test_platform.x
        
        'x vel for platform'
        test_platform.set_x_velocity(-2)
        
        "Platform movement when not scrolling (should be no movement)"
        'Player not moving'
        test_platform.update_x(False, False)
        self.assertEqual(init_x, test_platform.x, 'Platform should not move when player is stationary')
        
        'Player moving but not scrolling'
        test_platform.update_x(True, False)
        self.assertEqual(init_x, test_platform.x, 'Platform should not move when player is not scrolling')
        
        'Player scrolling'
        test_platform.update_x(True,True)
        self.assertEqual(init_x + test_platform.x_velocity, test_platform.x, 'Platform should move to the left')
        
        
        
        
        "ENEMY"
        
        'Enemy for the platform above'
        test_enemy = Enemy(test_platform.x , test_platform.y - 30, 25,25, test_platform, self.specs[1])
        
        'Health'
        self.assertEqual(test_enemy.health, 100, 'Health not what it should be on init')
        
        'Damage'
        test_enemy.take_damage()
        self.assertEqual(test_enemy.health, 95, "Wrong damage")
        
        "Dying"
        test_enemy.set_health(2)
        self.assertEqual(test_enemy.health, 2, "set_health not giving the wanted result")
        self.assertEqual(test_enemy.alive, True, "Enemy should be alive")
        
        test_enemy.take_damage()
        self.assertEqual(test_enemy.alive, False, "Enemy should be dead")
        
        "Movement"
        init_x = test_enemy.x
        test_enemy.update_x(False, False)
        self.assertGreater(test_enemy.x, init_x, "When on left edge the x should raise")
        print(test_enemy.x)
        
        
        "On right edge"
        test_enemy.set_x(test_platform.x + test_platform.width)
        self.assertEqual(test_enemy.x, test_platform.x + test_platform.width, "set_x not working")
        
        init_x_3 = test_enemy.x
        test_enemy.update_x(False,False)
        self.assertGreater(init_x_3, test_enemy.x, "Enemy should be moving left")
    
    
    
    
    
    
        
    
    def test_program_init_and_exit(self):
        self.specs = [[30,3],[25,4],[100,30]]
        self.gui = None
        self.gui_2 = None
        def thread_function():
            app = QtWidgets.QApplication(sys.argv)
            
            
            
            gui =GUI(app,self.specs)
            self.gui = gui
            print(gui,'1')
            gui.start()
          
          
            
        "The bot used as a tester"  
        testBot = QtTest.QTest
        
        'Threat to run app, otherwise the tests cant be run simultaneously'
        t1 = threading.Thread(target = thread_function)
        t1.start()
        
        time.sleep(2)
    
        t1.join(0)
        self.gui.exit_game()
        
        
        "Testing start menu exit button"
    
        exit_button = self.gui.exit_button
        
        testBot.mouseClick(exit_button, 1)
        time.sleep(0.5)
        self.assertEqual(self.gui.application_running, False, "Game not stopped")
        
        self.gui.exit_game()
        
        
    def test_program_start_and_mechanics(self):
        self.specs = [[30,3],[25,4],[100,30]]
        self.gui = None
        
        def thread_function():
            app = QtWidgets.QApplication(sys.argv)
            
            gui = GUI(app, self.specs)
            self.gui = gui
            print(gui,'1')
            gui.start()
          
          
            
        "The bot used as a tester"  
        testBot = QtTest.QTest
        
        'Threat to run app, otherwise the tests cant be run simultaneously'
        t1 = threading.Thread(target = thread_function)
        t1.start()
        
        time.sleep(1)
    
        
        
        "Testing start menu exit button"
    
        start_button = self.gui.start_button
        
        testBot.mouseClick(start_button, 1)
        time.sleep(1)
        self.assertEqual(self.gui.application_running, True, "Game running")
        self.assertEqual(self.gui.view.scene(), self.gui.scene, "Game scene not showing??")
        
        "Moving right and falling to lava"
        player = self.gui.test_player
        time.sleep(1)
        
        'Player is alive'
        self.assertGreater(player.health,0, 'Player should be alive and well')
    
        testBot.keyPress(self.gui,68)
        time.sleep(4)    
        testBot.keyRelease(self.gui, 68)
        
        self.assertEqual(self.gui.view.scene(), self.gui.Scen, "Menu should be showing")
        
        "Back in menu, can the game be restarted?"
        time.sleep(1)
        reStart_button = self.gui.start_button
        testBot.mouseClick(reStart_button, 1)
        time.sleep(1)
        
        self.assertEqual(self.gui.view.scene(), self.gui.scene, "Game should restart")
        player = self.gui.test_player
        
        
        
        
        "Testing enemies"
        time.sleep(1)
        platform = self.gui.platforms[0]
        print(platform, "PLATFOR")
        e_specs = self.specs[1]
        test_enemy = Enemy(platform.x, platform.y - 20, 30,30, platform, e_specs)
        
        self.gui.scene.addItem(test_enemy)
        self.gui.enemies.append(test_enemy)
        
        self.assertEqual(test_enemy.alive, True, "Test enemy is not alive?")
        
        
        "Shooting enemy"
        
        testBot.keyPress(self.gui, 32)
        testBot.keyRelease(self.gui, 32)
        time.sleep(1)
        testBot.keyPress(self.gui, 32)
        testBot.keyRelease(self.gui, 32)
        time.sleep(1)
        testBot.keyPress(self.gui, 32)
        testBot.keyRelease(self.gui, 32)
        health_0 = player.health
        time.sleep(2)
        
        self.assertEqual(test_enemy.alive, False, "Enemy should be dead")
        
        "ENEMY 2, damage from enemy touch?"
        
        platform = self.gui.platforms[0]
        test_enemy_2 = Enemy(platform.x, platform.y - 20, 30,30, platform,self.specs[1] ,1)
        
        self.gui.scene.addItem(test_enemy_2)
        self.gui.enemies.append(test_enemy_2)
        time.sleep(4)
    
        self.assertGreater(health_0, player.health, "Player should lose health when touched by enemy")
        self.gui.enemies.clear()
        self.gui.scene.removeItem(test_enemy_2)
        
        "ENEMY 3, damage from getting shot?"
        
        test_enemy_3 = Enemy(platform.x, platform.y - 20, 30,30, platform,self.specs[1] ,0)
        
        self.gui.scene.addItem(test_enemy_3)
        self.gui.enemies.append(test_enemy_3)
        time.sleep(5)
        self.assertEqual(self.gui.view.scene(), self.gui.Scen, "Menu should be up as the player died")
        self.gui.enemies.clear()
        self.gui.scene.removeItem(test_enemy_3)
        
        time.sleep(1)
        testBot.mouseClick(self.gui.start_button, 1)
        
        time.sleep(1)
        self.gui.completion = 9.99
        testBot.keyPress(self.gui, 68)
        time.sleep(2)
        testBot.keyPress(self.gui, 87)
        time.sleep(1)
        self.assertEqual(self.gui.view.scene,self.gui.Scen , "Winning should take the player to menu")
        
        
if __name__ == '__main__':
    unittest.main()