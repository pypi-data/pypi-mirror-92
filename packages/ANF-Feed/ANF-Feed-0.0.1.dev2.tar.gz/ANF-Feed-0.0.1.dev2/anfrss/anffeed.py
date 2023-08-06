'''
    Parsing Feeds from ANF News

Core Module of package.
Supports several languages:
- English
- German
- Kurmanji
- Spanish
( More languages available soon. )
'''

import feedparser
import re

ENGLISH = 'https://anfenglishmobile.com/feed.rss'
GERMAN = 'https://anfdeutsch.com/feed.rss'
KURMANJI = 'https://anfkurdi.com/feed.rss'
SPANISH = 'https://anfespanol.com/feed.rss'
ARAB = 'https://anfarabic.com/feed.rss'
HTML_TAG = re.compile(r'<[^>]+>')               # To remove HTML tags later


class ANFFeed:

    source = ENGLISH

    def __init__(self):
        try:
            self.feed = feedparser.parse(self.source)
        except NameError as e:
            raise e

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
        titles = []
        for i in self.entries:
            titles.append(i.title)
        return titles

    @property
    def summary(self):
        summary = []
        for i in self.entries:
            summary.append(i.summary)
        return summary

    @property
    def detailed(self):
        detailed = []
        for i in self.entries:
            text = i.content[0]['value']
            text = HTML_TAG.sub('', text)       # Remove Html Tags
            detailed.append(text)
        return detailed

    @property
    def link(self):
        links = []
        for i in self.entries:
            links.append(i.link)
        return links

    @property
    def all_feeds(self):
        return list(zip(self.title, self.summary, self.link, self.detailed))

    def download_article(self, article, dir, file='html'):
        '''
            Download Article

        Requests a chosen article
        and writes it to a file
        (default: HTML).

        :param article: The
            article to write
        :param dir: Directory
            to write to
        :type dir: str
        :param file: The desired
            file type to write
        :type file: str, default
        '''
        if file != 'html':
            raise NotImplementedError()

        raise NotImplementedError()


if __name__ == '__main__':
    pass
