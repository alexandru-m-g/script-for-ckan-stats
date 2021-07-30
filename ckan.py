import requests

from computers.computers import StatsComputer
from config import CKAN_URL, PACKAGE_SEARCH_ENDPOINT,CHUNK_SIZE


def process_datasets(stats_computer: StatsComputer) -> [dict]:
    start = 0
    while True:
        base_url = CKAN_URL + PACKAGE_SEARCH_ENDPOINT
        # full_url = '{}?ext_compute_freshness=for-data-completeness&start={}&rows={}&fq=type:dataset -extras_archived:true'.format(base_url, start, CHUNK_SIZE)
        full_url = '{}?start={}&rows={}&fq=type:dataset organization:reach-initiative -extras_archived:true'.format(base_url, start, CHUNK_SIZE)
        start += CHUNK_SIZE
        print('Getting data from: ' + full_url)
        headers = {
            'Content-Type': 'application/json',
            # 'Authorization': os.environ.get('API_KEY')
        }
        response = requests.request("GET", full_url, headers=headers)
        response.raise_for_status()
        dataset_list = response.json()['result']['results']
        for dataset in dataset_list:
            stats_computer.process_dataset(dataset)
        print('Processed {} datasets'.format(start))

        if len(dataset_list) < CHUNK_SIZE:
            break
