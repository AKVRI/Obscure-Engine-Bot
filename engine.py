import telebot
import os
import sys
import random
from telebot import types
import time
import datetime
import subprocess
import requests
import json
import bs4
import threading
import re
from concurrent.futures import ThreadPoolExecutor

token = input('Токен: ')
bot = telebot.TeleBot(token)
SERVER_FOLDER = "server"
owner_id = int(input('ID хоста: '))
feedback = input('Юзернейм хоста или ссылка на профиль создателя: ')
print('Online')
user_states = {}
msg = ['Класс!',
       "Восхитительно!",
       "Крутышка)",
       "Потрясно!",
       "Молодчик)",
       "Ай, тигр",
       "Хорош",
       "Обожаю тебя!",
       "Красавчик!",
       "Держи",
       "Заработал",
       "Заслужил",
       "Радуешь)",
       "Вкусно)",
       "+вайб",
       "WWW",
       "👍👍👍",
       "Любимчик мой)",
       "Умничка",
       "Зверь",
       "Ням))",
       "Воть))",
       "Ты моя няшечка"]
poxvala_sticker = ['CAACAgIAAxkBAAENcahneRPJkY5-91dgyl6lr4J74-vL1gAClQ4AAn5ZsEhgAoeI2KwG7DYE',
                   'CAACAgIAAxkBAAENcbBneRlTgt6qPD2h4rHEZpvyj2TUbQACCg8AAk0asEjI15EXWF4YAjYE',
                   'CAACAgIAAxkBAAENcbJneRlkEDhC2A5VcGGP9yYWG3YQ3wACXRAAAjxhuEgZL3SNWga-szYE',
                   'CAACAgIAAxkBAAENcbRneRmUogsSBHNY8du5lttPf8TsHwACFhEAApmQuUiHWCroqnrwLTYE',
                   'CAACAgIAAxkBAAENcbZneRmiLs75ymnxwO-Uk4ifEBJUQAACVBMAAizTsUjkeE8ecGWFeTYE',
                   'CAACAgIAAxkBAAENcbhneRm0NWw1w5rfXwvAKec_7293VwACMBAAAiIVsUiXHAZ5ELI3nzYE',
                   'CAACAgIAAxkBAAENcbxneRnPU0eC8P1oyTsR_mowTAJVHgACVQ8AAuZxsEgGLY3e_ozgDjYE',
                   'CAACAgIAAxkBAAENcZlneRHV2SezS2sjd42laq1WpJ5SHgACdhMAAkQosEiQP6XGsWjHIzYE',
                   'CAACAgIAAxkBAAENccBneRoGTgXrFRrAA9jL5a_vjn2ijwADDQACSeqxSK64o_7HGLBKNgQ',
                   'CAACAgIAAxkBAAENccJneRoZ7GCgh1E9HHHaPik7UzjcegACDhAAAjKPuEhvodzj31eewjYE',
                   'CAACAgIAAxkBAAENccRneRoxqWtQA5TPS_zWZadgE_bXVwAC8hEAAgsSuUjGEEWdLi6rojYE',
                   'CAACAgIAAxkBAAENcZdneRHQq0V3xj6Fu7T9-MHmBJgOyAACYhEAAhd8sUhcpXuorJ8UMDYE',
                   'CAACAgIAAxkBAAENcelneSyAK2biZCkTENcd3jvNolthPwACpBAAAh07uUiDm-oHa_eVjTYE',
                   'CAACAgIAAxkBAAENcjJneV4Wyf4IJe56HIaK3ns_AAFFkyYAAkAQAALT7LhI0HcI7PH-fHs2BA']
user_last_send_time = {}
active_searches = {}
tip_msg = ['Завари кофеек, это похоже надолго ☕',
           'Логи, логи, данные...',
           'Пока я ищу, можешь заняться своими делами...',
           'Как жизнь?)',
           "Я сразу напишу как что найду",
           "Считаешь себя доксером? А кто еще так считает?",
           "Иди поделай уроки пока)",
           "Мда, это происходит намного дольше чем обычно"]

