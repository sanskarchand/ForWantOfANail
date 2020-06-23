#!/usr/bin/env python

import bs4
from model import StoryModel

class FicParser:

    def __init__(self, htmlContent):
        
        self.soup =  bs4.BeautifulSoup(htmlContent, "html.parser")


    def constructMetadata(self):

        #<span class='xgray xcontrast_txt'>Rated: <a class='xcontrast_txt' href='https://www.fictionratings.com/' target='rating'>Fiction  T</a> - English - Adventure/Humor -  Harry P. - Chapters: 10   - Words: 40,849 - Reviews: <a href='/r/4390285/'>1,070</a> - Favs: 2,874 - Follows: 3,062 - Updated: <span data-xutime='1244652529'>6/10/2009</span> - Published: <span data-xutime='1215902997'>7/12/2008</span> - id: 4390285 </span>
        
        titles =  self.soup.findAll("b", {"class": "xcontrast_txt"})
        summ = self.soup.findAll("div", {"class": "xcontrast_txt"})
        
        links = self.soup.findAll("a", {"class": "xcontrast_txt"})
        author_link = None
        for link in links:
            if "/u/" in link["href"]:
                author_link = link
                break
        

        huge_payload = self.soup.select("span.xgray.xcontrast_txt")
        payload_children = list(huge_payload[0].children)

        modelObject = StoryModel.StoryMetadata()
        
        """
        Parse the payload: Has 9 children;
        Indices:
            1 -> Rating (inside anchor tag)
            2 -> - Language - Genre1/Genre2 - Chapters:[num] - Words:[num] - Reviews:
            3 -> Reviews (inside anchor tag)
            4 -> Favs: [num] - Follows: [num] - Updated:
            5 -> updated (inside span tag), m/d/y
            7- > published (inside span tag)
            8 -> - id: [num]
        """
       
        modelObject.title = titles[0].text
        modelObject.storyID =  payload_children[8].split(":")[1].strip()
        modelObject.author = author_link.text
        modelObject.authorID = self.extractUserID(author_link["href"])
        modelObject.rating = payload_children[1].text
        modelObject.summary = summ[0].text

        index2_list = list( map(lambda x: x.strip(), payload_children[2].split("-")) )
        index4_list = list( map(lambda x: x.strip(), payload_children[4].split("-")) )


        extractKeyFunc  = lambda dat: dat.split(":")[1].strip()
        numFromStringFunc = lambda num_str: int(num_str.replace(",", ""))
        
        modelObject.genreList = index2_list[2].split("/")

        # Parsing decision depends on existence of character list
        if "Chapters:" in index2_list[3]:
            modelObject.numChapters = numFromStringFunc( extractKeyFunc(index2_list[3]) )
            modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[4]) )
        else:
            # single character listed
            if ',' not in index2_list[3]:
                modelObject.characterList.append( index2_list[3] )
            else:
                modelObject.characterList.extend( index2_list[3].split(",") )

            modelObject.numChapters = numFromStringFunc( extractKeyFunc(index2_list[4]) )
            modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[5]) )

        modelObject.language = index2_list[1]

        modelObject.numFavs = numFromStringFunc( extractKeyFunc(index4_list[1]) )
        modelObject.numFollows = numFromStringFunc( extractKeyFunc(index4_list[2]) )
        modelObject.numReviews = numFromStringFunc( payload_children[3].text )
    
        modelObject.updatedTimestamp = payload_children[5]["data-xutime"]
        modelObject.publishedTimestamp = payload_children[7]["data-xutime"]
        modelObject.publishedDateString = str(payload_children[7].text)

        preStoryDiv = self.soup.select("div#pre_story_links")[0]

        # note:: possible collision with author name tag?
        # Minimal chance of error: These section links always pop up before the author links
        # indices 0 and 1 for section. 
        sectionPath = preStoryDiv.select("a.xcontrast_txt")
        path = []
        for item in sectionPath:
            path.append(str(item.text))

        if len(path) == 1:
            modelObject.crossover = True

            # X + Y Crossover
            liste = path[0].split("+")
            fandom1 = liste[0]
            fandom2 = liste[1].split(" ")[1]
            modelObject.fandomsCrossover.extend([fandom1, fandom2])

        else:
            modelObject.category = path[0]
            modelObject.fandom = path[1]



        chapterNav = self.soup.select("#chap_select")[0]
        optionTags = chapterNav.findAll("option")

        #NOTE: since the option tags are not closed, the _text_ attribute gives the 
        #titles for all chapters. So, we do the following to get the pure titles
        temp_li = [tag.text for tag in optionTags]
        pure_chapter_titles = self.extractPureChapterTitles(temp_li)

        for chap_title in pure_chapter_titles:
            modelObject.chapterTitles.append(chap_title)
        
       
        modelObject.numChapters = len(modelObject.chapterTitles)
        
        """
        mainStoryDiv = self.soup.select("div.storytextp")[0]

        ficModel = StoryModel.FanficModel()
        ficModel.metadata = modelObject
        ficModel.storyHTML = str(mainStoryDiv)

        ficModel.setRealFolder()
        """

        return modelObject
        


    def extractUserID(self, profileURL):
        # /u/1602381/Shadow-Rebirth

        print("GIVEN: ", profileURL)
        return profileURL.split("/")[2]

    def extractPureChapterTitles(self, whack_titles):

        last = whack_titles[-1]
        # Rest of the whack titles in reverse order
        rev_ = list(reversed(whack_titles))[1:]
        pure_titles = []

        for tit in rev_:

            index = tit.find(last)
            pure_titles.append( tit[:index] )

            last = tit
        
        # Remove the serial numbers from the chapter names
        pure_titles = [title.split(".")[1].strip() for title in pure_titles]
        return pure_titles[::-1]

