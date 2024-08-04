import pika
import logging
from rabbitmq import get_rabbitmq_connection, get_rabbitmq_channel

logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body):
    print(f"Received {body}")

def start_consuming():
    try:
        connection = get_rabbitmq_connection()
        channel = get_rabbitmq_channel(connection, 'fila-pedidos-saga-callback')
        # Declaração da fila
        channel.queue_declare(queue='fila-pedidos-saga-callback', durable=True)

        # Configuração do consumidor
        channel.basic_consume(queue='fila-pedidos-saga-callback', on_message_callback=callback, auto_ack=True)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f'Failed to connect to RabbitMQ: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')