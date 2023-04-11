import telebot
import requests
import json
from telebot import types


bot = telebot.TeleBot('************************************') #Add your API token from telegram bot
API = '********************************' # Add your API token from open weather

bot.delete_webhook()  # видалення веб-хуку

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Погода станом на зараз')
    item2 = types.KeyboardButton('1 день/3 години')
    item3 = types.KeyboardButton('5 днів/3 години')

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привіт, я допоможу дізнатися прогноз погоди. Вибери в меню період, на який хочеш отримати прогноз:', reply_markup=markup)

@bot.message_handler(content_types=['text'])

def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Погода станом на зараз':
            weather_now(message)
        if message.text == '1 день/3 години':
            one_day(message)
        if message.text == '5 днів/3 години':
            five_days(message)

@bot.message_handler(commands=['one_day'])
def one_day(message):
    bot.send_message(message.chat.id, 'Введіть назву міста:')
    bot.register_next_step_handler(message, get_weather, 'one_day')

@bot.message_handler(commands=['five_days'])
def five_days(message):
    bot.send_message(message.chat.id, 'Введіть назву міста:')
    bot.register_next_step_handler(message, get_weather, 'five_days')

@bot.message_handler(commands=['weather_now'])
def weather_now(message):
    bot.send_message(message.chat.id, 'Введіть назву міста:')
    bot.register_next_step_handler(message, get_weather_now_weather, 'weather_now')

def get_weather(message, command):
    city = message.text.strip().lower()
    if command == 'one_day':
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ua&appid={API}&units=metric&exclude=minutely,hourly,daily,alerts')
        if res.status_code == 200:
            data = json.loads(res.text)

            for forecast in data['list'][:8]:
                dt_txt = forecast['dt_txt']
                temp = forecast['main']['temp']
                feels_like = forecast['main']['feels_like']
                humidity = forecast['main']['humidity']
                visibility = forecast['visibility']
                wind_speed = forecast['wind']['speed']
                clouds = forecast['clouds']['all']
                weather_description = forecast['weather'][0]['description']
                if 'чисте' in weather_description:
                    photo = open('clear_sky.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'хмар' in weather_description:
                    photo = open('cloud.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'туман' in weather_description:
                    photo = open('fog.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'дощ' in weather_description:
                    photo = open('rain.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'сніг' in weather_description:
                    photo = open('snow.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()

                message_text = f'Прогноз погоди на {dt_txt}:\nТемпература: {temp}°C\nВідчувається як: {feels_like}°C\nВологість: {humidity}%\nВідстань видимості: {visibility} метрів\nШвидкість вітру: {wind_speed} м/с\nХмарність: {clouds}%\nОпис погоди: {weather_description}'
                bot.send_message(message.chat.id, message_text)
        else:
            bot.reply_to(message, f'Місто {city.capitalize()} не знайдено')

    elif command == 'five_days':
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang=ua&appid={API}&units=metric&exclude=minutely,hourly,daily,alerts')
        if res.status_code == 200:
            data = json.loads(res.text)

            for forecast in data['list']:
                dt_txt = forecast['dt_txt']
                temp = forecast['main']['temp']
                feels_like = forecast['main']['feels_like']
                humidity = forecast['main']['humidity']
                visibility = forecast['visibility']
                wind_speed = forecast['wind']['speed']
                clouds = forecast['clouds']['all']
                weather_description = forecast['weather'][0]['description']
                if 'чисте' in weather_description:
                    photo = open('clear_sky.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'хмар' in weather_description:
                    photo = open('cloud.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'туман' in weather_description:
                    photo = open('fog.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'дощ' in weather_description:
                    photo = open('rain.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                elif 'сніг' in weather_description:
                    photo = open('snow.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()

                message_text = f'Прогноз погоди на {dt_txt}:\nТемпература: {temp}°C\nВідчувається як: {feels_like}°C\nВологість: {humidity}%\nВідстань видимості: {visibility} метрів\nШвидкість вітру: {wind_speed} м/с\nХмарність: {clouds}%\nОпис погоди: {weather_description}'
                bot.send_message(message.chat.id, message_text)
        else:
            bot.reply_to(message, f'Місто {city.capitalize()} не знайдено')


def get_weather_now_weather(message, command, dt_txt=None):
    city = message.text.strip().lower()
    if command == 'weather_now':
        res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ua')
        if res.status_code == 200:
            data = json.loads(res.text)

            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            visibility = data['visibility']
            wind_speed = data['wind']['speed']
            clouds = data['clouds']['all']
            weather_description = data['weather'][0]['description']
            if 'чисте' in weather_description:
                photo = open('clear_sky.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
            elif 'хмар' in weather_description:
                photo = open('cloud.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
            elif 'туман' in weather_description:
                photo = open('fog.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
            elif 'дощ' in weather_description:
                photo = open('rain.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
            elif 'сніг' in weather_description:
                photo = open('snow.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()

            message_text = f'Прогноз погоди на {city}:\nТемпература: {temp}°C\nВідчувається як: {feels_like}°C\nВологість: {humidity}%\nВідстань видимості: {visibility} метрів\nШвидкість вітру: {wind_speed} м/с\nХмарність: {clouds}%\nОпис погоди: {weather_description}'
            bot.send_message(message.chat.id, message_text)

        else:

            bot.reply_to(message, f'Місто {city.capitalize()} не знайдено')

bot.polling(none_stop=True)
