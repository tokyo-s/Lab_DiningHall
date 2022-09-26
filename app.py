from flask import Flask, request
import threading
import logging

from DinningHall import DinningHall
from Distribution import Distribution

app = Flask(__name__)
logger = logging.getLogger(__name__)


def json_to_distribution(distribution):
    order_id = distribution['order_id']
    table_id = distribution['table_id']
    waiter_id = distribution['waiter_id']
    items = distribution['items']
    priority = distribution['priority']
    max_wait = distribution['max_wait']
    pick_up_time = distribution['pick_up_time']
    cooking_time = distribution['cooking_time']
    cooking_details = distribution['cooking_details']

    distribution_obj = Distribution(order_id, table_id, waiter_id, items, priority, max_wait,
                                    pick_up_time, cooking_time, cooking_details)

    return distribution_obj


@app.route('/distribution', methods=['POST'])
def get_distribution():
    distribution_json = request.json
    distribution = json_to_distribution(distribution_json)
    logger.warning(f'Received order {distribution.order_id}, Cooking time = {distribution.cooking_time}, '
                   f'sending for distribution')
    hall.send_distribution(distribution)
    logger.warning('Food received')

    return {}


if __name__ == '__main__':

    threading.Thread(
        target=lambda: {
            app.run(debug=True, use_reloader=False, host="0.0.0.0", port=8001)
        }
    ).start()

    hall = DinningHall()
    hall.run_test()
