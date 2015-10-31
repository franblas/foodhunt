# -*- coding: utf-8 -*-

from scraper import Scraper
from bs4 import BeautifulSoup as bs
import requests as rq
import re, spynner

class Carrefour(Scraper):

    def __init__(self):
        super(Carrefour, self).__init__()
        self.endpoint = 'http://courses.carrefour.fr'
        self.welcome_url = 'http://courses.carrefour.fr/drive/accueil'
        self.shop = 'carrefour'
        self.nextpageid = 'nextPage'
        self.browser = spynner.Browser(debug_level=spynner.ERROR)

    def prepare_cookie(self, storeDrive="240"):
        post_url = self.welcome_url +  '.body.overlayers.storeoverlayer.drivepickingform/' + storeDrive
        r = rq.post(post_url, data={'t:formdata': 'H4sIAAAAAAAAAFvzloEVAN3OqfcEAAAA'})
        cookies = {
            "JSESSIONID": r.cookies["JSESSIONID"],
            "fromAdServer": "2",
            "storeDrive": storeDrive,
            "serviceDrive": "3",
            "displayMobilePreHome": "false",
            "xtvrn": "$443617$"
        }
        self.log('Cookies are prepared')
        return cookies

    def get_data_from_url(self, url):
        '''
        url = "http://courses.carrefour.fr/drive/tous-les-rayons/boissons/colas-boissons-gazeuses/PID0/154250"
        '''
        self.create_directory(self.shop)
        filename = self.filename_maker(url=url)
        cookies = self.prepare_cookie()
        response = rq.get(url, cookies=cookies)
        self.log('Get data from ' + url)
        nb_pages = self.get_nb_pages(html_content=response.text.encode(self.encoding))
        with open(self.shop + '/' + filename, 'w') as out:
            out.write(response.text.encode(self.encoding))
        if nb_pages != 0:
            self.next_page_script(url=url, nbpages=nb_pages)


    def next_page_script(self, url, nbpages, formDrive='0', timeout=120):
        '''
        url = "http://courses.carrefour.fr/drive/tous-les-rayons/boissons/colas-boissons-gazeuses/PID0/154250"
        browser = spynner.Browser(debug_level=spynner.ERROR)
        browser.create_webview()
        browser.show()
        browser.close()
        '''
        self.browser.load(self.welcome_url, load_timeout=timeout)
        self.browser.load_jquery(True)
        js_command = "$('form#drivePickingForm_" + formDrive + "').find('input')[1].click();"
        self.browser.runjs(js_command)
        self.browser.wait(5)
        self.browser.load(url=url, load_timeout=timeout)
        for nb in range(nbpages):
            self.browser.click("a[id=" + str(self.nextpageid) + "]")
            self.browser.wait(5)
            filename = self.filename_maker(url=url) + '_' + str(nb + 1)
            html_content = self.browser.html.encode(self.encoding)
            self.find_next_page_id(html_content=html_content)
            self.create_directory(self.shop)
            self.log('Get data next page from ' + url)
            with open(self.shop + '/' + filename, 'w') as out:
                out.write(html_content)


    def find_next_page_id(self, html_content):
        soup = bs(html_content, self.bs_config)
        nextpages = soup.find_all('a', attrs={'class': 'page', 'id': re.compile(r'nextPage*'), 'href': re.compile(r'/drive/rayon.categoryproductlistcontainer.paging.nextpage*')})
        if nextpages:
            self.nextpageid = nextpages[0]['id']

    def filename_maker(self, url):
        split_url = url.split('/')
        category = split_url[5]
        under_category = split_url[6]
        filename = self.shop + '_' + category + '_' + under_category
        return filename

    def get_all_sections(self):
        cookies = self.prepare_cookie()
        response = rq.get(self.welcome_url, cookies=cookies)
        soup = bs(response.text.encode(self.encoding), self.bs_config)
        urls = soup.find_all('a', {'href': re.compile(r'/drive/tous-les-rayons/[\D\.\D]+/PID0/*')})
        res = list()
        for url in urls:
            ref = url['href']
            if len(ref.split('/')) > 6:
                res.append(ref)
        self.log('All sections scraped')
        return res

    def get_nb_pages(self, html_content):
        soup = bs(html_content, self.bs_config)
        pagenumbers = soup.find_all('ul', {'class': 'pageNumbers'})
        if pagenumbers:
            nb = len(pagenumbers[0].find_all('li')) - 1
            self.log('Found ' + str(nb) + ' next pages')
            return nb
        else:
            self.log('Found 0 next pages')
            return 0

    def parse_page_product(self, filename):
        data = open(filename).read().replace('\n', '')
        soup = bs(data, self.bs_config)
        prices = soup.find_all('div', attrs={'class': 'spec price'})
        units = soup.find_all('span', attrs={'class': 'unit'})
        names = soup.find_all('a', attrs={'onclick': re.compile(r'javascript:*'), 'href': re.compile(r'/drive/tous-les-rayons/*')})
        corrected_names = list()
        for name in names:
            if '<span>' in str(name):
                corrected_names.append(name)
        products = list()
        for name, unit, price in zip(corrected_names, units, prices):
            p = price.text.replace('Prix Promo : ', '').encode(self.encoding).replace('â‚¬', '.') # Euro sign is not well decode, TODO: Need to be fixed
            n = name.span.text
            u = unit.text
            products.append({'name': n, 'unit': u, 'price': p})
        return products
