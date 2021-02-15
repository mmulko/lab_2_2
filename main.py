from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time


def main(loc_lst: str):
    year = '(' + input("Enter year: ") + ')'
    point = input("Enter your location: ")
    location = coordinates_to_address(point)
    location = location.split(", ")[-1]
    print(location)
    file = create_list(loc_lst)
    y_list = get_year_list(year, file, location)
    z_list = get_data_list(y_list)
    g_list = get_coordinates_to_movie(z_list)
    return g_list


def get_coordinates(location: str):
    try:
        geolocator = Nominatim(user_agent="mmulko")
        try:
            time.sleep(1)
            location = geolocator.geocode(location)
            return [location.latitude, location.longitude]
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message %s")
    except AttributeError:
        return "None"


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
            index = year_list[num].index(loc)
            loc_list.append(year_list[num][0:index+1])
    return loc_list


def coordinates_to_address(point: str):
    geolocator = Nominatim(user_agent="mmulko")
    try:
        location = geolocator.reverse(point, language='en')
        return location.address
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s")


def get_data_list(loc_list):
    f_list = []
    for row in range(len(loc_list)):
        p_list = []
        for elem in loc_list[row]:
            stuff = list(elem)
            for elem_2 in stuff:
                if elem_2 == "}":
                    index = loc_list[row].index(elem)
                    p_list.append(loc_list[row][0:index + 1])
                    p_list.append(loc_list[row][index + 2:len(loc_list[row])])
        f_list.append(p_list)
    list2 = [x for x in f_list if x != []]
    return list2


def get_coordinates_to_movie(r_list):
    for num in range(len(r_list)):
        w_list = r_list[num][1]
        f_str = ""
        for num_2 in range(len(w_list)):
            w_list[num_2] = w_list[num_2].rstrip(",")
            if num_2 == 0:
                f_str = f_str + w_list[num_2]
            else:
                f_str = f_str + " " + w_list[num_2]
        if get_coordinates(f_str) == "None":
            r_list[num][1] = ["None"]
        else:
            r_list[num][1] = get_coordinates(f_str)
    return r_list


def calc_distance(n_list):
    pass


if __name__ == '__main__':
    print(main('locations.list'))
