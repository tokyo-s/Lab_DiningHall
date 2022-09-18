import logging
import requests

logger = logging.getLogger(__name__)
KITCHEN_URL = "http://kitchen-container:8000"


class Waiter:
    def __init__(self, waiter_id):
        self.waiter_id = waiter_id

    def serve_tables(self, tables):
        while True:
            for table in tables:
                if table.is_making_order():
                    table.waiting_order()
                    self.take_order(table)


    def take_order(self, table):
        order = table.generate_order(self.waiter_id)
        ## TODO: include here time needed for order to be taken (2,4) seconds
        logger.warning('Sending order to kitchen')
        self.send_order_to_kitchen(order)


    def send_order_to_kitchen(self, order):
        logger.warning('Sending order to kitchen')
        requests.post(f'{KITCHEN_URL}/order', json=order.__dict__)
