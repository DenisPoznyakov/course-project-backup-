import requests
from pprint import pprint
import os
import json

TOKEN_VK = ''
TOKEN_YA = ''

def create_json():
    json_data = [
    ]
    with open('log.json', 'w') as file:
        file.write(json.dumps(json_data, indent=2, ensure_ascii=True))

create_json()

def add_to_json(par_1, par_2):
    json_data = {
        par_1: par_2
    }
    data = json.load(open("log.json"))
    data.append(json_data)
    with open("log.json", "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)

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
        if not os.path.exists('backup photos VK'):
            os.mkdir('backup photos VK')
            add_to_json('backup photos VK', 'a folder has been created on the local disk')
        max_size_photo = {}
        params = self.get_common_params_vk()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': '1'})
        response = requests.get(f'{self.API_BASE_URL_VK}/photos.get', params=params)
        for photo in response.json()['response']['items']:
            max_size = 0
            for size in photo['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
                    if photo['likes']['count'] not in max_size_photo.keys():
                        max_size_photo[photo['likes']['count']] = size['url']
                    else:
                        max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = size['url']
        for photo_name, photo_url in max_size_photo.items():
            with open('backup photos VK/%s' % f'{photo_name}.jpg', 'wb') as file:
                img = requests.get(photo_url)
                file.write(img.content)
                add_to_json(photo_name, 'downloaded to local disk')

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
        add_to_json('backup photos VK', 'a folder has been created on Yandex Disk')

    def upload(self, file_path: str):
        url = self.API_BASE_URL_YA + '/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                    'Authorization': TOKEN_YA}
        params = {'path': f'backup photos VK/{file_name}',
                    'overwrite': 'true'}

        response = requests.get(url=url, headers=headers, params=params)
        href = response.json().get('href')

        uploader = requests.put(href, data=open(files_path, 'rb'))

if __name__ == '__main__':
    vk_client = VK(TOKEN_VK, 151422792)
    photos_info = vk_client.get_profile_photos()
    pprint(photos_info)
    ya_client = YA(TOKEN_YA)
    ya_client.folder_creation()

    photos_list = os.listdir('backup photos VK')
    for photo in photos_list:
        file_name = photo
        files_path = os.getcwd() + r'\backup photos VK\\' + photo
        result = ya_client.upload(files_path)
        add_to_json(photo, 'uploaded to Yandex Disk')