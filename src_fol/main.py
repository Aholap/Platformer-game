'''
Created on Mar 4, 2020

@author: Patedddd
'''
import sys
from PyQt5.QtWidgets import QApplication
from GUI import GUI



def main():
    f = open("obj_specs.txt", "r")
    init_specs = []
    line = f.readline()
    while line:
        if line.rstrip():
            
            data = (line.rstrip().split(':'))[1].split(',')
            for i in range(len(data)):
                data[i] = data[i].strip()
            
            init_specs.append(data)
        line = f.readline()
   
    app = QApplication(sys.argv)
    
    gui = GUI(app, init_specs)
    gui.application.exec_()
    'app.exec_()'
    
main()