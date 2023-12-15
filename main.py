import requests
from apikey import api_key
import os
from math import radians, cos, sin, acos
import re
from datetime import datetime
from time import sleep

#Function to print the menu
def menu():
    print(
        """\033[32m
    ███        ▄████████    ▄████████  ▄█    █▄     ▄████████  ▄█               ▄███████▄  ▄█          ▄████████ ███▄▄▄▄   ███▄▄▄▄      ▄████████    ▄████████ 
▀█████████▄   ███    ███   ███    ███ ███    ███   ███    ███ ███              ███    ███ ███         ███    ███ ███▀▀▀██▄ ███▀▀▀██▄   ███    ███   ███    ███ 
   ▀███▀▀██   ███    ███   ███    ███ ███    ███   ███    █▀  ███              ███    ███ ███         ███    ███ ███   ███ ███   ███   ███    █▀    ███    ███ 
    ███   ▀  ▄███▄▄▄▄██▀   ███    ███ ███    ███  ▄███▄▄▄     ███              ███    ███ ███         ███    ███ ███   ███ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
    ███     ▀▀███▀▀▀▀▀   ▀███████████ ███    ███ ▀▀███▀▀▀     ███            ▀█████████▀  ███       ▀███████████ ███   ███ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
    ███     ▀███████████   ███    ███ ███    ███   ███    █▄  ███              ███        ███         ███    ███ ███   ███ ███   ███   ███    █▄  ▀███████████ 
    ███       ███    ███   ███    ███ ███    ███   ███    ███ ███▌    ▄        ███        ███▌    ▄   ███    ███ ███   ███ ███   ███   ███    ███   ███    ███ 
   ▄████▀     ███    ███   ███    █▀   ▀██████▀    ██████████ █████▄▄██       ▄████▀      █████▄▄██   ███    █▀   ▀█   █▀   ▀█   █▀    ██████████   ███    ███ 
              ███    ███                                      ▀                           ▀                                                         ███    ███ 
        \033[m"""
    )
    print("Please run this code in maximized window".center(160))
    input("Press ENTER to continue".center(160))
    print(
        """
           Choose an option
 \033[32m( 1 )\033[m Request locals based in given coord's and area.
 \033[32m( 2 )\033[m Start travelling plan
        
        """
    )

    while True:
        try:
            op = int(input("\nInsert your option > "))
        except Exception:
            print("\033[31mInsert an valid option.\033[m")
        else:
            if op not in (1, 2):
                print("\033[31mInsert an valid option.\033[m")
            else:
                clear_terminal()
                return op

#Funciton to clean the terminal
def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

#Function to open the specified file and read its contents line by line and Split each line by "." to create a list of categories, and iterate through the list of categories
#The final result is a dictionary of categories
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

