#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5 import QtNetwork
from PyQt5 import QtWidgets
import PyQt5
from PyQt5 import QtCore
import config.const as const
import model.StoryModel as StoryModel

import queue
import os
import zlib
from ficparser import FicParser

class FicDownloadModel:

    def __init__(self, ficModel):
        self.ficModel = ficModel
        self.ficMetadata = self.ficModel.metadata
        self.storyID = self.ficMetadata.storyID
        self.chapters = self.ficMetadata.numChapters
        self.downloaded = 0

        self.urlQueue = queue.Queue()

        self.status = const.FicNetStatus.INITIATED
    
        self.labelMain = QtWidgets.QLabel(self.ficMetadata.title)
        self.labelDL = QtWidgets.QLabel("{}/{} chapters downloaded".format(0, self.chapters))

        self.widget = None
    
    def  update(self):
        self.labelDL.setText("{}/{} chapters downloaded".format(self.downloaded, self.chapters))
        
        '''
        if self.downloaded == self.chapters:
            self.status = const.FicNetStatus.COMPLETED
        '''
    def getInitialWidget(self):

        self.widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(layout)
    
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setStyleSheet("background-color: {};".format(const.COLOR_DL_QUEUE))
        self.labelMain.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.labelMain)
        layout.addWidget(self.labelDL)

        return self.widget




class DownloadManager(PyQt5.QtCore.QObject):

    def __init__(self, mainGUI):

        super().__init__()
        
        self.mainGUI = mainGUI
        self.manager = QtNetwork.QNetworkAccessManager()
        self.abstractFicQueue = queue.Queue()

        self.currentFic = None
        self.outputFile = QtCore.QFile()

        self.initialDownloadReply = None
        self.currentDownloadReply = None

    
    def appendRawFic(self, chapOneURL):
     
        url_ = QtCore.QUrl(chapOneURL)
        req = QtNetwork.QNetworkRequest(url_)
        self.initialDownloadReply = self.manager.get(req) # QNetworkReply
        self.initialDownloadReply.finished.connect(self.handleInitialDownloadFinished)

    def startDownloads(self):
        self.startNextFicDownload()


    def getFicQueue(self):
        return list(self.abstractFicQueue)
    '''
    def appendChapter(self, url):
        self.urlQueue.add(url)
    '''


    #--- SLOTS --
    def handleInitialDownloadFinished(self):
        
        # QByteArray type
        firstChapterData =  self.initialDownloadReply.readAll()
        pythonString = str(firstChapterData, "utf-8") 
        pythonString = self.getDecompressed( pythonString )

        #data_string = str(firstChapterData, "utf-8")
        data_string = pythonString
        
        par = FicParser.FicParser(data_string)
        
        #-- IMP SEQUENCE --
        init_metadata  = par.constructMetadata()
        ficModel = StoryModel.FanficModel()
        ficModel.metadata = init_metadata
        ficModel.setRealDirectory()
        #-- END --

        fic_dl_model = FicDownloadModel(ficModel)

        self.mainGUI.addFicDownloadWidget(fic_dl_model.getInitialWidget())

        self.abstractFicQueue.put(fic_dl_model)
        self.initialDownloadReply.deleteLater()

        #print("INIT DOWNLOAD HANDLED")

    def startNextFicDownload(self):

        if self.abstractFicQueue.empty():
            return
       
        #FicDownloadModel
        self.currentFic = self.abstractFicQueue.get()
        self.currentFic.status = const.FicNetStatus.DOWNLOADING
        
        path = os.path.join(const.DEFAULT_FILE_PATH, self.currentFic.ficModel.realDirectory)
        if not os.path.exists(path):
            os.makedirs(path)
        
        #populate chapter URL queue
        for chap_num in range(1, self.currentFic.chapters + 1):
            url = "https://www.fanfiction.net/s/{}/{}".format(self.currentFic.storyID, chap_num)
            self.currentFic.urlQueue.put(url)

        self.startNextDownload()

   

    def startNextDownload(self):
        
        curr_queue = self.currentFic.urlQueue

        if curr_queue.empty():
            self.currentFic.status = const.FicNetStatus.COMPLETED
            self.currentFic.ficModel.dumpToDisk()
            self.startNextFicDownload()
            return


        nextURL = curr_queue.get()
        myPrefix = self.currentFic.ficModel.getCleanPrefix()
        myFolder = self.currentFic.ficModel.realDirectory
        myPath = os.path.join(const.DEFAULT_FILE_PATH, myFolder)
        myFilename = myPrefix + "__Ch-" + str(self.currentFic.downloaded + 1) + ".html"
        
        fullPath = os.path.join(myPath, myFilename)

        self.currentFic.ficModel.addFilePath(fullPath)

        self.outputFile.setFileName(fullPath)
        self.outputFile.open(QtCore.QFile.WriteOnly)

        req = QtNetwork.QNetworkRequest(QtCore.QUrl(nextURL))
        self.currentDownloadReply = self.manager.get(req)
        self.currentDownloadReply.finished.connect(self.downloadFinished)
        self.currentDownloadReply.readyRead.connect(self.downloadReadyRead)




    def downloadFinished(self):
        self.outputFile.close()
        self.currentFic.downloaded += 1
        self.currentFic.update()
        self.startNextDownload()

    def downloadReadyRead(self):
        data = self.currentDownloadReply.readAll()
        pythonString = str(data, "utf-8")
        pythonString = self.getDecompressed(pythonString)
        # inefficient
        data = QtCore.QByteArray(bytes(pythonString, "utf-8")) 
        self.outputFile.write( data )


    def getDecompressed(self, data):

        if self.checkIfCompressed(data):
            print("GZIP COMPRESSION DETECTED!")
            return zlib.decompress(data, 16 + zlib.MAX_WBITS)

        return data

    def checkIfCompressed(self, data):

        # check first two bytes
        initialBytes = bytes(data[:2], "utf-8")
        
        return initialBytes[0] == 0x1f  and initialBytes[1] == 0x8b
    


