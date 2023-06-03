**Current usage**: python selenium\_dl.py <fanfic url> --skip-image
If Cloudflare keeps asking you to prove you're a human (and this tends to
happen in a loop recently), simply copy and paste the URL
into a new tab manually, exit the browser, and restart the program again.

**Note**: Please provide the path to your chrome executable in selenium\_dl.py.
This program is untested on windows, so in case you get an error, please try to
manually override the DATA\_DIR variable.

**Note2**: Requires python 3.10 (for match-case syntax)

**Note3**: Please use the --skip-image option with selenium\_dl.py

**Disclaimer**: The file res/ffnet\_icon.png belongs to FictionPress and not
 to me. It is provided here as a sample. This program is not affiliated with FictionPress or fanfiction.ne in any way.

Dependencies:
* Qt5
* html5lib 
* undetected\_chromedriver
* cloudscraper (unused for now)
* Selenium (with chromedriver) [optional]

### Current Capabilites:
* Downloading stories
* Basic Library
* Rudimentary Reading

## To add:
* Custom tagging and filtering [in-progress/half-done]
* Bulk downloads


### Screenshot(s)
Downloads tab:
![](https://github.com/sanskarchand/for_want_of_a_nail/blob/master/screenshots/Screenshot_2020-06-24_03-24-33.png)
Reader tab:
![](https://github.com/sanskarchand/for_want_of_a_nail/blob/master/screenshots/Screenshot_2020-07-13_00-43-53.png)
Details tab:
![](https://github.com/sanskarchand/for_want_of_a_nail/blob/master/screenshots/Screenshot_2020-07-13_22-46-14.png)
Library tab:
![](https://github.com/sanskarchand/for_want_of_a_nail/blob/master/screenshots/Screenshot_2021-01-17_17-46-50.png)
Sample metadata:
![](https://github.com/sanskarchand/for_want_of_a_nail/blob/master/screenshots/Screenshot_2021-01-18_08-23-38.png)
