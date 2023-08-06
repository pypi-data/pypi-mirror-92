from dotenv import load_dotenv

load_dotenv()

NAME = "settings-master"
VERSION = "0.1.0"

_path_to_readme = "README.md"

with open(_path_to_readme) as f:
    LONG_DESCRIPTION = f.read()

AUTHOR = "semenInRussia"
AUTHOR_EMAIL = "hrams205@gmail.com"

URL = "https://github.com/semenInRussia/FreeSpotify_back"

LICENSE = "MIT"
