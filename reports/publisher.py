import os
import json
import pika


def publish_report_to_rabbitmq(report):
    """
    Publishes a new Report (including all its ReportItems)
    to a RabbitMQ queue in JSON format.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_USER"),
                os.getenv("RABBITMQ_PASS"),
            )
        )
    )
    channel = connection.channel()

    queue_name = os.getenv("RABBITMQ_QUEUE")
    channel.queue_declare(queue=queue_name, durable=True)

    data = {
        "store": report.store.name,
        "date": report.date.strftime("%d/%m/%Y"),
        "is_rainy": report.is_rainy,
        "cones": report.cones,
        "cups": report.cups,
        "price": str(report.price),
        "notes": report.notes,
        "items": [
            {
                "ice_cream": item.ice_cream.type.name,
                "quantity": str(item.quantity),
                "need_refill": item.need_refill,
            }
            for item in report.items.all()
        ],
    }

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
        )
    )

    print(f"Published Report {report.id} with {len(data['items'])} items to RabbitMQ.")

    connection.close()
