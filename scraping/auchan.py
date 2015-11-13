# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time

class Auchan(Scraper):

    def __init__(self):
        super(Auchan, self).__init__()
        self.welcome_url = 'http://www.auchandirect.fr/'
        self.shop = 'auchan'

    def scraping(self):
        self.create_directory(self.shop)
        sections = self.get_all_sections()
        for section in sections:
            subsections = self.get_subsections(url=section)
            for subsection in subsections:
                data = self.get_data_from_url(url=subsection)
                filename = self.filename_maker(url_catego=section, url_subcatego=subsection)
                with open(self.shop + '/' + filename, 'w') as out:
                    out.write(data)
                time.sleep(2)

    def get_data_from_url(self, url):
        response = rq.get(url)
        self.log('Get data from ' + url)
        return response.text.encode(self.encoding)

    def get_all_sections(self):
        sections = list()
        data = self.get_data_from_url(url=self.welcome_url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('a', {'class': 'firsta'})
        for ref in refs:
            sections.append(self.welcome_url[:-1] + ref['href'])
        self.log('All sections scraped')
        return sections

    def get_subsections(self, url):
        subsections = list()
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('a', {'shape': 'rect'})
        for ref in refs:
            ref_split = ref['href'].split(';')[0].split('/')
            if len(ref_split) > 2:
                if 'id' in ref_split[3]:
                    pass
                else:
                    r = self.welcome_url[:-1] + ref['href'].split(';')[0]
                    subsections.append(r)
        self.log('All subsections scraped for ' + url)
        return subsections

    def filename_maker(self, url_catego, url_subcatego):
        split_url_catego = url_catego.split('/')
        split_url_subcatego = url_subcatego.split('/')
        category = split_url_catego[3]
        under_category = split_url_subcatego[5].replace(',', '').replace('-', '_')
        filename = self.shop + '_' + category + '_' + under_category
        return filename

    def parse_page_product(self, filename):
        pass

    def unit_maker(self):
        pass
