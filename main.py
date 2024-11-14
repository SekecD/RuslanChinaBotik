import telebot
import random
from config import Config
from sticker_config import sticker_pool

bot = telebot.TeleBot(Config.TEST_TOKEN)

user_message_count = {}
sticker_stats = {}


@bot.message_handler(commands=['stats'])
def send_stats(message):
    chat_id = message.chat.id
    print(f"Команда '/stats' вызвана в чате: {message.chat.type}, ID: {chat_id}")

    if chat_id not in sticker_stats or not sticker_stats[chat_id]:
        bot.send_message(chat_id, "Пока нет статистики... Немножечко лень")
        return

    sorted_stats = sorted(sticker_stats[chat_id].items(), key=lambda x: x[1]['count'], reverse=True)

    stats_message = "🏆 **Топ получивших стикеры** 🏆\n\n"
    stats_message += "Tоп-лист:\n\n"

    rank = 1
    for user_id, user_data in sorted_stats:
        username = user_data.get('name', 'Неизвестный пользователь')
        sticker_count = user_data.get('count', 0)
        stats_message += f"{rank}. **{username}**: {sticker_count} стикеров\n"
        rank += 1

    stats_message += "\n🎉 **SEO-Руслан гордится вами!** 🎉"

    bot.send_message(chat_id, stats_message, parse_mode='Markdown')

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

        bot.send_message(
            chat_id,
            f"{chosen_sticker['message']} (Шанс: {chosen_sticker['chance'] * 100:.0f}%) "
            f"<a href='tg://user?id={user_id}'>{user_name}</a>",
            parse_mode='HTML'
        )

bot.polling(none_stop=True)
