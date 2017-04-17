from time import sleep
import re
import random


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def random_pause():
    random_sleep_time = random.random() + random.randint(1, 5)
    sleep(random_sleep_time)