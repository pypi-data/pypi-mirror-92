import pandas as pd
from datetime import datetime, timedelta

from .utils import fetch_first, fetch_all_pages, parse_date, date_rfc1123


def get_layer(layer, print_url=False):
    filters = {
        'layer': layer
    }
    data = fetch_all_pages('layers', filters, print_url=print_url)
    featureCollection = {
        "type": "FeatureCollection",
        "features": [doc['feat'] for doc in data],
    }
    return featureCollection


def get_covid19(ev, start_date=None, end_date=None, fmt='csv', print_url=False):
    filters = {
        'ev': ev,
        'type': 'covid19',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=print_url)
    if fmt == 'csv':
        return pd.DataFrame(data)
    return data


def get_data(ev, start_date=None, end_date=None, fmt='csv', print_url=False):
    filters = {
        'ev': ev,
    }
    if start_date and end_date:
        filters['evstart'] = {'$gte': date_rfc1123(parse_date(start_date)), '$lt': date_rfc1123(parse_date(end_date) + timedelta(days=1))}
    elif start_date:
        filters['evstart'] = {'$gte': date_rfc1123(parse_date(start_date))}
    elif end_date:
        filters['evstart'] = {'$lt': date_rfc1123(parse_date(end_date) + timedelta(days=1))}
    data = fetch_all_pages('layers.data', filters, print_url=print_url)
    if fmt == 'csv':
        return pd.DataFrame(data)
    return data


def get_daily_mobility_matrix(source_layer, target_layer, date, source=None, target=None, fmt='csv', print_url=False):
    filters = {
        'date': date,
        'source_layer': source_layer,
        'target_layer': target_layer,
    }
    if source:
        filters['source'] = source
    if target:
        filters['target'] = target
    data = fetch_all_pages('mitma_mov.daily_mobility_matrix', filters, print_url=print_url)
    if fmt == 'csv':
        return pd.DataFrame(data)
    return data


def get_population(layer, start_date=None, end_date=None, fmt='csv', print_url=False):
    filters = {
        'layer': layer,
        'type': 'population',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=print_url)
    if fmt == 'csv':
        return pd.DataFrame(data)
    return data


def get_zone_movements(layer, start_date=None, end_date=None, fmt='csv', print_url=False):
    filters = {
        'layer': layer,
        'type': 'zone_movements',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=print_url)
    if fmt == 'csv':
        return pd.DataFrame(data)
    return data
