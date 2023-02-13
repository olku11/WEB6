import math
import requests


def lonlat_distance(a, b):
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    dx = abs(a_lon - b_lon) * 111000 * math.cos(math.radians((a_lat + b_lat) / 2))
    dy = abs(a_lat - b_lat) * 111000
    return math.sqrt(dx * dx + dy * dy)
