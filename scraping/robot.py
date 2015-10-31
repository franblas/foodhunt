# -*- coding: utf-8 -*-

from carrefour import Carrefour
import time, os, json

class Robot(object):

    def __init__(self, name):
        self.name = name

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
            datas = c.parse_page_product(folder + f)
            for d in datas:
                d['shop'] = shop
                d['category'] = category
                d['subcategory'] = subcategory
            self.log("Parsed: " + f)
            res += datas
            with open('carrefour_products.json', 'w') as out:
                json.dump(res, out)
