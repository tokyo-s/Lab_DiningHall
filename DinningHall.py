from config import *
from Table import Table
from Waiter import Waiter
import logging
import threading
import time

logger = logging.getLogger(__name__)


def calculate_order_mark(preparation_time, max_wait):

    if preparation_time <= max_wait:
        mark = 5
    elif preparation_time <= max_wait * 1.1:
        mark = 4
    elif preparation_time <= max_wait * 1.2:
        mark = 3
    elif preparation_time <= max_wait * 1.3:
        mark = 2
    elif preparation_time <= max_wait * 1.4:
        mark = 1
    else:
        mark = 0

    return mark


class DinningHall:
    def __init__(self, nr_waiters=NR_WAITERS, nr_tables=NR_TABLES):
        self.nr_waiters = nr_waiters
        self.nr_tables = nr_tables

        self.tables = [Table(table_id) for table_id in range(self.nr_tables)]
        self.waiters = [Waiter(waiter_id, self) for waiter_id in range(self.nr_waiters)]

        self.marks = []

    def run_test(self):
        logger.warning('Starting Dinning Hall Test')

        for waiter in self.waiters:
            threading.Thread(target=waiter.serve_tables, args=(self.tables,)).start()

        for table in self.tables:
            table.free()

    def send_distribution(self, distribution):
        waiter = self.waiters[distribution.waiter_id]
        waiter.receive_distribution(distribution)

    def calculate_order_mark(self, distribution):
        order_serving_time = int(time.time())
        distribution.order_total_preparing_time = order_serving_time - distribution.pick_up_time
        mark = calculate_order_mark(distribution.order_total_preparing_time, distribution.max_wait * TIME_UNIT / 1000)
        self.marks.append(mark)
        average_mark = sum(self.marks)/len(self.marks)
        logger.warning(f'Order {distribution.order_id} distributed, mark = {mark} '
                       f'total preparation time = {distribution.order_total_preparing_time} '
                       f'max wait = {distribution.max_wait * TIME_UNIT / 1000}')
        logger.warning(f'Average Restaurant Mark after order {distribution.order_id} is {average_mark}!!!!!!')
