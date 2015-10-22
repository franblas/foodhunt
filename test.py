# -*- coding: utf-8 -*-

from score import Score
from data import Data
import json, datetime

def order_by_score(res):
    ordered_res = list()
    for r in res:
        if ordered_res:
            if r.get('score') > ordered_res[0].get('score'):
                ordered_res[0] = r #TODO: has to be corrected
            else:
                ordered_res.append(r)
        else:
            ordered_res.append(r)
    return ordered_res

#datafile = 'data/points.json' # for a bottle of Coca-Cola, 1.5L (near home)
#datafile = 'data/points2.json' # for a paquet of petit lu 200g
datafile = 'data/points3.json' # for a bottle of Coca-Cola, 1.5L (near montaprnasse)


sc = Score()

position, points = Data().fromJSON(datafile)

#res = list()
for point in points:
    #res.append({'score': sc.final_score(point=point), 'point': point, 'position': position})
    print '----------------------------------------------'
    print point.get('name'), sc.final_score(point=point)
    print 'SC distance: ' + str(sc.sc_distance(point=point))
    print 'SC price: ' + str(sc.sc_price(point=point))
    print 'SC avail: ' + str(sc.sc_availability(point=point))
    print '----------------------------------------------'
