import json
import pandas as pd


def save_file(file_name):
    with open(f'files/{file_name}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    extracted_data = []

    for job in data['items']:
        name = job['name']
        employer_name = job['employer']['name']
        url = job['alternate_url']

        email = None
        phone = None
        if 'contacts' in job and job['contacts'] is not None:
            email = job['contacts'].get('email')
            phone = job['contacts'].get('phone')

        extracted_data.append({
            'Название вакансии': name,
            'Название работодателя': employer_name,
            'Ссылка на объявление': url,
            'Почта контакта': email,
            'Телефон контакта': phone
        })

    df = pd.DataFrame(extracted_data)

    df.to_excel(f'vacancies/{file_name}.xlsx', index=False, engine='openpyxl')