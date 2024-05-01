import requests
import json
import configparser
from pprint import pprint
from tqdm import tqdm
from datetime import datetime


def get_token_vk():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    token = str(config['VK']['token'])
    return token


def get_user_id_vk():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    user_id = config['VK']['id']
    return user_id


def get_token_yd():
    config_ = configparser.ConfigParser()
    config_.read('settings.ini')
    token_yd = str(config_['YD']['token_yd'])
    return token_yd


class VK:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'owner_id': 89673611,
            'access_token': self.token,
            'v': '5.199'
        }

    def get_album(self):

        """Выбираем альбом"""

        params = self.get_common_params()
        response = requests.get(f'{self.API_BASE_URL}/photos.getAlbums', params=params)
        res = response.json()['response']['items']

        albums_dict = {}
        for i in res:
            albums_dict[i['id']] = i['title']
        dict_ = {}
        for index, title in enumerate(albums_dict.values()):
            dict_[index + 1] = title
        pprint(dict_)
        user_input = int(input('Введите номер альбома:\n'))
        for key, value in dict_.items():
            if user_input == key:
                res = dict_[user_input]
        for id_album, title in albums_dict.items():
            if res == title:
                return id_album

    def get_photos(self, album_id):

        """Получаем фото"""

        photo_count = int(input('Введите количество фото для загрузки\n'))
        params = self.get_common_params()
        params.update({'album_id': album_id,
                       'extended': 1
                       })
        response = requests.get(f'{self.API_BASE_URL}/photos.get', params=params)
        photos_data = response.json().get('response').get('items')

        sizes_dict = {}
        for item in photos_data:
            max_size = 0
            for photo in item['sizes']:
                if photo['height'] != 0:
                    photo_size = photo['width'] * photo['height']
                else:
                    photo_size = 0
                if photo_size > max_size:
                    photo_date = datetime.fromtimestamp(int(item['date'])).strftime('%Y-%m-%d')
                    sizes_dict[item['id']] = [photo_size, item['likes']['count'], photo['url'], photo_date,
                                              photo['type']]

        sorted_dict = sorted(sizes_dict.values(), reverse=True)

        if photo_count > response.json()['response']['count']:
            print('Error')
        photos = sorted_dict[:photo_count]

        info_dict = []
        photos_for_upload = {}

        with open('info.json', 'w') as f:
            for photo in photos:
                photo[1] = str(f'{photo[1]}.jpg')
                if photo[1] in photos_for_upload:
                    photo[1] += f'_{photo[3]}.jpg'
                photos_for_upload[photo[1]] = photo[2]

                info_dict.append({
                    'file_name': photo[1],
                    'size': photo[4]
                })
            json.dump(info_dict, f, indent=2)

        return photos_for_upload


class YD:
    URL_YD = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token_yd, photos_dict):
        self.token_yd = token_yd
        self.photos_dict = photos_dict
        self.headers = {'Authorization': f'OAuth {self.token_yd}'}

    def load_photos(self):

        """Создаем папку"""

        folder_name = input('Введите имя папки:\n')

        params = {
            'path': folder_name
        }
        resp = requests.put(self.URL_YD, params=params, headers=self.headers)
        if resp.status_code == 201:
            print("Папка создана")
        else:
            print("Error")

        """Загружаем файлы"""

        for name, url in tqdm(self.photos_dict.items()):
            params = {
                'url': url,
                'path': f'{folder_name}/{name}'
            }
            resp = requests.post(f'{self.URL_YD}/upload', params=params, headers=self.headers)
        if resp.status_code == 202:
            print("Загрузка успешно завершена")


if __name__ == '__main__':
    vk_client = VK(get_token_vk(), get_user_id_vk())
    yandex_disk = YD(get_token_yd(), vk_client.get_photos(vk_client.get_album()))
    yandex_disk.load_photos()
