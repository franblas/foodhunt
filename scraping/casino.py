# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time, spynner

class Casino(Scraper):

    def __init__(self):
        super(Casino, self).__init__()
        self.endpoint = 'http://www.casinodrive.fr'
        self.welcome_url = 'http://www.casinodrive.fr/ecommerce/GC-catalog/fr/WE35303/'
        self.shop = 'casino'
        self.browser = spynner.Browser(debug_level=spynner.ERROR)

    def get_data_from_url(self, url):
        response = rq.get(url)
        self.log('Get data from ' + url)
        return response.text.encode(self.encoding)


    def get_all_sections(self):
        sections = list()
        data = self.get_data_from_url(url=self.welcome_url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('a', {'class': 'color2'})
        for ref in refs:
            if 'menu' in ref['onclick']:
                sections.append(self.endpoint + ref['href'])
        self.log('All sections scraped')
        return sections

    def get_subsections(self, url):
        subsections = list()
        toremove = list()
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        rayon = soup.find('div', {'class': 'rayon'})
        refs = rayon.find_all('a', {'class': 'color2'})
        for ref in refs:
            for c in ref.children:
                if c.find('figure') == None:
                    toremove.append(self.endpoint + ref['href'])
            if 'sousMenu' in ref['onclick']:
                subsections.append(self.endpoint + ref['href'])
        self.log('All subsections scraped for url ' + url)
        for tr in toremove:
            subsections.remove(tr)
        return subsections

    def get_all_products_page(self, url, timeout=120):
        self.create_directory(self.shop)
        self.browser.load(url=url, load_timeout=timeout)
        self.browser.load_jquery(True)
        js_command = "window.scrollTo(0,document.body.scrollHeight);"
        self.browser.runjs(js_command)
        self.browser.wait(5)
        html_content = self.browser.html.encode(self.encoding)
        self.log('Get all products for ' + url)
        self.browser.close()
        return html_content

    def filename_maker(self, url_catego, url_subcatego):
        split_url_catego = url_catego.split('/')
        split_url_subcatego = url_subcatego.split('/')

        tmp_catego = split_url_catego[6][2:].split('-')
        tmp_catego.pop(0)
        category = '-'.join(tmp_catego)

        tmp_subcatego = split_url_subcatego[6][2:].split('-')
        tmp_subcatego.pop(0)
        under_category = '-'.join(tmp_subcatego)

        filename = self.shop + '_' + category + '_' + under_category
        return filename

    def parse_page_product(self, filename):
        data = open(filename).read().replace('\n', '').decode(self.encoding)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('div', {'class': 'inner'})
        products = list()
        for ref in refs:
            description = filter(None, ref.find('div', {'class': 'description'}).text.strip().lower().split('\t'))
            n = description[0]
            p = ref.find('div', {'class': 'prix'}).text.strip().replace(',', '.')[:-1]
            if len(description) > 1:
                unit = description[1].replace(',', '.').replace(' ','')
            else:
                unit = '1x1'
            u = self.unit_maker(name=n, unit=unit)
            products.append({'name': n, 'unit': u, 'price': p})
        return products

    def unit_maker(self, name, unit):
        first_test = re.findall(r'x \d+\D+|x\d+\D+', unit)
        if first_test:
            test_1 = re.findall(r'\d+ ?\D+', unit)
            tt = re.findall(r'\d+', test_1[0])
            if len(test_1) > 1:
                return tt[0] + 'x' + ''.join(test_1[1:])
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
