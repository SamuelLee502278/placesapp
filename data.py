import requests
from config import secret

def textsearch(usersearch):
    textsearch_array = []
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+ usersearch + "&key=" + secret
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print(f"Error code {r.status_code} fetching data from Google Places TextSearch API")
        return None
    content = r.json()["results"]
    for item in content:
        textsearch_array.append(item['place_id'])
        print(item['place_id'])
    return textsearch_array 

def findplace(usersearch):
    results = []
    usersearch = "+".join(usersearch.split(" "))
    textsearch_array = textsearch(usersearch) 
    for candidates in textsearch_array:
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + candidates + "&fields=formatted_address,name,geometry,photo,formatted_phone_number&key=" + secret
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
            # "photo": content['photo']
        }
        results.append(place)
    return results


if __name__=="__main__":
    findplace()