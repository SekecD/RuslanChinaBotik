import telebot
import random
import json
from copy import deepcopy
from config import Config
from sticker_config import sticker_pool

bot = telebot.TeleBot(Config.TEST_TOKEN)

USER_DATA_FILE = "user_data.json"

user_message_count = {}
sticker_stats = {}
user_traits = {}

initial_traits = {
    "сила": 0, "устойчивость": 0, "броня": 0, "ловкость": 0, "счастье": 0, "спокойствие": 0,
    "скрытность": 0, "аура": 0, "спиритизм": 0, "фимоз": 0, "уверенность": 0, "криворукость": 0, "хайп": 0
}


def load_data():
    global user_message_count, sticker_stats, user_traits
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            user_message_count = data.get("user_message_count", {})
            sticker_stats = data.get("sticker_stats", {})
            user_traits = data.get("user_traits", {})
    except FileNotFoundError:
        print("Файл с данными не найден. Создаём новый.")
        user_message_count = {}
        sticker_stats = {}
        user_traits = {}


def save_data():
    data = {
        "user_message_count": user_message_count,
        "sticker_stats": sticker_stats,
        "user_traits": user_traits
    }
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=['stats'])
def send_stats(message):
    chat_id = str(message.chat.id)
    print(f"Команда /stats вызвана в чате: {message.chat.type}, ID: {chat_id}")

    if chat_id not in sticker_stats or not any(sticker_stats[chat_id]):
        bot.send_message(chat_id, "😴 Пока нет статистики... Немножечко лень 😴")
        return

    sorted_stats = sorted(sticker_stats[chat_id].items(), key=lambda x: sum(user_traits.get(x[0], {}).values()),
                          reverse=True)
    stats_message = "🏆 <b>Топ пользователей по характеристикам</b> 🏆\n\n📋 <u>Топ-лист:</u>\n\n"
    for rank, (user_id, user_data) in enumerate(sorted_stats, start=1):
        username = f"<a href='tg://user?id={user_id}'>{user_data.get('name', 'Неизвестный')}</a>"
        total_traits = sum(user_traits.get(user_id, {}).values())
        stats_message += f"{rank}. {username}: {total_traits:.0f} очков ⭐️\n"
    stats_message += "\n🎉 <b>SEO-Руслан гордится вами!</b> 🎉"
    bot.send_message(chat_id, stats_message, parse_mode='HTML')


@bot.message_handler(commands=['mytop'])
def send_traits(message):
    chat_id = message.chat.id
    print(f"Команда /mytop вызвана в чате: {message.chat.type}, ID: {chat_id}")
    user_id = str(message.from_user.id)  # Приведение ID пользователя к строке
    user_name = message.from_user.first_name or "Пользователь"

    if user_id not in user_traits:
        user_traits[user_id] = deepcopy(initial_traits)

    # Генерация сообщения с характеристиками
    traits_message = f"📜 <b>Характеристики {user_name}</b> 📜\n\n"
    for trait, value in user_traits[user_id].items():
        traits_message += f"🔹 <b>{trait.capitalize()}</b>: {value}\n"

    bot.send_message(chat_id, traits_message, parse_mode='HTML')

    save_data()

def choose_sticker():
    sticker = random.choices(sticker_pool, weights=[s['chance'] for s in sticker_pool], k=1)[0]
    return sticker


@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'],
                     content_types=['text', 'photo', 'sticker', 'video', 'video_note'])
def track_user_messages(message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in user_message_count:
        user_message_count[chat_id] = {}
    if user_id not in user_message_count[chat_id]:
        user_message_count[chat_id][user_id] = 0

    user_message_count[chat_id][user_id] += 1

    if user_message_count[chat_id][user_id] == 10:
        user_message_count[chat_id][user_id] = 0

        chosen_sticker = choose_sticker()
        bot.send_sticker(chat_id, chosen_sticker['id'])

        if chat_id not in sticker_stats:
            sticker_stats[chat_id] = {}
        if user_id not in sticker_stats[chat_id]:
            sticker_stats[chat_id][user_id] = {'name': message.from_user.first_name, 'count': 0}
        sticker_stats[chat_id][user_id]['count'] += 1

        if user_id not in user_traits:
            user_traits[user_id] = initial_traits.copy()
        for trait, value in chosen_sticker['traits'].items():
            user_traits[user_id][trait] += value

        bot.send_message(
            chat_id,
            f"{chosen_sticker['message']} (Шанс: {chosen_sticker['chance'] * 100:.0f}%) "
            f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>",
            parse_mode='HTML'
        )

        save_data()


load_data()

bot.polling(none_stop=True)