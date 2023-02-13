def coord(a):
    x_low, y_low = a['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
        'lowerCorner'].split()
    x_up, y_up = a['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
        'upperCorner'].split()
    if float(x_low) >= float(x_up):
        x = float(x_low) - float(x_up)
    else:
        x = float(x_up) - float(x_low)

    if float(y_low) >= float(y_up):
        y = float(y_low) - float(y_up)
    else:
        y = float(y_up) - float(y_low)
    return x, y