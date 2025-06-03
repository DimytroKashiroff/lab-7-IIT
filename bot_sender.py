import pika
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Функція надсилання повідомлення в RabbitMQ
def send_to_rabbitmq(username, text):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='lab7_queue')
    message = f"{username}: {text}"
    channel.basic_publish(exchange='', routing_key='lab7_queue', body=message)
    connection.close()

# Обробка повідомлення від користувача
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or update.effective_user.first_name
    text = update.message.text
    send_to_rabbitmq(username, text)
    await update.message.reply_text("Повідомлення надіслано!")

# Запуск Telegram-бота
if __name__ == '__main__':
    app = ApplicationBuilder().token("ТВОКЕН_ТУТ").build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot No1 is running...")
    app.run_polling()
