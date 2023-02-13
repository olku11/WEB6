import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image
import function
import disance
import pygame

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    # обработка ошибочной ситуации
    pass

a = response.json()
finx, finy = function.coord(a)

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
working_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

map_params = {
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "~".join(["{0},pma".format(org_point), "{0},pmb".format(f'{toponym_longitude},{toponym_lattitude}')])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

if response:
    Image.open(BytesIO(
        response.content)).show()
    distance = disance.lonlat_distance((float(point[0]), float(point[1])),
                                       (float(toponym_longitude), float(toponym_lattitude)))
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill((0, 0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        intro_text = [f'адрес: {org_address}',
                      f'имя: {org_name}',
                      f'часы работы: {working_time}',
                      f'расстояние: {distance} метров']

        font = pygame.font.Font(None, 25)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()

    pygame.quit()
