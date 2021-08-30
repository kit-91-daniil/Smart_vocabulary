from collections import namedtuple
from enum import Enum, auto
import re
import requests
from translate import Translator

from_lang = "en"
to_lang = "ru"
translator = Translator(from_lang=from_lang, to_lang=to_lang)
translation_result = namedtuple("translation_result", "translation message")


class TranslatorMessages(Enum):
    can_not_been_translated = auto()
    internet_disconnected = auto()
    success = auto()


def translate_word(word: str) -> translation_result:
    """Trying to translate word. Returns instance of translation_result - namedtuple
    - In case of success returns translation and 'success' flag
    - In case of connection to internet error returns None and
    'internet disconnected' flag
    -In case of incorrect symbols or too long string returns None and
    'can_not_been_translated flag'
    """
    try:
        translation = translator.translate(word)
        pattern = "[(а-я)(А-Я)(-:)\s]+$"
        regex = re.compile(pattern)
        is_translation_match = regex.match(translation)
        if len(translation) > 40 or not is_translation_match:
            return translation_result(None, TranslatorMessages.can_not_been_translated)
        return translation_result(translation, TranslatorMessages.success)
    except requests.exceptions.ConnectionError:
        return translation_result(None, TranslatorMessages.internet_disconnected)


if __name__ == "__main__":
    print(type(translate_word("Hello")))
