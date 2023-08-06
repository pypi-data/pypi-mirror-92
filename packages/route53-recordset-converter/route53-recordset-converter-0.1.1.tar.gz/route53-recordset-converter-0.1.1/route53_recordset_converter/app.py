# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import json


class Route53RecordsetConverter(object):
    def convert(self, input_filename: str, skip_headers=True):
        output = []
        with open(input_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip CSV headers

            for row in csv_reader:
                record_type = row[1]

                record_name = row[0]
                if '\\052' in record_name:
                    record_name = record_name.replace('\\052', '*')

                value = row[2]
                if record_type in ['CNAME', 'MX']:
                    value = "%s." % value

                output.append({
                    'name': record_name,
                    'type': record_type,
                    'value': [
                        value
                    ],
                    'ttl': int(row[3]),
                })
        return output


def main(params):
    input_csv_file = params['<input_csv_file>']
    output_json_file = params['<output_json_file>']
    skip_headers = True
    if params.get('--no-headers-skip'):
        skip_headers = False

    c = Route53RecordsetConverter()
    results = c.convert(input_csv_file, skip_headers)

    with open(output_json_file, mode='w+') as output_file:
        output_file.write(json.dumps(results))
