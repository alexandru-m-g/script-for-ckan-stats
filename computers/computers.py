from abc import ABC, abstractmethod
from typing import Iterable


class StatsComputer(ABC):
    @abstractmethod
    def process_dataset(self, dataset: dict):
        pass

    @abstractmethod
    def to_csv_rows(self) -> Iterable[Iterable]:
        pass

    @abstractmethod
    def header_row(self) -> Iterable:
        pass


class OrgStatsComputer(StatsComputer):

    csv_header = 'organization_name', 'organization_title', 'fresh_datasets', 'not_fresh_datasets', \
                 'tagged_datasets', 'not_tagged_datasets'


    def __init__(self) -> None:
        self.org_map = {}

    def process_dataset(self, dataset: dict):
        name = dataset['organization']['name']
        title = dataset['organization']['title']
        has_tags = len(dataset.get('tags', []))
        is_fresh = dataset.get('is_fresh', False)

        org_dict = self.org_map.get(name)
        if not org_dict:
            org_dict = {
                'title': title,
                'fresh_datasets': 0,
                'not_fresh_datasets': 0,
                'tagged_datasets': 0,
                'not_tagged_datasets': 0,
            }
            self.org_map[name] = org_dict

        if is_fresh:
            org_dict['fresh_datasets'] += 1
        else:
            org_dict['not_fresh_datasets'] += 1
        if has_tags:
            org_dict['tagged_datasets'] += 1
        else:
            org_dict['not_tagged_datasets'] += 1

    def to_csv_rows(self):
        return ((org_name, org_dict['title'], org_dict['fresh_datasets'], org_dict['not_fresh_datasets'],
                 org_dict['tagged_datasets'], org_dict['not_tagged_datasets'])
                for org_name, org_dict in self.org_map.items())

    def header_row(self) -> Iterable:
        return self.csv_header


class DatasetsStatsComputer(StatsComputer):

    csv_header = 'dataset_name', 'dataset_title', 'number_of_resources', 'org_name', 'org_title'

    def __init__(self) -> None:
        self.datasets = []

    def process_dataset(self, dataset: dict):
        org_name = dataset['organization']['name']
        org_title = dataset['organization']['title']
        dataset_name = dataset['name']
        dataset_title = dataset['title']
        resources_num = len(dataset.get('resources', []))

        self.datasets.append((dataset_name, dataset_title, resources_num, org_name, org_title))

    def to_csv_rows(self):
        return self.datasets

    def header_row(self) -> Iterable:
        return self.csv_header

