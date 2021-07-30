import csv

from ckan import process_datasets
from computers.computers import OrgStatsComputer, DatasetsStatsComputer, StatsComputer


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
    stats_computer = DatasetsStatsComputer()
    process_datasets(stats_computer)
    write_csv(stats_computer)
    pass

