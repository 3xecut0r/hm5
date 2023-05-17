import logging
import asyncio
import sys
from datetime import datetime, timedelta

import aiohttp

OPTION = sys.argv[1]
API = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='


def count_date(num, url):
    if int(num) > 10:
        return "Invalid argument"

    today = datetime.now().date()
    term = today - timedelta(days=int(num))
    term = str(term).split('-')[::-1]
    convert = '.'.join(term)
    url = url + convert
    return url


link = count_date(OPTION, API)
result = []


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(link) as response:
                if response.status == 200:
                    data = await response.json()
                    for el in data['exchangeRate']:
                        if el['currency'] == 'EUR' or el['currency'] == 'USD':
                            date = data['date']
                            currency = el['currency']
                            sale = el['saleRate']
                            purchase = el['purchaseRate']

                            convert_data = {
                                date: {
                                    currency: {
                                        'sale': sale,
                                        'purchase': purchase
                                    }
                                }
                            }

                            result.append(convert_data)
                else:
                    logging.error(f'Error status: {response.status}')
        except aiohttp.ClientConnectorError:
            logging.error(f'Connection error: {link}')
        except aiohttp.client_exceptions.InvalidURL as er: # noqa
            logging.error(f'{link}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(message)s')
    asyncio.run(main())
    print(result)
