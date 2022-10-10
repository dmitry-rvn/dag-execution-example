from datetime import date

import requests


API_URL = 'https://www.nbrb.by/api/exrates/rates'
API_DATE_FORMAT = '%Y-%m-%d'


def get_currency_rate(currency_code: str, dt: date) -> float:
    response = requests.get(
        url=f'{API_URL}/{currency_code}',
        params={'parammode': 2, 'ondate': dt.strftime(API_DATE_FORMAT)}
    )
    data = response.json()
    return round(data['Cur_OfficialRate'] / data['Cur_Scale'], 6)
