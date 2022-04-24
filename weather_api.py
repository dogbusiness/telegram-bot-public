import os
import requests
# one_call_api_request = 'https://api.openweathermap.org/data/2.5/onecall'
WEATHER_API_APPID = os.environ.get('WEATHER_API_APPID')
parameters = {
    'appid': WEATHER_API_APPID,
    'lon': 39.17,
    'lat': 51.6664,
    'exclude': 'minutely,daily',
    'units': 'metric',
    'lang': 'ru'
}

def weather_forecast():

# Sending request
    response = requests.get(url='https://api.openweathermap.org/data/2.5/onecall', params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    # print(weather_data)

    # Forming twelve hours forecast
    twelve_hours = {weather_data['hourly'][i]['temp']: weather_data['hourly'][i]['weather'][0]['description'] for i in range(0, 12)}
    # print(twelve_hours)
    values = list(twelve_hours.values())
    keys = list(twelve_hours.keys())
    str = ''
    for i in range(len(twelve_hours)):
        str += '\n'f'{keys[i]}: {values[i]}'
    return str

# print(twelve_hours)


# for item in twelve_hours:
#     if item < 803:
#         print('Clear Sky')


