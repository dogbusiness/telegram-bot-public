import os
import requests
import datetime as dt

# Constants
ALPHAV_KEY = os.environ.get('ALPHAV_KEY')
NEWS_KEY = os.environ.get('NEWS_KEY')
STOCK = "AMD"
FUNC = 'TIME_SERIES_DAILY'

def stock_news():
    period = str(dt.date.today() - dt.timedelta(days = 4))

    response = requests.get(f'https://newsapi.org/v2/everything?q={STOCK}&from={period}&sortBy=popularity&apiKey={NEWS_KEY}')
    response.raise_for_status
    news_json = response.json()


    current_news = {f'news_{i}':
    [news_json['articles'][i]['author'],
    news_json['articles'][i]['title'], 
    news_json['articles'][i]['description']
    ] for i in range(0, 3)}
    # print(current_news)
    
    return current_news
    

def hist_closes():
    # Получаем даты вчера и позавчера и переводим их в строки
    # now_date = dt.datetime.now().strftime('%Y-%m-%d')
    now_date = dt.date.today()
    yesterday_date = now_date - dt.timedelta(days = 1)
    now_date = str(now_date)
    before_yesterday_date = yesterday_date - dt.timedelta(days = 1)
    yesterday_date, before_yesterday_date = str(yesterday_date), str(before_yesterday_date)

    # Отправляем запрос и получаем json
    response = requests.get(url=f'https://www.alphavantage.co/query?function={FUNC}&symbol={STOCK}&apikey={ALPHAV_KEY}')
    response.raise_for_status()
    history_json = response.json()

    # Предотвращаем ошибку, если биржа закрыта или нет данных на какой-либо день
    try:
        yesterday_close = float(history_json['Time Series (Daily)'][yesterday_date]['4. close'])
    except KeyError:
        yesterday_close = 'Биржа была закрыта или нет данных на этот день'
    try:
        before_yesterday_close = float(history_json['Time Series (Daily)'][before_yesterday_date]['4. close'])
    except KeyError:
        before_yesterday_close = 'Биржа была закрыта или нет данных на этот день'
    
    # Высчитываем процент изменения стоимости на закрытии
    # Для дебага:
    # yesterday_close, before_yesterday_close = 115.75, 113.46
    if isinstance(yesterday_close, float) and isinstance(before_yesterday_close, float):
        difference = round(yesterday_close - before_yesterday_close, 2)
        percent_difference = round((yesterday_close / before_yesterday_close - 1) * 100, 2)
        if difference >= 0:
            output = f'{yesterday_date}: {yesterday_close}\n{before_yesterday_date}: {before_yesterday_close}\n{STOCK}: {difference}\n🔺{percent_difference}%'
        else:
            output = f'{yesterday_date}: {yesterday_close}\n{before_yesterday_date}: {before_yesterday_close}\n{STOCK}: {difference}\n🔻{percent_difference}%'
    else:
        percent_difference = 'None'
        output = f'{yesterday_date}: {yesterday_close}\n{before_yesterday_date}: {before_yesterday_close}\n{STOCK}: ¯\_(ツ)_/¯'

    return percent_difference, output


def stocks():
    percentage, closes_message = hist_closes()
    if percentage == 'None':
        return closes_message, 'None'
    # НЕ ЗАБЫВАЙ ЧТО НОВОСТИ ДОЛЖНЫ ПОЯВИТЬСЯ ТОЛЬКО ЕСЛИ РАЗНИЦА 5 % ИЛИ БОЛЕЕ. СООТВЕТСТВЕННО ELSE ВНИЗУ НУЖНО ЗАМЕНИТЬ
    else:
        return closes_message, stock_news()
