# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import json
from io import StringIO

CSV_FORMAT_AWS = "aws"
CSV_FORMAT_REGISTERIT = "register.it"

CSV_FORMATS = [
    CSV_FORMAT_AWS,
    CSV_FORMAT_REGISTERIT,
]


class Route53RecordsetConverter(object):
    def format(self, record: dict, csv_format: str) -> dict:
        if csv_format == CSV_FORMAT_AWS:
            return self._format_aws(record)
        if csv_format == CSV_FORMAT_REGISTERIT:
            return self._format_registerit(record)
        raise ValueError("unsupported format %s" % csv_format)

    def convert(self, input_filename: str, skip_headers=True, csv_format=CSV_FORMAT_AWS):
        output = []
        with open(input_filename) as csv_file:
            if csv_format == CSV_FORMAT_REGISTERIT:
                content = csv_file.read().replace('\\', '\\\\').replace('""', '\\"')
                csv_reader = csv.reader(
                    StringIO(content), delimiter=',', doublequote=False, escapechar='\\')
            else:
                csv_reader = csv.reader(csv_file, delimiter=',')

            if skip_headers:
                next(csv_reader, None)  # skip CSV headers

            for record in csv_reader:
                formatted_record = self.format(record, csv_format)
                output.append(formatted_record)

        return self._merge_records(output)

    def _format_aws(self, record: dict) -> dict:
        record_type = record[1]

        record_name = record[0]
        if '\\052' in record_name:
            record_name = record_name.replace('\\052', '*')

        value = record[2]
        if record_type in ['CNAME', 'MX']:
            value = "%s." % value

        return {
            'name': record_name,
            'type': record_type,
            'value': [
                value
            ],
            'ttl': int(record[3]),
        }

    def _format_registerit(self, record: dict) -> dict:
        '''
        example CSV
        "NOME","TTL","TIPO","VALORE"
        "www.example.com.",600,"CNAME","example.com."
        '''

        return {
            'name': record[0],
            'type': record[2],
            'value': [
                record[3],
            ],
            'ttl': int(record[1]),
        }

    def _merge_records(self, records: list) -> list:
        record_dict = {}
        for record in records:
            key = "%s_%s" % (record['type'], record['name'])
            if not key in record_dict:
                record_dict[key] = record
                continue
            record_dict[key]['value'] += (record['value'])
        records = []
        for key in record_dict:
            records.append(record_dict[key])
        return records


def main(params):
    input_csv_file = params['<input_csv_file>']
    output_json_file = params['<output_json_file>']

    skip_headers = True
    if params.get('--no-headers-skip'):
        skip_headers = False

    csv_format = CSV_FORMAT_AWS
    if params.get('--csv-format'):
        csv_format = params.get('--csv-format')

    c = Route53RecordsetConverter()
    results = c.convert(input_csv_file, skip_headers, csv_format)

    with open(output_json_file, mode='w+') as output_file:
        output_file.write(json.dumps(results))
