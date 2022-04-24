#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData


ORIGIN_CITY_IATA = 'LON'
TOMORROW = (dt.datetime.now() + dt.timedelta(days=1)).strftime('%d/%m/%Y')
PLUS_SIX_MONTH = (dt.datetime.now() + dt.timedelta(days=(6 * 30))).strftime('%d/%m/%Y')


def flight():
    # Importing classes
    data_manager = DataManager()
    flight_search = FlightSearch()

    # Getting data from sheet
    sheet_data = data_manager.get_sheet()
    print(sheet_data)

    # Check if iatacodes are empty using flight_search and data_manager
    for i in range(len(sheet_data)):
        if sheet_data[i]['iataCode'] == '':
            print('At least one IATA code not found. Getting IATA for all cities...')
            sheet_data = flight_search.get_iata(sheet_data)
            print(sheet_data)
            data_manager.put_iata(sheet_data)
            break

    # Finding cheap flights
    final_output = []
    for destination in sheet_data:
        curr_flight = flight_search.find_flights(ORIGIN_CITY_IATA, destination["iataCode"], TOMORROW, PLUS_SIX_MONTH)
        if curr_flight == None:
            pre_final_output = f"(•`_´•)\nНе нашла полетов из {ORIGIN_CITY_IATA} в {destination['iataCode']}.\n(•`_´•)"
            final_output.append(pre_final_output)
        else:
            pre_final_output = f"(｡◕‿‿◕｡)\nПодходящий под настройки полет стоит {curr_flight.price}$ (мин. цена для этого города - " \
                        f"{destination['lowestPrice']}$). Из {curr_flight.origin_city}-{curr_flight.origin_airport} в" \
                        f" {curr_flight.destination_city}-{curr_flight.destination_airport}" \
                        f" Вылет - {curr_flight.out_date}. Возвращение - {curr_flight.return_date}\n(｡◕‿‿◕｡)"
            final_output.append(pre_final_output)
    # print(final_output)
    return final_output

    # Sending via telegram
