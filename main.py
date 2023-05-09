import json
import os.path
from datetime import datetime
from pprint import pprint
from ya_disk import YandexDisk


import requests

print("Начало работы")
print('Формирую запрос')

with open('vk_token.txt', 'r', encoding='utf-8') as t1:
    vk_token = t1.read().strip()
with open('ya_token.txt', 'r', encoding='utf-8') as t1:
    ya = YandexDisk(t1.read().strip())
# us_id = int(input('Укажите Id пользователя\n').strip())
with open('Us_id.txt', 'r', encoding='utf-8') as t1:
    us_id = t1.read().strip()

URL = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': us_id,
    'access_token': vk_token,
    'album_id': 'wall',
    'count': 5,
    'extended': '1',
    # 'photo_sizes': '1',
    'v': '5.131'
}
print('Выполняю запрос')

res = requests.get(URL, params=params)
photos_dict = res.json()




def max_size(sizes):
    max_height = 0
    url = ''
    type_jpg = ''
    for size in sizes:
        if size['height'] > max_height:
            max_height = size['height']
            url = size['url']
            type_jpg = size['type']
    return url, type_jpg


count_photo = photos_dict['response']['count']

if count_photo == 0:
    print('Фотографии не найдены')
    exit()

photos_items = photos_dict['response']['items']
json_file = []
progress = 0
for photo in photos_items:
    name_file = str(photo['likes']['count'])
    if os.path.exists(r'photos/' + name_file+'.jpg'):
        name_file += '_' + datetime.fromtimestamp(photo['date']).strftime('%Y-%m-%d')
    name_file += '.jpg'
    url_req, typ_jpg = max_size(photo['sizes'])
    # print(url_req)
    with open(r'photos/' + name_file, 'wb') as file_photo:
        response = requests.get(url_req)
        file_photo.write(response.content)
    ya.upload_file_to_disk('KURS/' + name_file, r'photos/' + name_file)

    json_file.append({'file_name': name_file, 'size': typ_jpg})
    progress += 1
    print(f'Загружено {progress} из {count_photo} фотографий - {name_file}')
# pprint(json_file)

with open('photos.json', 'w') as f_json:
    json.dump(json_file, f_json, ensure_ascii=False, indent=2)

print('Работа успешно окончена')
