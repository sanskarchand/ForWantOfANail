#!/usr/bin/env python

import datetime

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPalette, QColor

import config.const as const

class FicDescriptionWidget(QtWidgets.QWidget):

    def __init__(self, ficModel):
        super().__init__()
        self.ficModel = ficModel
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)


        self.rightContainer = QtWidgets.QWidget()
        self.leftContainer = QtWidgets.QWidget()
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.rightContainer.setLayout(self.rightLayout)
        self.leftContainer.setLayout(self.leftLayout)
        

        # -- RIGHT SIDE --
        self.titleLabel = QtWidgets.QLabel("<b>Title</b>: " + ficModel.metadata.title)
        self.authorLabel = QtWidgets.QLabel("<i>Author</i>: " + ficModel.metadata.author)
        self.summaryLabel = QtWidgets.QLabel("<b>Desc:</b>: " + ficModel.metadata.summary)
        self.summaryLabel.setWordWrap(True)
        #debug drawing
        #self.titleLabel.setStyleSheet("border: 1px solid black;")
        #self.authorLabel.setStyleSheet("border: 1px solid black;")

        self.editTagsLabel = QtWidgets.QLabel("Enter tags below (one per line, and spaces denoted by underscores" +
                                        "<i>e.g. all_time_favorite</i>)")
        self.editTagsLabel.setWordWrap(True)
        self.editTagsArea = QtWidgets.QPlainTextEdit()
        self.editTagsButton = QtWidgets.QPushButton("Save Tags")
        self.editTagsButton.released.connect(self.handleSaveTags)

        text = "" 
        for ind, tag in enumerate(ficModel.tags):
            text += tag
            if ind != len(ficModel.tags) - 1:
                text += "\n"
        self.editTagsArea.setPlainText(text)


        #-- LEFT SIDE ---
        self.imageLabel = QtWidgets.QLabel()
        self.imagePixmap = None
        if ficModel.metadata.hasImage:
            self.imagePixmap = QtGui.QPixmap(self.ficModel.imageFilePath)
        else:
            self.imagePixmap = QtGui.QPixmap(const.RES_NOIMG_PATH)

        self.imageLabel.setPixmap(self.imagePixmap)

        self.infoLabel = QtWidgets.QLabel()
        
        self.info_text = ""

        if ficModel.metadata.updatedTimestamp:
            val = datetime.datetime.fromtimestamp(int(ficModel.metadata.updatedTimestamp))
            updated_string = f"{val:%Y-%m-%d %H:%M:%S}"
            self.info_text += "<b>Updated: </b>" + updated_string + "<br>"
        
        val = datetime.datetime.fromtimestamp(int(ficModel.metadata.publishedTimestamp))
        published_string = f"{val:%Y-%m-%d %H:%M:%S}"
        self.info_text += "<b>Published: </b>" + published_string + "<br>"
        
        fandomStr = None
        if ficModel.metadata.crossover:
            fandomStr = ficModel.metadata.fandomsCrossover[0] + " and "
            fandomStr += ficModel.metadata.fandomsCrossover[1] + " crossover"
        else:
            fandomStr = ficModel.metadata.fandom

        self.info_text += "<b>Fandom: </b>" + fandomStr + "<br>"

        self.info_text += "<b>Words: </b>" + str(ficModel.metadata.numWords) + "<br>"
        self.info_text += "<b>Chapters: </b>" + str(ficModel.metadata.numChapters) + "<br>"
        
        if len(ficModel.metadata.characterList):
            self.info_text += "<b>Characters: </b>" + ", ".join(ficModel.metadata.characterList) + "<br>"

        self.info_text += "<b>Genres: </b>" + ", ".join(ficModel.metadata.genreList)

        self.infoLabel.setText(self.info_text)
        self.infoLabel.setWordWrap(True)
        

        

        self.layout.addWidget(self.leftContainer)
        self.layout.addWidget(self.rightContainer)
        
        self.rightLayout.setSpacing(0)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.addWidget(self.titleLabel, Qt.AlignTop)
        self.rightLayout.addWidget(self.authorLabel, Qt.AlignTop)
        self.rightLayout.addWidget(self.summaryLabel, Qt.AlignTop)

        self.rightLayout.addWidget(self.editTagsLabel, Qt.AlignTop)
        self.rightLayout.addWidget(self.editTagsArea, Qt.AlignTop)
        self.rightLayout.addWidget(self.editTagsButton, Qt.AlignTop)

        self.leftLayout.addWidget(self.imageLabel, Qt.AlignTop)
        self.leftLayout.addWidget(self.infoLabel, Qt.AlignTop)


    # signals
    def handleSaveTags(self):
        data = self.editTagsArea.toPlainText()
        tags = set(data.split("\n"))

        if tags != self.ficModel.tags:
            #self.ficModel.tags = self.ficModel.tags.union(tags)
            self.ficModel.tags = tags
            self.ficModel.dumpToDisk()


