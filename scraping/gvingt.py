# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time

class GVingt(Scraper):

    def __init__(self):
        super(GVingt, self).__init__()
        self.endpoint = 'http://www.g20-minute.com/'
        self.welcome_url = 'http://www.g20-minute.com/fr/rayons/32945/'
        self.shop = 'g20'

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
        refs = soup.find_all('a', {'class': 'itemlink'})
        for ref in refs:
            if 'favoris' not in ref['href'] and 'promo' not in ref['href']:
                sections.append(self.endpoint[:-1] + ref['href'])
        self.log('All sections scraped')
        return sections

    def get_subsections(self, url):
        subsections = list()
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('ul', {'class': 'verticalnav'})
        items = refs[0].find_all('li', {'class': 'item'})
        for i in items:
            for c in i.children:
                if i.find('ul'):
                    r = self.endpoint[:-1] + c.parent.find('a')['href']
                    subsections.append(r)
        self.log('All subsections scraped for ' + url)
        return list(set(subsections))

    def filename_maker(self, url_catego, url_subcatego):
        split_url_catego = url_catego.split('/')
        split_url_subcatego = url_subcatego.split('/')
        category = split_url_catego[6]
        under_category = split_url_subcatego[7].replace(',', '').replace('-', '_')
        filename = self.shop + '_' + category + '_' + under_category
        return filename

    def parse_page_product(self, filename):
        data = open(filename).read().replace('\n', '').decode(self.encoding)
        soup = bs(data, self.bs_config)
        categos_found = soup.find('ul', {'class': 'breadcrumb'})
        categos_spl = categos_found.find_all('span')
        category = categos_spl[1].text.lower()
        subcategory = categos_spl[3].text.lower()
        products_found = soup.find_all('div', {'class': 'item'})
        products = list()
        for product in products_found:
            name = product.find('span', {'class': 'pbrand'}).text  + ' ' + product.find('span', {'class': 'pname'}).text
            n = name.lower()
            p = product.find('div', {'class': 'price'}).text.replace('\t', '').strip().encode(self.encoding).replace('€', '.')
            unit = product.find('span', {'class': 'package'}).text.lower().replace(',', '.')
            u = self.unit_maker(name=n, unit=unit)
            products.append({'name': n, 'unit': u, 'price': p})
        return category, subcategory, products


    def unit_maker(self, name, unit):
        first_test = re.findall(r'x \d+\D+|x\d+\D+', unit)
        if first_test:
            test_1 = re.findall(r'\d+ ?\D+', unit)
            tt = re.findall(r'\d+', test_1[0])
            if len(test_1) > 1:
                return tt[0] + 'x' + test_1[1]
            else:
                return '1x' + test_1[0]
        else:
            n_test = re.findall(r'\d+.?\d+?\D+|\d+ \D+', unit)
            if n_test:
                if 'la' in unit or 'le' in unit or 'l' in unit:
                    return '1x' + n_test[0].replace(' ', '')
                else:
                    return '1x' + unit
            else:
                return '1x' + unit
