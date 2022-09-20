import logging
import time
import random
import requests
import json

logger = logging.getLogger(__name__)
KITCHEN_URL = "http://kitchen-container:8000"


def send_order_to_kitchen(order):
    logger.warning('Sending order to kitchen')
    requests.post(f'{KITCHEN_URL}/order', json=order.__dict__)


class Waiter:
    def __init__(self, waiter_id):
        self.waiter_id = waiter_id

    def serve_tables(self, tables):
        while True:
            for table in tables:
                table.lock.acquire()
                if table.is_making_order():
                    table.waiting_order()
                    table.lock.release()
                    self.take_order(table)
                else:
                    table.lock.release()

    def take_order(self, table):
        order = table.generate_order(self.waiter_id)
        time.sleep(random.randint(2, 4))
        send_order_to_kitchen(order)
