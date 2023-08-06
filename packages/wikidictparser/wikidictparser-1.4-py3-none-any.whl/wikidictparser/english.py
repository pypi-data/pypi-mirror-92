from .base import WiktionaryParserBase


class EnWiktionaryParser(WiktionaryParserBase):
    """English Wiktionary Parser class

    This class is used to parse english wiktionary.

    """

    def __init__(self):
        url = "https://en.wiktionary.org/wiki/{}?printable=yes"
        super().__init__(url)
