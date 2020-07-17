from enum import Enum
import os

MIN_WIN_DIMENSIONS = (800, 600)
MIN_DROP_DOWN_WIDTH = 120
# relative to main folder
DEFAULT_PATH = "fics"
RES_PATH = "res"
DEFAULT_META_PATH = os.path.join(DEFAULT_PATH, "metadata")
DEFAULT_FILE_PATH = os.path.join(DEFAULT_PATH, "files")
RES_NOIMG_PATH = os.path.join(RES_PATH, "noimg.jpg")

SPECIAL_CHARS =" ',?:"

COLOR_DL_QUEUE = "#B1B1B1"
COLOR_FIC_CARD = "#4B5E6B"
COL_TUPLE_FIC_CARD = (177, 174, 176)
COL_TUPLE_FIC_CARD_PRESSED = (120, 118, 126)


FANDOM_CROSSOVER = "[Crossover]"
FANDOM_ALL = "<ALL>"

class FicNetStatus(Enum):
    INITIATED = 0
    DOWNLOADING = 0
    COMPLETED = 0
