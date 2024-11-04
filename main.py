from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ваш Telegram ID, куда будут приходить сообщения
ADMIN_ID = '1812220468'

# Словарь для хранения отправителей и их сообщений
user_message_map = {}

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку\n\n"
        "🖊 Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого\n\n"
        "Отправить можно 💬 текст, 🔉 аудио, 📹 видеосообщения."
    )

# Обработчик текстовых сообщений
def handle_text(update: Update, context: CallbackContext):
    user = update.effective_user
    username = f"@{user.username}" if user.username else f"ID {user.id}"
    user_message_map[update.message.message_id] = user.id

    admin_message = f"У тебя новый вопрос от {username}\n\"{update.message.text}\""
    context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # Отправка второго сообщения с самим текстом
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Братан, у тебя новое сообщение динь дон:\n\"{update.message.text}\"")

# Обработчик ответов на сообщения
def forward_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.reply_to_message.message_id in user_message_map:
        original_user_id = user_message_map[update.message.reply_to_message.message_id]
        context.bot.send_message(chat_id=original_user_id, text=update.message.text)

def main():
    # Вставьте свой токен бота
    TOKEN = '7330511100:AAEurVlLEoHMa-svccTgVUrZNqBduyqZCRU'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.reply & Filters.text, forward_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
