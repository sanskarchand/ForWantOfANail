#!/usr/bin/env python

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
        self.storyHTML = None

        self.realFolder = None
        
        # For in-app
        self.ficFolder = None
        self.tags = []


    def getMetadata(self):
        return metadata
