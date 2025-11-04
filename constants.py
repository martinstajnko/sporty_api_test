""" Project Constants """

from enums import ContentFlags

JOKE_API_URL = "https://v2.jokeapi.dev/"
LANGUAGES_ENDPOINT = "languages"
DEFAULT_LANGUAGE = "en"
LANGUAGE_CODE = "langcode"
FLAGS_ENDPOINT = "flags"

TIMESTAMP_LENGTH = 13

# Language Codes for langcode endpoint
LANGUAGE_MAPPINGS = {
    "English": "en",
    "German": "de", 
    "Spanish": "es",
    "French": "fr",
    "Portuguese": "pt",
    "Czech": "cs"
}

EXPECTED_CONTENT_FLAGS = [
    ContentFlags.NSFW.value,
    ContentFlags.RELIGIOUS.value, 
    ContentFlags.POLITICAL.value,
    ContentFlags.RACIST.value,
    ContentFlags.SEXIST.value,
    ContentFlags.EXPLICIT.value
]

CLEAN_FLAGS = {
    ContentFlags.NSFW.value: False,
    ContentFlags.RELIGIOUS.value: False,
    ContentFlags.POLITICAL.value: False,
    ContentFlags.RACIST.value: False,
    ContentFlags.SEXIST.value: False,
    ContentFlags.EXPLICIT.value: False
}