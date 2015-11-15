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
        data = open(filename).read().replace('\n', '').decode(self.encoding)
        soup = bs(data, self.bs_config)
        products_found = soup.find_all('div', {'class': 'bloc-produit-content'})
        products = list()
        for product in products_found:
            info1 = product.find('div', {'class': 'infos-produit-1'})
            if info1.span:
                price = info1.span.text
            else:
                price = info1.find('div', {'class': 'prix-promo'}).text
            p = price.strip().encode(self.encoding).replace('€', '')

            info2 = product.find('div', {'class': 'infos-produit-2'})
            brand = info2.find('h2').text
            names = info2.find_all('h4')
            name = brand
            for nn in names:
                name += ' ' + nn.text
            n = name.lower()

            unit = ''
            for i in filter(None, info2.p.text.replace('\t', ' ').strip().split(' '))[:-1]:
                unit += ' ' + i
            u = self.unit_maker(name=n, unit=unit.lower().replace(',', '.'))

            products.append({'name': n, 'unit': u, 'price': p})
        return products

    def unit_maker(self, name, unit):
        if '€' in unit.encode(self.encoding):
            uu = ''
            for j in unit.strip().split(' ')[:-5]:
                uu += ' ' + j
                unit = uu
        if 'x' not in unit:
            n_test = re.findall(r'\d+ x \d+.\d+?\D+', name)
            n_test2 = re.findall(r'\d+,\d+?\D+', name)
            if n_test:
                nb = n_test[0].replace(' ', '')
                return nb
            elif n_test2:
                nb2 = n_test2[0].replace(' ', '').replace(',', '.')
                return '1x' + nb2
            else:
                return '1x' + unit.replace(' ', '')
        else:
            return unit.replace(' ', '')
