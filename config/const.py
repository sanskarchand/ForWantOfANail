from enum import Enum
import os

MIN_WIN_DIMENSIONS = (800, 600)

# relative to main folder
DEFAULT_PATH = "fics"
DEFAULT_META_PATH = os.path.join(DEFAULT_PATH, "metadata")
DEFAULT_FILE_PATH = os.path.join(DEFAULT_PATH, "files")

SPECIAL_CHARS =" ',?:"

COLOR_DL_QUEUE = "#B1B1B1"
COLOR_FIC_CARD = "#4B5E6B"
COL_TUPLE_FIC_CARD = (177, 174, 176)
COL_TUPLE_FIC_CARD_PRESSED = (120, 118, 126)

class FicNetStatus(Enum):
    INITIATED = 0
    DOWNLOADING = 0
    COMPLETED = 0
