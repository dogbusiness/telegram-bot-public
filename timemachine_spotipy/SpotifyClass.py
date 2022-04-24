import os
import requests
from bs4 import BeautifulSoup
import spotipy
import datetime as dt

SPOTI_CLIENT_ID = os.environ.get('SPOTI_CLIENT_ID')
SPOTI_CLIENT_SECRET = os.environ.get('SPOTI_CLIENT_SECRET')

class Spotify:
    def __init__(self):
        self.client_id = SPOTI_CLIENT_ID
        self.client_secret = SPOTI_CLIENT_SECRET

    def create_playlist(self, year):
        #----------Проверяем адекватность года----------#
        try:
            year = int(year)
        except ValueError:
            return f'Год {year} некорректен'
        
        year_now = dt.datetime.now().year
        if 1970 <= year > (year_now - 1):
            return f'Год {year} некорректен'

        #----------Часть парсинга----------#
        response = requests.get(f'https://playback.fm/charts/top-100-songs/{year}')

        if response.status_code != 200:
            print(response.status_code)
        else:
            print('Все ок')

        soup = BeautifulSoup(response.text, 'html.parser')

        tracks = soup.find_all(name='a', itemprop='name')
        track_list = [track.getText().replace('\n', '') for track in tracks]
        # print(track_list)

        artists = soup.find_all(name='a', class_='artist')
        # artist_list = [artist.getText().replace('\n', '') for artist in artists]
        # print(artist_list)

        #----------Spotify_API----------#
        # Запутано устроена авторизация. Сначала авторизируемся с помощью token
        token = spotipy.oauth2.SpotifyOAuth(client_id=self.client_id,
                                            client_secret=self.client_secret,
                                            scope='playlist-modify-public', redirect_uri='https://example.com/')

        # Объект авторизации используем для создания объекта sp и для дальнейших действий
        sp = spotipy.Spotify(auth_manager=token)

        user_id = sp.current_user()['id']
        # print(user_id)

        # Для добавления в плейлист можно использовать только uris, а не сырые названия. Используем search для этого
        track_uris = []
        for track in track_list:
            result = sp.search(q=f'track:{track} year:{year}', type='track')
            # print(result)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                track_uris.append(uri)
            except IndexError:
                print(f"{track} doesn't exist in Spotify. Skipped.")

        # Сначала создаем плейлист, затем добавляем uri-айтемы
        playlist = sp.user_playlist_create(user=user_id, name=f'Top 100 of {year}', public=True)
        # print(playlist)
        playlist_url = playlist['external_urls']['spotify']
        # print(playlist_url)
        playlist_id = playlist['id']
        # print(playlist_id)

        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

        return playlist_url
        # Обложка меняется с помощью playlist_upload_cover_image(playlist_id, image_b64). Однако мне выдает 401 ошибку
        # Возможно для этого нужен платный акк
        # with open('base64cover.txt') as f:
        #     image_base64 = f.read()

