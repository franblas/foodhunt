# -*- coding: utf-8 -*-

import json
import requests as rq

endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/'
apikey = 'AIzaSyBhhoOIKEQRxakb1CocIKZBuqeSbbLEoUQ'

#latitude = 48.834972 # rue gassendi
#longitude = 2.326856 # rue gassendi
latitude = 48.839312 # near Montparnasse
longitude = 2.322275 # near Montparnasse
radius = 500 # in meters
placetype = 'grocery_or_supermarket&food'

url = endpoint + 'json?location=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(radius) + '&types=' + str(placetype) + '&key=' + str(apikey)
response = rq.get(url)

res = json.loads(response.content)

print res
#for r in res.get('results'):
#    print r.get('name'), r.get('vicinity')
