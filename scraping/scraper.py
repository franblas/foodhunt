# -*- coding: utf-8 -*-

import os

class Scraper(object):

    def __init__(self):
        self.encoding = 'utf-8'
        self.bs_config = 'html5lib'

    def log(self, msg):
        print '[INFO] ' + msg

    def create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def name_format(self, name):
        n = name.decode(self.encoding).strip()
        print n
        n = n.replace('é', 'e')
        n = n.replace('è', 'e')
        n = n.replace('ê', 'e')
        n = n.replace('ë', 'e')
        n = n.replace('à', 'a')
        n = n.replace('â', 'a')
        n = n.replace('ä', 'a')
        n = n.replace('û', 'u')
        n = n.replace('ü', 'u')
        n = n.replace('î', 'i')
        n = n.replace('ï', 'i')
        n = n.replace('ô', 'o')
        n = n.replace('ö', 'o')
        n = n.replace('ç', 'c')
        n = n.replace('ÿ', 'y')
        n = n.replace('œ', 'oe')
        return n
