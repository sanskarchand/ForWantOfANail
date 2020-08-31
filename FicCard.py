#!/usr/bin/env python

from PyQt5.Qt import QMenu
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QColor 

import config.const as const 
class FicCard(QtWidgets.QWidget):

    def __init__(self, refMainLayout, ficModel):

        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # Looks weird due to the gaps caused by the layout 
        #self.setStyleSheet("background-color: {}".format(const.COLOR_FIC_CARD))
        #self.setStyleSheet("QWidget { border: 1px solid black; }")
        self.setBgColor(const.COL_TUPLE_FIC_CARD) 
        self.setAutoFillBackground(True)

        self.labelTitle = QtWidgets.QLabel(ficModel.metadata.title)
        self.labelTitle.setStyleSheet("font-weight: bold;")
        self.labelTitle.setWordWrap(True)
        
        if ficModel.metadata.crossover:
            label = ficModel.metadata.fandomsCrossover[0] + " and " + ficModel.metadata.fandomsCrossover[1] + " crossover"
            self.labelFandom = QtWidgets.QLabel(label)
        else:
            self.labelFandom = QtWidgets.QLabel(ficModel.metadata.fandom)
        self.labelFandom.setWordWrap(True)

        self.labelAuthor = QtWidgets.QLabel("By " + ficModel.metadata.author)
        self.labelAuthor.setStyleSheet("font-style: italic;")
        self.labelAuthor.setWordWrap(True)
        
        tag_string = "Tags: " + ", ".join(ficModel.getTagList())
        self.labelTags = QtWidgets.QLabel(tag_string)
        self.labelTags.setWordWrap(True)



        self.layout.addWidget(self.labelTitle)
        self.layout.addWidget(self.labelFandom)
        self.layout.addWidget(self.labelAuthor)
        self.layout.addWidget(self.labelTags)

        self.refMainLayout  = refMainLayout
        self.ficModel = ficModel
        
        self.menu = QMenu(self)
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.action_tags = self.menu.addAction("Edit Tags")
    
    def setBgColor(self, col_tuple):
        myPalette = self.palette()
        bgColor = QColor(*col_tuple)
        myPalette.setColor(QPalette.Background, bgColor)
        self.setPalette(myPalette)
    
    def mousePressEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        self.setBgColor(const.COL_TUPLE_FIC_CARD_PRESSED)

    def mouseReleaseEvent(self, event):
        self.refMainLayout.setReadingFic(self.ficModel)
        self.setBgColor(const.COL_TUPLE_FIC_CARD)
    # Context menu policy
    def contextMenuEvent(self, event):
        action = self.menu.exec_(self.mapToGlobal(event.pos()))
        if action == self.action_tags:
            self.refMainLayout.showFicDetails(self.ficModel)

    def refreshCards(self):
        pass


