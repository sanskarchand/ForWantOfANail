#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
import config.const as const
from network.DownloadManager import DownloadManager

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.centralWidget = QtWidgets.QWidget()
        self.centralLayout = QtWidgets.QGridLayout()
        
        self.tabWidget = QtWidgets.QTabWidget()
        self.splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.htmlTextBrowser = QtWidgets.QTextBrowser()

        # tab 3 - Downloading stuff stuff
        self.tabDlContainer = QtWidgets.QWidget()
        self.tabDlLayout = QtWidgets.QGridLayout()
        self.tabDlFicContainer = QtWidgets.QWidget()
        self.tabDlFicLayout = QtWidgets.QVBoxLayout()

        self.urlBar = QtWidgets.QLineEdit()
        self.butDownloadFic = QtWidgets.QPushButton("&Add to Queue", self)
        self.butActualDownload = QtWidgets.QPushButton("&Download All", self)
        self.listDownloadFicWidgets = []
        
        
        # Other stuff
        self.downloadManager = DownloadManager(self)
      
        self.initializeGUI()
    
    def initializeGUI(self):
        
        self.centralWidget.setLayout(self.centralLayout)
        self.splitter.addWidget(QtWidgets.QLabel("Hahaha"))
        self.splitter.addWidget(self.htmlTextBrowser)

        # -- TAB INITIALIZATION -- #
        container_1 = self.splitter
        container_2 = QtWidgets.QWidget()
        container_3 = self.createDownloadBar()

        self.tabWidget.addTab(container_1, "Read")
        self.tabWidget.addTab(container_2, "Library")
        self.tabWidget.addTab(container_3, "Download Manager")
        # -- TAB INITIALIZATION -- #

        self.centralLayout.addWidget(self.tabWidget, 0, 0)
        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("ForWantOfANail")
        self.setMinimumSize(*const.MIN_WIN_DIMENSIONS)

    def addFicDownloadWidget(self, widget):
        # the download manager should handle the updating
        self.tabDlFicLayout.addWidget(widget)


    def createDownloadBar(self):

        self.tabDlContainer.setLayout(self.tabDlLayout)
        self.tabDlFicContainer.setLayout(self.tabDlFicLayout)
         
        self.tabDlFicContainer.setStyleSheet("background-color:#" + const.COLOR_DL_QUEUE + ";")
        self.tabDlLayout.setVerticalSpacing(0)
        self.tabDlFicLayout.setSpacing(0)

        self.tabDlLayout.addWidget(self.urlBar, 0, 0, Qt.AlignTop)
        self.tabDlLayout.addWidget(self.butDownloadFic, 0, 1, 
                Qt.AlignTop)
        self.tabDlLayout.addWidget(self.butActualDownload, 1, 1, Qt.AlignTop)

        self.tabDlLayout.addWidget(self.tabDlFicContainer, 2, 0)

        # button.released is a PYQT_SIGNAL
        self.butDownloadFic.released.connect(self.handleFicDownload)
        self.butActualDownload.released.connect(self.handleActualDownload)

        return self.tabDlContainer


    def handleFicDownload(self):
        text = self.urlBar.text()
        if text == "":
            pass

        self.downloadManager.appendRawFic(self.urlBar.text())

    def handleActualDownload(self):
        self.downloadManager.startDownloads()

