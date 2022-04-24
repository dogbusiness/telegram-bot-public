import os
import requests
from flight_data import FlightData

TEQUILA_API = os.environ.get('TEQUILA_API')

class FlightSearch:

    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.teq_api = TEQUILA_API
        self.endpoint_locations = "https://tequila-api.kiwi.com/locations/query"
        self.endpoint_search = "https://tequila-api.kiwi.com/v2/search"


    def get_iata(self, city_sheet):
        header = {
            'apikey': self.teq_api
        }
        for city in city_sheet:
            curr_city = city['city']
            parameters = {
                'term': curr_city
            }
            response = requests.get(url=self.endpoint_locations, params=parameters, headers=header)
            response = response.json()
            print(response)
            city['iataCode'] = response['locations'][0]['code']
        print(city_sheet)
        return city_sheet

    def find_flights(self, orig_city, dest_city, from_time, to_time):
        header = {
            'apikey': self.teq_api
        }
        parameters = {
            "fly_from": orig_city,
            "fly_to": dest_city,
            "date_from": from_time,
            'date_to': to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url=self.endpoint_search, headers=header, params=parameters)
        try:
            data = response.json()["data"][0]
            print(data)
        except IndexError:
            print(f"(•`_´•) Не найдено полетов из {orig_city} в {dest_city}. (•`_´•)")
            return None

        # Призываем flight_data для удобного чтения
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data

