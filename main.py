from twitter2 import twitter_accounts
from geopy.geocoders import Nominatim
import folium
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def starter_map():
    return render_template("index.html")


def find_given_key(element, given_key):
    """
    (dict, string) -> list
    this function returns a list with names and locations
    of followers in twitter
    """
    res = []
    for user in element['users']:
        user_location = user['location']
        user_nick = user[given_key]
        res.append((user_nick, user_location))
    return res


def interprite_names_into_coordinates(loc):
    """
    (string) -> (list)
    this function interprates names of locations into coordinates
    >>> interprite_names_into_coordinates('Los Angeles, California, USA')
    [34.0536909, -118.2427666]
    >>> interprite_names_into_coordinates('Kyiv, Ukraine')
    [50.4500336, 30.5241361]
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(loc, timeout=10)
    if location is not None:
        return [location.latitude, location.longitude]
    else:
        return [40.730610, -73.935242]


def name_location(name):
    user_dict = twitter_accounts(name)
    user_name = find_given_key(user_dict, "screen_name")
    return user_name


def create_map(data):
    """
    this function creates a map with all friends' locations
    """
    m = folium.Map(zoom_start=12)
    fs = folium.FeatureGroup(name="Friends locations")
    for person in data:
        if len(person) == 2:
            if person[1] != "":
                coord = interprite_names_into_coordinates(person[1])
                fs.add_child(folium.Marker(location=coord, popup=person[0],
                                           color='green', icon=folium.Icon()))
    m.add_child(fs)
    friends_map = m.get_root().render()

    return friends_map


@app.route("/map", methods=["POST"])
def create_final_map():
    """
    this function creates html map
    """
    name = str(request.form['name'])
    res = {"friends_map_str": create_map(name_location(name))}
    return render_template("friends.html", **res)


if __name__ == "__main__":
    app.run(debug=True, port=4356)