#Function that will permit the user to choose the categories and subcategories of his interest, and permit to choose more than one category or subcategory
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
                print("Choose the category that you want.\n")
                print(f"Category directory > {category_string}\n")
                print(
                    "\033[32m( ID )\033[m | Category\033[33m(n° of subcategories)\033[m"
                )
                print("―" * 40)
                for pos, category in enumerate(current.keys()):
                    quantity_sub = len(current[category].keys())
                    print(
                        f"\033[32m( {str(pos).zfill(2)} )\033[m | {category}\033[33m({quantity_sub})\033[m",
                        flush=True,
                    )
                    sleep(0.015)
                print()
                try:
                    next_category_input = input(
                        "Insert the next category ID that you want \033[32m(Enter to actual)\033[m > "
                    )
                    next_category_id = int(next_category_input)
                except Exception:
                    if next_category_input.strip() == "":
                        break
                    print("\033[31mInsert an valid ID.\033[m")
                    sleep(1.5)
                else:
                    if next_category_id not in range(0, len(current.keys()) - 1):
                        print("\033[31mInsert an valid ID.\033[m")
                        sleep(1.5)
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
 \033[32m( 1 )\033[m Yes
 \033[31m(Enter)\033[m No
                
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

#Function to calculate the distance between the coordinates given by the user and the coordinates of the place choosen
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

#Function to extract the information from the json file, and organize it in a list, and organizes the list of dictionaries in order of distance, from smallest to largest
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

#Function to print the information extracted from the json file
def printInfos(organized_sorted_by_distance):
    if len(organized_sorted_by_distance) == 0:
        print("\033[31mThere isn't any place for this categories on this area.\033[m")
        return None
    for item in organized_sorted_by_distance:
        print("\n", flush=True)
        print(f"{' '*5}\033[33m{item['name']}\033[m")
        print("\033[32mCountry:\033[m", item["country"])
        print("\033[32mCity:\033[m", item["city"])
        print("\033[32mLatitude and Longitude:\033[m", item["lat_long"])
        print("\033[32mDistrict:\033[m", item["district"])
        print("\033[32mDistance:\033[m", "{:.2f}".format(item["distance"]), "Km")
        print("\033[32mAdress:\033[m", item["formatted"])
        print("\033[32mCategories:\033[m", item["categories"])
        sleep(1)

#Functions to validate the input latitude
def validLat(input_text):
    pattern = re.compile(r"^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$", re.IGNORECASE)
    return bool(pattern.match(input_text))

#Functions to validate the input longitude
def validLon(input_text):
    pattern = re.compile(
        r"^-?((\d{1,2}(\.\d+)?)|1[0-7]\d(\.\d+)?|180(\.0+)?)$", re.IGNORECASE
    )
    return bool(pattern.match(input_text))

#Functions to request the time zone, time and date, by an api url
def requestTimeZone(lat, long):
    url = f"https://timeapi.io/api/Time/current/coordinate?latitude={lat}&longitude={long}"
    response = requests.get(url)
    d = response.json()
    return [d["timeZone"], d["time"], d["dateTime"]]

#Functions to request the currency of the capital of the destination by an api url
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

#Function to test the internet
def testInternet():
    url_teste = "http://www.google.com"

    try:
        resposta = requests.get(url_teste)
        resposta.raise_for_status()
        return True
    except requests.RequestException:
        return False

#The function main is the principal function of the program, that:
    
        #Uses testInternet() to assert that there is an internet connection.
        #Reading Categories from File:
        #Calls fileToDict("categories.txt") to read categories from a file and organize them into a nested dictionary (database).
        #User Input invokes menu() to get a user's choice.
        #Collects user input for latitude, longitude, and the distance to search for places.

    #Category Selection and API Request (Option 1):
        #If the user chooses option 1, it selects categories using getCategories(database).
        #Constructs an API request URL based on the selected categories, location, and distance.
        #Makes a request to the Geoapify API using the constructed URL.
        #Processes the API response using functions like catchJsonInfos and prints the information using printInfos.

    #Travel Plan (Option 2):
        #Calls requestTimeZone to get time zone information for the destination.
        #Calculates and displays the time difference between the user's local time and the destination time.
        #Requests the country for currency conversion using requestCurrency.
        #Displays information about the destination currency.
        #Asks the user if they want to see tourism places in the area.
        #Constructs and sends a request to the Geoapify API to get tourism-related places.
        #Processes the API response and prints the information.

    #Exiting (Option 3):
        #When the program finishes, the program exits.

def main():
    
    assert testInternet()
    
    database = fileToDict("categories.txt")

    # Selected categories after user choose.
    menu_op = menu()

    # Requesting the information input's.
    while True:
        local_coords_lat = input("Insert your latitude > ")
        if validLat(local_coords_lat):
            break
        else:
            print("\033[31mInsert an valid latitude.\033[m")

    while True:
        local_coords_lon = input("Insert your longitude > ")
        if validLon(local_coords_lon):
            break
        else:
            print("\033[31mInsert an valid longitude.\033[m")

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
        print(
            "You've chosen the \033[32mtravel plan\033[m. Here are the specific info's:\n"
        )
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
        print(f"This is a difference of \033[32m{difference}\033[m hours.\n")
        print(f"The destiny TimeZone is \033[32m{destiny_info[0]}\033[m.\n")

        # Requesting the country for currency conversion
        capital = destiny_info[0].split("/")[1]
        currency_info = requestCurrency(capital)
        if currency_info is not None:
            print(f"Your destiny currency is \033[32m{currency_info}.\033[m\n")

        print(
            """\n
           Do you want to see the tourism places in the area?
 \033[32m( 1 )\033[m Yes
 \033[31m( 2 )\033[m No
        
        """
        )

        while True:
            try:
                op = int(input("\nInsert your option > "))
            except Exception:
                print("\033[31mInsert an valid option.\033[m")
            else:
                if op not in (1, 2):
                    print("\033[31mInsert an valid option.\033[m")
                else:
                    clear_terminal()
                    break

        url = f"https://api.geoapify.com/v2/places?categories=tourism,beach,entertainment&filter=circle:{local_coords_lon},{local_coords_lat},{how_far_meters}&bias=proximity:{local_coords_lon},{local_coords_lat}&limit=30&apiKey={api_key}"

        response = requests.get(url)
        organized_response_dict = catchJsonInfos(
            response.json(), local_coords_lat, local_coords_lon
        )

        printInfos(organized_response_dict)
    else:
        exit()


if __name__ == "__main__":
    clear_terminal()
    main()
