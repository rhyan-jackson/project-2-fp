import requests
from apikey import api_key
import os
from math import radians, cos, sin, acos
import re
from datetime import datetime


def menu():
    #     print(
    #         """
    # ██╗░░░██╗░█████╗░░█████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗  ███████╗░██████╗░█████╗░░█████╗░██████╗░███████╗
    # ██║░░░██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    # ╚██╗░██╔╝███████║██║░░╚═╝███████║░░░██║░░░██║██║░░██║██╔██╗██║  █████╗░░╚█████╗░██║░░╚═╝███████║██████╔╝█████╗░░
    # ░╚████╔╝░██╔══██║██║░░██╗██╔══██║░░░██║░░░██║██║░░██║██║╚████║  ██╔══╝░░░╚═══██╗██║░░██╗██╔══██║██╔═══╝░██╔══╝░░
    # ░░╚██╔╝░░██║░░██║╚█████╔╝██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║  ███████╗██████╔╝╚█████╔╝██║░░██║██║░░░░░███████╗
    # ░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝  ╚══════╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚══════╝
    #           """
    #     )
    print(
        """
    ███        ▄████████    ▄████████  ▄█    █▄     ▄████████  ▄█               ▄███████▄  ▄█          ▄████████ ███▄▄▄▄   ███▄▄▄▄      ▄████████    ▄████████ 
▀█████████▄   ███    ███   ███    ███ ███    ███   ███    ███ ███              ███    ███ ███         ███    ███ ███▀▀▀██▄ ███▀▀▀██▄   ███    ███   ███    ███ 
   ▀███▀▀██   ███    ███   ███    ███ ███    ███   ███    █▀  ███              ███    ███ ███         ███    ███ ███   ███ ███   ███   ███    █▀    ███    ███ 
    ███   ▀  ▄███▄▄▄▄██▀   ███    ███ ███    ███  ▄███▄▄▄     ███              ███    ███ ███         ███    ███ ███   ███ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
    ███     ▀▀███▀▀▀▀▀   ▀███████████ ███    ███ ▀▀███▀▀▀     ███            ▀█████████▀  ███       ▀███████████ ███   ███ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
    ███     ▀███████████   ███    ███ ███    ███   ███    █▄  ███              ███        ███         ███    ███ ███   ███ ███   ███   ███    █▄  ▀███████████ 
    ███       ███    ███   ███    ███ ███    ███   ███    ███ ███▌    ▄        ███        ███▌    ▄   ███    ███ ███   ███ ███   ███   ███    ███   ███    ███ 
   ▄████▀     ███    ███   ███    █▀   ▀██████▀    ██████████ █████▄▄██       ▄████▀      █████▄▄██   ███    █▀   ▀█   █▀   ▀█   █▀    ██████████   ███    ███ 
              ███    ███                                      ▀                           ▀                                                         ███    ███ 
        """
    )
    input("Press ENTER to continue".center(160))
    print(
        """
           Choose an option
 ( 1 ) Request locals based in given coord's and area.
 ( 2 ) Start travelling plan
        
        """
    )

    while True:
        try:
            op = int(input("\nInsert your option > "))
        except Exception:
            print("Insert an valid option.")
        else:
            if not 1 <= op or not op <= 2:
                print("Insert an valid option.")
            else:
                clear_terminal()
                return op


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def fileToDict(filename):
    with open(filename, "r") as file:
        categories_all = [line.strip().split(".") for line in file.readlines()]

        database = {}

        for categories in categories_all:
            current = database
            for division in categories:
                if division not in current:
                    current[division] = {}
                current = current[division]
        return database


def getCategories(categories_database):
    categories_selected = []
    while True:
        current = categories_database
        category_string = ""
        category_list = []
        while True:
            while True:
                clear_terminal()
                print()
                print(
                    "Choose the category that you want | example: category(n° of sub.)\n"
                )
                print(f"Category directory > {category_string}\n")
                print("( ID ) | Category")
                print("―――――――――――――――――――")
                for pos, category in enumerate(current.keys()):
                    quantity_sub = len(current[category].keys())
                    print(f"( {str(pos).zfill(2)} ) | {category}({quantity_sub})")
                print()
                try:
                    next_category_input = input(
                        "Insert the next category ID that you want (Enter to actual) > "
                    )
                    next_category_id = int(next_category_input)
                except Exception:
                    if next_category_input.strip() == "":
                        break
                    print("Insert an valid ID. (Error)")
                else:
                    if not 0 <= next_category_id <= len(current.keys()) - 1:
                        print("Insert an valid ID.")
                    else:
                        break

            if next_category_input.strip() == "":
                next_category = ""
            else:
                next_category = list(current.keys())[next_category_id]

            if next_category == "" and "".join(category_list) == "":
                break

            elif next_category == "":
                categories_selected.append(category_string)
                break

            category_list.append(next_category)
            category_string = ".".join(category_list)

            current = current[next_category]

            if len(current.keys()) == 0:
                categories_selected.append(category_string)
                break

            clear_terminal()
        pass_var = True
        print(f'Already selected > {", ".join(categories_selected)}')
        print(
            """
           Do you want to continue selecting?
 ( 1 ) Yes
 (Enter) No
                
                """
        )
        while True:
            op = input("\nInsert your option > ")
            if op == "1":
                break
            else:
                pass_var = False
                break
        if not pass_var:
            break
        clear_terminal()
    return categories_selected


def distanceByCoords(lat1, lat2, lng1, lng2):
    lat1Rad, lat2Rad, lng1Rad, lng2Rad = (
        radians(lat1),
        radians(float(lat2)),
        radians(lng1),
        radians(float(lng2)),
    )
    rTerra = 6371

    return (
        acos(
            sin(lat1Rad) * sin(lat2Rad)
            + cos(lat1Rad) * cos(lat2Rad) * cos(lng2Rad - lng1Rad)
        )
        * rTerra
    )


