""" Project Enums """

from enum import Enum


class HttpStatusCodes(Enum):
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_CREATED = 201


class JokeCategories(Enum):
    PROGRAMMING = "Programming"
    DARK = "Dark"
    MISC = "Misc"
    ANY = "Any"
    NONEXISTING = "NonExisting"


class JokeTypes(Enum):
    SINGLE = "single"
    TWOPART = "twopart"


class JokeLanguages(Enum):
    CZECH = "cs"
    GERMAN = "de" 
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    PORTUGUESE = "pt"


class SystemLanguages(Enum):
    CZECH = "cs"
    GERMAN = "de"
    ENGLISH = "en" 
    ITALIAN = "it"
    RUSSIAN = "ru"


class ContentFlags(Enum):
    NSFW = "nsfw"
    RELIGIOUS = "religious" 
    POLITICAL = "political"
    RACIST = "racist"
    SEXIST = "sexist"
    EXPLICIT = "explicit"