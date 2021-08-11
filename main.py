import csv

from ckan import process_datasets
from computers.computers import OrgStatsComputer, DatasetsStatsComputer, StatsComputer
from computers.post_filters import DateOfDatasetFilter


def write_csv(stats_computer: StatsComputer):
    print('Started writing report')
    writer = None
    with open('results.csv', 'w', newline='') as csv_file:
        if not writer:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(stats_computer.header_row())

        for row in stats_computer.to_csv_rows():
            writer.writerow(row)

    print('Finished writing report')


if __name__ == '__main__':
    post_filter = DateOfDatasetFilter('2015-12-31T23:59:59.999')
    stats_computer = DatasetsStatsComputer(post_filter=post_filter)
    process_datasets(stats_computer)
    write_csv(stats_computer)
    pass

