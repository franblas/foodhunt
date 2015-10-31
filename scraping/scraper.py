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
