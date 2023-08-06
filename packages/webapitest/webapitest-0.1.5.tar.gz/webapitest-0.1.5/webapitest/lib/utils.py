import csv
import codecs
import logging

logger = logging.getLogger('webapitest')


def write_csv(csv_path, data):
    f = codecs.open(csv_path, 'w', 'utf_8_sig')
    csv_writer = csv.writer(f)
    for line in data:
        csv_writer.writerow(line)
    f.close()


def read_csv(path: str) -> list:
    data = []
    f = open(path, 'r')
    reader = csv.reader(f)
    content = next(reader)
    for line in content:
        data.append(line)
    f.close()
    return data
