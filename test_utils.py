# -*- coding: utf-8 -*-
"""
Created on Tue May 17 2022

@author: Michael Lin
Test example comes from https://realpython.com/beautiful-soup-web-scraper-python/
"""
from utils import WebScrapper
from unittest import TestCase
from bs4 import BeautifulSoup


class TestWebScrapper(TestCase):
    def setUp(self) -> None:
        self.url = 'https://realpython.github.io/fake-jobs/'
        self.test_web_scrapper = WebScrapper(url=self.url)

    def test_get_raw_html(self):
        test_html = self.test_web_scrapper.get_raw_html()
        self.assertIsNotNone(test_html)
        self.assertTrue(bool(BeautifulSoup(test_html, 'html.parser').find()))  # Assert it is html

    def test_get_title(self):
        test_title = self.test_web_scrapper.get_title()
        self.assertEqual(test_title, 'Fake Python')

    def test_get_text(self):
        test_text = self.test_web_scrapper.get_text()
        self.assertIsNotNone(test_text)
        self.assertIsInstance(test_text, list)

    def test_get_specific_tag(self):
        test_data = self.test_web_scrapper.get_specific_tag(tag='p', class_='subtitle is-3')
        self.assertEqual(test_data, 'Fake Jobs for Your Web Scraping Journey')

    def test_get_section_by_id(self):
        test_section = self.test_web_scrapper.get_section_by_id(id_='ResultsContainer')
        self.assertIsNotNone(test_section)

    def extract_matching_string(self):
        test_string_sensitive = self.test_web_scrapper.filter_text(id_='ResultsContainer', tag='h2', pattern='Python',
                                                                   case_sensitive=True)
        self.assertEqual(test_string_sensitive, [])

        test_string_insensitive = self.test_web_scrapper.filter_text(id_='ResultsContainer', tag='h2', pattern='python')
        self.assertIsNotNone(test_string_insensitive)
        self.assertEqual(len(test_string_insensitive), 10)
