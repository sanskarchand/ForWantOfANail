#ifndef FANFICMODEL_H
#define FANFICMODEL_H

#include <string>
#include <vector>

struct StoryMetadata
{
    std::string title;
    std::string storyID;

    std::string author;
    std::string authorID;

    std::string fandom;

    std::string desc;

    std::vector<std::string> genreList;
    std::vector<std::string> characterList;

    std::string rating;

    int numchapters;
    int numWords;
    int numReviews;
    int numFavs;

    bool crossover = false;
    std::string crossFandom;
};


class FanficModel
{
public:
   FanficModel(StoryMetadata metaData):
    s_metaData(metaData)
   { }

   FanficModel(std::string fileName);
   ~FanficModel() {};


public:
    StoryMetadata  s_metaData;
    std::string    storyHTML;

    std::string     realFolder;

    // for in-application classification
    std::string    ficFolder;       //pun fully intended
    std::vector<std::string> ficTags;

public:
    inline StoryMetadata  getMetadata() { return s_metaData; }


};

#endif // FANFICMODEL_H
