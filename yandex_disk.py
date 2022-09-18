# В данной программе не реализована обработка всех возможных ошибок, например,
# при вводе не существующего пути или имени файла

import requests
from pprint import pprint
import os.path
import getpass


def set_headers(token):
    """
    Формирует словарь заголовков, которые будут передаваться в HTTP-запросе
    :param token: получает токен для авторизации в яндекс.диске
    :return: Сформированный словарь с заголовками
    """
    headers_dict = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }
    return headers_dict


def set_params(action):
    """
    Формирует словарь параметров, которые будут передаваться в HTTP-запросе
    :param Получает словарь действия, в котором могут содержаться необходимые параметры
    :return: Сформированный словарь с заголовками
    """
    params_dict = {}

    params_dict['path'] = action.get('path')
    params_dict['href'] = action.get('href')
    params_dict['overwrite'] = action.get('overwrite')

    if params_dict:
        return params_dict
    else:
        return


def set_url(action):
    """
    Берет добавочную строку из словаря действий и формирует строку URL для HTTP-запроса
    :return: строка URL
    """
    main_url = 'https://cloud-api.yandex.net/v1/disk'
    url = main_url + action['url_suff']

    return url


def init_actions_list():
    """
    Создает список возможных действий для использования при формировании http-запросов
    :return: список возможных действий
    """

    actions_list = [
        {'id': 1, 'name': 'Получить информацию о папке или файле', 'url_suff': '/resources', 'method': 'GET',
         'path': ''},
        {'id': 2, 'name': 'Создать папку', 'url_suff': '/resources', 'method': 'PUT', 'path': ''},
        {'id': 3, 'name': 'Загрузить файл', 'url_suff': '/resources/upload', 'method': 'PUT', 'path': ''},
        {'id': 4, 'name': 'Получить ссылку для загрузки файла', 'url_suff': '/resources/upload', 'method': 'GET',
         'path': ''}
    ]

    return actions_list


def choose_action(actions_list):
    """
    Получает список возможных действий
    Спрашивает у пользователя какое из действий следует выполнить
    :return: Словарь для формирования HTTP-запросов
    """
    print('Доступные для выполнения действия:')
    for action in actions_list:
        if action['id'] != 4:
            print(f'{action["id"]} - {action["name"]}')
    action_id = int(input('Введите номер действия, которое нужно выполнить '))

    if action_id == 1:
        selected_action = actions_list[action_id - 1]
        selected_action['path'] = input('Введите путь к папке или файлу, информацию о которых вы хотите получить: ')
        return selected_action
    elif action_id == 2:
        selected_action = actions_list[action_id - 1]
        selected_action['path'] = input('Введите путь к папке, которую вы хотите создать: ')
        return selected_action
    elif action_id == 3:
        selected_action = actions_list[action_id - 1:]
        path_to_upload = input('Введите путь к файлу, который вы хотите загрузить: ')

        if os.path.isfile(os.path.abspath(path_to_upload)) and os.path.exists(os.path.abspath(path_to_upload)):
            filename_to_upload = os.path.basename(os.path.abspath(path_to_upload))
            path_on_disk_for_upload = input('Введите путь на диске, куда хотите загрузить файл \n'
                                            '(для корневого каталога ничего вводить не надо): '
                                            '') + '/' + filename_to_upload
            selected_action[1]['path'] = path_on_disk_for_upload
            selected_action[1]['overwrite'] = 'true'

            get_href_for_upload = run_request(selected_action[1], TOKEN)

            selected_action[0]['href'] = get_href_for_upload.json().get('href')
            selected_action[0]['file_to_upload'] = path_to_upload

            return selected_action[0]

        else:
            print('Ошибка в пути и/или такого файла не существует')


def run_request(action, TOKEN):
    """
    Формирует и выполняет HTTP-запрос
    :param action: словарь действия, в котором содержится информация для формирования запроса
    :param TOKEN: токен для авторизации
    :return: полученный объект
    """

    headers = set_headers(TOKEN)
    params = set_params(action)
    url = set_url(action)

    if action['method'].lower() == 'get':
        resp = requests.get(url, headers=headers, params=params, timeout=10)

    if action['method'].lower() == 'put' and action['id'] != 3:
        resp = requests.put(url, headers=headers, params=params, timeout=10)

    elif action['method'].lower() == 'put' and action['id'] == 3:
        resp = requests.put(action['href'], data=open(action['file_to_upload'], 'rb'))

    return resp


if __name__ == '__main__':

    TOKEN = getpass.getpass('Введите токен ')

    main_action = choose_action(init_actions_list())
    main_resp = run_request(main_action, TOKEN)

    print(main_resp)

    if main_action['id'] == 1:
        pprint(main_resp.json())