def catchJsonInfos(dict_from_json, lat_client, lon_client):
    data = dict_from_json

    places_organized_list = []

    for features in data["features"]:
        try:
            name = features["properties"]["name"]
            country = features["properties"]["country"]
            city = features["properties"]["city"]
            lat = features["properties"]["lat"]
            lon = features["properties"]["lon"]
            distances = distanceByCoords(lat, lat_client, lon, lon_client)
            district = features["properties"]["district"]
            adress = features["properties"]["formatted"]
            categories = features["properties"]["categories"]
        except KeyError:
            continue
        else:
            info_dict = {
                "name": name,
                "country": country,
                "city": city,
                "lat_long": (lat, lon),
                "distance": distances,
                "district": (district),
                "formatted": adress,
                "categories": categories,
            }

            places_organized_list.append(info_dict)

    organized_sorted_by_distance = sorted(
        places_organized_list, key=lambda d: d["distance"]
    )

    return organized_sorted_by_distance


def printInfos(organized_sorted_by_distance):
    for item in organized_sorted_by_distance:
        print("\n")
        print("-" * 50)
        print("Name:", item["name"])
        print("Country:", item["country"])
        print("City:", item["city"])
        print("Latitude and Longitude:", item["lat_long"])
        print("District:", item["district"])
        print("Distance:", "{:.2f}".format(item["distance"]), "Km")
        print("Adress:", item["formatted"])
        print("Categories:", item["categories"])
        print("-" * 50)

def validLat(input_text):
    pattern = re.compile(r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$", re.IGNORECASE)
    return bool(pattern.match(input_text))


def validLon(input_text):
    pattern = re.compile(
        r"^-?((\d{1,2}(\.\d+)?)|1[0-7]\d(\.\d+)?|180(\.0+)?)$", re.IGNORECASE
    )
    return bool(pattern.match(input_text))

def requestTimeZone(lat, long):
    url = f"https://timeapi.io/api/Time/current/coordinate?latitude={lat}&longitude={long}"
    response = requests.get(url)
    d = response.json()
    return [d["timeZone"], d["time"], d["dateTime"]]


def requestCurrency(capital):
    url = f"https://restcountries.com/v3.1/capital/{capital}"
    response = requests.get(url)
    d = response.json()
    try:
        currency = list(d[0]["currencies"].keys())[0]
    except Exception:
        currency = None
    finally:
        return currency


def main():
    database = fileToDict("categories.txt")

    # Selected categories after user choose.
    menu_op = menu()

    # Requesting the information input's.
    while True:
        local_coords_lat = input("Insert your latitude > ")
        if validLat(local_coords_lat):
            break
        else:
            print("Insert an valid latitude.")

    while True:
        local_coords_lon = input("Insert your longitude > ")
        if validLon(local_coords_lon):
            break
        else:
            print("Insert an valid longitude.")

    while True:
        how_far_meters_inp = input("Insert how far you want to go (km) > ")
        try:
            how_far_meters = float(how_far_meters_inp) * 1000
        except ValueError:
            pass
        else:
            if how_far_meters > 0:
                break
        finally:
            print("Insert an valid number")

    # local_coords_lat = '38.9'
    # local_coords_lon = '77.03'

    if menu_op == 1:
        selected = getCategories(database)

        # Treating data to make the request in API
        url = f"https://api.geoapify.com/v2/places?categories={','.join(selected)}&filter=circle:{local_coords_lon},{local_coords_lat},{how_far_meters}&bias=proximity:{local_coords_lon},{local_coords_lat}&limit=20&apiKey={api_key}"

        response = requests.get(url)
        organized_response_dict = catchJsonInfos(
            response.json(), local_coords_lat, local_coords_lon
        )

        printInfos(organized_response_dict)

    elif menu_op == 2:
        clear_terminal()
        print("You've choosen the travel plan. Here are the specific info's: ")
        destiny_info = requestTimeZone(local_coords_lat, local_coords_lon)
        datetime_obj_destiny = datetime.strptime(
            destiny_info[2][:18], "%Y-%m-%dT%H:%M:%S"
        )
        actual_datetime = datetime.now()
        print(
            f"Your local time > {actual_datetime.strftime('%H:%M:%S')} | {datetime_obj_destiny.strftime('%H:%M:%S')} < Your destiny time\n"
        )
        difference = abs(
            round((datetime.now() - datetime_obj_destiny).total_seconds() / 3600)
        )
        print(f"This is a difference of {difference} hours.")
        print(f"The destiny TimeZone is {destiny_info[0]}.")

        # Requesting the country for currency conversion
        capital = destiny_info[0].split("/")[1]
        currency_info = requestCurrency(capital)
        if currency_info is not None:
            print(f"Your destiny currency is {currency_info}.")
        # Aqui a URL vai ser pré-definida pra TOURIST PORPOUSES.

        # url = f"https://api.geoapify.com/v2/places?categories={','.join(selected)}&filter=circle:{local_coords_lon},{local_coords_lat},{how_far_meters}&bias=proximity:{local_coords_lon},{local_coords_lat}&limit=20&apiKey={api_key}"

        # response = requests.get(url)
        # organized_response_dict = catchJsonInfos(
        # response.json(), local_coords_lat, local_coords_lon
    # )

    else:
        exit()

    # local_coords_lat = "40.730610"
    # local_coords_lon = "-73.935242"
    # how_far_meters = 20 * 1000


if __name__ == "__main__":
    clear_terminal()
    main()
