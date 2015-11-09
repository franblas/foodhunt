# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time

class SimplyMarket(Scraper):

    def __init__(self):
        super(SimplyMarket, self).__init__()
        self.welcome_url = 'http://www.livraison.simplymarket.fr/'
        self.shop = 'simplymarket'
        self.nextpageid = ''

    def scraping(self):
        self.create_directory(self.shop)
        sections = self.get_all_sections()[5:]
        for section in sections:
            subsections = self.get_subsections(url=section)
            for subsection in subsections:
                data = self.get_data_from_url(url=subsection)
                filename = self.filename_maker(url_catego=section, url_subcatego=subsection)
                with open(self.shop + '/' + filename, 'w') as out:
                    out.write(data)
                self.nextpageid = self.find_next_page_id(url=subsection)
                while(self.nextpageid != ''):
                    page_id = str(self.nextpageid[-1])
                    data = self.get_data_from_url(url=self.nextpageid)
                    with open(self.shop + '/' + filename + '_' + page_id, 'w') as out:
                        out.write(data)
                    self.nextpageid = self.find_next_page_id(url=self.nextpageid)
                    time.sleep(2)
                time.sleep(2)

    def get_data_from_url(self, url):
        response = rq.get(url)
        self.log('Get data from ' + url)
        return response.text.encode(self.encoding)

    def get_all_sections(self):
        sections = list()
        data = self.get_data_from_url(url=self.welcome_url)
        soup = bs(data, self.bs_config)
        refs = soup.find_all('a', {'class': 'linkMenu'})
        for ref in refs:
            sections.append(self.welcome_url + ref['href'])
        self.log('All sections scraped')
        return sections

    def get_subsections(self, url):
        subsections = list()
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        vignettes = soup.find_all('div', {'class': 'tabloVignette'})
        for vignette in vignettes:
            sublist = vignette.find('ul', {'class': 'popup-liste'})
            if sublist:
                subsub = sublist.find_all('a', {'class': 'aSousFam'})[1:]
                for s in subsub:
                    subsections.append(self.welcome_url + s['href'])
            else:
                subsections.append(self.welcome_url + vignette.a['href'])
        self.log('All subsections scraped for ' + url)
        return subsections

    def find_next_page_id(self, url):
        data = self.get_data_from_url(url=url)
        soup = bs(data, self.bs_config)
        nextpage = soup.find_all('a', {'class': 'pageSuivante'})
        if nextpage:
            self.log('Found a next page')
            return self.welcome_url + nextpage[0]['href']
        else:
            self.log('Found 0 next page')
            return ''

    def filename_maker(self, url_catego, url_subcatego):
        split_url_catego = url_catego.split('/')
        split_url_subcatego = url_subcatego.split('/')
        category = split_url_catego[3].split(',')[0].replace('livraison-courses-','')
        under_category = split_url_subcatego[3].split(',')[0].replace('achat-en-ligne-','')
        filename = self.shop + '_' + category + '_' + under_category
        return filename

    def parse_page_product(self, filename):
        data = open(filename).read().replace('\n', '').decode(self.encoding)
        soup = bs(data, self.bs_config)
        products_found = soup.find_all('div', {'class': 'tabloVignette'})
        products = list()
        for product in products_found:
            prod = product.thead.a.text
            p_split = prod.split(' ')
            u = p_split[-1]
            if not re.findall(r'\d', u):
                u = '1'
            n = prod.replace(u, '')
            p = product.find('div', {'class': 'prix'}).text.strip().replace(',', '.').encode(self.encoding).replace('€', '')
            u = self.unit_maker(name=n, unit=u)
            products.append({'name': n, 'unit': u, 'price': p})
        return products

    def unit_maker(self, name, unit):
        if 'x' not in unit:
            n_test = re.findall(r'x\d+', name)
            if n_test:
                nb = n_test[0].replace('x', '')
                return nb + 'x' + unit
            else:
                return '1x' + unit
        else:
            return unit
