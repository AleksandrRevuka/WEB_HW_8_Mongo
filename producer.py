import pika

from datetime import datetime

import json

import connect
from models import Contact


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="task_mock", exchange_type="direct")
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_bind(exchange="task_mock", queue="task_queue")


def main():
    contacts = Contact.objects()
    for contact in contacts:
        message = {"id": str(contact.id)}

        channel.basic_publish(
            exchange="task_mock",
            routing_key="task_queue",
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == "__main__":
    main()
