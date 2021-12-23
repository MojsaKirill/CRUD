import asyncio
import json
from datetime import datetime, timedelta
from typing import List

import httpx
from dateutil.rrule import DAILY, rrule


async def get_rate_date_code(date: str, code: str = None):
    """
    https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate=2021-11-01
    https://www.nbrb.by/api/exrates/rates?ondate=2021-11-01&periodicity=0
    """
    q = asyncio.Queue(maxsize=50)
    response = []
    consumers = []
    producers = []

    dt_start = datetime.strptime(date, '%Y-%m-%d')
    dt_stop = datetime.now() + timedelta(days=3)
    for dt in rrule(DAILY, dtstart=dt_start, until=dt_stop):
        consumers.append(_consumer(q, response))
        producers.append(_producer(q, dt.strftime('%Y-%m-%d'), code))

    await asyncio.gather(*producers)
    await asyncio.gather(*consumers)
    return response


async def _get_rate(date: str, code: str = None):
    #TODO
    main_url = 'https://www.nbrb.by/api/exrates/rates'
    if not code:
        url = main_url + f'?ondate={date}&periodicity=0'
    else:
        url = main_url + f'/{code}?parammode=2&ondate={date}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    result = json.loads(response.text)
    return result


async def _producer(queue: asyncio.Queue, date: str, code: str = None):
    await queue.put(_get_rate(date=date, code=code))


async def _consumer(queue: asyncio.Queue, resp: List):
    result = await (await queue.get())
    if isinstance(result, list):
        resp.extend(result)
    else:
        resp.append(result)
