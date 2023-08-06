'''
    Parsing Feeds from ANF News
    ===========================

Core Module of package.
Supports several languages:
    - English
    - German
    - Kurmanji
    - Spanish
( More languages available soon. )

:class: ANFFeed

See docs of containing class/es
to learn more about.
'''

import re
import feedparser


ENGLISH = 'https://anfenglishmobile.com/feed.rss'
GERMAN = 'https://anfdeutsch.com/feed.rss'
KURMANJI = 'https://anfkurdi.com/feed.rss'
SPANISH = 'https://anfespanol.com/feed.rss'
ARAB = 'https://anfarabic.com/feed.rss'
HTML_TAG = re.compile(r'<[^>]+>')               # To remove HTML tags later


class ANFFeed:
    '''
        ANF Feed Parser

    :param source:
        Link to set;
        Depending on chosen
        Language;
    :type source: str
    '''

    source = ENGLISH

    def __init__(self):
        try:
            self.feed = feedparser.parse(self.source)
        except NameError:
            raise NameError

        self.entries = self.feed.entries

    @classmethod
    def set_language(cls, language):
        '''
            Set language of link

        :param language: Language to set
        :type language: str
        '''
        if language == 'english':
            cls.source = ENGLISH
        elif language == 'german':
            cls.source = GERMAN
        elif language == 'kurmanjî':
            cls.source = KURMANJI
        elif language == 'spanish':
            cls.source = SPANISH
        elif language == 'arab':
            cls.source = ARAB
        else:
            # We should not reach this
            # as the GUI just shows
            # available options
            raise NotImplementedError()

    @property
    def title(self):
        ''' Titles Attribute
        '''
        titles = []
        for i in self.entries:
            titles.append(i.title)
        return titles

    @property
    def summary(self):
        ''' Summary Attribute
        '''
        summary = []
        for i in self.entries:
            summary.append(i.summary)
        return summary

    @property
    def detailed(self):
        ''' Detailed Attribute
        '''
        detailed = []
        for i in self.entries:
            text = i.content[0]['value']
            text = HTML_TAG.sub('', text)       # Remove Html Tags
            detailed.append(text)
        return detailed

    @property
    def link(self):
        ''' Links Attribute
        '''
        links = []
        for i in self.entries:
            links.append(i.link)
        return links

    @property
    def all_feeds(self):
        ''' All Feeds Attribute
        '''
        return list(zip(self.title, self.summary, self.link, self.detailed))

    def download_article(self, ident, target, file='html'):
        '''
            Download Article

        Requests a chosen article
        and writes it to a file
        (default: HTML).

        :param ident: Identifier;
            Can be link or title
            which will identify
            the article to down-
            load
        :type ident: str
        :param target: Directory
            to write to
        :type target: str
        :param file: The desired
            file type to write
        :type file: str, default
        '''

        import requests

        # Try first if ident is a link
        # If not it's the title
        try:
            content = requests.get(ident)
            print(content)
        except Exception as missing_schema:
            print(missing_schema)
        finally:
            pass

        raise NotImplementedError()


if __name__ == '__main__':
    pass
