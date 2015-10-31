# -*- coding: utf-8 -*-

import math

class Score(object):

    def __init__(self):
        pass

    def final_score(self, point):
        score = (self.sc_distance(point) + self.sc_price(point) + self.sc_availability(point))**2
        return score * 1000

    def sc_distance(self, point):
        score = self.inverse(math.log(point.get('distance')))
        return score

    def sc_price(self, point):
        point_type = point.get('type')
        price = float(point.get('price'))
        if price == -1:
            price = 1000
        elif point_type == 'superette ville':
            price = price + price * (20.0 / 100) # 20% of majoration
        elif point_type == 'superette':
            price = price + price * (10.0 / 100) # 10% of majoration
        else:
            price = price
        score = self.inverse(price)
        return score

    def sc_availability(self, point):
        ava = ['tiny', 'small', 'medium', 'large', 'big']
        score = self.special_availability(ava.index(point.get('size')))
        return score

    '''
    Maths
    '''
    def special_availability(self, val):
        return math.exp(val - math.e) / 2.0

    def inverse(self, val, coeff=1.0):
        if val == 0:
            print 'Value should not be null'
            val = 0.00001
        return coeff * (1.0 / val)

    def gaussian(self, val, s_sigma, mu):
        if s_sigma <= 0:
            print 'Error, Squared sigma should be > 0'
            return
        a = 1.0 / (math.sqrt(s_sigma * 2 * math.pi))
        b = (-1.0 * (val - mu)**2) / (2 * s_sigma)
        return a * math.exp(b)
