import requests
from pprint import pprint
from urllib.parse import urlencode

TOKEN_VK = 'vk1.a.EsVK4t3jGAAYz1i84jpMnj0DuPN-GQ6j77mK9jXIx4fvl0YOt9We6I_dlXYa0JHrtsafkz5SQXxdzb6akBeWi3SoePAXiVamT3QtitVmOefahsLt9yIukTxpMu25X6a1KcjWsre_ZUNlbglJlFwT1_w7AQjRDBapsEqXpauo-Nu7CTSlEc8qScGnqr4DXG1fEZmO6L1EZ46nYtVyQPzWQA'
TOKEN_YA = 'OAuth y0_AgAAAAAbF_21AADLWwAAAADyrrtr6Xg3WBLMSjqjbfp_kikw3TPLVbs'

class VK:

    API_BASE_URL_VK = 'https://api.vk.com/method'

    def __init__(self, token_vk, user_id_vk):
        self.token_vk = token_vk
        self.user_id = user_id_vk

    def get_common_params_vk(self):
        return {
            'access_token': self.token_vk,
            'v': '5.131'
        }

    def get_profile_photos(self):
        max_size_photo = {}
        params = self.get_common_params_vk()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': '1'})
        response = requests.get(f'{self.API_BASE_URL_VK}/photos.get', params=params)
        for photo in response.json()['response']['items']:
            max_size = 0
            # photos_info = {}
            for size in photo['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
                    if photo['likes']['count'] not in max_size_photo.keys():
                        max_size_photo[photo['likes']['count']] = size['url']
                        # photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                    else:
                        max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = size['url']
                        # photos_info['file_name'] = f"{photo['likes']['count']}+{photo['date']}.jpg"
        return max_size_photo

class YA:

    API_BASE_URL_YA = 'https://cloud-api.yandex.net'

    def __init__(self, token_ya):
        self.token_ya = token_ya

    def folder_creation(self):
        url = self.API_BASE_URL_YA + '/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': TOKEN_YA}
        params = {'path': 'backup photos VK'}
        response = requests.put(url=url, headers=headers, params=params)

    def upload(self, file_path: str):
        url = self.API_BASE_URL_YA + '/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                    'Authorization': TOKEN_YA}
        params = {'path': f'backup photos VK/{file_name}',
                    'overwrite': 'true'}

        response = requests.get(url=url, headers=headers, params=params)
        href = response.json().get('href')

        for file in vk_client.get_profile_photos():
            uploader = requests.put(href, data=photos_info.values())

        # uploader = requests.put(href, data=open(files_path, 'rb'))

if __name__ == '__main__':
    vk_client = VK(TOKEN_VK, 151422792)
    photos_info = vk_client.get_profile_photos()
    pprint(photos_info)
    ya_client = YA(TOKEN_YA)
    ya_client.folder_creation()

    for photo in photos_info:
        file_name = photos_info.keys()
        files_path = photos_info.values()
        # result = ya_client.upload(files_path)
        # print(f'Фотография {photos_info.keys()} загружена на Яндекс диск')
        # print(photos_info.keys())