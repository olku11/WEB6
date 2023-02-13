import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
import requests
import function
from PIL import Image

# Пусть наше приложение предполагает запуск:# python search.py Москва, ул. Ак. Королева, 12# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass# Преобразуем ответ в json-объект
json_response = response.json()
finx, finy = function.coord(json_response)


# Преобразуем ответ в json-объект
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

# Собираем параметры для запроса к StaticMapsAPI:

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": f'{str(round(finx, 3))},{str(round(finy, 3))}',
    "pt": f"{','.join(toponym_coodrinates.split())},pm2wtm",
    "l": "map"}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
if response:
    Image.open(BytesIO(
        response.content)).show()