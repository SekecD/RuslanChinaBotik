import telebot
import random
from config import Config

bot = telebot.TeleBot(Config.TOKEN)

user_message_count = {}
sticker_stats = {}

sticker_pool = [
    {'id': 'CAACAgIAAxkBAAENHXtnNGgqh3m9skg-FG6YcPXGdvHHDAACyVcAAlDTIEkyq5UzKXmolDYE', 'chance': 0.1, 'message': 'Вам выпал монсруозный Ярик'},
    {'id': 'CAACAgIAAxkBAAENHihnNPqdbLnF0zh0LU5NVooyQ9su9wACvFYAAvS8KEmi8QT8WAQcAAE2BA', 'chance': 0.3, 'message': 'Вам выпал ужаленеый Тигран'},
    {'id': 'CAACAgIAAxkBAAENHipnNPquoj1u2zoYgZ4E43IqTY9kowACbWkAAkw1KUmjU1q0J3wLmDYE', 'chance': 0.05, 'message': 'Вам выпал бешеный Елисей'},
    {'id': 'CAACAgIAAxkBAAENHi9nNPq86ruNvyBHZhnESc7DBXGI6wAC3lkAAgL1IUkUjqkTjshZtDYE', 'chance': 0.2, 'message': 'Вам выпал репер Влад'},
    {'id': 'CAACAgIAAxkBAAENHjFnNPr63UkpFsJk4ffA6VsozGj4vAACEVIAAqGBKUkzzUP2Z6TtnzYE', 'chance': 0.03, 'message': 'Вам выпал гига Руслан'},
    {'id': 'CAACAgIAAxkBAAENHjNnNPsFZJV8BLLgy2QcO507mceK6QACZFoAAjUoIUn5izprfvq-PzYE', 'chance': 0.10, 'message': 'Вам выпал округленый Руслан'},
    {'id': 'CAACAgIAAxkBAAENHjVnNPsUgpSdUu6LxkVuwQIO-BHGegACoVcAApbiKUmvO0oITRkKwzYE', 'chance': 0.25, 'message': 'Вам выпал счастливый Кирюша'},
    {'id': 'CAACAgIAAxkBAAENHjlnNPseKqlpa_H5RIQj6IvuoDMC8AACP1YAAoMXKEmiEycmHVj67jYE', 'chance': 0.4, 'message': 'Вам выпал спокойный Ярик'},
    {'id': 'CAACAgIAAxkBAAENHjtnNPsr8oIZOvVZ7_HBkuCPh9AoLgACKV4AAmRuIEkZvtwFcE0HhTYE', 'chance': 0.06, 'message': 'Вам выпал крутой Андрей'},
    {'id': 'CAACAgIAAxkBAAENHj9nNPs-kG0I0GHjgsj7rhSfISsCZQACSVgAArP9IEm1kxkRQuYoyDYE', 'chance': 0.52, 'message': 'вам выпал поцелуй Андрей'},
    {'id': 'CAACAgIAAxkBAAENHkFnNPtIHYj5qIA5ibGxDaIU84K86AACcl8AAswhIEnLjoI8r-nWkTYE', 'chance': 0.20, 'message': 'Вам выпал подозрительный Руслан'},
    {'id': 'CAACAgIAAxkBAAENHkNnNPtXR5FYva3yr6HXMlH-knF8RwACIFoAAoWmIEmx3YJp4eH3tDYE', 'chance': 0.10, 'message': 'Вам выпал колдун Егор'},
    {'id': 'CAACAgIAAxkBAAENHkVnNPthltMOKvUm5S1WtotyUKtS7wACy2MAAs-jIUl6kdUF41G13zYE', 'chance': 0.05, 'message': 'Вам выпал мак комбо делюкс 3 сыра и 1 грибок'},
    {'id': 'CAACAgIAAxkBAAENHkdnNPttbgRVd6lKt0Tjbgr5qC5migACZFsAAnZVIEkr9v1sYeW78jYE', 'chance': 0.4, 'message': 'Вам выпал Тигран щекастый'},
    {'id': 'CAACAgIAAxkBAAENHklnNPt5YKseT8E5jYXENrQPWyRfWgAC4lsAAqPzIEkB-jrX-WEbmTYE', 'chance': 0.2, 'message': 'Вам выпал дотер Елисей'},
    {'id': 'CAACAgIAAxkBAAENHktnNPul3k2TorDo69_-BjQQ5tke5gAC-VoAAgNsIUkrUjlVWIR0ZjYE', 'chance': 0.15, 'message': 'Вам выпал победитель Влад'},
    {'id': 'CAACAgIAAxkBAAENHk1nNPuu5zn5XPuasYOWBcHrG3qawgACC1cAAjXcKUnKxRuqq1W1tDYE', 'chance': 0.20, 'message': 'Вам выпало 2 крипа'}
]


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


@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
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
