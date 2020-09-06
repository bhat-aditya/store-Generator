import json
import requests
import numpy as np
import pandas as pd 
from math import cos, asin, sqrt
from googleplaces import GooglePlaces, types, lang

test_data = pd.read_csv('testdata-latlong.csv')
df_final  = test_data.filter(['Lat', 'Long'], axis = 1) 
df_final  = df_final.assign(place_name = np.zeros(len(test_data)), Latitude = np.zeros(len(test_data)), Longitude = np.zeros(len(test_data)))

APIkey = ''
google_places = GooglePlaces(APIkey)

#Haversine formula for calculating distance between 2 co-ordinates
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

for index, row in test_data.iloc[1:].iterrows():

    latitude  = test_data.loc[:index].tail(2).head(1).iloc[0,0]
    longitude = test_data.loc[:index].tail(2).head(1).iloc[0,1]

    #Searching a radius of 2500m
    query = google_places.nearby_search(
        lat_lng = {'lat' : latitude, 'lng' : longitude},
        radius  = 1500,
        types = [types.TYPE_CONVENIENCE_STORE] or [types.TYPE_DEPARTMENT_STORE] or [types.TYPE_GROCERY_OR_SUPERMARKET]
    )

    try:
        plclist = list()
        latlist = list()
        lnglist = list()
        dislist = list()

        for place in query.places:
            plclist.append(place.name)
            latlist.append(place.geo_location['lat'])
            lnglist.append(place.geo_location['lng'])
            tempdist = distance(latitude, longitude, place.geo_location['lat'], place.geo_location['lng'])
        
        i   = dislist.index(min(dislist))
        lat = latlist[i]
        lng = lnglist[i]
        plc = plclist[i]

        df_final.loc[index, 'place_name'] = plclist[i]
        df_final.loc[index, 'Latitude']   = latlist[i]
        df_final.loc[index, 'Longitude']  = lnglist[i]

    except:
        df_final.loc[index, 'place_name'] = 0
        df_final.loc[index, 'Latitude']   = 0
        df_final.loc[index, 'Longitude']  = 0

print(df_final)