from .config import MENU
import random
import time
import uuid


class Table:
    def __init__(self, table_id, status='Free'):
        self.status = status
        self.order = None
        self.table_id = table_id

    def waiting_order(self):
        self.status = 'Waiting order'

    def making_order(self):
        self.status = 'Making order'

    def free(self):
        self.status = 'Free'

    def is_free(self):
        return self.status == 'Free'

    def is_making_order(self):
        return self.status == 'Making order'

    def generate_order(self, waiter_id):

        nr_foods = random.randint(1, 4)
        items = random.choices(MENU, k=nr_foods)
        item_ids = [item['id'] for item in items]
        priority = random.randint(1, 5)

        max_wait = 1.3 * max([food_item['preparation-time'] for food_item in items])  # preparation-time_

        self.order = {
            "order_id": str(uuid.uuid4()),
            "table_id": self.table_id,
            "waiter_id": waiter_id,
            "items": item_ids,
            "priority": priority,
            "max_wait": max_wait,
            "pick_up_time": time.time()
        }

        return self.order
