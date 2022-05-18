# -*- coding: utf-8 -*-
"""
Created on Tue May 17 2022

@author: Michael Lin
"""
import logging
import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url):
        self._url = url
        self._logger = logging.Logger

    @property
    def raw_html(self):
        return requests.get(self._url).text

    @property
    def soup(self):
        return BeautifulSoup(self.raw_html, features='html.parser')

    def get_raw_html(self):
        return self.raw_html

    def get_text(self):
        return list(self.soup.stripped_strings)

    def get_title(self):
        return self.soup.title.text

    def get_specific_tag(self, tag, class_):
        try:
            return self.soup.find(tag, class_=class_).text.strip()
        except Exception as e:
            self._logger.error(f'Tag {tag} does not exist in class {class_}')
            raise e

    def get_section_by_id(self, id_):
        try:
            return self.soup.find(id=id_)
        except Exception as e:
            self._logger.error(f'Id {id_} does not exist in url {self._url}')
            raise e

    def extract_matching_string(self, id_, tag, pattern, case_sensitive=False):
        """
        Extract any matching string using id, tag and pattern
        :param id_: id in body
        :param tag: html tag underneath id section
        :param pattern: string pattern
        :param case_sensitive: whether we want to do case sensitivity check, default to False
        :return: matching strings in list
        """
        try:
            section = self.get_section_by_id(id_=id_)
        except Exception as e:
            self._logger.error(f'Id {id_} does not exist in url {self._url}')
            raise e

        if case_sensitive:
            return [x.text.strip() for x in list(section.find_all(tag, string=pattern))]
        else:
            return [x.text.strip() for x in list(section.find_all(tag, string=lambda text: pattern in text.casefold()))]
