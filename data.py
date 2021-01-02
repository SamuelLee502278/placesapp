import requests
import config as creds
import difflib
import utility 

utility = utility.UtilityClass()

class DataClass:

    def __init__(self):
        self.searchstore = None

    def textsearch(self, usersearch):
        textsearch_array = []
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+ usersearch + "&key=" + creds.secret
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print(f"Error code {r.status_code} fetching data from Google Places TextSearch API")
            return None
        content = r.json()["results"]
        for item in content:
            textsearch_array.append(item['place_id'])
        return textsearch_array 

    def findplace(self, usersearch):
        results = []
        usersearch = "+".join(usersearch.split(" "))
        textsearch_array = self.textsearch(usersearch) 
        for candidates in textsearch_array:
            url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + candidates + "&fields=formatted_address,name,geometry,photo,formatted_phone_number&key=" + creds.secret
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                print(f"Error code {r.status_code} fetching data from Google Places Detail API")
                return None
            content = r.json()['result']
            place = {
                "name" : content['name'],
                "address" : content['formatted_address'],
                "lat" : content['geometry']['location']['lat'],
                "lng" : content['geometry']['location']['lng'],
            }
            results.append(place)
        return results

    def getyelpinfo(self, new_item):
        endpoint = "https://api.yelp.com/v3/businesses/search"
        headers = {'Authorization':'bearer %s' % creds.yelpkey}
        parameters =  {
        'latitude' : float(new_item['lat']),
        'longitude' :  float(new_item['lng']),
        'limit':5,
        'radius':100,
            }
        count = 0   
        output = requests.get(url = endpoint, params = parameters, headers = headers)
        content = output.json()['businesses']
        newlist = []
        for item in content:
            word = utility.addelementstring(item['name'], str(count))
            count = count + 1
            newlist.append(word)
        result = difflib.get_close_matches(new_item['name'], newlist, cutoff = 0.2)
        placeinfo = self.parse_yelpinfo(result, content)
        return placeinfo

    def parse_yelpinfo(self, result, content):
        dict_title = ['rating', 'price', 'display_phone', 'url']
        result_set = []
        if len(result) == 0:
            result_set = ['None', 'None', 'None', 'None']
        else:
            index = int(result[0][len(result[0])-1])
            for i in range(len(dict_title)):
                if dict_title[i] in content[index]:
                    result_set.append(content[index][dict_title[i]])
                else:
                    result_set.append('None')
        placeinfo = {
            'rating': result_set[0],
            'price': result_set[1],
            'phone': result_set[2],
            'website': result_set[3]
        }
        return placeinfo

    def storesearch(self, store):
        self.searchstore = store

    def getsearch(self):
        return self.searchstore

