#!/usr/bin/env python

from PyQt5 import QtWidgets
import MainWindow
import sys

def main():
    app = QtWidgets.QApplication([])
    
    mainWindow = MainWindow.MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())


main()
