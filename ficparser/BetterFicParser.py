#!/usr/bin/env python

import bs4
from model import StoryModel
import config.const as const

class FicParser:

    def __init__(self, htmlContent):
        
        # Don't use html.parser - it auto-fixes tags and breaks on some fics
        # .e.g https://www.fanfiction.net/s/107806/1/Blackadder-Serpent-of-the-Seven-Seas
        self.soup =  bs4.BeautifulSoup(htmlContent, "html5lib")


    def getMainStory(self):

        # Add left alignment to all paragraph tags.
        # Otherwise, all the text will show up center-aligned, and that wouldn't be very pleasant to read
        paras = self.soup.select("div.storytextp")[0].findAll("p")
        for p in paras:
            p["style"]= "text-align: left;"

        return  str(self.soup.select("div.storytextp")[0])
        

    def constructMetadata(self):

        #<span class='xgray xcontrast_txt'>Rated: <a class='xcontrast_txt' href='https://www.fictionratings.com/' target='rating'>Fiction  T</a> - English - Adventure/Humor -  Harry P. - Chapters: 10   - Words: 40,849 - Reviews: <a href='/r/4390285/'>1,070</a> - Favs: 2,874 - Follows: 3,062 - Updated: <span data-xutime='1244652529'>6/10/2009</span> - Published: <span data-xutime='1215902997'>7/12/2008</span> - id: 4390285 </span>
        titles =  self.soup.findAll("b", {"class": "xcontrast_txt"})
        summ = self.soup.findAll("div", {"class": "xcontrast_txt"})
        has_image = False   # either there is no image, or ffnet is preventing us from seeing it (script.png)


        image_tags = self.soup.findAll("img", {"class": "cimage"})
        if image_tags:
            image_tag = image_tags[0]
            image_link = "" 
            if image_tag.has_attr("data-original"):
                has_image = True
                image_link = image_tag["data-original"]
                print("image_link: ", image_link)




        links = self.soup.findAll("a", {"class": "xcontrast_txt"})
        author_link = None
        for link in links:
            if "/u/" in link["href"]:
                author_link = link
                break
        
        profile_top = self.soup.find("div", {"id": "profile_top"})
        if profile_top is None:
            print("Error: the fic is only half-downloaded (page not fully loaded). Try again later")

        huge_payload = profile_top.select("span.xgray.xcontrast_txt")
        payload_children = list(huge_payload[0].children)

        modelObject = StoryModel.StoryMetadata()
        modelObject.hasImage = has_image

        #modelObject.imgUrlPath = "https://" + image_link[2:]
        modelObject.imgUrlPath = "https://fanfiction.net" + image_link
        
        #payload_children[2] = payload_children[2].replace("Sci-Fi", "SciFi")
        
        # Does not account for fics that are uploaded at once, with all their chapters (e.g. reuploads)       
        #isOneShot = "Updated" not in payload_children[4]
        
        missingUpdatedField = "Updated" not in payload_children[4]
        isOneShot = True
        for idx, plchd in enumerate(payload_children):
            #print(idx, plchd)
            ind = str(plchd).find("Chapters:")
            if ind != -1:
                isOneShot = False     
               
                
       
        modelObject.title = titles[0].text
        
        '''
        print("DEBUG PAYLOAD")
        for idx, c  in enumerate(payload_children):
                print(f"{idx}\t=>\t{c}")
        '''

        if missingUpdatedField:
            
            modelObject.storyID =  payload_children[6].split(":")[-1].strip()
        else:
            modelObject.storyID =  payload_children[8].split(":")[-1].strip()

        modelObject.author = author_link.text
        modelObject.authorID = self.extractUserID(author_link["href"])
        modelObject.rating = payload_children[1].text
        modelObject.summary = summ[0].text

        index2_list = list( map(lambda x: x.strip(), payload_children[2].split(" - ")) )
        index4_list = list( map(lambda x: x.strip(), payload_children[4].split(" - ")) )


        extractKeyFunc  = lambda dat: dat.split(":")[1].strip()
        numFromStringFunc = lambda num_str: int(num_str.replace(",", ""))
        
        modelObject.genreList = index2_list[2].split("/")
        if "Hurt" in modelObject.genreList:
            ind = modelObject.genreList.index("Hurt")
            modelObject.genreList.pop(ind)  # pop 'Hurt'
            modelObject.genreList.pop(ind)  # pop 'Comfort'
            modelObject.genreList.insert(ind, "Hurt/Comfort")


        # Parsing decision depends on existence of character list, which in turn depends on 
        #   whether the fic is a oneshot

        #modelObject.numChapters = numFromStringFunc( extractKeyFunc(index2_list[3]) )
        #modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[4]) )
        modelObject.characterList.append( index2_list[3] )
        #modelObject.language = index2_list[1]

        #modelObject.numFavs = numFromStringFunc( extractKeyFunc(index4_list[1]) )
        #modelObject.numFollows = numFromStringFunc( extractKeyFunc(index4_list[2]) )
        #modelObject.numReviews = numFromStringFunc( payload_children[3].text )

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

            ind_plus = path[0].index("+") # the first plus
            ind_cross = path[0].index("Crossover")

            fandom1 = path[0][:ind_plus].strip()
            fandom2 = path[0][ind_plus+1:ind_cross].strip()

            modelObject.fandomsCrossover.extend([fandom1, fandom2])
            modelObject.fandom = const.FANDOM_CROSSOVER

        else:
            modelObject.category = path[0]
            modelObject.fandom = path[1]

        
        if not isOneShot:
            chapterNav = self.soup.select("#chap_select")[0]
            optionTags = chapterNav.findAll("option")

            #NOTE: since the option tags are not closed, the _text_ attribute gives the 
            #titles for all chapters. So, we do the following to get the pure titles
            temp_li = [tag.text for tag in optionTags]
            pure_chapter_titles = self.extractPureChapterTitles(temp_li)

            for chap_title in pure_chapter_titles:
                modelObject.chapterTitles.append(chap_title)
            
           
            modelObject.numChapters = len(modelObject.chapterTitles)
        else:
            modelObject.chapterTitles.append("<Oneshot>")
        
        return modelObject
        


    def extractUserID(self, profileURL):
        # /u/1602381/Shadow-Rebirth

        #print("GIVEN: ", profileURL)
        return profileURL.split("/")[2]

    def extractPureChapterTitles(self, whack_titles):

        # After using html5lib instead of html.parser, this too is unnecessary
        return whack_titles

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
