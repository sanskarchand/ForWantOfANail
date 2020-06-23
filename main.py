#!/usr/bin/env python

from PyQt5 import QtWidgets
import MainWindow
import sys, os
import config.const as const

def main():
    app = QtWidgets.QApplication([])
    
    mainWindow = MainWindow.MainWindow()
    mainWindow.show()

    if not os.path.exists(const.DEFAULT_META_PATH):
        os.makedirs(const.DEFAULT_META_PATH)
    if not os.path.exists(const.DEFAULT_FILE_PATH):
        os.makedirs(const.DEFAULT_FILE_PATH)
    

    sys.exit(app.exec_())


main()
