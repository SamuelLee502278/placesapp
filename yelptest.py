# import requests
# import difflib
# import config as creds
# import utility

# utility = utility.UtilityClass()

# endpoint = "https://api.yelp.com/v3/businesses/search"
# headers = {'Authorization':'bearer %s' % creds.yelpkey}
# parameters =  {
#     'latitude' : 29.58426399999999,
#     'longitude' :  -95.64731499999999,
#     'limit':5,
#     'radius':100,
# }
# count = 0   
# output = requests.get(url = endpoint, params = parameters, headers = headers)
# content = output.json()['businesses']
# newlist = []
# for item in content:
#     word = utility.addelementstring(item['name'], str(count))
#     count = count + 1
#     newlist.append(word)
# result = difflib.get_close_matches('bakery', newlist, cutoff = 0.2)
# print(result)
# index = int(result[0][len(result[0])-1])
# print(content[index])
