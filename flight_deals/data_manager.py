import os
import requests

AUTH_SHEETY = os.environ.get('AUTH_SHEETY')

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_endpoint = 'https://api.sheety.co/6152012fa02524ae289efe2cbb0d2588/flightDeals/prices'
        self.header = {
            'Authorization': AUTH_SHEETY
        }

    # Getting info from Sheety
    def get_sheet(self):
        response = requests.get(url=self.sheety_endpoint, headers=self.header)
        raw_data = response.json()
        formatted_data = raw_data['prices']
        print(raw_data)
        return formatted_data

    # Put IATA codes got from flight search to Sheets
    def put_iata(self, sheet_with_iata):
        for i in range(len(sheet_with_iata)):
            print('Putting Iata')
            endpoint = f'{self.sheety_endpoint}/{sheet_with_iata[i]["id"]}'
            new_data = {
                'price': {
                        'iataCode': sheet_with_iata[i]['iataCode']
                }
            }
            response = requests.put(url=endpoint, headers=self.header, json=new_data)
            print(response.text)
