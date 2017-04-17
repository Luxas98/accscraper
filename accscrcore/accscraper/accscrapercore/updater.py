import json

from collections import defaultdict

import pika
from pymongo import ASCENDING
from accscraper.accscrapercore import MongoStorage


class Updater(object):
    _connection = None

    def __init__(self):
        self.mongo = MongoStorage()
        self.mongo.db.rental_apartments.apartments.create_index([('id', ASCENDING)])
        self.current_apartments = defaultdict(set)

    def process_apartment(self, apartment):
        client = apartment['client']
        if client not in self.current_apartments:
            self.current_apartments[client] = self.mongo.get_client_apartments_ids(client)

        print('Processing apartment')
        print(apartment)
        self.mongo.insert_apartment(apartment)
        self.current_apartments[client].add(apartment['id'])


def handler_wrapper(updater):
    def handle_message(channel, method_frame, header_frame, apartment):
        """
            apartment = {
                'client': client,
                'id': id,
                'address': address,
                'price': price,
                'features': apartment_features,
                'url': url
            }

        @param channel:
        @param method_frame:
        @param header_frame:
        @param body:
        @return:
        """
        apartment = json.loads(apartment.decode("utf-8"))
        updater.process_apartment(apartment)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    return handle_message


def consume(connection):
    print('Start consuming apartments')
    channel = connection.channel()
    channel.queue_declare(queue='apartments', durable=True, exclusive=False, auto_delete=False)
    channel.basic_consume(handler_wrapper(Updater()), 'apartments')
    channel.start_consuming()


if __name__ == '__main__':
    params = pika.URLParameters("amqp://guest:guest@%s:%d/" % ("rabbitmq", 5672))
    connection = pika.BlockingConnection(params)
    consume(connection)
    connection.close()
