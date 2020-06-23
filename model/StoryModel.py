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

    def verifySoundness(self):
        
        for k, v in vars(self).items():
            if v == None:
                raise IncompleteMetadataException()
    
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
        
        # For in-app classification; pun fully intended
        self.ficPath = []
        self.tags = set()

    def addTag(self, tag):
        self.tags.add(tag)

    def addFilePath(self, path):
        self.realFiles.append(path)
        
    def getCleanPrefix(self):
        return self.metadata.title.replace(" ", "_").replace("'", "_")

    def setRealDirectory(self):
        self.realDirectory = policyGetRealFolder(self.metadata)

    def getMetadata(self):
        return metadata
    
    def dumpToDisk(self):

        path  = const.DEFAULT_META_PATH
        path = os.path.join(path, policyGetRealFolder(self.metadata) + ".ffmdata") 

        with open(path, "wb") as fi:
            pickle.dump(self, fi)



def policyGetRealFolder(fanficMetadata):
    ''' 
    if fanficMetadata.crossover:
        name = "crossover"
    else:
        name = fanficMetadata.fandom.replace(" ", "_")
    '''
    name = fanficMetadata.title.replace(" ", "_")
    name = name.replace("'", "_")

    return name + "_" + fanficMetadata.storyID
