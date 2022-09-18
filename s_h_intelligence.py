import requests


def get_s_h_list_from_url():
    """
    Делает запрос get по заданной url
    Получает данные в виде списка словарей
    :return: возвращает список словарей с характеристиками супергероев
    """

    url = 'https://akabab.github.io/superhero-api/api/all.json'
    resp = requests.get(url, timeout=10)

    return resp.json()


def find_most_int_s_h(s_h_list, s_h_names):
    """
    Из полученных на вход списка супергероев и списка имен супергероев формирует новый список по полученным именам
    и коэффициенту интеллекта из общего списка
    Потом сортирует список по коэффициенту в обратном порядке и выводит имя первого супергероя из списка,
    у этого супергероя будет максимальный коэффициент интеллекта
    :param s_h_list: список супергероев со всеми характеристиками
    :param s_h_names: список имен супергероев, которых надо сравнить по коэффициенту интеллекта
    :return: ничего не возвращает
    """

    s_h_int_list = sorted([[item['name'], item['powerstats']['intelligence']] for item in s_h_list
                           for name in s_h_names if item['name'] == name], key=lambda hero: hero[1], reverse=True)

    print()
    print(f'Самый умный из {", ".join(s_h_names)} - это {s_h_int_list[0][0]}')


if __name__ == '__main__':

    find_most_int_s_h(get_s_h_list_from_url(), ['Hulk', 'Captain America', 'Thanos'])

