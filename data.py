# -*- coding: utf-8 -*-

import json
from geo import Geo

class Data(object):

    def __init__(self):
        self.geo = Geo()

    def fromJSON(self, jsonfile):
        with open(jsonfile, 'r') as out:
            datas = json.load(out)
        res = list()
        position = datas.get("Myself")
        for k in datas.keys():
            if k != "Myself":
                d = datas.get(k)
                d['distance'] = float(self.geo.distance(position=position, point=d)) / 1000 # convert to kms
                d['name'] = k
                res.append(d)
            else:
                pass
        return position, res

    def toJSON(self):
        pass

    def __str__(self):
        pass
