import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def main(loc_lst):
    year = '(' + input("Enter year: ") + ')'
    point = input("Enter your location: ")
    location = coordinates_to_address(point)
    location = location.split(", ")[-1]
    print(location)
    file = create_list('locations.list')
    y_list = get_year_list(year, file, location)
    return y_list


def get_coordinates(location: str):
    geolocator = Nominatim(user_agent="mmulko")
    try:
        location = geolocator.geocode(location)
        return (location.latitude, location.longitude)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s")


def create_list(file):
    f_list = []
    with open(file) as f:
        for _ in range(14):
            f.readline()
        for line in f:
            res = line.split()
            for elem in range(len(res)):
                res[elem].rstrip("\n")
            f_list.append(res)
    return f_list


def get_year_list(year, file, loc):
    year_list = []
    for num in range(14, len(file) - 1):
        if year in file[num]:
            year_list.append(file[num])
    loc_list = []
    for num in range(len(year_list)):
        if loc in year_list[num]:
            loc_list.append(year_list[num])
    return loc_list


def coordinates_to_address(point: str):
    geolocator = Nominatim(user_agent="mmulko")
    try:
        location = geolocator.reverse(point, language='en')
        return location.address
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s")


if __name__ == '__main__':
    print(main('locations.list'))
