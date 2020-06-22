#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5 import QtNetwork
import PyQt5
from PyQt5 import QtCore
import queue

from parser import FicParser

class DownloadManager(PyQt5.QtCore.QObject):

    def __init__(self):

        super().__init__()
        
        self.manager = QtNetwork.QNetworkAccessManager()
        self.urlQueue = queue.Queue()

        self.initialDownloadReply = None
        self.currentDownloadReply = None
    
    def appendRawFic(self, chapOneURL):
        
        url_ = QtCore.QUrl(chapOneURL)
        req = QtNetwork.QNetworkRequest(url_)
        self.initialDownloadReply = self.manager.get(req) # QNetworkReply

        self.initialDownloadReply.finished.connect(self.handleInitialDownloadFinished)

    def appendChapter(self, url):
        self.urlQueue.add(url)

    #--- SLOTS --
    def handleInitialDownloadFinished(self):

        firstChapterData = self.initialDownloadReply.readAll()
        data_string = str(firstChapterData, "utf-8")
        
        par = FicParser.FicParser(data_string)
        metadata = par.getMetadata()

        self.initialDownloadReply.deleteLater()


