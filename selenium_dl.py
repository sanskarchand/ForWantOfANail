#!/usr/bin/env python
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from ficparser import FicParser, BetterFicParser
import model.StoryModel as StoryModel
from config import const
import time
import os
from pathlib import Path
import platform


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
WAITING_TIME = 7  # time to wait between downloads, in seconds

if platform.system() == "Linux":
    DATA_DIR =  Path(os.getenv("HOME")) / '.config/google-chrome/Profile 1/'
elif platform.system() == "Windows":
    DATA_DIR = Path(os.environ("USERPROFILE")) /'AppData'/'Local'/'Google'/'Google Chrome'/'User Data'


#profile = webdriver.FirefoxProfile()
#profile.set_preference("general.useragent.override", USER_AGENT)
#options = webdriver.ChromeOptions() 
#options.add_argument("--disable-blink-features=AutomationControlled")
options = uc.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome-stable'
options.add_argument(f"--user-data-dir={DATA_DIR}")
#options.add_argument(f"--user-agent={USER_AGENT}")

def downloadThing(chap_num, driver, ficModel, url, isImage=False):

    print("Downloading ", url)
    driver.get(url)
    #content = driver.page_source

    myPrefix = ficModel.getCleanPrefix()
    myFolder = ficModel.realDirectory
    myPath = os.path.join(const.DEFAULT_FILE_PATH, myFolder)
    
    fullPath = None

    if not isImage:
        myFilename =  myPrefix + "__Ch-" + str(chap_num) + ".html"
        fullPath = os.path.join(myPath, myFilename)

        ficModel.addFilePath(fullPath)
    else:
        # .webp file; doesn't matter
        myFilename = ficModel.realDirectory + "__image.jpeg"
        fullPath = os.path.join(myPath, myFilename)

        ficModel.imageFilePath = fullPath
    
    print(fullPath)
    with open(fullPath, "w") as f:
        if not isImage:
            content = driver.page_source
            f.write(content)
        else:
            imgElem = driver.find_element(By.TAG_NAME, 'img')
            if imgElem:
                imgElem.screenshot(fullPath)




def main():
    if len(sys.argv) < 2:
        print("Supply a url.")
        print("Usage: python selenium_dl.py <url>")

    skip_image = len(sys.argv) >= 3 and sys.argv[2] == "--skip-image"
    
    url = sys.argv[1]
    #driver = webdriver.Firefox(profile)
    #driver = webdriver.Chrome(options=options)
    driver = uc.Chrome(options=options)
    print("URL", url)
    driver.get(url)
    while "/cdn-cgi/styles/challenges.css" in driver.page_source:
        print("Still cloudflare, waiting for 5 secs")
        time.sleep(5)

    src = driver.page_source

    #parsed = FicParser.FicParser(src)
    parsed = BetterFicParser.FicParser(src)

    init_metadata = parsed.constructMetadata()
    ficModel = StoryModel.FanficModel()
    ficModel.metadata = init_metadata
    ficModel.setRealDirectory()


    # make the necessary directory
    path = os.path.join(const.DEFAULT_FILE_PATH, ficModel.realDirectory)
    if not os.path.exists(path):
        os.makedirs(path)
    
    
    time.sleep(WAITING_TIME)

    for chap_num in range(1, ficModel.metadata.numChapters + 1):
        url = "https://www.fanfiction.net/s/{}/{}".format(ficModel.metadata.storyID, chap_num)
        downloadThing(chap_num, driver, ficModel, url)
        time.sleep(WAITING_TIME)

    if ficModel.metadata.hasImage:
        if skip_image:
            print("Skipping image download. You can add it manually later.")
            ficModel.metadata.hasImage = False
        else:
            downloadThing(None, driver, ficModel, ficModel.metadata.imgUrlPath, True)

    
    ficModel.dumpToDisk()




    driver.close()


if __name__ == '__main__':
    main()
