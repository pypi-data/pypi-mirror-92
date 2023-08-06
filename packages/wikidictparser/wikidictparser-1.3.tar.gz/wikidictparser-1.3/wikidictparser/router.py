# -*- coding: utf-8 -*-
import logging

from .english import EnWiktionaryParser
from .polish import PlWiktionaryParser

parser_routing_dict = {
    # english
    'wiktionary': EnWiktionaryParser,
    'en': EnWiktionaryParser,
    'english': EnWiktionaryParser,
    'enwiki': EnWiktionaryParser,
    'enwiktionary': EnWiktionaryParser,
    # polish
    'wikislownik': PlWiktionaryParser,
    'wikisłownik': PlWiktionaryParser,
    'pl': PlWiktionaryParser,
    'polish': PlWiktionaryParser,
    'plwiki': PlWiktionaryParser,
    'plwiktionary': PlWiktionaryParser,
}


def get_parser(language):
    """get parser function

    This function routes the user to appriopriate parser.

    Inputs:

        - language (str) - string specyfying which wikitionary to use

    Possible language values:

        - wiktionary | en | english | enwiki | enwiktionary
            - english wiktionary parser

        - wikisłownik | wikislownik | pl | polish | plwiki | plwiktionary
            - polish wiktionary parser
    """

    if language not in parser_routing_dict.keys():
        raise KeyError(
            f'"{language}" is not a valid option for parser language.')

    return parser_routing_dict[language]()


def set_logging_level(level):
    temp_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
    }
    logging.basicConfig(level=temp_dict[level])
