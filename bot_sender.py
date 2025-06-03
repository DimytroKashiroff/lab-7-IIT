import pika

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги (якщо ще не існує)
channel.queue_declare(queue='lab7_queue')

# Надсилання повідомлення
message = 'Hello from sender!'
channel.basic_publish(exchange='', routing_key='lab7_queue', body=message)
print(f"[x] Sent: {message}")

# Закриваємо з'єднання
connection.close()
