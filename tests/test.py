import argparse

import requests
from sys import argv


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default='https://vk-images.herokuapp.com/')
    parser.add_argument('-p', '--port', default='')
    return parser


# Получаем данные из аргументов
args_parser = createParser()
namespace = args_parser.parse_args(argv[1:])

SERVICE_URL = namespace.url
SERVICE_PORT = namespace.port


def _get_request_url():
    # Указываем url
    if SERVICE_URL[-1] == '/':
        request_url = SERVICE_URL[:-1]
    else:
        request_url = SERVICE_URL
    # Добавляем port
    if SERVICE_PORT:
        request_url += f':{SERVICE_PORT}'

    return request_url


def post_request():
    # Формируем url для post запроса
    url = _get_request_url() + '/api/upload/'
    # Добавляем файл в запрос
    files = {'image': open('tests/test.jpeg', 'rb')}
    # Отправляем запрос
    response = requests.post(url, files=files)
    return response.json()


def get_request(image_id):
    # Формируем url для get запроса
    url = _get_request_url() + '/api/get/'
    # Добавляем id в параметры запрос
    params = {'id': image_id}
    # Отправляем запрос
    response = requests.get(url, params=params)
    return response


# Отправляем post запрос
image_upload = post_request()
# Если в ответе есть id
if image_upload.get('id'):
    image_get = get_request(image_upload.get('id'))
    if image_get.status_code == 200:
        print(f'Изображение: {image_get.url}')
    else:
        print('Неверно указан идентификатор изображения!')
else:
    print('Ошибка при загрузке изображения на сервер!')
