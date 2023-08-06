import unittest
import requests
from anfrss.parser import anffeed


class TestLinkIsActive(unittest.TestCase):

    def test_english_connection(self):
        self.assertTrue(requests.get(anffeed.ENGLISH))

    def test_german_connection(self):
        self.assertTrue(requests.get(anffeed.GERMAN))

    def test_kurmanji_connection(self):
        self.assertTrue(requests.get(anffeed.KURMANJI))

    def test_spanish_connection(self):
        self.assertTrue(requests.get(anffeed.SPANISH))

    def test_arab_connection(self):
        self.assertTrue(requests.get(anffeed.ARAB))


class TestSetLanguage(unittest.TestCase):

    feed = anffeed.ANFFeed()

    def test_english(self):
        self.feed.set_language('english')
        self.assertEqual(
            self.feed.source,
            'https://anfenglishmobile.com/feed.rss'
        )

    def test_german(self):
        # Set Language
        self.feed.set_language('german')
        self.assertEqual(self.feed.source, 'https://anfdeutsch.com/feed.rss')

    def test_krumanji(self):
        self.feed.set_language('kurmanjî')
        self.assertEqual(self.feed.source, 'https://anfkurdi.com/feed.rss')

    def test_spanish(self):
        self.feed.set_language('spanish')
        self.assertEqual(self.feed.source, 'https://anfespanol.com/feed.rss')

    def test_arab(self):
        self.feed.set_language('arab')
        self.assertEqual(self.feed.source, 'https://anfarabic.com/feed.rss')


class TestHtmlRegex(unittest.TestCase):
    def test(self):
        template = '<a href="test.link">Link</a>'
        self.assertEqual(anffeed.HTML_TAG.sub('', template), 'Link')
