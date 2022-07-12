import datetime
import base64
import requests
import webbrowser


class Spotify:
    access_token = None
    access_token_expires = datetime.datetime.now()
    token_url = "https://accounts.spotify.com/api/token"
    scope = 'user-library-read'
    redirect_uri = 'http://www.example.com/callback/'
    base_url = 'https://api.spotify.com/'

    def __init__(self, client_id, client_secret):
        self.client_id = self.__check_value(client_id)
        self.client_secret = self.__check_value(client_secret)

    @staticmethod
    def __check_value(value):
        if value is None:
            raise Exception("Необходимо установить корректное значение")
        return value

    @staticmethod
    def __get_code_from_response(url):
        if 'code' in url:
            return url.split('code=')[1]
        else:
            raise Exception('Не удалось получить код')

    def __get_code_from_browser(self):
        """
        Отправляем первоначальный запрос на сервер и получаем authorization code.
        """
        auth_url = 'https://accounts.spotify.com/authorize?'
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': self.scope}
        response = requests.get(url=auth_url, params=params)
        if response.status_code not in range(200, 299):
            raise Exception("Не удалось получить ответ")
        webbrowser.open_new(response.url)
        code = self.__get_code_from_response(input('Введите код с браузерной строки: '))
        return code

    def __get_client_authorization_data(self):
        """
        Возвращаем строку закодированную в base64.
        """
        authorization_data = f"{self.client_id}:{self.client_secret}"
        authorization_data_base64 = base64.b64encode(authorization_data.encode())
        return authorization_data_base64.decode()

    def __get_token_headers(self):
        """
        Получаем header Authorization.
        """
        authorization_data_base64 = self.__get_client_authorization_data()
        return {
            "Authorization": f"Basic {authorization_data_base64}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def __get_token_data(self):
        return {
            "grant_type": "authorization_code",
            'code': self.__get_code_from_browser(),
            'redirect_uri': self.redirect_uri
        }

    def __get_auth_data(self):
        token_url = self.token_url
        token_data = self.__get_token_data()
        token_headers = self.__get_token_headers()
        response = requests.post(token_url, data=token_data, headers=token_headers)
        if response.status_code not in range(200, 299):
            raise Exception("Не удалось получить токен")
        data = response.json()
        time_now = datetime.datetime.now()
        access_token = data['access_token']  # токен
        time_to_expiration = data['expires_in']  # Срок действия токена в секундах
        expires = time_now + datetime.timedelta(seconds=time_to_expiration)  # Время, когда закончится токен
        self.access_token = access_token
        self.access_token_expires = expires
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        time_now = datetime.datetime.now()
        if expires < time_now:
            self.__get_auth_data()
            return self.get_access_token()
        elif token is None:
            self.__get_auth_data()
            return self.get_access_token()
        return token

    def __get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_available_genre_seeds(self, resource_type='recommendations', version='v1'):
        url = f"{self.base_url}{version}/{resource_type}/available-genre-seeds"
        headers = self.__get_resource_header()
        response = requests.get(url, headers=headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()

    def get_saved_albums(self, resource_type='albums', version='v1'):
        url = f"{self.base_url}{version}/me/{resource_type}"
        headers = {**self.__get_resource_header(), 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()

    def get_artist(self, artist_id_sp, resource_type='artists', version='v1'):
        url = f"{self.base_url}{version}/{resource_type}/{artist_id_sp}"
        headers = {**self.__get_resource_header(), 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()

    def get_album_tracks(self, album_id_sp, resource_type='albums', version='v1'):
        url = f"{self.base_url}{version}/{resource_type}/{album_id_sp}/tracks"
        headers = {**self.__get_resource_header(), 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()

    def get_track(self, track_id_sp, resource_type='tracks', version='v1'):
        url = f"{self.base_url}{version}/{resource_type}/{track_id_sp}"
        headers = {**self.__get_resource_header(), 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()


def main():
    spotify_object = Spotify('5bc548965f74488c9de9703cb3a34ebf', '330999281cdd4d029d3791e889048eaa')

    def get_track_info_duration(track_id):
        data = spotify_object.get_track(track_id)
        return data['duration_ms']

    def get_artist_genres(artist_id):
        data = spotify_object.get_artist(artist_id)
        return data['genres']

    def get_album_tracks(album_id):
        result = []
        data = spotify_object.get_album_tracks(album_id)
        for item in data['items']:
            result.append({
                'track_name': item['name'].replace("'", '"'),
                'spotify_id': item['id'],
                'duration': get_track_info_duration(item['id'])
            })

        return result

    def get_info_for_bd():
        result = []
        data = spotify_object.get_saved_albums()
        albums_list = data['items']
        for item in albums_list:
            result.append({'name_album': item['album']['name'].rstrip("'"),
                           'album_id_sp': item['album']['id'],
                           'release_date': item['album']['release_date'],
                           'artist_name': item['album']['artists'][0]['name'],
                           'artist_id_sp': item['album']['artists'][0]['id'],
                           'artist_genres': get_artist_genres(item['album']['artists'][0]['id']),
                           'album_tracks': get_album_tracks(item['album']['id'])
                           })
        return result

    return get_info_for_bd()
