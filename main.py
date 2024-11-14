import telebot
import random
from config import Config
from sticker_config import sticker_pool

bot = telebot.TeleBot(Config.TEST_TOKEN)

user_message_count = {}
sticker_stats = {}
user_traits = {}

initial_traits = {
    "сила": 0, "устойчивость": 0, "броня": 0, "ловкость": 0, "счастье": 0, "спокойствие": 0,
    "скрытность": 0, "аура": 0, "спиритизм": 0, "фимоз": 0, "уверенность": 0, "криворукость": 0, "хайп": 0
}

@bot.message_handler(commands=['stats'])
def send_stats(message):
    chat_id = message.chat.id
    print(f"Команда '/stats' вызвана в чате: {message.chat.type}, ID: {chat_id}")

    if chat_id not in sticker_stats or not sticker_stats[chat_id]:
        bot.send_message(chat_id, "Пока нет статистики... Немножечко лень")
        return

    sorted_stats = sorted(sticker_stats[chat_id].items(), key=lambda x: sum(user_traits[x[0]].values()), reverse=True)
    stats_message = "🏆 **Топ пользователей по характеристикам** 🏆\n\n"
    stats_message += "Tоп-лист:\n\n"
    rank = 1
    for user_id, user_data in sorted_stats:
        username = f"<a href='tg://user?id={user_id}'>{user_data.get('name', 'Неизвестный')}</a>"
        total_traits = sum(user_traits[user_id].values())
        stats_message += f"{rank}. {username}: {total_traits:.0f} очков\n"
        rank += 1

    stats_message += "\n🎉 **SEO-Руслан гордится вами!** 🎉"
    bot.send_message(chat_id, stats_message, parse_mode='HTML')

@bot.message_handler(commands=['trait'])
def send_traits(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Пользователь"

    if user_id not in user_traits:
        user_traits[user_id] = initial_traits.copy()

    traits_message = f"📜**Характеристики {user_name}**📜\n\n"
    for trait, value in user_traits[user_id].items():
        traits_message += f"**{trait.capitalize()}**: {value}\n"

    bot.send_message(chat_id, traits_message, parse_mode='Markdown')


def choose_sticker():
    random_value = random.random()
    cumulative_probability = 0.0
    for sticker in sticker_pool:
        cumulative_probability += sticker['chance']
        if random_value <= cumulative_probability:
            return sticker
    return sticker_pool[-1]

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'], content_types=['text', 'photo', 'sticker', 'video', 'video_note'])
def track_user_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Пользователь"

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
            sticker_stats[chat_id][user_id] = {'name': user_name, 'count': 0}

        sticker_stats[chat_id][user_id]['count'] += 1

        if user_id not in user_traits:
            user_traits[user_id] = initial_traits.copy()

        for trait, value in chosen_sticker['traits'].items():
            user_traits[user_id][trait] += value

        bot.send_message(
            chat_id,
            f"{chosen_sticker['message']} (Шанс: {chosen_sticker['chance'] * 100:.0f}%) "
            f"<a href='tg://user?id={user_id}'>{user_name}</a>",
            parse_mode='HTML'
        )

bot.polling(none_stop=True)
