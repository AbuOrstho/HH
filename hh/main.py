import requests
import json

from xlsx_save import save_file


def fetch_vacancies(file_name, city_id=None, education_level=None, experience=None, is_for_disabled=None, page=19,
                    per_page=100):
    """
    Получает список вакансий по заданным критериям из API HH.ru и сохраняем их в виде json файла.
    Каждый элемент списка содержит информацию о вакансии, включая название, работодателя, ссылку,
    контактный email и телефон (если доступны).

    :param file_name: str - Имя файла для сохранения.
    :param city_id: str - Идентификатор города в системе HH.ru, определяющий географическую область поиска.
    :param education_level: str - Требуемый уровень образования для вакансии ('secondary', 'special_secondary', 'higher').
    :param experience: str - Требуемый опыт работы кандидатов ('noExperience', 'between1And3', 'between3And6', 'moreThan6').
    :param is_for_disabled: bool - Должны ли вакансии быть доступны для людей с инвалидностью. True - доступны, False - нет.
    :param page: int - Номер страницы результатов поиска (начиная с 0).
    :param per_page: int - Количество вакансий на странице (максимальное количество элементов на странице).

    :return: json - Сохраняет в файл всю необходимую информацию
    """

    url = "https://api.hh.ru/vacancies"
    params = {
        "area": city_id,
        "education_level": education_level,
        "experience": experience,
        "order_by": "publication_time",
        "per_page": per_page,
        "page": page,
        "is_for_disabled": is_for_disabled
    }

    response = requests.get(url, params=params)
    print(response.url)
    vacancies = response.json()
    with open(f"files/{file_name}.json", 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в файл")
    result = []


def data_validation(user_data):
    dict_education_level = {
        'Среднее': 'secondary',
        'Среднее специальное': 'special_secondary',
        'Высшее': 'higher',
    }
    dict_experience = {
        'Без опыта': 'noExperience',
        'От 1 до 3 лет': 'between1And3',
        'От 3 до 6 лет': 'between3And6',
        'Больше 6 лет': 'moreThan6',
    }
    dick_is_for_disabled = {
        'Да': True,
        'Нет': False,
    }

    file_name = list(user_data.keys())[0]
    print(file_name)
    city_id = ''
    education_level = dict_education_level[user_data[file_name]['education']]
    experience = dict_experience[user_data[file_name]['experience']]
    is_for_disabled = dick_is_for_disabled[user_data[file_name]['disability']]

    json_file = json.load(open('cities.json', 'r', encoding='UTF-8'))
    name_to_id = {value: key for value, key in json_file.items()}

    if user_data[file_name]['text'] in name_to_id.values():
        print(1)
        city_id = name_to_id.get(city_id, None)

    print(
        file_name,
        city_id,
        education_level,
        experience,
        is_for_disabled)

    fetch_vacancies(file_name=str(file_name),
                    city_id=city_id,
                    education_level=education_level,
                    experience=experience,
                    is_for_disabled=is_for_disabled)
    save_file(str(file_name))


