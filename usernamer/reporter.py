import csv

from io import StringIO
from time import time


class Reporter:
    def __init__(self, data):
        self.data = data
        self.filename = f'users_report_{int(time())}.csv'

    @property
    def header(self):
        return self.data[0].keys()

    @property
    def csv(self):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=self.header, delimiter=';')
        writer.writeheader()
        writer.writerows(self.data)
        csv_report = output.getvalue()
        output.close()
        return csv_report.encode('utf-8-sig')
