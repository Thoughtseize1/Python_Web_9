import argparse
import asyncio
from datetime import date, datetime, timedelta

import aiohttp
import logging
import platform

from prettytable import PrettyTable


parser = argparse.ArgumentParser()
parser.add_argument(
    "days", type=int, help="An integer count of days", nargs="?", default=3
)
parser.add_argument(
    "-f",
    "--first_currency",
    type=str,
    help="First desired currency",
    nargs="?",
    default="USD",
)
parser.add_argument(
    "-s",
    "--second_currency",
    type=str,
    help="Sirst desired currency",
    nargs="?",
    default="EUR",
)
args = parser.parse_args()
days = args.days
first_currency = args.first_currency
second_currency = args.second_currency

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


def print_result(urls) -> None:
    limit = len(urls)
    if limit > 10:
        limit = 10
        print(
            "The max value of days is 10. Now you will see currency for last 10 days."
        )
    table_with_currency = PrettyTable(["Currency:", "Sale:", "Buy:"])
    for url in urls[:limit]:
        try:
            date_of_currency = url[-10:]
            currency = asyncio.run(request(url))
            first_exchange_rate = next(
                item
                for item in currency["exchangeRate"]
                if item["currency"] == first_currency
            )
            second_exchange_rate = next(
                item
                for item in currency["exchangeRate"]
                if item["currency"] == second_currency
            )
            table_with_currency.add_row(["    ", date_of_currency, "    "])
            table_with_currency.add_row(
                [
                    first_currency,
                    first_exchange_rate["saleRate"],
                    first_exchange_rate["purchaseRate"],
                ]
            )
            table_with_currency.add_row(
                [
                    second_currency,
                    second_exchange_rate["saleRate"],
                    second_exchange_rate["purchaseRate"],
                ]
            )
        except AttributeError:
            print("No display data")
            return None
    table_string = table_with_currency.get_string()
    print(table_string)


def make_urls_for_days(number_of_days):
    today_is = date.today()
    urls = []
    for day in range(number_of_days):
        formatted_date = (today_is - timedelta(days=day)).strftime("%d.%m.%Y")
        urls.append(
            "https://api.privatbank.ua/p24api/exchange_rates?json&date="
            + formatted_date
        )
    return urls


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print_result(make_urls_for_days(days))
