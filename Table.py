import threading
from config import MENU, FOOD_LIMIT, PRIORITY_LIMIT, TIME_UNIT
from Order import Order
import random
import time
import uuid
import logging

logger = logging.getLogger(__name__)


class Table:
    def __init__(self, table_id, status='Making order'):
        self.status = status
        self.order = None
        self.table_id = table_id
        self.lock = threading.Lock()

    def waiting_order(self):
        self.status = 'Waiting order'

    def making_order(self):
        self.status = 'Making order'

    def free(self):

        logger.warning(f'Table {self.table_id} if free')
        self.order = None
        self.status = 'Free'

        threading.Thread(target=self.wait_for_new_clients).start()

    def is_free(self):
        return self.status == 'Free'

    def is_making_order(self):
        return self.status == 'Making order'

    def generate_order(self, waiter_id):

        nr_foods = random.randint(1, FOOD_LIMIT)
        items = random.choices(MENU, k=nr_foods)
        item_ids = [item['id'] for item in items]
        priority = random.randint(1, PRIORITY_LIMIT)

        max_wait = 1.3 * max([food_item['preparation-time'] for food_item in items])  # preparation-time_

        self.order = Order(order_id=str(uuid.uuid4()), table_id=self.table_id, waiter_id=waiter_id,
                           items=item_ids, priority=priority, max_wait=max_wait, pick_up_time=time.time())

        return self.order

    def validate_order(self, distribution):
        if not self.order or self.order.order_id != distribution.order_id:
            return False
        return True

    def wait_for_new_clients(self):
        time.sleep(random.randint(2, 4) * TIME_UNIT / 1000)
        self.making_order()

        logger.info(f"Table {self.id} waiting for the waiter")
