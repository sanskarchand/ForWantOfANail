#!/usr/bin/env python 
import os
from config import const
from model.StoryModel import FanficModel
import argparse


# human-friendly format
FORMAT = "{title} by {author} [{storyID}]"

##============##
parser = argparse.ArgumentParser()
parser.add_argument("command", help="The main action verb. e.g. get-story, get-authors")
parser.add_argument("--sort-by", help="The criterion for sorting results")
##============##

loadedFicModels = []



def load_data():
    # TODO: add caching and optimizations here
    target_files = os.listdir(const.DEFAULT_META_PATH)
    tempLoadedFicModels = []

    for filename in target_files:
        
        ind = filename.rfind(".")
        if filename[ind:] == ".json":
            path = os.path.join(const.DEFAULT_META_PATH, filename)
            with open(path, "r") as fi:
                json_string = fi.read()
                ficModel = FanficModel()
                ficModel.deserialize(json_string)
                loadedFicModels.append(ficModel)

def get_story(args):
    result = []
    for ficModel in loadedFicModels:
        # filtering here
        result.append(ficModel)

    return result



def main():
    load_data()


    args = parser.parse_args()
    results = []

    match args.command:
        case "get-story":
            results = get_story(args)

    
    print(f"{len(results)} results")
    for ficModel in results:
        data = ficModel.metadata.serialize()
        print(FORMAT.format_map(data))




if __name__ == "__main__":
    main()
