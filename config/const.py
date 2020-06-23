from enum import Enum
import os

MIN_WIN_DIMENSIONS = (800, 600)

# relative to main folder
DEFAULT_PATH = "fics"
DEFAULT_META_PATH = os.path.join(DEFAULT_PATH, "metadata")
DEFAULT_FILE_PATH = os.path.join(DEFAULT_PATH, "files")

COLOR_DL_QUEUE = "#B1B1B1"
class FicNetStatus(Enum):
    INITIATED = 0
    DOWNLOADING = 0
    COMPLETED = 0
