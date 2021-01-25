#!/usr/bin/env python

from PyQt5 import QtWidgets, QtGui, QtCore
import MainWindow
import sys, os
import config.const as const

def main():
    app = QtWidgets.QApplication([])
    if const.QT_STYLE != '':
        app.setStyle(const.QT_STYLE)
    
    # set icon
    icon = QtGui.QIcon()
    icon.addFile('res/ffnet_icon.png', QtCore.QSize(60,60))
    app.setWindowIcon(icon) 
    
    mainWindow = MainWindow.MainWindow()
    mainWindow.show()

    if not os.path.exists(const.DEFAULT_META_PATH):
        os.makedirs(const.DEFAULT_META_PATH)
    if not os.path.exists(const.DEFAULT_FILE_PATH):
        os.makedirs(const.DEFAULT_FILE_PATH)
    

    sys.exit(app.exec_())


main()
