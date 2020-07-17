#!/usr/bin/env python

import config.const as const
import pickle
import os

class IncompleteMetadataException(Exception):
    pass

class StoryMetadata:
    
    def __init__(self):
        
        #-- DAT_HEADING --
        self.title = None
        self.storyID = None
        
        self.author = None
        self.authorID = None
        
        #-- DAT_MAIN --
        self.category = None

        self.crossover = False
        self.fandom = None
        self.fandomsCrossover = []

        self.language = None
        self.summary = None
        self.genreList = []
        self.characterList = []
        self.pairingList = []
        self.chapterTitles = []


        self.rating = None
        self.numChapters = None
        self.numWords = None
        self.numReviews = None 
        self.numFavs = None
        self.numFollows = None


        self.updatedTimestamp = None
        self.publishedTimestamp = None
        self.publishedDateString = None

        self.imgUrlPath = "";
        self.hasImg = False;

    def verifySoundness(self):
        
        for k, v in vars(self).items():
            if v == None:
                raise IncompleteMetadataException()

    def generateXMLString(self):
        ''' 
        #-- DAT_HEADING --
        self.title = None
        self.storyID = None
        
        self.author = None
        self.authorID = None
        
        #-- DAT_MAIN --
        self.category = None

        self.crossover = False
        self.fandom = None
        self.fandomsCrossover = []

        self.language = None
        self.summary = None
        self.genreList = []
        self.characterList = []
        self.pairingList = []
        self.chapterTitles = []


        self.rating = None
        self.numChapters = None
        self.numWords = None
        self.numReviews = None 
        self.numFavs = None
        self.numFollows = None


        self.updatedTimestamp = None
        self.publishedTimestamp = None
        self.publishedDateString = None
        '''


    


    '''
    def __str__(self):
        return ("Fanfic Metadata\n"
                "Title:{}\n"
                "StoryID:{}\n"
                "Fandom:{}\n"
                "Description:{}\n"
                "Genres:{}\n").format(self.title, self.storyID, 
                        self.fandom, self.desc, self.genreList)
    '''



class FanficModel:
    
    def __init__(self):

        self.metadata = None
        
        self.realDirectory = None
        self.realFiles = []
        self.imageFilePath = None    

        # For in-app classification; pun fully intended
        self.ficPath = []
        self.tags = set()
    def __eq__(self, otherModel):
        return self.metadata.storyID == otherModel.metadata.storyID

    def addTag(self, tag):
        self.tags.add(tag)

    def addFilePath(self, path):
        self.realFiles.append(path)
        
    def getCleanPrefix(self):
        val = self.metadata.title
        for char in const.SPECIAL_CHARS:
            val = val.replace(char, "_")

        return val

    def getTagList(self):
        return list(self.tags)

    def setRealDirectory(self):
        self.realDirectory = policyGetRealFolder(self.metadata)

    def getMetadata(self):
        return metadata

    def getMetaFileName(self):
        return policyGetRealFolder(self.metadata) + ".ffmdata"
    
    def dumpToDisk(self):

        path  = const.DEFAULT_META_PATH
        path = os.path.join(path, self.getMetaFileName())

        with open(path, "wb") as fi:
            pickle.dump(self, fi)




def policyGetRealFolder(fanficMetadata):
    ''' 
    if fanficMetadata.crossover:
        name = "crossover"
    else:
        name = fanficMetadata.fandom.replace(" ", "_")
    '''
   
    name = fanficMetadata.title
    
    for char in const.SPECIAL_CHARS:
        name = name.replace(char, "_")


    return name + "_" + fanficMetadata.storyID
