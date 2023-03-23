"""Get response from a foreign API."""
import requests
from config import AGIFY_API_URL, OK


def predictage(query: dict) -> dict:
    items_dict = {
        'name': 'Unable to get name from query, defaults to Matthew',
        'age': None,
        'count': None
    }
    try:
        name = query.get('name')
    except Exception:
        print(f'{__name__}: Unable to get name from query, defaults to Matthew')
        params = {'name': 'Matthew'}
    else:
        params = {'name': name}
        items_dict['name'] = name
    response = requests.get(AGIFY_API_URL, params=params)
    if response.status_code != OK:
        print(f'{__name__}: Failed with status code {response.status_code}')
        return items_dict
    response_data = response.json()
    if not response_data:
        print(f'{__name__}: Empty content')
        return items_dict
    for key in items_dict.keys():
        if key != 'name':
            items_dict[key] = response_data.get(key)
    print(items_dict)
    return items_dict
