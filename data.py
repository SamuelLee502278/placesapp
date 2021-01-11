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

    def get_businessearch(self, new_item):
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

    def get_businessdetails(self, id):
        dict_title = ['photos','hours']
        result_set = []
        endpoint = "https://api.yelp.com/v3/businesses/" + id
        headers = {'Authorization':'bearer %s' % creds.yelpkey}
        output = requests.get(url = endpoint, headers = headers)
        content = output.json()
        for i in range(len(dict_title)):
            if dict_title[i] in content:
                result_set.append(content[dict_title[i]])
            else:
                result_set.append('None')
        return result_set
        
    def parse_yelpinfo(self, result, content):
        dict_title = ['id','rating', 'price', 'display_phone', 'url']
        result_set_search = []
        if len(result) == 0:
            result_set_search = ['None', 'None', 'None', 'None', 'None']
            result_set_details = [['None', 'None', 'None'], 'None']
        else:
            index = int(result[0][len(result[0])-1])
            for i in range(len(dict_title)):
                if dict_title[i] in content[index]:
                    result_set_search.append(content[index][dict_title[i]])
                else:
                    result_set_search.append('None')
        if result_set_search[0] != 'None':
            result_set_details = self.get_businessdetails(result_set_search[0])
            for i in range(3-len(result_set_details[0])):
                result_set_details[0].append('None')
        placeinfo = {
            'id': result_set_search[0],
            'rating': result_set_search[1],
            'price': result_set_search[2],
            'phone': result_set_search[3],
            'website': result_set_search[4],
            'photo1': result_set_details[0][0],
            'photo2': result_set_details[0][1],
            'photo3': result_set_details[0][2],
            'hours': result_set_details[1]
        }
        print(placeinfo)
        return placeinfo

    def storesearch(self, store):
        self.searchstore = store

    def getsearch(self):
        return self.searchstore

