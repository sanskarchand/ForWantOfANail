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
        

        # No longer needed after the switch to html5lib
        stringFinal = ""
        for child in self.soup.select("div.storytextp")[0].children:
            print("CHILD = ", str(child))
            stringFinal += str(child)
        return stringFinal
        

    def constructMetadata(self):

        #<span class='xgray xcontrast_txt'>Rated: <a class='xcontrast_txt' href='https://www.fictionratings.com/' target='rating'>Fiction  T</a> - English - Adventure/Humor -  Harry P. - Chapters: 10   - Words: 40,849 - Reviews: <a href='/r/4390285/'>1,070</a> - Favs: 2,874 - Follows: 3,062 - Updated: <span data-xutime='1244652529'>6/10/2009</span> - Published: <span data-xutime='1215902997'>7/12/2008</span> - id: 4390285 </span>
        titles =  self.soup.findAll("b", {"class": "xcontrast_txt"})
        summ = self.soup.findAll("div", {"class": "xcontrast_txt"})
        #image_tag = self.soup.findAll("div", attrs={"data-original"}) #<REM>
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
            print("Error: the fic is only half-downloaded. Try again later")

        huge_payload = profile_top.select("span.xgray.xcontrast_txt")
        payload_children = list(huge_payload[0].children)

        modelObject = StoryModel.StoryMetadata()
        modelObject.hasImage = has_image

        #modelObject.imgUrlPath = "https://" + image_link[2:]
        modelObject.imgUrlPath = "https://fanfiction.net" + image_link
        
        """
        Parse the payload: Has 9 children;
        Indices:
            1 -> Rating (inside anchor tag)
            2 -> - Language - Genre1/Genre2 - Chapters:[num] - Words:[num] - Reviews:
            3 -> Reviews (inside anchor tag)
            4 -> Favs: [num] - Follows: [num] - Updated:
            5 -> updated (inside span tag), m/d/y
            7- > published (inside span tag)
            8 -> - id: [num] ( if complete, - Status: Complete - id: [num] )


            --- alt, if oneshot
            if no reviews:
                2->  - Language - Genre1/Genre2 - Words:[num] -Favs:[num] - Follows: [num] - Published:
                3 -> published (inside span tag)
                4 -> - id: [num] ( if complete, - Status: Complete - id: [num] )

                Code will change this to the below format


            2 -> - Language - Genre1/Genre2 - Words:[num] - Reviews:
            5-> published (inside span tag)
            6 -> - id: [num] ( if complete, - Status: Complete - id: [num] )
        """

        # handle the no-review one-shot case gracefully
        # handle this later
        '''
        if 'Reviews' not in payload_children[2] and 'Updated' not in payload_children[4]:
        
            while len(payload_children) < 7:
                payload_children.append(None)

            favs_index = payload_children[2].find('- Favs')
            rem = payload_children[2][favs_index:]
            payload_children[2] = payload_children[2][:favs_index]  + " - Reviews:"
            



            payload_children[5] = payload_children[3]
            payload_children[6] = payload_children[4]
        '''

        # Sci-Fi genere -> problems
        payload_children[2] = payload_children[2].replace("Sci-Fi", "SciFi")
        
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

        if not isOneShot:
            if "Chapters:" in index2_list[3]:
                modelObject.numChapters = numFromStringFunc( extractKeyFunc(index2_list[3]) )
                modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[4]) )
            else:
                # single character listed
                if ',' not in index2_list[3]:
                    modelObject.characterList.append( index2_list[3] )
                else:
                    modelObject.characterList.extend( index2_list[3].split(",") )

                print("Li = ", index2_list)
                modelObject.numChapters = numFromStringFunc( extractKeyFunc(index2_list[4]) )
                modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[5]) )

            modelObject.language = index2_list[1]

            modelObject.numFavs = numFromStringFunc( extractKeyFunc(index4_list[1]) )
            modelObject.numFollows = numFromStringFunc( extractKeyFunc(index4_list[2]) )
            modelObject.numReviews = numFromStringFunc( payload_children[3].text )
        else:
            modelObject.numChapters = 1
            # No character list
            if "Words:" in index2_list[3]:
                modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[3]) )
            else:
                # single character listed
                if ',' not in index2_list[3]:
                    modelObject.characterList.append( index2_list[3] )
                else:
                    modelObject.characterList.extend( index2_list[3].split(",") )

                modelObject.numWords = numFromStringFunc( extractKeyFunc(index2_list[4]) )

            modelObject.language = index2_list[1]
            #print("extractKeyFunc with index4_list", index4_list)
            modelObject.numFavs = numFromStringFunc( extractKeyFunc(index4_list[1]) )
            modelObject.numFollows = numFromStringFunc( extractKeyFunc(index4_list[2]) )
            modelObject.numReviews = numFromStringFunc( payload_children[3].text )


        
        if missingUpdatedField:
            modelObject.publishedTimestamp = payload_children[5]["data-xutime"]
            modelObject.publishedDateString = str(payload_children[5].text)
        else:
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

