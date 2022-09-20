from flask import Flask, request
import threading
import logging

from DinningHall import DinningHall

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/distribution', methods=['POST'])
def get_distribution():
    distribution = request.json
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
