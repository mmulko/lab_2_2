from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from math import radians, cos, sin, asin, sqrt
import folium


def main(loc_lst: str):
    year = '(' + input("Enter year: ") + ')'
    point = input("Enter your location: ")
    location = coordinates_to_address(point)
    print(border("Your location is defined as: " + location))
    user_1 = input("Is it correct? [Y/N]: ")
    if user_1 == "N":
        return "What a shame, try different points then!"
    else:
        print("What a luck, let's build a map!")
    location = location.split(", ")[-1]
    file = create_list(loc_lst)
    print("Process status: 20%")
    y_list = get_year_list(year, file, location)
    print("Process status: 36%")
    z_list = get_data_list(y_list)
    print("Process status: 52%")
    g_list = get_coordinates_to_movie(z_list)
    print("Process status: 68%")
    f_list = calc_distance(g_list, point)
    print("Process status: 84%")
    res = creat_map(f_list, point, year)
    return res


def border(msg):
    """
    This function puts border around text
    >>> border("Hello")
    '+-----+\n|Hello|\n+-----+'
    """
    row = len(msg)
    h = ''.join(['+'] + ['-' * row] + ['+'])
    result = h + '\n'"|" + msg + "|"'\n' + h
    return result


def get_coordinates(location: str):
    """
    This function get coordinates from location
    >>> get_coordinates("Kiev, Ukraine")
    [50.4500336, 30.5241361]
    """
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
    """
    This function creates list of rows from file
    """
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
    """
    This function gets movies from one year and country
    """
    year_list = []
    for num in range(14, len(file) - 1):
        if year in file[num]:
            year_list.append(file[num])
    loc_list = []
    for num in range(len(year_list)):
        if loc in year_list[num]:
            index = year_list[num].index(loc)
            loc_list.append(year_list[num][0:index + 1])
    return loc_list


def coordinates_to_address(point: str):
    """
    This function converts coordinates to address
    >>> coordinates_to_address("50.4500336, 30.5241361")
    Independence Square, Khreshchatyk Street, Центр, Shevchenkivskyi district, Kyiv, Київська міська громада, 1001, Ukraine
    """
    geolocator = Nominatim(user_agent="mmulko")
    try:
        time.sleep(1)
        location = geolocator.reverse(point, language='en')
        return location.address
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s")


def get_data_list(loc_list):
    """
    This function divides movie name and address into two separate lists
    """
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
    """
    This function converts movie addresses two coordinates for all movies
    """
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


def calc_distance(n_list, point):
    """
    This function calculates distance between original location and movie
    production address for all movies in list
    """
    R = 3959.87433
    f_list = []
    count = 0
    for num in range(len(n_list)):
        p_list = point.split(", ")
        lon_2 = p_list[0]
        lat_2 = p_list[1]
        if n_list[num][1] == "None":
            break
        else:
            lon_1 = n_list[num][1][0]
            lat_1 = n_list[num][1][1]
        dLat = radians(float(lat_2) - float(lat_1))
        dLon = radians(float(lon_2) - float(lon_1))
        lat1 = radians(float(lat_1))
        lat2 = radians(float(lat_2))
        a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
        c = 2 * asin(sqrt(a))
        res = R * c
        if count > 0:
            if res < f_list[0] or res == f_list[0]:
                f_list.append(res)
                count += 1
                if count > 9:
                    f_list.pop()
                    n_list[count - 10].clear()
            else:
                n_list[num].clear()
        else:
            f_list.append(res)
            count += 1
    n_list[len(n_list) - 1].clear()
    list2 = [x for x in n_list if x != []]
    return list2


def creat_map(f_list, point, year):
    """
    This function generates map
    """
    p_list = []
    point_lst = point.split(", ")
    p_list.append(point_lst[0])
    p_list.append(point_lst[1])
    map_1 = folium.Map(tiles="Stamen Terrain", location=p_list, zoom_start=7)
    map_1.add_child(folium.Marker(location=p_list, popup="Your location",
                                  icon=folium.Icon()))
    for num in range(len(f_list)):
        f_str = ""
        for num_2 in range(len(f_list[num][0])):
            if num_2 == 0:
                f_str = f_str + f_list[num][0][num_2]
            else:
                f_str = f_str + " " + f_list[num][0][num_2]
        map_1.add_child(folium.Marker(location=f_list[num][1], popup=f_str,
                                      icon=folium.Icon()))
        folium.PolyLine(locations=[f_list[num][1], p_list],
                        color='red').add_to(map_1)
    map_1.save("Map_" + year + ".html")
    map_name = "Map_" + year + ".html"
    print("Process status: 100%")
    return "Find your map at: " + map_name


if __name__ == '__main__':
    print(main('locations.list'))
