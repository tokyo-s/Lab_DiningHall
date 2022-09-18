from fastapi import FastAPI, Request
import threading
import uvicorn
import logging

from DinningHall import DinningHall

app = FastAPI()
logger = logging.getLogger(__name__)


@app.post("/distribution")
async def get_distribution(request: Request):

    distribution = await request.json()
    logger.warning('Food received')

    return {"Hello": "World"}


if __name__ == '__main__':

    threading.Thread(
        target=lambda: {
            uvicorn.run(app, host='0.0.0.0', port=8001)
        }
    ).start()

    hall = DinningHall()
    hall.run_test()
