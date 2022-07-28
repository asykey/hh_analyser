import os
import csv


class FileWriter:
    def __init__(self, filename: str):
        self.fields = None
        self.filename = filename

    def __reload_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def set_fields(self, fields: list):
        self.fields = fields
        self.__reload_file()
        with open(self.filename, 'a', encoding='utf-8') as outfile:
            csv.DictWriter(outfile, fieldnames=fields, delimiter=';').writeheader()

    def write_data(self, data: dict):
        with open(self.filename, 'a', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=self.fields, delimiter=';')
            writer.writerow(data)

