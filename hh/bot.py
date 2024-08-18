from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
from json.decoder import JSONDecodeError

from main import fetch_vacancies, data_validation

import logging



logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

bot_token = "6356352622:AAG-fcDuCODAmcQUeRxk4Lb0KOHXM4SKfQY"


bot = Bot(bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    ts = message.date.strftime('%Y.%m.%d %H:%M:%S')
    print(f"Имя пользователя {message.from_user.first_name}, ник {message.from_user.username}, "
          f"и его id {message.from_user.id}\n" 
          f"Время {ts}, сообщение {message.text}")
    await message.reply(
        f'Привет {message.from_user.first_name}! Чтобы получить информацию по вакансиям введите имя города'
        f' или страны')


# Словарь для хранения ответов пользователя
user_data = {}

# Клавиатура с уровнями образования
education_kb = ReplyKeyboardMarkup(resize_keyboard=True)
education_kb.add(KeyboardButton('Среднее'))
education_kb.add(KeyboardButton('Среднее специальное'))
education_kb.add(KeyboardButton('Высшее'))

# Клавиатура с опытом работы
experience_kb = ReplyKeyboardMarkup(resize_keyboard=True)
experience_kb.add(KeyboardButton('Без опыта'))
experience_kb.add(KeyboardButton('От 1 до 3 лет'))
experience_kb.add(KeyboardButton('От 3 до 6 лет'))
experience_kb.add(KeyboardButton('Больше 6 лет'))

# Клавиатура с конечным выбором
final_kb = ReplyKeyboardMarkup(resize_keyboard=True)
final_kb.add(KeyboardButton('Да'))
final_kb.add(KeyboardButton('Нет'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Введите любой текст, чтобы начать.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(
    lambda message: message.text not in ["Назад", "Да", "Нет", "Среднее", "Среднее специальное", "Высшее", "Без опыта",
                                         "От 1 до 3 лет", "От 3 до 6 лет", "Больше 6 лет"])
async def ask_education(message: types.Message):
    user_data[message.from_user.id] = {'text': message.text}
    await message.reply("Выберите уровень образования:", reply_markup=education_kb)


@dp.message_handler(lambda message: message.text in ["Среднее", "Среднее специальное", "Высшее"])
async def ask_experience(message: types.Message):
    user_data[message.from_user.id]['education'] = message.text
    await message.reply("Выберите ваш опыт работы:", reply_markup=experience_kb)


@dp.message_handler(lambda message: message.text in ["Без опыта", "От 1 до 3 лет", "От 3 до 6 лет", "Больше 6 лет"])
async def final_question(message: types.Message):
    user_data[message.from_user.id]['experience'] = message.text
    await message.reply("Доступно людям с инвалидностью?", reply_markup=final_kb)


@dp.message_handler(text=['Да', 'Нет'])
async def complete(message: types.Message):
    file_name = message.from_user.id
    user_data[file_name]['disability'] = message.text
    data_validation(user_data)
    with open(f'vacancies/{message.from_user.id}.xlsx', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f"Файл вакансий для параметров:\n"
                                                               f"Город: {user_data[file_name]['text']}\n"
                                                               f"Образование: {user_data[file_name]['education']}\n"
                                                               f"Опыт работы: {user_data[file_name]['experience']}\n"
                                                               f"Доступно людям с инвалидностью?: {user_data[file_name]['disability']}\n"
                                                               "",
                                reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    executor.start_polling(dp)
