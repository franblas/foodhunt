# -*- coding: utf-8 -*-

from database import Database
from carrefour import Carrefour
from simplymarket import SimplyMarket
from monoprix import Monoprix
import time, os, json

class Robot(object):

    def __init__(self, name):
        self.name = name
        self.db = Database('test')

    def log(self, msg):
        print '[INFO] [' + self.name + '] ' + msg

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
            self.db.insert_product(collection='carrefour', doc=datas)
        self.db.close()

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
            self.db.insert_product(collection='simplymarket', doc=datas)
        self.db.close()

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
