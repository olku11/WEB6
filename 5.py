import sys
import requests
import function

toponym_to_find = " ".join(sys.argv[1:])

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
else:
    json_response = response.json()
    finx, finy = function.coord(json_response)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": ",".join(toponym_coodrinates.split(" ")),
        'kind': 'district',
        'results': '1',
        'format': 'json'
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    print(response.json()["response"]["GeoObjectCollection"][
              "featureMember"][0]["GeoObject"]['name'])
