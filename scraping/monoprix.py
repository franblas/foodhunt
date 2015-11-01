# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time

class Monoprix(Scraper):

    def __init__(self):
        super(Monoprix, self).__init__()
        self.endpoint = 'http://courses.monoprix.fr'
        self.welcome_url = 'http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html'
        self.shop = 'monoprix'
        self.nextpageid = ''

    def get_data_from_url(self, url):
        response = rq.get(url)
        self.log('Get data from ' + url)
        return response.text.encode(self.encoding)

    def get_all_sections(self): # without mode
        sections = list()
        data = self.get_data_from_url(url=self.welcome_url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('a', {'class': 'Color01'})
        for ref in refs:
            sections.append(self.endpoint + ref['href'])
        self.log('All sections scraped')
        return sections[:-1]

    def get_subsections(self, url):
        subsections = list()
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        sub_url = soup.find('ul', {'class', 'SideNav'}).find('ul')
        refs = sub_url.find_all('a')
        for r in refs:
            sub_ref = self.endpoint + r['href']
            data = self.get_data_from_url(url=sub_ref)
            soup = bs(data, self.bs_config)
            top_nav = soup.find('div', {'id': 'topNavigation'})
            sub_refs = top_nav.find_all('a')
            for rr in sub_refs:
                subsections.append(self.endpoint + rr['href'])
        self.log('All subsections scraped for ' + url)
        return subsections
