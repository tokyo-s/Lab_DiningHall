from config import *
from Table import Table
from Waiter import Waiter
import logging
import threading
import time

logger = logging.getLogger(__name__)


class DinningHall:
    def __init__(self, nr_waiters=NR_WAITERS, nr_tables=NR_TABLES):
        self.nr_waiters = nr_waiters
        self.nr_tables = nr_tables

        self.tables = [Table(table_id) for table_id in range(self.nr_tables)]
        self.waiters = [Waiter(waiter_id) for waiter_id in range(self.nr_waiters)]

    def run_test(self):
        logger.warning('Starting Dinning Hall Test')

        for waiter in self.waiters:
            threading.Thread(target=waiter.serve_tables, args=(self.tables,)).start()

    def send_distribution(self, distribution):
        time.sleep(2)
        self.tables[distribution['table_id']].making_order()
