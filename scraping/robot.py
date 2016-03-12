# -*- coding: utf-8 -*-

from database import Database
from carrefour import Carrefour
from simplymarket import SimplyMarket
from monoprix import Monoprix
from auchan import Auchan
from gvingt import GVingt
from casino import Casino
import time, os, json

class Robot(object):

    def __init__(self, name):
        self.name = name
        self.db = Database('products')

    def log(self, msg):
        print '[INFO] [' + self.name + '] ' + msg

    '''
    Carrefour
    '''
    def carrefour_scraping(self):
        urls = Carrefour().get_all_sections()
        for u in urls:
            c = Carrefour()
            url = c.endpoint + u
            c.get_data_from_url(url=url)
            self.log("Scraped: " + url)
            time.sleep(5)

    def carrefour_parsing(self, folder='carrefour/'):
        c = Carrefour()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            f_split = f.split('_')
            shop = f_split[0]
            category = f_split[1]
            subcategory = f_split[2]
            if len(f_split) > 3:
                datas = c.parse_page_product(filename=folder + f, isNextPage=True)
            else:
                datas = c.parse_page_product(filename=folder + f, isNextPage=False)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()

    '''
    SimplyMarket
    '''
    def simplymarket_scraping(self):
        s = SimplyMarket()
        s.scraping()

    def simplymarket_parsing(self, folder='simplymarket/'):
        s = SimplyMarket()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            f_split = f.split('_')
            shop = f_split[0]
            category = f_split[1]
            subcategory = f_split[2]
            datas = s.parse_page_product(filename=folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()

    '''
    Monoprix
    '''
    def monoprix_scraping(self):
        m = Monoprix()
        sections = m.get_all_sections()
        for section in sections:
            subsections, subsubsections = m.get_subsections(url=section)
            for subsection, subsubsection in zip(subsections, subsubsections):
                m = Monoprix()
                subsub_new_id = subsubsection.split(';')[0] + ';jsessionid=' + m.get_session_id()
                try:
                    html_content = m.get_all_products_page(url=subsub_new_id)
                except:
                    html_content = m.get_all_products_page(url=subsub_new_id)
                filename = m.filename_maker(url_catego=section, url_subcatego=subsection, url_subsubcatego=subsubsection)
                with open(m.shop + '/' + filename, 'w') as out:
                    out.write(html_content)
                time.sleep(5)
                self.log('Products scraped '+ subsubsection)
            self.log('All products scraped for ' + section)

    def monoprix_parsing(self, folder='monoprix/'):
        m = Monoprix()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            f_split = f.split('_')
            shop = f_split[0]
            category = f_split[1]
            sub = f_split[2]
            for ff in f_split[3:]:
                sub += '-' + ff
            subcategory = sub.decode('utf-8')
            datas = m.parse_page_product(filename=folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()

    '''
    Auchan
    '''
    def auchan_scraping(self):
        a = Auchan()
        a.scraping()

    def auchan_parsing(self, folder='auchan/'):
        a = Auchan()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            f_split = f.split('_')
            shop = f_split[0]
            category = f_split[1]
            sub = f_split[2]
            for ff in f_split[3:]:
                sub += '-' + ff
            subcategory = sub.decode('utf-8')
            datas = a.parse_page_product(filename=folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()

    '''
    G20
    '''
    def g20_scraping(self):
        g = GVingt()
        g.scraping()

    def g20_parsing(self, folder='g20/'):
        g = GVingt()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            shop = f.split('_')[0]
            category, subcategory, datas = g.parse_page_product(filename=folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()

    '''
    Casino
    '''
    def casino_scraping(self):
        ca = Casino()
        sections = ca.get_all_sections()
        for section in sections:
            subsections = ca.get_subsections(url=section)
            for subsection in subsections:
                ca = Casino()
                html_content = ca.get_all_products_page(url=subsection)
                filename = ca.filename_maker(url_catego=section, url_subcatego=subsection)
                with open(ca.shop + '/' + filename, 'w') as out:
                    out.write(html_content)
                time.sleep(5)
                self.log('Products scraped '+ subsection)
            self.log('All products scraped for ' + section)

    def casino_parsing(self, folder='casino/'):
        ca = Casino()
        files = list()
        for o in os.walk(folder):
            files = o[2]
        res = list()
        for f in files:
            f_split = f.split('_')
            shop = f_split[0]
            category = f_split[1]
            subcategory = f_split[2]
            datas = ca.parse_page_product(filename=folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            self.db.insert_product(collection='shopproducts', doc=datas)
        self.db.close()
