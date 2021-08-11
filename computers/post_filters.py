from abc import ABC, abstractmethod
from dateutil import parser


class PostFilter(ABC):
    @abstractmethod
    def allow_dataset(self, dataset: dict) -> bool:
        pass


class DateOfDatasetFilter(PostFilter):

    def __init__(self, max_date_str: str) -> None:
        super().__init__()
        self.max_date = parser.parse(max_date_str)

    def allow_dataset(self, dataset: dict) -> bool:
        dataset_date: str = dataset['dataset_date']
        temp_range = dataset_date.replace('[', '').replace(']', '')
        start_date_str, end_date_str = temp_range.split(' TO ')
        end_date = None if end_date_str == '*' else parser.parse(end_date_str)
        if end_date:
            return end_date < self.max_date
        return False
