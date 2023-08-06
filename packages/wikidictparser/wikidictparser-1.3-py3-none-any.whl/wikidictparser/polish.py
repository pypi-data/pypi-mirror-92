import logging
import bs4
import re

import pandas as pd

from .base import WiktionaryParserBase


class PlWiktionaryParser(WiktionaryParserBase):
    """Polish Wiktionary Parser class

    This class is used to parse polish wiktionary.

    """

    def __init__(self):
        url = "https://pl.wiktionary.org/wiki/{}?printable=yes"
        self.language_of_interest = 'pl'
        super().__init__(url)

    def fetch_by_meaning(self, word):
        """Get data for word and return result sorted by meaning"""
        result = self.fetch(word)
        out_dict = {}
        if result==None:
            return None
        for major in result['znaczenia'].keys():
            for minor in result['znaczenia'][major]:
                local_id = str(major)+'.'+str(minor)
                out_dict[local_id] = {}
                temp = result['znaczenia'][major][minor]
                out_dict[local_id]['global_id'] = "%s_%s"%(word, local_id)
                for key in temp.keys():
                    out_dict[local_id][key] = temp[key]
                try:
                    out_dict[local_id]['odmiana'] = result['odmiana'][major][minor]
                except KeyError:
                    out_dict[local_id]['odmiana'] = 'nieodmienny'
        return out_dict


    def get_word_data(self):
        """Get word data function

        This function gets the data about the word and outputs a json file.
        """
        # get a list of tags inside main content of the page
        self.content_tag_list = self.soup.find(
            'div', {'class': 'mw-parser-output'})
        # return None if the word could not be found
        if not self.content_tag_list:
            logging.info(f'The data about the word "{ self.current_word }"' +
                         ' could not be found.')
            return None
        # get dictionary with language sections
        self.language_section_dict = self.get_language_section_dict()
        # divide the language section into dictionary
        # with subsection names as keys
        self.divide_subsections()
        # parse meanings for each language
        self.parse_meanings()
        # parse declination for each meaning if exists
        self.parse_declination()
        # parse conjugation for each meaning if exists
        

        try:
            return {k:v for k, v in self.language_section_dict['pl'].items() if k in ('znaczenia', 'odmiana')}
        except:
            return None

    def get_language_section_dict(self):
        """Get language section function

        This function divides the main contents of the page
        into dictionary where the keys are language codes
        (e.g. 'pl', 'en') and the values are the list of tags
        corresonding to that language.

        Returns:

            - language_section_dict (dict) - dictionary with language sections

        """
        contents = self.content_tag_list.contents
        # create the dict and set initial key for first sections to be omitted
        language_section_dict = {'_': []}
        last_lang = '_'
        # iterate through tags
        for tag in contents:
            tag_name = tag.name
            # if the tag is language tag then set default dict key
            # to language code
            if tag_name == 'h2':
                last_lang = tag.select(
                    'span.lang-code.primary-lang-code')[0].attrs['id']
                # logging.debug(f'Found language "{last_lang}".')
                language_section_dict[last_lang] = []
            # append the tag to list for the given language if element is a Tag
            if isinstance(tag, bs4.element.Tag):
                language_section_dict[last_lang].append(tag)
        # delete the initial tags
        del language_section_dict['_']
        return language_section_dict

    def divide_subsections(self):
        """ Divide subsections function

        This function divides the languages sections
        into subsections depending on the heading.
        """
        # for every language section
        for lang in self.language_section_dict.keys():
            # create a dict for subsection name and corresponding tag list
            subsection_dict = {}
            subsections = self.language_section_dict[lang]
            # starts with heading subsection
            subsection_name = 'heading'
            subsection_dict[subsection_name] = []
            for tag in subsections:
                # span.field-title elements contain subsection names
                if tag.select('span.field-title'):
                    # text content is <subsection_name>: last char is skipped
                    subsection_name = \
                        tag.select('span.field-title')[0].text[:-1]
                    # logging.debug(f'Found subsection "{subsection_name}".')
                    # list for new subsection is created
                    subsection_dict[subsection_name] = []
                # tag is being appended to last subsection
                subsection_dict[subsection_name].append(tag)
            # language sections dict will contan subsection dicts
            self.language_section_dict[lang] = subsection_dict

    def parse_meanings(self):
        """ Parse meanings function.

        This function parsers the meanings subsection
        (marked with key "znaczenia").
        """
        # For every language section:
        for lang in self.language_section_dict.keys():
            meaning_tags = self.language_section_dict[lang]['znaczenia']
            major = 0
            minor = 0
            part_of_speech = None
            meanings = {}
            logging.debug(f'Language {lang}.')
            # for every tag in meaning subsection
            for tag in meaning_tags:
                logging.debug(f'Tag {tag}')
                # if part of speech tag then parse
                if tag.select('p > i'):
                    major = major + 1
                    meanings[major] = {}
                    minor = 0
                    part_of_speech = tag.select('p > i')[0].text
                    logging.debug(f'Major {major},\
                         part of speech {part_of_speech}.')
                # If meaning exists then parse meaning.
                elif tag.select('span.field-title'):
                    logging.debug(f'Found tag {tag}')
                    pass
                elif tag.select('dl > dd'):
                    try:
                        for meaning in tag.select('dl > dd'):
                            minor = minor + 1
                            meaning_text = meaning.text
                            number = meaning_text.split(' ')[0]
                            meaning_text = meaning_text[len(number):]
                            logging.debug(f'Minor {minor}, number {number}, ' +
                                          f'tekst/text: {meaning_text}.')
                            # check if numbering is correct
                            # - if not raise Exception
                            if f'({major}.{minor})' != number:
                                raise Exception('The numbering for meaning ' +
                                                f'{meaning} is inconsistent.')
                            meanings[major][minor] = {
                                'część_mowy/part_of_speech': part_of_speech,
                                'tekst/text': meaning_text,
                            }
                    except Exception:
                        logging.debug(f'Failed to parse tag {tag}.')
            self.language_section_dict[lang]['znaczenia'] = meanings

    def parse_numbering(self, number_string, meaning_dict):
        """Parse numbering function

        This function parses numbering into
        range of applicability.

        i.e. from (2-4) into a list of numbers
        2.1, 2.2, 3.1, 4.1 where applicable
        """
        number_list = []
        number_string = number_string[1:-1]
        logging.debug(f'No brackets: {number_string}')
        # separating number expression separated by commas
        number_string_list = number_string.strip(' ').split(',')
        logging.debug(f'string list {number_string_list}')
        # for every unit number expression (like 1.1-3) - parse
        for unit_number_string in number_string_list:
            expression_majors = r'^(\d+)\-(\d+)$'  # matches 2-3
            expression_major = r'^(\d+)$'  # matches 1
            expression_minors = r'^(\d+)\.(\d+)\-(\d+)$'  # matches 1.1-3
            expression_minor = r'^(\d+)\.(\d+)$'  # matches 1.1
            # Try out every match and add appriopriate (major, minor) tuple/s
            if re.match(expression_minors, unit_number_string):
                logging.debug('Expression minors')
                match = re.match(expression_minors, unit_number_string)
                major = int(match[1])
                minor_1 = int(match[2])
                minor_2 = int(match[3])
                for minor_key in range(minor_1, minor_2+1):
                    number_list.append((major, minor_key))
            if re.match(expression_minor, unit_number_string):
                logging.debug('Expression minor')
                match = re.match(expression_minor, unit_number_string)
                logging.debug(f'Match 1 {match[1]}, match 2 {match[2]}')
                major = int(match[1])
                minor = int(match[2])
                number_list.append((major, minor))
            if re.match(expression_majors, unit_number_string):
                logging.debug('Expression majors')
                match = re.match(expression_majors, unit_number_string)
                logging.debug(f'Match 1 {match[1]}, match 2 {match[2]}')
                major_1 = int(match[1])
                major_2 = int(match[2])
                for major_key in range(major_1, major_2+1):
                    for minor_key in meaning_dict[major_key].keys():
                        number_list.append((major_key, minor_key))
            if re.match(expression_major, unit_number_string):
                logging.debug('Expression major')
                match = re.match(expression_major, unit_number_string)
                logging.debug(f'Match 1 {match[1]}')
                major = int(match[1])
                for minor_key in meaning_dict[major].keys():
                    number_list.append((major, minor_key))
        return number_list

    def clean_declination_df(self, df, part_of_speech):
        """Clean declination dataframe

        This function cleans declination dataframe.
        It is due to the fact that pandas.read_html
        doesn't work perfectly on wikitionary tables.
        """
        parts_of_speech = part_of_speech.split(' ')
        logging.debug(parts_of_speech)
        # check if a verb with normal conjugation
        if 'czasownik' in part_of_speech and\
                'nieosobowy' not in parts_of_speech and\
                'niewłaściwy' not in parts_of_speech:
            col_names = list(df.columns)
            # delete unnamed columns
            cols_to_delete =\
                [col_name for col_name in col_names
                    if col_name[:7] == 'Unnamed']
            df = df.drop(columns=cols_to_delete)
            # merge first two columns
            for i in range(df.shape[0]):
                if df['forma'].iloc[i] != df['forma.1'].iloc[i]:
                    df['forma'].iloc[i] =\
                        df['forma'].iloc[i] + ' ' + df['forma.1'].iloc[i]
            df = df.drop(columns=['forma.1'])
            # merge first two rows as a df header
            for col in df.columns:
                if df[col].iloc[0] != col:
                    df[col].iloc[0] = col.split('.')[0] + ' ' + df[col].iloc[0]
            new_header = df.iloc[0]
            df = df.iloc[1:]
            df.columns = new_header

        # if an adjective
        if 'przymiotnik' in parts_of_speech or 'zaimek' in parts_of_speech:
            # set new header
            new_header = ['przypadek', 'liczba pojedyncza mos/mzw',
                          'liczba pojedyncza mrz',
                          'liczba pojedyncza ż', 'liczba pojedyncza n',
                          'liczba mnoga mos', 'liczba mnoga nmos']
            if df.shape[0]>11:
                for i in range(13,20):
                    df.iloc[i,0] = df.iloc[i,0]+" stopień wyższy"
                for i in range(24,31):
                    df.iloc[i,0] = df.iloc[i,0]+" stopień najwyższy"
                df = df.iloc[list(range(2,9))+list(range(13,20))+list(range(24,31))]
            else:
                df = df.iloc[2:-2]
            df.columns = new_header
        # set first column as index
        index_column = list(df.columns)[0]
        df = df.set_index(index_column)
        return df

    def parse_declination(self):
        """Parse declination function

        This function parsers declination and conjugation.

        """
        # if polish definition exists
        if 'pl' not in list(self.language_section_dict.keys()):
            return

        # if declination subsection exists
        if 'odmiana' in list(self.language_section_dict['pl'].keys()):
            declination_tags = self.language_section_dict['pl']['odmiana']
        else:
            return
        declination_dict = {}
        # for every tag in declination tags
        for tag in declination_tags:
            logging.debug(f'Declination tag {tag}')
            dds = tag.select('dl > dd')
            for dd in dds:
                # check if not empty
                if not dd.text:
                    continue
                # find corresponding numbers
                logging.debug(
                    f'DD text: {dd.text}'
                )
                prog = re.compile(r'\([\d\ \.\,\-]*\)')
                corresponding_number = prog.search(dd.text)
                
                if not corresponding_number:
                    print('Bad numbering')
                    corresponding_number = '(1)'
                else:
                    logging.debug(
                        f'DD match group: {corresponding_number.group()}'
                    )
                    corresponding_number = corresponding_number.group()
                logging.debug(
                    f'Meaning numbers: {corresponding_number}.')
                logging.debug(
                    f'DD contents: {dd.contents[0]}'
                )
                number_list = self.parse_numbering(
                    corresponding_number,
                    self.language_section_dict['pl']['znaczenia'],
                )
                logging.debug(
                    f'Number list {number_list}'
                )
                # check if doesn't decline
                declination = None
                if dd.find('span', {'title': 'nieodmienny'}):
                    logging.debug('nieodmienny')
                    declination = 'nieodmienny'
                elif dd.find('span', {'title': 'zobacz'}):
                    logging.debug('odnośnik')
                    declination = 'specjalne'
                # if a table found
                elif dd.select('table'):
                    table = dd.select('table')[0]
                    if table.select('style'):
                        table.style.extract()
                    table_string = str(table)
                    table_string = table_string.replace('<br/><', '<')
                    table_string = table_string.replace('<br/>', ',')
                    # check if table inside table
                    if table.select('table'):
                        bad_tags = """<tr><td colspan="8" style="padding:0;border:none;"><table class="wikitable odmiana collapsible collapsed" style="width:100%; margin:5px 0 0 0;"><tbody>"""
                        table_string = table_string.replace(bad_tags, '')
                        bad_tags = """</tbody></table></td></tr>"""
                        table_string = table_string.replace(bad_tags, '')
                    declination_df = pd.read_html(table_string, header=0)[0]
                    part_of_speech =\
                        self.language_section_dict['pl']['znaczenia'][number_list[0][0]][1]['część_mowy/part_of_speech']
                    declination_df = self.clean_declination_df(declination_df,
                                                               part_of_speech)
                    declination = declination_df.to_dict('index')
                    for key1, value1 in declination.items():
                        for key2, value2 in value1.items():
                            value1[key2] = value2.replace(' / ',',').replace(' /',',').replace('/ ',',').replace('/',',').replace(', ',',').split(',')
                else:
                    raise Exception(
                        f"Could not parse declination for {number_list}.")
                for numbers in number_list:
                    major = numbers[0]
                    minor = numbers[1]
                    if minor == 1:
                        declination_dict[major] = {}
                    logging.debug(f'major {major}, minor {minor}')
                    declination_dict[major][minor] = declination
            self.language_section_dict['pl']['odmiana'] = declination_dict
