#!/usr/bin/env python

import config.const as const
import pickle
import os
import json

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
        self.hasImage = False;

    def verifySoundness(self):
        
        for k, v in vars(self).items():
            if v == None:
                raise IncompleteMetadataException()

    
    def serialize(self):
        dict_ = {
            'title': self.title,
            'storyID': self.storyID,
            'author': self.author,
            'authorID': self.authorID,


            'category': self.category,
            'fandom': self.fandom,
            'fandomsCrossover': self.fandomsCrossover,

            'language': self.language,
            'summary': self.summary,
            'genreList': self.genreList,
            'characterList': self.characterList,
            'pairingList': self.pairingList,
            'chapterTitles': self.chapterTitles,
            'rating': self.rating,
            'numChapters': self.numChapters,
            'numWords': self.numWords,
            'numReviews': self.numReviews,
            'numFavs': self.numFavs,
            'numFollows': self.numFollows,


            'updatedTimestamp': self.updatedTimestamp,
            'publishedTimestamp': self.publishedTimestamp,
            'publishedDateString': self.publishedDateString,

            'imgUrlPath': self.imgUrlPath,
            'hasImage': self.hasImage
        }
    
        
        return dict_
    
    def deserialize(self, json_dict):
        dict_ = json_dict

        self.title = dict_['title']
        self.storyID = dict_['storyID']
        self.author = dict_['author']
        self.authorID = dict_['authorID']


        self.category = dict_['category']
        self.fandom = dict_['fandom']
        self.fandomsCrossover = dict_['fandomsCrossover']

        self.language = dict_['language']
        self.summary = dict_['summary']
        self.genreList = dict_['genreList']
        self.characterList = dict_['characterList']
        self.pairingList = dict_['pairingList']
        self.chapterTitles = dict_['chapterTitles']
        self.rating = dict_['rating']
        self.numChapters = dict_['numChapters']
        self.numWords = dict_['numWords']
        self.numReviews = dict_['numReviews']
        self.numFavs = dict_['numFavs']
        self.numFollows = dict_['numFollows']

        self.updatedTimestamp = dict_['updatedTimestamp']
        self.publishedTimestamp = dict_['publishedTimestamp']
        self.publishedDateString = dict_['publishedDateString']

        self.imgUrlPath = dict_['imgUrlPath']
        self.hasImage = dict_['hasImage']



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
        return policyGetRealFolder(self.metadata) + ".json"
    
    
    def serialize(self):

        dict_ = {
                'ficPath': self.ficPath,
                'realDirectory': self.realDirectory,
                'realFiles': self.realFiles,
                'imageFilePath': self.imageFilePath,
                'tags': list(self.tags),

                'metadata': self.metadata.serialize()
        }

        return json.dumps(dict_, indent=4)
    
    def deserialize(self, json_string):
        dict_ = json.loads(json_string)

        
        self.ficPath = dict_['ficPath']
        self.realDirectory = dict_['realDirectory']
        self.realFiles = dict_['realFiles']
        self.imageFilePath = dict_['imageFilePath']
        self.tags = set(dict_['tags'])

        metadata_dict = dict_['metadata']
        self.metadata = StoryMetadata()
        self.metadata.deserialize(metadata_dict)
        

    def dumpToDisk(self):

        path  = const.DEFAULT_META_PATH
        path = os.path.join(path, self.getMetaFileName())

        with open(path, "w") as fi:
            fi.write(self.serialize())



    
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
