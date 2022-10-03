import logging
import threading
import time
import random
import requests
from config import TIME_UNIT

logger = logging.getLogger(__name__)
KITCHEN_URL = "http://kitchen-container:8000"


def send_order_to_kitchen(order):
    logger.warning(f'Waiter {order.waiter_id} sends order {order.order_id} to kitchen')
    requests.post(f'{KITCHEN_URL}/order', json=order.__dict__)


class Waiter:
    def __init__(self, waiter_id, dinning_hall):
        self.waiter_id = waiter_id
        self.dinning_hall = dinning_hall
        self.distributions = []
        self.distribution_lock = threading.Lock()
        self.serving_tables = {}

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

            self.serve_distribution()

    def take_order(self, table):
        time.sleep(random.randint(2, 4) * TIME_UNIT / 1000)
        order = table.generate_order(self.waiter_id)
        self.serving_tables[table.table_id] = table
        table.waiting_order()
        send_order_to_kitchen(order)

    def receive_distribution(self, distribution):
        self.distribution_lock.acquire()
        self.distributions.append(distribution)
        self.distribution_lock.release()

        logger.warning(f'Waiter {self.waiter_id} received order {distribution.order_id}.')

    def serve_distribution(self):
        self.distribution_lock.acquire()

        for distribution in self.distributions:
            if distribution.table_id not in self.serving_tables:
                logger.warning(f'Distribution {distribution.order_id} gone to wrong Waiter - {self.waiter_id}')
                continue

            if not self.serving_tables[distribution.table_id].validate_order(distribution):
                logger.warning(f'Distribution order {distribution.order_id} is wrong')
                continue

            self.dinning_hall.calculate_order_mark(distribution)
            self.serving_tables[distribution.table_id].free()
            del self.serving_tables[distribution.table_id]

        self.distributions.clear()
        self.distribution_lock.release()

