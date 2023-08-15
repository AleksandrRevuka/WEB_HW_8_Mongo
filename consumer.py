import pika

import time
import json

import connect
from models import Contact

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def send_message(_id):
    contact = Contact.objects(id=_id).first()
    email = contact["email"]
    return contact, email, True


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact, email, message_sent = send_message(message["id"])
    contact.update(message_sent=message_sent)
    time.sleep(1)
    print(f" [x] Done: {email}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
