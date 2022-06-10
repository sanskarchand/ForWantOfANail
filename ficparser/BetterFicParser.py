#!/usr/bin/env python

import bs4
from model import StoryModel
import config.const as const
import pprint
from collections import defaultdict

ELEM_KEYWORDS = ["Rated",
                 "Chapters", "Words",
                 "Reviews", "Favourites", "Follows",
                 "Updated", "Published", "id"
                ]


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
       


    def extractNamedElem(self, elem_string, metadata_text):
        ind  = metadata_text.find(elem_string) 
        if ind == -1:
            return None
        
        val = metadata_text[ind:]
        return val

    def extractNamedValue(self, elem_string, metadata_text):
        whole = self.extractNamedElem(elem_string, metadata_text)
        if whole is None:
            return None

        idx = whole.find(":")
        if idx == -1:
            print("error: colon missing during parsing of ", elem_string)
            return None
        
        delim_idx = whole.find(" - ", idx+1)
        return whole[idx+2:delim_idx]
    
    def intFromString(self, string):
        return int(string.replace(",", ""))
        
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
                print("auth link", link)
                author_link = link
                break
        
        profile_top = self.soup.find("div", {"id": "profile_top"})
        if profile_top is None:
            print("Error: the fic is only half-downloaded (page not fully loaded). Try again later")

        mdata_dates_raw = self.soup.findAll("span", {"data-xutime": True})
        mdata_dates = defaultdict(str)
        for date in mdata_dates_raw:
            if "Published" in date.previous_sibling.text:
                mdata_dates["published"] = date["data-xutime"]
            elif "Updated" in date.previous_sibling.text:
                mdata_dates["updated"] = date["data-xutime"]


        huge_payload = profile_top.select("span.xgray.xcontrast_txt")
        payload_children = list(huge_payload[0].children)
        all_mdata_text = ''.join([pc.text for pc in payload_children])

        # do some preprocessing before this
        all_mdata_text = all_mdata_text.replace("Sci-Fi", "SciFi")
        print(all_mdata_text)

        modelObject = StoryModel.StoryMetadata()
        modelObject.hasImage = has_image
        modelObject.imgUrlPath = "https://fanfiction.net" + image_link

    
        # Now, onto the actual parsing
        # Element order (square brackets denote optional presence, and
        # angle brackets are for required elems)
        # <rating><genre>[character list][chapters]<words>[review][favs][follows][updated]<published><storyid>

        published = self.extractNamedValue("Published", all_mdata_text)
        print('published is ', published)
        updated = self.extractNamedValue("Updated", all_mdata_text)
        storyID = self.extractNamedValue("id", all_mdata_text)
        numChapters = self.extractNamedValue("Chapters", all_mdata_text)
        rated = self.extractNamedValue("Rated", all_mdata_text)


        missingUpdatedField = updated is None
        isOneShot = numChapters is None

        modelObject.title = titles[0].text
        modelObject.author = author_link.text
        modelObject.authorID = self.extractUserID(author_link["href"])
        modelObject.storyID = storyID
        modelObject.rating = rated
        modelObject.summary = summ[0].text
        modelObject.numChapters = int(numChapters or 1)
        modelObject.rating = rated
        modelObject.publishedTimestamp = mdata_dates["published"]
        modelObject.updatedTimestamp = mdata_dates["updated"]

        
        modelObject.genreList = all_mdata_text.split("-")[2].split("/")

        #modelObject.genreList = index2_list[2].split("/")

        if "Hurt" in modelObject.genreList:
            ind = modelObject.genreList.index("Hurt")
            modelObject.genreList.pop(ind)  # pop 'Hurt'
            modelObject.genreList.pop(ind)  # pop 'Comfort'
            modelObject.genreList.insert(ind, "Hurt/Comfort")


        # Extract chapter titles
        if not isOneShot:
            chapter_nav = self.soup.select("#chap_select")[0]
            option_tags = chapter_nav.findAll("option")

            temp_li = [tag.text for tag in option_tags]
            pure_chap_titles = self.extractPureChapterTitles(temp_li)
            modelObject.chapterTitles.extend(pure_chap_titles)
        else:
            modelObject.chapterTitles.append("<Oneshot>")

        
        

        # Extract fandom stuff
        preStoryDiv = self.soup.select("div#pre_story_links")[0]
        sectionPath = preStoryDiv.select("a.xcontrast_txt")
        path = [str(item.text) for item in sectionPath]
        
        if len(path) == 1:
            modelObject.crossover = True
            modelObject.fandom = const.FANDOM_CROSSOVER
            modelObject.fandomsCrossover = self.extractCrossoverFandoms(path[0])
        else:
            modelObject.category = path[0].strip()
            modelObject.fandom = path[1].strip()
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(modelObject.__dict__)

        return modelObject # return metadata
        
    def extractCrossoverFandoms(self, path):
        if path.count("+") == 2:
            print("Warning: crossover: fandom name has + in it")

        idx = path.index("+")
        idx2 = path.index(" Crossover")

        fandom1 = path[:idx].strip()
        fandom2 = path[idx+1:idx2].strip()
        return [fandom1, fandom2]


    def extractUserID(self, profileURL):
        # /u/1602381/Shadow-Rebirth

        #print("GIVEN: ", profileURL)
        idx = profileURL.find("/u/") + 3
        idx2 = profileURL.find("/", idx)
        return profileURL[idx:idx2]


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

