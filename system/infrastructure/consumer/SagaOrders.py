import pika
import logging
from rabbitmq import get_rabbitmq_connection, get_rabbitmq_channel
from pydantic import ValidationError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.order_exceptions import (
    OrderDoesNotExistError,
    OrderUpdateError,
)
from system.application.usecase import order_usecase
from system.application.dto.requests.order_request import (
    UpdateOrderStatusRequest,
)

logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body, app):
    with app.app_context():
        message = body.decode('utf-8')
        print(f"Received {message}")
        # Suponha que a mensagem seja um JSON contendo os dados necessários
        import json
        try:
            data = json.loads(message)
            order_id = data.get('order_id')
            new_status = data.get('status')

            # Chame o use case updateOrder com os dados extraídos
            if order_id and new_status:
                try:
                    update_order_request = UpdateOrderStatusRequest(status=new_status)
                except ValidationError as ex:
                    return ex.errors(), 400
                try:
                    order = order_usecase.UpdateOrderStatusUseCase.execute(
                        order_id=order_id, status=update_order_request.status
                    )
                except OrderDoesNotExistError:
                    return "This Order does not exist", 400
                except InfrastructureError:
                    return {"error": "Internal Error"}, 500
                except OrderUpdateError:
                    return {"error": "This Order could not be updated"}, 400
                return order.response
            else:
                print("Invalid message format")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON message: {e}")

def start_consuming(app):
    try:
        connection = get_rabbitmq_connection()
        channel = get_rabbitmq_channel(connection, 'fila-pedidos-saga-callback')
        channel.queue_declare(queue='fila-pedidos-saga-callback', durable=True)

        def on_message(ch, method, properties, body):
            callback(ch, method, properties, body, app)

        # Configuração do consumidor
        channel.basic_consume(queue='fila-pedidos-saga-callback', on_message_callback=on_message, auto_ack=True)

        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f'Failed to connect to RabbitMQ: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')