import sys
import aiohttp
import asyncio
import logging
import platform
import dataclasses
from typing import List
from logging import Logger
from datetime import datetime, timedelta


@dataclasses.dataclass
class Query:
    dates: List[datetime]
    currencies: set


@dataclasses.dataclass
class Currency:
    name: str
    currency_sale: str
    currency_buy: str


@dataclasses.dataclass
class Request:
    url: str
    date: datetime

    @property
    def full_url(self) -> str:
        return f"{self.url}?json&date={self.date.strftime('%d.%m.%Y')}"


class CurrencyRateAPI:
    def __init__(self, base_url: str, logger: Logger) -> None:
        self.base_url = base_url
        self.logger = logger

    async def get_currency_rates(self, dates: List[datetime]) -> list[dict]:
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.__execute_request(session, Request(self.base_url, date)) for date in dates]
            results = await asyncio.gather(*tasks)
        return results

    async def __execute_request(self, session: aiohttp.ClientSession, req: Request) -> dict | None:
        try:
            await asyncio.sleep(1/50)
            async with session.get(req.full_url) as response:
                if response.status == 200:
                    result = await response.json()                    
                    return result
                else:
                    self.logger.error(f"An error occurred. Error status: {response.status}")
                    return None
        except aiohttp.ClientConnectorError as err:
            self.logger.error(f"Connection error occurred: {req.full_url} {str(err)}")
            return None
           

class CurrencyRateConsoleUtility:
    def __init__(self, api: CurrencyRateAPI, logger: Logger) -> None:
        self.api: CurrencyRateAPI = api
        self.logger = logger

    def __ensure_uppercase_currencies(self, query: Query) -> None:
        query.currencies = set([currency.upper() for currency in query.currencies])

    def parse_input(self, days, currencies: list) -> Query:
        if not sys.argv[1].isdigit():
            raise ValueError("Invalid input: Please enter a digit for days")
        days = int(days)
        if not 1 <= days <= 10:
            raise ValueError("Invalid number of days. Enter value between 1 and 10")
                       
        today = datetime.now()
        dates = []
        for i in range(days):
            date = today - timedelta(days=i)
            dates.append(date)
        currencies = {"USD", "EUR"}.union(currencies)
        query = Query(dates, currencies)
        self.__ensure_uppercase_currencies(query)
        return query
    
    def __compose_currency(self, rate: dict) -> Currency:
        name = rate["currency"]
        buy = rate["purchaseRate"] if "purchaseRate" in rate.keys() else rate["purchaseRateNB"]
        sale = rate["saleRate"] if "saleRate" in rate.keys() else rate["saleRateNB"]
        return Currency(name, sale, buy)
    
    async def query_currency_rates(self, query: Query) -> dict[str, List[Currency]]:
        if not query:
            return {}
        self.__ensure_uppercase_currencies(query)
        all_rates = await self.api.get_currency_rates(query.dates)
        formatted_rates = dict[str, List[Currency]]()
        for rate in all_rates:
            date = rate["date"]
            filtered_rates = [self.__compose_currency(r) for r in rate['exchangeRate'] if r['currency'] in query.currencies]
            formatted_rates[date] = filtered_rates
        return formatted_rates


def pretty_print_result(dct: dict) -> None:
    for date, currencies in dct.items():
        print(f"{'=':=^{27}}")
        print(f"Date: {date}")
        print(f"{'-':-^{27}}")
        if not currencies:
            print("No data available")
        else:
            print("{:^10}|{:^8}|{:^8}".format("Currency", "Buy", "Sale"))
            print(f"{'-':-^{27}}")
            for currency in currencies:
                print(f"{currency.name:^10}|{currency.currency_buy:^8.2f}|{currency.currency_sale:^8.2f}")
        print(f"{'=':=^{27}}")


async def main():
    logger = logging.getLogger(__name__)
    result = None

    try:
        days = sys.argv[1]
        currencies = sys.argv[2:] if len(sys.argv) > 2 else []
        
        api = CurrencyRateAPI("https://api.privatbank.ua/p24api/exchange_rates", logger)
        utility = CurrencyRateConsoleUtility(api, logger)
       
        result = await utility.query_currency_rates(utility.parse_input(days, currencies))
    except IndexError as err:
        print("The required parameter <number_of_days> is missing")
        sys.exit()
    except ValueError as err:
        print(err)
        sys.exit()
    return result

        
if __name__ == '__main__':
    if platform.system() == "Windows":

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        r = asyncio.run(main())
        pretty_print_result(r)