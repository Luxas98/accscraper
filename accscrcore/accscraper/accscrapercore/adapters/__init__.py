import json

import pika
import pika.exceptions
from abc import ABCMeta, abstractmethod
from accscraper.accscrapercore.utils import random_pause


class Adapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_page(self, page_number):
        raise NotImplementedError

    @abstractmethod
    def process_page(self, page):
        raise NotImplementedError

    def run_scraping(self):
        page_number = 1
        while True:
            page = self.get_page(page_number)
            apartments = self.process_page(page)
            if not apartments:
                break

            RabbitMQApartmentProducer().process_apartments(apartments)
            random_pause()
            page_number += 1
            print('%s proccessed page number %s' % (self.__class__, page_number))


class RabbitMQApartmentProducer(object):
    _channel = None

    @property
    def channel(self):
        if not RabbitMQApartmentProducer._channel:
            params = pika.URLParameters("amqp://guest:guest@%s:%d/" % ("rabbitmq", 5672))
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(
                queue='apartments',
                durable=True,
                exclusive=False,
                auto_delete=False
            )

            RabbitMQApartmentProducer._channel = channel
        return RabbitMQApartmentProducer._channel

    def process_apartments(self, apartments):
        for apartment in apartments:
            try:
                self._publish(apartment)
            except pika.exceptions.ConnectionClosed:
                # IF connection closed try to reconnect and publish again
                RabbitMQApartmentProducer._channel = None
                self._publish(apartment)

    def _publish(self, apartment):
        apartment = json.dumps(apartment)
        self.channel.basic_publish(exchange='',
                                   routing_key='apartments',
                                   body=apartment,
                                   mandatory=True)
