import json
from math import radians, cos, sin, acos

def informations():
    with open('arquivo.json') as json_file: 
        data = json.load(json_file) 
    
    result_list = []
    
    for features in data['features']:
        name = features["properties"]["name"]
        country = features["properties"]["country"]
        city = features["properties"]["city"]
        lat = features["properties"]["lat"]
        lon = features["properties"]["lon"]
        distances=distance(lat, 40.6272585, lon, -8.6438262)
        district = features["properties"]["district"]
        adress = features["properties"]["formatted"]
        categorie = features["properties"]["categories"]
        
        info_dict = {"name": name, "country": country, "city": city, "lat_long": (lat, lon) ,"distance": distances, "district": (district), "formatted": adress, "categories": categorie}
        
        result_list.append(info_dict)
    
    for item in result_list:
        print("Name:", item["name"])
        print("Country:", item["country"])
        print("City:", item["city"])
        print("Latitude and Longitude:", item["lat_long"])
        print("District:", item["district"])
        print("Distance:", "{:.2f}".format(item["distance"]), "Km")
        print("Adress:", item["formatted"])
        print("Categories:", item["categories"])
        print("----")

def distance(lat1, lat2, lng1, lng2):
    
        lat1Rad = radians(lat1)
        lat2Rad = radians(lat2)
        lng1Rad = radians(lng1)
        lng2Rad = radians(lng2)

        rTerra = 6371

        return acos(
                sin(lat1Rad) * sin(lat2Rad) +
                cos(lat1Rad) * cos(lat2Rad) *
                cos(lng2Rad - lng1Rad)
            ) * rTerra

def main():
    informations()


if __name__ == '__main__':
    main()

