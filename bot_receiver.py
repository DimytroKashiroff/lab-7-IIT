# Lab7ReceiverBot – перевіряє чергу та надсилає повідомлення
import pika
import asyncio
from telegram import Bot

bot_token = "7560158248:AAF2WtTCAKiwF3uHQtKuMSMw2cKqIn-uXuk"
chat_id = "1008720046"  # заміни на свій реальний chat_id

bot = Bot(token=bot_token)

# Отримати повідомлення з RabbitMQ
def get_messages_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='lab7_queue')

    method_frame, header_frame, body = channel.basic_get(queue='lab7_queue', auto_ack=True)
    connection.close()
    return body.decode() if body else None

# Цикл перевірки кожні 15 хв
async def check_queue():
    while True:
        message = get_messages_from_rabbitmq()
        if message:
            await bot.send_message(chat_id=chat_id, text=f"Викладач {message} почав віддалену пару")
        await asyncio.sleep(30)  # кожні 30 secynd

# Запуск
if __name__ == '__main__':
    print("Lab7ReceiverBot is running...")
    asyncio.run(check_queue())
