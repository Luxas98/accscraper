from time import sleep
from typing import List
import random
from accscraper.accscrapercore.adapters import Adapter
from accscraper.accscrapercore.adapters.pararius_adapter import ParariusAdapter


class AdapterControler(object):
    def __init__(self, adapters):
        self.adapters = adapters  # type: List[Adapter]

    def process_adapters(self):
        print('Processing adapters')
        while True:
            for a in self.adapters:
                print('[%s] Processing adapter' % a.__class__)
                a.run_scraping()
            # TODO: use scheduler? run in specific hour between 12:00 - 13:00?
            sleep(86400 - random.randint(1, 7200))


if __name__ == '__main__':
    adapters = []  # type: List[Adapter]
    adapter = ParariusAdapter()
    adapters.append(adapter)

    ctrl = AdapterControler(adapters)
    ctrl.process_adapters()