def check_user_id(user_id):
    try:
        with open('server/obscure-db.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if str(user_id) in line:
                    return True
    except FileNotFoundError:
        pass
    return False

def check_contact_exists(phone):
    try:
        with open('server/obscure-db.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if f'{phone}' in line:
                    return True
    except FileNotFoundError:
        pass
    return False

def check_premium_status(user_id):
    try:
        with open('premium.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if str(user_id) in line:
                    return "👑 True"
    except FileNotFoundError:
        pass
    return "None"

def get_balance(user_id):
    try:
        with open('user_balance.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if str(user_id) in line:
                    return int(line.split()[1])
    except FileNotFoundError:
        pass
    return 0

def update_balance(user_id, balance):
    try:
        with open('user_balance.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    with open('user_balance.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            if str(user_id) in line:
                file.write(f'{user_id} {balance}\n')
            else:
                file.write(line)
        if not any(str(user_id) in line for line in lines):
            file.write(f'{user_id} {balance}\n')

def is_user_banned(user_id):
    try:
        with open('banned.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if str(user_id) in line:
                    return True
    except FileNotFoundError:
        pass
    return False

def check_exceptions(query):
    try:
        with open('exceptions.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if str(query) in line:
                    return True
    except FileNotFoundError:
        pass
    return False

@bot.message_handler(commands=['fr'])
def balance_message(message):
    user_id = message.from_user.id
    global owner_id
    if user_id == owner_id:
        bot.send_message(message.from_user.id, '╒')
        bot.send_message(message.from_user.id, '╞')
        bot.send_message(message.from_user.id, '╘')
    else:
        return
    
@bot.message_handler(commands=['balance'])
def balance_message(message):
    user_id = message.from_user.id
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Прости, но твой баланс был обнулен.')
        return
    if not check_user_id(user_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Твои возможности ограничены. Нажми на кнопку ниже чтобы получить доступ к базе.', reply_markup=markup)
    balance = get_balance(user_id)
    bot.send_message(message.from_user.id, f'ID: {user_id}\nБаланс: {balance}⭐')

def send_query(query, user_id):
    global tip_msg
    start_time = time.time()
    balance = get_balance(user_id)
    cost_per_match = 2

    if balance < cost_per_match:
        bot.send_message(chat_id=user_id, text="😢 Недостаточно средств.")
        sticker_id = "CAACAgIAAxkBAAENcdhneSNs7mRxDaonQe66OYtXpr14uwACdxAAAjYxuUipiV8LHjyI8zYE"
        bot.send_sticker(user_id, sticker_id)
        return

    if len(query) < 6:
        bot.send_message(chat_id=user_id, text="🚫 Ошибка: запрос должен содержать не менее 6 символов.")
        sticker_id = "CAACAgIAAxkBAAENcclneRq0vz6p1AvCnFNZ6R2252Im7wACGREAArsyuUi7Sgs7Em4O8DYE"
        bot.send_sticker(user_id, sticker_id)
        return

    if check_exceptions(query):
        bot.send_message(chat_id=user_id, text="🛑 По неким причинам я не могу предоставить данные по твоему запросу.")
        sticker_id = "CAACAgIAAxkBAAENcYtneRBIIejqzFnhsKyOYlhCQEHH3QACZQ8AAm8QsUjWO5BQXrE91jYE"
        bot.send_sticker(user_id, sticker_id)
        return

    results, media_results = search_files(query, user_id)

    if not results and not media_results:
        bot.send_message(chat_id=user_id, text="🙈 Ничего не найдено.")
        sticker_id = "CAACAgIAAxkBAAENcYtneRBIIejqzFnhsKyOYlhCQEHH3QACZQ8AAm8QsUjWO5BQXrE91jYE"
        bot.send_sticker(user_id, sticker_id)
        return

    max_matches = min(balance // cost_per_match, len(results) + len(media_results))
    bot.send_message(chat_id=user_id, text=f"👁️ Найдено совпадений: {max_matches}")

    # Отправка текстовых совпадений
    for i in range(min(max_matches, len(results))):
        result = results[i]
        parts = re.split(r'[/|]', result['line_content'])
        formatted_line = '\n'.join(parts)
        max_length = 4000
        if len(formatted_line) > max_length:
            chunks = [formatted_line[i:i + max_length] for i in range(0, len(formatted_line), max_length)]
            for chunk in chunks:
                bot.send_message(
                    chat_id=user_id,
                    text=f"╒ File: {result['file']}\n╞ Path: {result['path']}\n╞ Line: {result['line_number']}\n╘ Content (chunk):\n\n{chunk}"
                )
                time.sleep(1)
        else:
            bot.send_message(
                chat_id=user_id,
                text=f"╒ File: {result['file']}\n╞ Path: {result['path']}\n╞ Line: {result['line_number']}\n╘ Content:\n\n{formatted_line}"
            )
            time.sleep(1)

    # Отправка медиафайлов
    for i in range(max_matches - len(results)):
        if i < len(media_results):
            file_path = media_results[i]
            file_name = os.path.basename(file_path)  # Получаем имя файла
            file_info_message = f"╒ File: {file_name}\n╞ Path: {file_path}\n╘ Sending media file..."

            # Отправляем информацию о медиафайле
            bot.send_message(chat_id=user_id, text=file_info_message)

            # Отправляем сам медиафайл
            try:
                if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    with open(file_path, 'rb') as photo:
                        bot.send_photo(chat_id=user_id, photo=photo)
                elif file_path.lower().endswith(('.mp4', '.avi')):
                    with open(file_path, 'rb') as video:
                        bot.send_video(chat_id=user_id, video=video)
                elif file_path.lower().endswith(('.mp3', '.wav')):
                    with open(file_path, 'rb') as audio:
                        bot.send_audio(chat_id=user_id, audio=audio)

                time.sleep(1)  # Задержка между отправками
            except Exception as e:
                print(f"Ошибка при отправке файла {file_path}: {e}")

    reduce = max_matches * cost_per_match
    update_balance(user_id, balance - reduce)
    bot.send_message(user_id, f"Списание -{reduce}⭐")
    sticker_id = "CAACAgIAAxkBAAENcZNneRExyAE0-4rlmTSxScNqowqU5wACOQ4AAqC4uEhG_YXC59BTIzYE"
    bot.send_sticker(user_id, sticker_id)

def search_files(query, user_id):
    results = []
    media_results = []
    encodings = ['utf-8', 'latin-1', 'cp1252']
    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mp3', '.wav']

    # Поиск в текстовых файлах
    for root, dirs, files in os.walk(SERVER_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            # Проверяем текстовые файлы
            if file.lower().endswith(('.txt', '.log', '.csv', '.doc', '.docx', '.xlsx', '.json', '.svb')):  # Добавьте нужные расширения
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            for line_number, line in enumerate(f, start=1):
                                if query.lower() in line.lower():
                                    results.append({
                                        "file": file,
                                        "path": file_path,
                                        "line_number": line_number,
                                        "line_content": line.strip()
                                    })
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"😵 ReadFileError {file_path}: {e}")
                        break

            # Проверяем медиафайлы
            if query.lower() in file.lower() and any(file.lower().endswith(ext) for ext in media_extensions):
                media_results.append(file_path)

    return results, media_results

@bot.message_handler(commands=['help'])
def help_message(message):
    global feedback
    user_id = message.from_user.id
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Помощь? А она тебе поможет?')
        return
    if not check_user_id(user_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Чтобы получить доступ к базе, мне необходимо тебя узнать.', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcY1neRCfWAQbnZVbh8w_DAMyCUoAATkAAjsOAAL8KrhIGj-4RJJg-Qc2BA"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    bot.send_message(message.from_user.id, f'''
🔍 Примеры поиска:
Номер телефона - 79002004505
Айпи адрес - 0.0.0.0
Телеграм айди - 1234567890
Имя - Алишер
Юзернейм - @example_username
Номер карты - 1234567887654321

🎫 Услуги:
Совпадение по Глобальному поиску -2⭐
IPGeoLocation тул -1⭐
Скрыть данные -329⭐

⛏️ Майнинг:
Контакт +8⭐
Прочая валид информация +10⭐ ~ +100⭐
👁️‍🗨️ Обладатели Премиума мгновенно получат 500⭐

❕ Любая поступающая информация проходит модерацию:
⚠️ Некачественная/Недостоверная информация без доков -5⭐
⛔ Если на модерацию поступает дерьмо - перманетный БАН.

По всем вопросам: {feedback}''')

@bot.message_handler(commands=['donate'])
def user_info_message(message):
    global feedback
    user_id = message.from_user.id
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Собираешься купить разбан?')
        return
    if not check_user_id(user_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Может для начала узнаем друг друга?', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcY1neRCfWAQbnZVbh8w_DAMyCUoAATkAAjsOAAL8KrhIGj-4RJJg-Qc2BA"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    bot.send_message(message.from_user.id, f'По всем вопросам: {feedback}')
    
@bot.message_handler(commands=['my_info'])
def user_info_message(message):
    global owner_id
    user_id = message.from_user.id
    if not check_user_id(user_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Кто ты?', reply_markup=markup)
        return
    moders = []
    try:
        with open('moders.txt', 'r', encoding='utf-8') as file:
            for line in file:
                moders.append(int(line.strip()))
    except FileNotFoundError:
        pass
    if user_id == owner_id:
        status = 'owner'
    elif user_id in moders:
        status = 'moderator'
    else:
        status = 'user'
    if is_user_banned(user_id):
        status = 'BANNED'
        update_balance(user_id, 0)
    name = message.from_user.first_name
    balance = get_balance(user_id)
    premium_status = check_premium_status(user_id)
    bot.send_message(message.from_user.id, f'╒ Name: {name}\n╞ ID: {user_id}\n╞ Баланс: {balance}⭐\n╞ Status: {status}\n╘ Premium: {premium_status}')
    
@bot.message_handler(commands=['share'])
def share_message(message):
    user_id = message.from_user.id
    if active_searches.get(user_id, False):
        a = bot.send_message(message.from_user.id, "🔍 В данный момент уже производится активный поиск..")
        bot.pin_chat_message(user_id, a.message_id)
        sticker_id = "CAACAgIAAxkBAAENcaxneRcWxfLsPGhp0rxLGZmqrzpZXQACTA8AAig6sEiGytjCw_r7ZzYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Эта функция больше недоступна.')
        return
    if not check_user_id(user_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Пока у тебя нет доступа к базе.', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcY1neRCfWAQbnZVbh8w_DAMyCUoAATkAAjsOAAL8KrhIGj-4RJJg-Qc2BA"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    last_send_time = user_last_send_time.get(user_id, 0)
    current_time = time.time()
    if current_time - last_send_time < 86400:
        remaining_time = int(86400 - (current_time - last_send_time))
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        bot.send_message(message.from_user.id, f"Внести информацию в базу можно снова через {hours} часов {minutes} минут.")
        sticker_id = "CAACAgIAAxkBAAENcY9neRDQFNwTEZff3YcUd0S8rdcp0QACRxAAApAxsEgpkCt5BkG2ujYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    user_states[user_id] = True
    bot.send_message(message.from_user.id, 'Предоставь всю имеющуюся информацию одним сообщением (фотки, видео, документы, текст и т.д.)\nНаши модераторы проверят твою информацию, затем ты получишь соответственное сообщение.\nЧтобы выйти напиши аборт...')
    bot.register_next_step_handler(message, share_info)

@bot.message_handler(commands=['tools'])
def tool_message(message):
    user_id = message.from_user.id
    if active_searches.get(user_id, False):
        a = bot.send_message(message.from_user.id, "🔍 В данный момент уже производится активный поиск..")
        bot.pin_chat_message(user_id, a.message_id)
        sticker_id = "CAACAgIAAxkBAAENcaxneRcWxfLsPGhp0rxLGZmqrzpZXQACTA8AAig6sEiGytjCw_r7ZzYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Доступ запрещен.')
        return
    if not check_user_id(user_id):
        update_balance(user_id, 0)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Чтобы получить доступ к инструментам, необходимо зарегистрироваться.', reply_markup=markup)
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton(text="⚙️ IPGeoLocation")
    button2 = types.KeyboardButton(text="⚙️ Obscure Implementer")
    button3 = types.KeyboardButton(text="🥷 Стереть данные")
    button4 = types.KeyboardButton(text="🔙 Назад")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    toolmsg = bot.send_message(message.from_user.id, "🧰 Выбери инструмент:", reply_markup=markup)
    sticker_id = "CAACAgIAAxkBAAENcjZneV6Uhh1P5f8Kgcs_6GR6LZrW-QAC0RIAAlYquUhxtFuq2H_r5zYE"
    sticker = bot.send_sticker(message.from_user.id, sticker_id)
    bot.register_next_step_handler(message, tool_handler, toolmsg, sticker)
    
def tool_handler(message, toolmsg, sticker):
    global owner_id
    user_id = message.from_user.id
    balance = get_balance(user_id)
    bot.delete_message(user_id, toolmsg.message_id)
    bot.delete_message(user_id, sticker.message_id)
    if message.text == '⚙️ IPGeoLocation':
        if balance < 1:
            bot.send_message(chat_id=user_id, text="😢 Недостаточно средств.")
            sticker_id = "CAACAgIAAxkBAAENcdhneSNs7mRxDaonQe66OYtXpr14uwACdxAAAjYxuUipiV8LHjyI8zYE"
            bot.send_sticker(user_id, sticker_id)
            return
        bot.send_message(message.from_user.id, "⚙️ Выбран IPGeoLocation тул.\nЧтобы выйти напиши аборт...")
        bot.send_message(message.from_user.id, "Введи IP адрес:")
        bot.register_next_step_handler(message, ip_geo_location)
    elif message.text == '🔙 Назад':
        bot.send_message(message.from_user.id, '😊 Чтобы начать поиск, просто отправь мне запрос.')
        sticker_id = "CAACAgIAAxkBAAENcaJneRLeFucNm_UqGRrvO0rHNbTDdAACgxAAAv-IuEgmnSDE-AvTOTYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        if user_id == owner_id:
            bot.send_message(message.from_user.id, '''
OWNER PANEL
/give_ban - Выдать бан
/give_premium - Выдать премиум
/add_moder - Добавить модератора
/gift - Начислить звезды
/reduce - Списать звезды
/send_to_all - Рассылка
/add_string - Добавить строку в БД
/add_media - Добавить медиа в БД
/fr - Фреймы''')
    elif message.text == '⚙️ Obscure Implementer':
        msg = bot.send_message(message.from_user.id, "⚙️ Секунду...")
        file_path = 'Obscure-Implementer.zip'
        try:
            with open(file_path, 'rb') as file:
                bot.send_document(user_id, file, caption='https://github.com/AKVRI/Obscure-Implementer')
        except Exception as e:
            bot.send_message(message.from_user.id, "Проблема на сервере... Попробуй позже.")
        bot.delete_message(user_id, msg.message_id)    
    elif message.text == '🥷 Стереть данные':
        if balance < 329:
            bot.send_message(chat_id=user_id, text="😢 Недостаточно средств. Для скрытия данных необходимо 329⭐")
            sticker_id = "CAACAgIAAxkBAAENceBneSWhEyBzI6Bgyrsd5Yk58p271QAClA4AAmpwsEiLvN8wLPe3-zYE"
            bot.send_sticker(user_id, sticker_id)
            return
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton(text="👍 Да")
        button2 = types.KeyboardButton(text="👎 Нет")
        markup.add(button1, button2)
        msg = bot.send_message(message.from_user.id, "🥷 Данные будут стерты и не смогут быть добавлены в БД снова. Услуга стоит 329⭐. Продолжить?", reply_markup=markup)
        bot.register_next_step_handler(message, hide_data, msg)
    else:
        bot.send_message(message.from_user.id, '😊 Чтобы начать поиск, просто отправь мне запрос.')
        sticker_id = "CAACAgIAAxkBAAENcaJneRLeFucNm_UqGRrvO0rHNbTDdAACgxAAAv-IuEgmnSDE-AvTOTYE"
        bot.send_sticker(message.from_user.id, sticker_id)

def hide_data(message, msg):
    user_id = message.from_user.id
    if message.text == '👍 Да':
        bot.delete_message(user_id, msg.message_id)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton(text="🥷 Стереть данные", request_contact=True)
        markup.add(button1)
        bot.send_message(user_id, 'Нажми кнопку ниже или отправь контакт из меню.', reply_markup=markup)
        bot.register_next_step_handler(message, hide_contact)
    elif message.text == '👎 Нет':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'оке', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcaZneROCme9rEftT7vvXm5Y4JTms1AACgREAAs9ZuEiQUL5pwX8kyjYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, '😊 Чтобы начать поиск, просто отправь мне запрос.', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcaJneRLeFucNm_UqGRrvO0rHNbTDdAACgxAAAv-IuEgmnSDE-AvTOTYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    
def ip_geo_location(message):
    user_id = message.from_user.id
    if message.text.lower() == 'аборт':
        bot.send_message(message.from_user.id, 'оке')
        sticker_id = "CAACAgIAAxkBAAENcaZneROCme9rEftT7vvXm5Y4JTms1AACgREAAs9ZuEiQUL5pwX8kyjYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    ip = message.text
    balance = get_balance(user_id)
    try:
        result = subprocess.check_output(['python', 'IPGeoLocation/ipgeolocation.py', '-t', ip]).decode('utf-8')
        bot.send_message(message.from_user.id, result)
        reduce = 1
        update_balance(user_id, balance - reduce)
        bot.send_message(user_id, f"Списание -{reduce}⭐")
        sticker_id = "CAACAgIAAxkBAAENcZNneRExyAE0-4rlmTSxScNqowqU5wACOQ4AAqC4uEhG_YXC59BTIzYE"
        bot.send_sticker(user_id, sticker_id)
    except Exception as e:
        bot.send_message(message.from_user.id, f'Упс! {e}')
    
@bot.message_handler(commands=['start'])
def start_message(message):
    global owner_id
    user_id = message.from_user.id
    if active_searches.get(user_id, False):
        a = bot.send_message(message.from_user.id, "🔍 В данный момент уже производится активный поиск..")
        bot.pin_chat_message(user_id, a.message_id)
        sticker_id = "CAACAgIAAxkBAAENcaxneRcWxfLsPGhp0rxLGZmqrzpZXQACTA8AAig6sEiGytjCw_r7ZzYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 По неким причинам доступ к базе запрещен.')
        return
    if not check_user_id(user_id):
        update_balance(user_id, 0)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
        markup.add(contact_button)
        bot.send_message(message.from_user.id, 'Привет? Я тебя не узнаю, мы знакомы?', reply_markup=markup)
        sticker_id = "CAACAgIAAxkBAAENcY1neRCfWAQbnZVbh8w_DAMyCUoAATkAAjsOAAL8KrhIGj-4RJJg-Qc2BA"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    else:
        bot.send_message(message.from_user.id, '😊 Чтобы начать поиск, просто отправь мне запрос.')
        sticker_id = "CAACAgIAAxkBAAENcaJneRLeFucNm_UqGRrvO0rHNbTDdAACgxAAAv-IuEgmnSDE-AvTOTYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        if user_id == owner_id:
            bot.send_message(message.from_user.id, '''
OWNER PANEL
/give_ban - Выдать бан
/give_premium - Выдать премиум
/add_moder - Добавить модератора
/gift - Начислить звезды
/reduce - Списать звезды
/send_to_all - Рассылка
/add_string - Добавить строку в БД
/add_media - Добавить медиа в БД
/fr - Фреймы''')

def ban_user(user_id):
    with open('banned.txt', 'a', encoding='utf-8') as file:
        file.write(f'{user_id}\n')
        
def premium(user_id):
    with open('premium.txt', 'a', encoding='utf-8') as file:
        file.write(f'{user_id}\n')
        
def add_moder(user_id):
    with open('moders.txt', 'a', encoding='utf-8') as file:
        file.write(f'{user_id}\n')

@bot.message_handler(commands=['add_string'])
def add_string(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Добавь новую строку в базу (символ / | - разделитель, не используй Enter):')
    bot.register_next_step_handler(message, add_string_to)

def add_string_to(message):
    text = message.text
    if message.text and message.text.lower() == 'аборт':
        bot.send_message(message.from_user.id, 'оке')
        sticker_id = "CAACAgIAAxkBAAENcaZneROCme9rEftT7vvXm5Y4JTms1AACgREAAs9ZuEiQUL5pwX8kyjYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    new_string = message.text
    try:
        with open('server/obscure-db.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []
    with open('server/obscure-db.txt', 'w', encoding='utf-8') as file:
        file.write(new_string + '\n')
        for line in lines:
            file.write(line)
    bot.send_message(message.from_user.id, '+данные!')
    sticker_id = "CAACAgIAAxkBAAENccBneRoGTgXrFRrAA9jL5a_vjn2ijwADDQACSeqxSK64o_7HGLBKNgQ"
    bot.send_sticker(message.from_user.id, sticker_id)
    
@bot.message_handler(commands=['add_media'])
def add_media(message):
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(user_id, "🚫 У тебя нет прав для выполнения этой команды.")
        return

    bot.send_message(user_id, "Введи имя файла (с расширением), под которым ты хочешь сохранить файл:")
    bot.register_next_step_handler(message, process_file_name)

def process_file_name(message):
    user_id = message.from_user.id
    file_name = message.text.strip()

    # Проверяем, что имя файла не пустое
    if not file_name:
        bot.send_message(user_id, "🚫 Fatal.")
        return

    bot.send_message(user_id, "Отправь файл для добавления его в БД:")
    bot.register_next_step_handler(message, save_media_file, file_name)

def save_media_file(message, file_name):
    user_id = message.from_user.id
    file_path = os.path.join(SERVER_FOLDER, file_name)

    # Проверяем, что сообщение содержит медиафайл
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(user_id, f"✅ Файл {file_name} успешно сохранен.")
    elif message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(user_id, f"✅ Файл {file_name} успешно сохранен.")
    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(user_id, f"✅ Файл {file_name} успешно сохранен.")
    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(user_id, f"✅ Файл {file_name} успешно сохранен.")
    else:
        bot.send_message(user_id, "🚫 Отправь только медиафайл (фото, видео, аудио или документ).")
    
@bot.message_handler(commands=['send_to_all'])
def send_to_all(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Отправь сообщение для рассылки:')
    bot.register_next_step_handler(message, send_to_all_message)

def send_to_all_message(message):
    text = message.text
    if message.text and message.text.lower() == 'аборт':
        bot.send_message(message.from_user.id, 'оке')
        sticker_id = "CAACAgIAAxkBAAENcaZneROCme9rEftT7vvXm5Y4JTms1AACgREAAs9ZuEiQUL5pwX8kyjYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    try:
        with open('user_balance.txt', 'r', encoding='utf-8') as file:
            users = file.readlines()
    except FileNotFoundError:
        return
    for user in users:
        user_id = int(user.split()[0])
        try:
            if message.text:
                bot.send_message(user_id, f"{message.text}\n\n✉️ Отправлено администратором")
            elif message.photo:
                bot.send_photo(user_id, message.photo[-1].file_id, caption=f"{message.text}\n\n✉️ Отправлено администратором")
            elif message.video:
                bot.send_video(user_id, message.video.file_id, caption=f"{message.text}\n\n✉️ Отправлено администратором")
            elif message.document:
                bot.send_document(user_id, message.document.file_id, caption=f"{message.text}\n\n✉️ Отправлено администратором")
            elif message.audio:
                bot.send_audio(user_id, message.audio.file_id, caption=f"{message.text}\n\n✉️ Отправлено администратором")
        except Exception as e:
            bot.send_message(message.from_user.id, f'Ошибка при отправке пользователю {user_id}: {e}')
            time.sleep(1)
    bot.send_message(message.from_user.id, 'Рассылка совершена.')

@bot.message_handler(commands=['reduce'])
def reduce_stars(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Введи ID пользователя:')
    bot.register_next_step_handler(message, star_num_reduce)

def star_num_reduce(message):
    try:
        receiver = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректный ID.')
        return
    bot.send_message(message.from_user.id, 'Введи кол-во звезд для списания:')
    bot.register_next_step_handler(message, lambda msg: process_reduce_stars(msg, receiver))

def process_reduce_stars(message, receiver):
    try:
        stars = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректное число.')
        return
    balance = get_balance(receiver)
    if stars > balance:
        bot.send_message(message.from_user.id, '🚫 Невозможно списать, значение превышает баланс.')
        return
    update_balance(receiver, get_balance(receiver) - stars)
    bot.send_message(message.from_user.id, f'Списано {stars}⭐ с пользователя {receiver}.')
    try:
        bot.send_message(receiver, f'Списание за плохое поведение:')
        bot.send_message(receiver, f'-{stars}⭐')
        sticker_id = 'CAACAgIAAxkBAAENceBneSWhEyBzI6Bgyrsd5Yk58p271QAClA4AAmpwsEiLvN8wLPe3-zYE'
        bot.send_sticker(receiver, sticker_id)
    except Exception as e:
        bot.send_message(message.from_user.id, f'Ошибка: {e}')

@bot.message_handler(commands=['gift'])
def give_stars(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Введи ID пользователя:')
    bot.register_next_step_handler(message, star_num_gift)

def star_num_gift(message):
    try:
        receiver = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректный ID.')
        return
    bot.send_message(message.from_user.id, 'Введи кол-во звезд для начисления:')
    bot.register_next_step_handler(message, lambda msg: process_give_stars(msg, receiver))

def process_give_stars(message, receiver):
    global msg
    try:
        stars = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректное число.')
        return
    update_balance(receiver, get_balance(receiver) + stars)
    bot.send_message(message.from_user.id, f'Начислено {stars}⭐ пользователю {receiver}.')
    poxvala = random.choice(msg)
    try:
        bot.send_message(receiver, f'🎁 Вознаграждение:')
        bot.send_message(receiver, f'{poxvala} +{stars}⭐')
        sticker_id = random.choice(poxvala_sticker)
        bot.send_sticker(receiver, sticker_id)
    except Exception as e:
        bot.send_message(message.from_user.id, f'Ошибка: {e}')
    
@bot.message_handler(commands=['give_ban'])
def give_ban(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Введи ID пользователя:')
    bot.register_next_step_handler(message, process_ban_user)

@bot.message_handler(commands=['give_premium'])
def give_premium(message):
    global owner_id
    user_id = message.from_user.id
    if user_id != owner_id:
        bot.send_message(message.from_user.id, '🚫 У тебя нет прав для выполнения этой команды.')
        return
    bot.send_message(message.from_user.id, 'Введи ID пользователя:')
    bot.register_next_step_handler(message, prem_user)
    
def prem_user(message):
    try:
        user_prem = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректный ID.')
        return
    premium(user_prem)
    bot.send_message(message.from_user.id, f'👑 Выдал премку пользователю {user_prem}.')
    try:
        bot.send_message(user_prem, '👑 Мои поздравления! Тебе выдали премку!')
        sticker_id = "CAACAgIAAxkBAAENcZlneRHV2SezS2sjd42laq1WpJ5SHgACdhMAAkQosEiQP6XGsWjHIzYE"
        bot.send_sticker(user_prem, sticker_id)
        update_balance(user_prem, get_balance(user_prem) + 500)
        bot.send_message(user_prem, 'Пополнение +500⭐')
    except Exception as e:
        bot.send_message(message.from_user.id, f'Ошибка: {e}')
    
def process_ban_user(message):
    try:
        user_to_ban = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, '🚫 Некорректный ID.')
        return
    ban_user(user_to_ban)
    bot.send_message(message.from_user.id, f'✋ Пользователь {user_to_ban} забанен.')
    try:
        bot.send_message(user_to_ban, '🚫 Упс... БАН! Ты больше не можешь пользоваться базой. Если ты считаешь что БАН необоснован, свяжись с модераторами.')
        sticker_id = "CAACAgIAAxkBAAENcZVneRFQ6Am6Xlb5fajXHhfBTomCSwACIw8AAmHBuUj4raDZBZXApzYE"
        bot.send_sticker(user_to_ban, sticker_id)
    except Exception as e:
        bot.send_message(message.from_user.id, f'Ошибка: {e}')

def hide_contact(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardRemove()
    if message.contact:
        contact = message.contact
        name = contact.first_name or "---"
        lastname = contact.last_name or "---"
        user_id = contact.user_id or "---"
        user = bot.get_chat(contact.user_id)
        username = user.username or "---"
        phone = contact.phone_number
        with open('exceptions.txt', 'a', encoding='utf-8') as file:
            file.write(f'{name} {lastname} @{username} {user_id} {phone}\n')
        msg = bot.send_message(message.from_user.id, 'Работаем...', reply_markup=markup)
        time.sleep(1)
        bot.delete_message(user_id, msg.message_id)
        bot.send_message(message.from_user.id, 'Есть! Данные будут полностью удалены с серверов в течение часа.')
        balance = get_balance(user_id)
        reduce = 329
        update_balance(user_id, balance - reduce)
        bot.send_message(user_id, f"Списание -{reduce}⭐")
        sticker_id = "CAACAgIAAxkBAAENcZNneRExyAE0-4rlmTSxScNqowqU5wACOQ4AAqC4uEhG_YXC59BTIzYE"
        bot.send_sticker(user_id, sticker_id)
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, '🛑 Операция отменена, неверный запрос.', reply_markup=markup)
        return
    
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    global poxvala_sticker
    global msg
    global owner_id
    giver_id = message.from_user.id
    giver_username = message.from_user.username
    giver_name = message.from_user.first_name
    contact = message.contact
    if check_contact_exists(contact.phone_number):
        bot.send_message(message.from_user.id, '✋ Номер уже в базе.')
        sticker_id = "CAACAgIAAxkBAAENcdZneSMIP1tHQUImb1z2Pv1cyWievwACEw8AAmrksUj-IGawpgwPhDYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    name = contact.first_name or "---"
    lastname = contact.last_name or "---"
    user_id = contact.user_id or "---"
    user = bot.get_chat(contact.user_id)
    username = user.username or "---"
    phone = contact.phone_number
    if check_exceptions(phone):
        bot.send_message(chat_id=giver_id, text="🛑 Данный контакт защищен.")
        bot.send_message(user_id, f"⚠️ Пользователь {giver_name} @{giver_username} {giver_id} пытался только что добавить твой контакт в базу.")
        sticker_id = "CAACAgIAAxkBAAENdD5ne-hDGR_ao2h2wWF7zwpCS5YG7wACuw0AAsXdsEiP7t2Z4f08gzYE"
        bot.send_sticker(user_id, sticker_id)
        return
    if check_exceptions(username):
        bot.send_message(chat_id=giver_id, text="🛑 Данный контакт защищен.")
        bot.send_message(user_id, f"⚠️ Пользователь {giver_name} @{giver_username} {giver_id} пытался только что добавить твой контакт в базу.")
        sticker_id = "CAACAgIAAxkBAAENdD5ne-hDGR_ao2h2wWF7zwpCS5YG7wACuw0AAsXdsEiP7t2Z4f08gzYE"
        bot.send_sticker(user_id, sticker_id)
        return
    if check_exceptions(name):
        bot.send_message(chat_id=giver_id, text="🛑 Данный контакт защищен.")
        bot.send_message(user_id, f"⚠️ Пользователь {giver_name} @{giver_username} {giver_id} пытался только что добавить твой контакт в базу.")
        sticker_id = "CAACAgIAAxkBAAENdD5ne-hDGR_ao2h2wWF7zwpCS5YG7wACuw0AAsXdsEiP7t2Z4f08gzYE"
        bot.send_sticker(user_id, sticker_id)
        return
    with open('server/obscure-db.txt', 'a', encoding='utf-8') as file:
        file.write(f'╒ Name: {name}/╞ Last Name: {lastname}/╞ Username: @{username}/╞ ID: {user_id}/╘ Phone: {phone}\n')
    markup = types.ReplyKeyboardRemove()
    poxvala = random.choice(msg)
    receiver = message.from_user.id
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Ты не можешь пользоваться по неким причинам.')
        return
    update_balance(receiver, get_balance(receiver) + 8)
    bot.send_message(message.from_user.id, f'{poxvala} +8⭐', reply_markup=markup)
    sticker_id = random.choice(poxvala_sticker)
    sticker = bot.send_sticker(message.from_user.id, sticker_id)

def animate_message(user_id, message_id):
    global owner_id
    try:
        while True:
            emoji = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾',
                     '🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🫐', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌶', '🫑', '🌽', '🥕', '🫒', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗', '🍖', '🦴', '🌭', '🍔', '🍟', '🍕', '🫓', '🥪', '🥙', '🧆', '🌮', '🌯', '🫔', '🥗', '🥘', '🫕', '🥫', '🍝', '🍜', '🍲', '🍛', '🍣', '🍱', '🥟', '🦪', '🍤', '🍙', '🍚', '🍘', '🍥', '🥠', '🥮', '🍢', '🍡', '🍧', '🍨', '🍦', '🥧', '🧁', '🍰', '🎂', '🍮', '🍭', '🍬', '🍫', '🍿', '🍩', '🍪', '🌰', '🥜', '🫘', '🍯', '🥛', '🍼', '🫖', '☕️', '🍵', '🧃', '🥤', '🍶', '🍺', '🍻', '🥂', '🍷', '🥃', '🍸', '🍹', '🧉', 
                     '🍾', '🧊', '🥄', '🍴', '🍽', '🥣', '🥡', '🥢', '🍕', '🍔', '🌭', '🍟', '🍗', '🍖', '🍝', '🍜', '🍲', '🍣', '🍱', '🍤', '🍙', '🍚', '🍘', '🍥', '🍦', '🍨', '🍧', '🍰', '🎂', '🍮', '🍭', '🍬', '🍫', '🍿', '🍩', '🍪', '🌰', '🥜', '🫘', '🍯', '🥛', '🍼', '🫖', '☕️', '🍵', '🧃', '🥤', '🍶', '🍺', '🍻', '🥂', '🍷', '🥃', '🍸', '🍹', '🧉', '🍾', '🧊', '📱', '💻', '🖥️', '🖨️', '📺', '📷', '📸', '📹', '🎥', '📼', '🔋', '🔌', '💡', '🔦', '🕯️', '🧯', '🧰', '🧲', '🧪', '🧫', '🧬', '🔬', '🔭', '📡', '🛰', '🚀', '⚓', '⛵', '🛳️', '🚢', '✈️', '🛩️', '🛫', '🛬', '🚁', '🚂', '🚆', '🚄', '🚅', '🚈', '🚊', '🚉', '🚏', '🚌', '🚍', '🚙', '🚗', '🚕', '🚖', '🚘', '🚲', '🛴', '🛵', '🛹', '🚏', '🛶', '⛷️', 
                     '🏂', '🏍️', '🛵', '🚨', '🚔', '🚍', '🚘', '🚖', '🚗', '🚙', '🚌', '🚎', '🚏', '🚦', '🚧', '⚠️', '🔞', '🔑', '🗝️', '🔒', '🔓', '🧳', '💼', '📦', '📮', '📬', '📭', '📫', '📪', '📈', '📉', '📊', '📋', '📅', '📆', '🗓️', '🗃️', '🗄️', '🗑️', '🗂️', '📁', '📂', '📑', '📊', '📈', '📉', '📜', '📃', '📄', '📅', '📆', '🗓️', '🗃️', '🗄️', '🗑️', '🗂️', '📁', '📂', '📑', '📊', '📈', '📉', '📜', '📃', '📄', '📅', '📆', '🗓️', '🗃️', '🗄️', '🗑️', '🗂️', '📁', '📂', '📑', '📊', '📈', '📉', '📜', '📃', '📄', '📅', '📆', '🗓️', '🗃️', '🗄️', '🗑️', '🗂️', '📁', '📂', '📑', '📊', '📈', '📉', '📜', '📃', '📄', '📅', '📆', '🗓️', '🗃️', '🗄️', '🗑️', '🗂️', '📁', '📂', '📑', '📊', '📈', '📉', '📜', '📃', '📄', '📅']
            frames = [f'🔍 Поиск... {random.choice(emoji)}', 
                      f'🔍 Поиск... {random.choice(emoji)}{random.choice(emoji)}', 
                      f'🔍 Поиск... {random.choice(emoji)}{random.choice(emoji)}{random.choice(emoji)}']
            for frame in frames:
                bot.edit_message_text(chat_id=user_id, message_id=message_id, text=frame)
                time.sleep(2)
    except Exception as e:
        pass
    
def random_msg(user_id):
    global tip_msg
    msg = random.choice(tip_msg)
    try:
        while True:
            time.sleep(30)
            rmsg = bot.send_message(user_id, msg)
            time.sleep(180)
            bot.delete_message(user_id, rmsg.message_id)
    except Exception as e:
        pass

@bot.message_handler(content_types=['text'])
def search_message(message):
    global tip_msg
    user_id = message.from_user.id
    if active_searches.get(user_id, False):
        a = bot.send_message(message.from_user.id, "🔍 В данный момент уже производится активный поиск..")
        bot.pin_chat_message(user_id, a.message_id)
        sticker_id = "CAACAgIAAxkBAAENcaxneRcWxfLsPGhp0rxLGZmqrzpZXQACTA8AAig6sEiGytjCw_r7ZzYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        return
    if is_user_banned(user_id):
        bot.send_message(message.from_user.id, '🚫 Доступ запрещен.')
        return
    if not check_user_id(user_id):
        if message.content_type == 'text':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            contact_button = types.KeyboardButton(text="⟡ Познакомиться ⟡", request_contact=True)
            markup.add(contact_button)
            bot.send_message(message.from_user.id, 'Я тебя не знаю... Представься для начала.', reply_markup=markup)
            sticker_id = "CAACAgIAAxkBAAENcY1neRCfWAQbnZVbh8w_DAMyCUoAATkAAjsOAAL8KrhIGj-4RJJg-Qc2BA"
            bot.send_sticker(message.from_user.id, sticker_id)
            return
    else:
        
        active_searches[user_id] = True
        wait = bot.send_message(message.from_user.id, '🔍 Поиск...')
        wait_id = wait.message_id
        anim = threading.Thread(target=animate_message, args=(user_id, wait_id))
        anim.start()
        query = message.text
        if not query or query.startswith('/'):
            bot.delete_message(chat_id=message.from_user.id, message_id=wait.message_id)
            bot.send_message(message.from_user.id, '🚫 Запрос не предоставлен.')
            sticker_id = "CAACAgIAAxkBAAENcclneRq0vz6p1AvCnFNZ6R2252Im7wACGREAArsyuUi7Sgs7Em4O8DYE"
            sticker = bot.send_sticker(message.from_user.id, sticker_id)
            active_searches[user_id] = False
            return
        with ThreadPoolExecutor() as executor:
            executor.submit(send_query, query, user_id)
        bot.delete_message(chat_id=message.from_user.id, message_id=wait.message_id)
        active_searches[user_id] = False

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio']) 
def share_info(message):
    global owner_id
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id]:
        pass
    else:
        return
    if message.text and message.text.lower() == 'аборт':
        bot.send_message(message.from_user.id, 'оке')
        sticker_id = "CAACAgIAAxkBAAENcaZneROCme9rEftT7vvXm5Y4JTms1AACgREAAs9ZuEiQUL5pwX8kyjYE"
        bot.send_sticker(message.from_user.id, sticker_id)
        user_states.pop(user_id, None)
        return
    if message.text:
        if check_exceptions(message.text):
            bot.send_message(message.from_user.id, '🛑 Сообщение содержит исключения.')
            user_states.pop(user_id, None)
            return
    user_last_send_time[user_id] = time.time()
    moders = []
    try:
        with open('moders.txt', 'r', encoding='utf-8') as file:
            for line in file:
                moders.append(int(line.strip()))
    except FileNotFoundError:
        pass
    name = message.from_user.first_name or "---"
    bot.send_message(owner_id, f'✉️ Сообщение от пользователя {name} {message.from_user.id}:')
    bot.forward_message(chat_id=owner_id, from_chat_id=user_id, message_id=message.id)
    for moder in moders:
        bot.send_message(moder, f'✉️ Сообщение от пользователя {name} {message.from_user.id}:')
        bot.forward_message(chat_id=moder, from_chat_id=user_id, message_id=message.id)
    bot.send_message(message.from_user.id, 'Отправлено! Если инфа полезна, ты получишь вознаграждение)')
    sticker_id = "CAACAgIAAxkBAAENcahneRPJkY5-91dgyl6lr4J74-vL1gAClQ4AAn5ZsEhgAoeI2KwG7DYE"
    bot.send_sticker(message.from_user.id, sticker_id)
    user_states.pop(user_id, None)
    return

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print(e)