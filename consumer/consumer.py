import asyncio
import json
import os
import pika
import requests

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')


# ======================
#  DISCORD LOGIC
# ======================
def send_discord_message(message):
    """
    Send a message to a Discord channel using a webhook.
    """
    print(f"[Discord] Sending message: {message}", flush=True)
    headers = {'Content-Type': 'application/json'}
    price = round(float(message['price']), 2)

    data = {
        'content': f"""
        **New Report!**
        On {message['date']}, the store {message['store']} sold:
        - {message['cones']} cones
        - {message['cups']} cups
        Total price: {price} BGN
        They left the following notes: {message['notes']}
        The following ice creams were sold:
        {' '.join([f"{item['quantity']} {item['ice_cream']}{' (needs refill)' if item['need_refill'] else ''}" for item in message['items']])}
        """
    }

    response = requests.post(DISCORD_WEBHOOK_URL, headers=headers, data=json.dumps(data))

    if response.status_code != 204:
        print(f"[Discord] Error sending message: {response.text}", flush=True)

        for _ in range(3):
            response = requests.post(DISCORD_WEBHOOK_URL, headers=headers, data=json.dumps(data))
            if response.status_code == 204:
                print(f"[Discord] Message sent successfully!", flush=True)
                break
            else:
                print(f"[Discord] Error sending message: {response.text}", flush=True)

    if response.status_code == 204:
        print(f"[Discord] Message sent successfully!", flush=True)


# ======================
#  RABBITMQ LOGIC
# ======================
def rabbitmq_consumer():
    print("[RabbitMQ] Connecting to RabbitMQ...", flush=True)
    """
    Connect to RabbitMQ, consume messages from the queue, and schedule
    a Discord send operation in the event loop when a message arrives.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)


    def callback(ch, method, properties, body):
        """
        This function is called whenever a new message arrives
        in the RabbitMQ queue.
        """
        message_text = body.decode('utf-8')
        print(f"[RabbitMQ] Received message: {message_text}", flush=True)

        # Schedule the Discord message send on the bot's event loop
        send_discord_message(json.loads(message_text))
        # Acknowledge the message so it’s not re-delivered
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=False
    )

    print("[RabbitMQ] Starting to consume...", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[RabbitMQ] Error consuming messages: {e}", flush=True)
    finally:
        channel.stop_consuming()
        connection.close()


# ======================
#  MAIN STARTUP
# ======================
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(rabbitmq_consumer())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
