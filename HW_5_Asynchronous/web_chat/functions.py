import asyncio
import logging

import aiohttp
from aiofile import AIOFile, LineReader
from aiopath import AsyncPath
from datetime import date, datetime, timedelta


def make_urls_for_days(number_of_days: int):
    today_is = date.today()
    urls = []
    if number_of_days >= 1:
        for day in range(number_of_days):
            formatted_date = (today_is - timedelta(days=day)).strftime("%d.%m.%Y")
            urls.append(
                "https://api.privatbank.ua/p24api/exchange_rates?json&date="
                + formatted_date
            )
        return urls
    else:
        return None


async def log_exchange_command(username):
    async with AIOFile("chat.log", "a") as afp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await afp.write(f"{timestamp}: Exchange command executed by {username}\n")


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {url}: {e}")
        return None


async def get_once_exchange():
    res = await request(
        "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    )

    exchange_usd, *_ = list(filter(lambda el: el["ccy"] == "USD", res))
    exchange_eur, *_ = list(filter(lambda el: el["ccy"] == "EUR", res))

    return f"USD: buy: {exchange_usd['buy']}, sale: {exchange_usd['sale']}. EUR: buy: {exchange_eur['buy']}, sale: {exchange_eur['sale']}"


async def get_exchange(urls) -> list:
    limit = len(urls)
    if limit > 10:
        limit = 10
        print(
            "The max value of days is 10. Now you will see currency for last 10 days."
        )
    answer = []
    for url in urls[:limit]:
        try:
            date_of_currency = url[-10:]
            currency = await request(url)
            first_exchange_rate = next(
                item for item in currency["exchangeRate"] if item["currency"] == "USD"
            )
            second_exchange_rate = next(
                item for item in currency["exchangeRate"] if item["currency"] == "EUR"
            )
            answer.append(date_of_currency)

            answer.append(
                f"USD Buy: {first_exchange_rate['saleRate']} USD Sale: {first_exchange_rate['purchaseRate']}"
            )
            answer.append(
                f"EUR Buy: {second_exchange_rate['saleRate']} EUR Sale: {second_exchange_rate['purchaseRate']}"
            )
        except AttributeError:
            print("No display data")
            return None

    return answer
