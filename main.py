import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def main(loc_lst):
    year = '(' + input("Enter year: ") + ')'
    point = input("Enter your location: ")
    file = open('locations.list', 'r')
    y_list = get_year_list(year, file)
    return y_list


def get_coordinates(location: str):
    geolocator = Nominatim(user_agent="mmulko")
    try:
        location = geolocator.geocode(location)
        return (location.latitude, location.longitude)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s")


def get_year_list(year, file):
    df = pd.DataFrame(file)
    year_list = []
    for num in range(14, len(df[0]) - 1):
        smth = df[0][num].split()
        if year in smth:
            year_list.append(smth)
    return year_list


if __name__ == '__main__':
    print(main('locations.list'))
