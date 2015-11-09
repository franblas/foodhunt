# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, time, spynner

class Monoprix(Scraper):

    def __init__(self):
        super(Monoprix, self).__init__()
        self.endpoint = 'http://courses.monoprix.fr'
        self.welcome_url = 'http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html'
        self.shop = 'monoprix'
        self.browser = spynner.Browser(debug_level=spynner.ERROR)

    def get_data_from_url(self, url):
        response = rq.get(url)
        self.log('Get data from ' + url)
        return response.text.encode(self.encoding)

    def get_session_id(self):
        post_url = self.endpoint +  '/productlist.productslist.nbproductbypageform'
        r = rq.post(post_url, data={'t:formdata': 'H4sIAAAAAAAAAFvzloEVAN3OqfcEAAAA'})
        cookies =  r.cookies["JSESSIONID"]
        self.log('Cookies are prepared')
        return cookies

    def get_all_sections(self): # without section mode of monop
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
        subsubsections = list()
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
                subsections.append(sub_ref)
                subsubsections.append(self.endpoint + rr['href'])
        self.log('All subsections scraped for ' + url)
        return subsections, subsubsections

    def get_all_products_page(self, url, timeout=120):
        self.create_directory(self.shop)
        self.browser.load(url=url, load_timeout=timeout)
        self.browser.load_jquery(True)
        self.browser.click("a[title=Tous]")
        self.browser.wait(5)
        html_content = self.browser.html.encode(self.encoding)
        self.log('Get all products for ' + url)
        self.browser.close()
        return html_content

    def filename_maker(self, url_catego, url_subcatego, url_subsubcatego):
        split_url_catego = url_catego.split('/')
        split_url_subcatego = url_subcatego.split('/')
        split_url_subsubcatego = url_subsubcatego.split('/')
        category = ''.join([i for i in split_url_catego[4].split(';')[0] if not i.isdigit()])
        under_category = ''.join([i for i in split_url_subcatego[4].split(';')[0] if not i.isdigit()])
        underunder_category = ''.join([i for i in split_url_subsubcatego[4].split(';')[0] if not i.isdigit()])
        filename = self.shop + '_' + category[:-1] + '_' + under_category[:-1] + '_' + underunder_category[:-1]
        return filename
