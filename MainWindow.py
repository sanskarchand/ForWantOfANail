#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
import config.const as const
from network.DownloadManager import DownloadManager
from ficparser import FicParser
import FicCard
import FicMain
import os, pickle
from model.StoryModel import FanficModel

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.loadedFicModels = []
        self.currentReadingFic = None
        self.currentReadingChapterIndex = None

        self.centralWidget = QtWidgets.QWidget()
        self.centralLayout = QtWidgets.QGridLayout()
        
        self.tabWidget = QtWidgets.QTabWidget()

        # tab 1 - reading tab
        self.splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.readNavWidget = QtWidgets.QWidget()
        self.readNavWidgetLayout = QtWidgets.QGridLayout()

        self.nextChapButton = QtWidgets.QPushButton()
        self.textInfoLabel = QtWidgets.QLabel("<NO TEXT>")
        self.chaptersComboBox = QtWidgets.QComboBox()
        self.prevChapButton = QtWidgets.QPushButton()

        self.htmlTextBrowser = QtWidgets.QTextBrowser()

        # tab 2-  library stuff
        self.tabLibContainer = QtWidgets.QWidget()
        self.tabLibCardContainer = QtWidgets.QWidget()

        self.tabLibContainerLayout = QtWidgets.QGridLayout()
        self.tabLibCardContainerLayout = QtWidgets.QGridLayout()
        self.filterAreaWidget = QtWidgets.QWidget()
        self.filterAreaLayout = QtWidgets.QHBoxLayout()
        self.filterFandomComboBoxLabel = QtWidgets.QLabel("Fandom:")
        self.filterFandomComboBox = QtWidgets.QComboBox()
        self.filterTagsEditLabel = QtWidgets.QLabel("Tags:")
        self.filterTagsEdit = QtWidgets.QLineEdit()
        self.filterTagsEditCompleter = None#QtWidgets.QCompleter()
        self.butFilterFics = QtWidgets.QPushButton("Filter")
        self.butPopulateLibrary = QtWidgets.QPushButton("&Populate")

        self.tabLibScrollArea = QtWidgets.QScrollArea()

        # tab 3 - Downloading stuff stuff
        self.tabDlContainer = QtWidgets.QWidget()
        self.tabDlLayout = QtWidgets.QGridLayout()
        self.tabDlFicContainer = QtWidgets.QWidget()
        self.tabDlFicLayout = QtWidgets.QVBoxLayout()

        self.urlBar = QtWidgets.QLineEdit()
        self.butDownloadFic = QtWidgets.QPushButton("&Add to Queue", self)
        self.butActualDownload = QtWidgets.QPushButton("&Download All", self)
        self.listDownloadFicWidgets = []

        # tab 4- temporary, for 
        self.tabFicDetailsContainer = QtWidgets.QWidget()
        self.tabFicDetailsLayout = QtWidgets.QVBoxLayout()
        
        
        # Other stuff
        self.downloadManager = DownloadManager(self)
      
        self.initializeGUI()

        self.postInitialization()

    #FIXME: temp fix for using cloudflare, match timings
    def tempDLGetButton(self):
        return self.butActualDownload

    
    def initializeGUI(self):
        
        self.centralWidget.setLayout(self.centralLayout)
        
        # -- TAB INITIALIZATION -- #
        container_1 = self.createReadingTab()
        container_2 = self.createLibraryTab()
        container_3 = self.createDownloadTab()
        container_4 = self.createDetailsTab()

        self.tabWidget.addTab(container_1, "Read")
        self.tabWidget.addTab(container_2, "Library")
        self.tabWidget.addTab(container_3, "Download Manager")
        self.tabWidget.addTab(container_4, "Fic Details")
        # -- TAB INITIALIZATION -- #

        self.centralLayout.addWidget(self.tabWidget, 0, 0)
        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("ForWantOfANail")
        self.setMinimumSize(*const.MIN_WIN_DIMENSIONS)

    def addFicDownloadWidget(self, widget):
        # the download manager should handle the updating
        self.tabDlFicLayout.addWidget(widget)

    
    def createReadingTab(self):

        self.readNavWidget.setLayout(self.readNavWidgetLayout)
        self.readNavWidgetLayout.setVerticalSpacing(0)
        
        # set button icons and other styles
        self.textInfoLabel.setStyleSheet("text-align: center;")
        style_1 = QtWidgets.QCommonStyle()
        self.prevChapButton.setIcon(style_1.standardIcon(QtWidgets.QStyle.SP_ArrowLeft))
        self.nextChapButton.setIcon(style_1.standardIcon(QtWidgets.QStyle.SP_ArrowRight))

        self.chaptersComboBox.setMinimumWidth(const.MIN_DROP_DOWN_WIDTH)

        #connect
        self.prevChapButton.released.connect(self.handleNavPrevPage)
        self.nextChapButton.released.connect(self.handleNavNextPage)
        self.chaptersComboBox.currentIndexChanged.connect(self.handleChangeDropDownTitle)

        # html alignment
        self.htmlTextBrowser.setAlignment(Qt.AlignLeft)

        self.readNavWidgetLayout.addWidget(self.textInfoLabel, 0, 1, Qt.AlignHCenter)
        self.readNavWidgetLayout.addWidget(self.prevChapButton, 1, 0, Qt.AlignLeft)
        self.readNavWidgetLayout.addWidget(self.chaptersComboBox, 1, 1, Qt.AlignHCenter)
        self.readNavWidgetLayout.addWidget(self.nextChapButton, 1, 2, Qt.AlignRight)

        self.splitter.addWidget(self.readNavWidget)
        self.splitter.addWidget(self.htmlTextBrowser)

        return self.splitter

    def createDownloadTab(self):

        self.tabDlContainer.setLayout(self.tabDlLayout)
        self.tabDlFicContainer.setLayout(self.tabDlFicLayout)
         
        self.tabDlLayout.setVerticalSpacing(0)
        self.tabDlLayout.setContentsMargins(0, 0, 0, 0)

        self.tabDlFicLayout.setSpacing(5)
        self.tabDlFicLayout.setContentsMargins(0, 0, 0, 0) # l, t, r, b
        self.tabDlFicLayout.setAlignment(Qt.AlignTop)


        # url example
        self.urlBar.setPlaceholderText("e.g. https://www.fanfiction.net/s/4390285/1/Searching-for-Disaster")

        self.tabDlLayout.addWidget(self.urlBar, 0, 0)
        self.tabDlLayout.addWidget(self.butDownloadFic, 0, 1)
        self.tabDlLayout.addWidget(self.butActualDownload, 1, 1)

        self.tabDlLayout.addWidget(self.tabDlFicContainer, 2, 0)

        # button.released is a PYQT_SIGNAL
        self.butDownloadFic.released.connect(self.handleFicDownload)
        self.butActualDownload.released.connect(self.handleActualDownload)

        return self.tabDlContainer

    def createLibraryTab(self):
        self.tabLibContainer.setLayout(self.tabLibContainerLayout)
        self.tabLibContainerLayout.setVerticalSpacing(0)
        self.tabLibContainerLayout.setAlignment(Qt.AlignTop)
        

        self.tabLibCardContainer.setLayout(self.tabLibCardContainerLayout)
        self.tabLibCardContainerLayout.setVerticalSpacing(5)
        self.tabLibCardContainerLayout.setAlignment(Qt.AlignTop)

        self.tabLibScrollArea.setWidget(self.tabLibCardContainer)
        self.tabLibScrollArea.setWidgetResizable(True)

        self.filterAreaWidget.setLayout(self.filterAreaLayout)
        self.filterAreaLayout.addWidget(self.filterFandomComboBoxLabel)
        self.filterAreaLayout.addWidget(self.filterFandomComboBox)
        self.filterAreaLayout.addWidget(self.filterTagsEditLabel)
        self.filterAreaLayout.addWidget(self.filterTagsEdit)
        self.filterAreaLayout.addWidget(self.butFilterFics)
        self.filterAreaLayout.addWidget(self.butPopulateLibrary)


        self.tabLibContainerLayout.addWidget(self.filterAreaWidget, 0, 0)
        #self.tabLibContainerLayout.addWidget(self.butPopulateLibrary, 0, 1)
        self.tabLibContainerLayout.addWidget(self.tabLibScrollArea, 1, 0)
        self.butPopulateLibrary.released.connect(self.handleFicPopulate)

        self.butFilterFics.released.connect(self.handleFicFilter)
        
        return self.tabLibContainer
    
    def createDetailsTab(self):
        self.tabFicDetailsContainer.setLayout(self.tabFicDetailsLayout)
        return self.tabFicDetailsContainer
    

    def postInitialization(self):

        if not os.path.exists(const.DEFAULT_META_PATH):
            os.makedirs(const.DEFAULT_META_PATH)
        if not os.path.exists(const.DEFAULT_FILE_PATH):
            os.makedirs(const.DEFAULT_FILE_PATH)

        self.handleFicPopulate()
        self.resetFilterElements()
        self.tabWidget.setCurrentIndex(1)

    def resetFilterElements(self):
        self.filterFandomComboBox.clear()

        fandom_set = set()
        tag_set = set()
        for fic in self.loadedFicModels:
            fandom_set.add(fic.metadata.fandom)
            tag_set.union(fic.tags)
            for fic in fic.metadata.fandomsCrossover:
                fandom_set.add(fic)
            
        
        fandom_list = list(fandom_set)
        fandom_list.sort()
        # filter for all fandoms at top | effectively a non-filter
        fandom_list.insert(0, const.FANDOM_ALL)

        self.filterFandomComboBox.addItems(fandom_list)
        self.filterTagsEditCompleter = QtWidgets.QCompleter(list(tag_set), self)
        self.filterTagsEdit.setCompleter(self.filterTagsEditCompleter)


    #--- SIGNALS --

    def handleFicPopulate(self):

        self.clearLayout(self.tabLibCardContainerLayout)


        target_files = os.listdir(const.DEFAULT_META_PATH)
        tempLoadedFicModels = []

        for filename in target_files:
            
            ind = filename.rfind(".")
            if filename[ind:] == ".json":
                # Un-pickle and add
                path = os.path.join(const.DEFAULT_META_PATH, filename)
                
                with open(path, "r") as fi:
                    json_string = fi.read()
                    ficModel = FanficModel()
                    ficModel.deserialize(json_string)
                    
                    # due to __eq__ magic method in FanficModel
                    if ficModel not in self.loadedFicModels:
                        tempLoadedFicModels.append(ficModel)
        
        self.loadedFicModels.extend(tempLoadedFicModels)
        
        for idx, model in enumerate(self.loadedFicModels):
            widget = FicCard.FicCard(self, model)
            row, col = self.getGridCoordsFromIndex(idx)
            self.tabLibCardContainerLayout.addWidget(widget, row, col)

        self.resetFilterElements()

    def handleFicFilter(self):
        self.clearLayout(self.tabLibCardContainerLayout)

        fics = self.loadedFicModels
        
        index = self.filterFandomComboBox.currentIndex()
        fi_fandom = self.filterFandomComboBox.itemText(index)
        fi_tags = self.filterTagsEdit.text().lstrip().rstrip()
        if fi_tags != '':
            fi_tags = set(fi_tags.split(" "))
        else:
            fi_tags = set([])


        if fi_fandom != '' and fi_fandom != const.FANDOM_ALL:
            fics = [fic for fic in fics if fic.metadata.fandom == fi_fandom or fi_fandom in fic.metadata.fandomsCrossover]

        if fi_tags:
            fics = [fic for fic in fics if fi_tags.issubset(fic.tags)]


        for idx, model in enumerate(fics):
            widget = FicCard.FicCard(self, model)
            row, col = self.getGridCoordsFromIndex(idx)
            self.tabLibCardContainerLayout.addWidget(widget, row, col)



        
    def handleFicDownload(self):
        text = self.urlBar.text()
        if text == "":
            pass

        self.downloadManager.appendRawFic(self.urlBar.text())

    def handleActualDownload(self):
        self.downloadManager.startDownloads()



    def handleNavNextPage(self):

        if self.currentReadingChapterIndex == self.currentReadingFic.metadata.numChapters - 1:
            return

        self.currentReadingChapterIndex += 1
        self.setReadingPage(self.currentReadingChapterIndex)

    def handleNavPrevPage(self):

        if self.currentReadingChapterIndex == 0:
            return
        self.currentReadingChapterIndex -= 1
        self.setReadingPage(self.currentReadingChapterIndex)


    def handleChangeDropDownTitle(self, index):
        self.setReadingPage(index)

    # --- utils

    def showFicDetails(self, ficModel):
        #self.tabFicDetails = FicMain.FicDescriptionWidget(ficModel)
        child = self.tabFicDetailsLayout.takeAt(0)
        if child and child.widget() is not None:
            child.widget().deleteLater()

        self.tabFicDetailsLayout.addWidget(FicMain.FicDescriptionWidget(ficModel))
        self.tabFicDetailsLayout.update()
        self.tabWidget.setCurrentIndex(3)

    def setReadingHTML(self, file_path):

        with open(file_path, "r") as f:
            dat = f.read()
            par = FicParser.FicParser(dat)
            mainHTML = par.getMainStory()

            self.htmlTextBrowser.setHtml(mainHTML)


    def setReadingPage(self, index):
        self.currentReadingChapterIndex = index
        self.setReadingHTML(self.currentReadingFic.realFiles[index])
        
        self.chaptersComboBox.setCurrentIndex(index)
        ficName = self.currentReadingFic.metadata.title
        #chapName = self.currentReadingFic.metadata.chapterTitles[index]

        label_text = ficName #+ "\n" + chapName
        self.textInfoLabel.setText(label_text)

    def setReadingFic(self, ficModel):
        self.currentReadingFic = ficModel

        #populate combobox
        self.chaptersComboBox.clear()
        for title in self.currentReadingFic.metadata.chapterTitles:
            self.chaptersComboBox.addItem(title)
        #self.currentReadingChapterIndex = 0
        self.setReadingPage(0)
        self.tabWidget.setCurrentIndex(0)
        #self.setReadingHTML(self.currentReadingFic.realFiles[0])

    


    def getGridCoordsFromIndex(self, index):

        row = index // 3
        col = index % 3

        return (row, col)
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

