# -*- coding: utf-8 -*-

import math

PI = math.pi
EARTH_RADIUS = 6371000 # in meters

class Geo(object):

    def __init__(self):
        self.EARTH_RADIUS = EARTH_RADIUS
        self.PI = PI

    def point(self, lat, lon):
        return {'lat': lat, 'lng': lon}

    def distance(self, position, point):
        lat1 = point.get('lat')
        lon1 = point.get('lng')
        lat2 = position.get('lat')
        lon2 = position.get('lng')
        return self.haversine(lon1, lat1, lon2, lat2)

    def haversine(self, longitude1, latitude1, longitude2, latitude2):
        def deg_to_rad(deg):
            return deg * self.PI / 180

        if longitude1 == latitude1 and longitude1 == latitude1:
            return 0
        else:
            # convert decimal degrees to radians
            lat1 = deg_to_rad(latitude1)
            lat2 = deg_to_rad(latitude1)
            lon1 = deg_to_rad(longitude1)
            lon2 = deg_to_rad(longitude2)
            # haversine formula
            dlon = (lon2 - lon1)
            dlat = (lat2 - lat1)
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.asin(math.sqrt(a))
            return c * EARTH_RADIUS
