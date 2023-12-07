import requests
from apikey import api_key
import os
import json

def menu():
    print(
        """
██╗░░░██╗░█████╗░░█████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗  ███████╗░██████╗░█████╗░░█████╗░██████╗░███████╗
██║░░░██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
╚██╗░██╔╝███████║██║░░╚═╝███████║░░░██║░░░██║██║░░██║██╔██╗██║  █████╗░░╚█████╗░██║░░╚═╝███████║██████╔╝█████╗░░
░╚████╔╝░██╔══██║██║░░██╗██╔══██║░░░██║░░░██║██║░░██║██║╚████║  ██╔══╝░░░╚═══██╗██║░░██╗██╔══██║██╔═══╝░██╔══╝░░
░░╚██╔╝░░██║░░██║╚█████╔╝██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║  ███████╗██████╔╝╚█████╔╝██║░░██║██║░░░░░███████╗
░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝  ╚══════╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚══════╝
          """
    )

    print("Press any key to continue".center(112))
    input()
    print(
        """
---------< Choose an option >---------
 > [1] Start category selection
        
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
            print()
            print("Choose the category that you want, this maybe have subcategories.\n")
            print(f"Category directory > {category_string}\n")
            for category in current.keys():
                quantity_sub = len(current[category].keys())
                print(f"{category}({quantity_sub})")
            print()

            next_category = input("Insert the next category that you want > ")

            clear_terminal()

            if next_category.strip() == "":
                categories_selected.append(category_string)
                break

            category_list.append(next_category)
            category_string = ".".join(category_list)

            current = current[next_category]

            if len(current.keys()) == 0:
                categories_selected.append(category_string)
                break
            pass_var = True
        print(
                """
---------< Do you want to continue selecting? >---------
 > [1] Yes
 > [Any other option] No
                
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


# Treating the category data

def main():
    database = fileToDict("categories2.txt")

    # Selected categories after user choose.
    menu_op = menu()
    if menu_op == 1:
        selected = getCategories(database)
    else:
        exit()

    # Requesting the information input's.
    local_coords_lat = input("Insert your latitude > ")
    local_coords_lon = input("Insert your longitude > ")
    how_far_meters = float(input("Insert how far you want to go (km) > ")) * 1000

    # Treating data to make the request in API

    area = f"circle:{local_coords_lon},{local_coords_lat},{how_far_meters}"
    url = f"https://api.geoapify.com/v2/places?categories={','.join(selected)}&filter={area}&apiKey={api_key}"

    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    clear_terminal()
    main()