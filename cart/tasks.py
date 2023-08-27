import requests

from celery import Celery

from celery import shared_task

from config import TOUR_API, REDIS_URL, PAYMENT_API

app = Celery(
    'tasks',
    backend=f'{REDIS_URL}',
    broker=f'{REDIS_URL}'
)


@app.task
def release_tour(bill_id, tour_id, reserve_count):
    response = requests.get(
        f"{PAYMENT_API}/bills/check/{bill_id}"
    )

    result = {
        'bill_id': bill_id,
        'tour_id': tour_id,
        'reserve_count': reserve_count,
        'canceled': True
    }

    if response.status_code != 200:
        return result

    data = response.json()

    if not data.get("payed"):
        response = requests.patch(
            f"{TOUR_API}/tour/{tour_id}/release",
            json={
                'count': reserve_count
            }
        )

        return result
    result['canceled'] = False

    return result


@app.task
def add(a, b):
    total = a + b

    return total
