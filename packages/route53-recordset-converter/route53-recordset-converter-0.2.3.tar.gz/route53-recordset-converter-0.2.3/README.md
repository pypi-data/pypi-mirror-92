# Route53 recordset converter

This software is aimed to convert the input CSV file from [route53-transfer](https://pypi.org/project/route53-transfer/) to a JSON file which can be then used in a Terraform google_dns_record_set

## Requirements

- Python 3.7.9 or higher

## Installation

```bash
pip install route53-recordset-converter
```

## Usage

- Dump AWS Route 53 Hosted Zone records to a CSV using [route53-transfer](https://pypi.org/project/route53-transfer/)

```bash
route53-transfer dump example.com example.com.csv
```

- Convert the CSV file to a JSON one

```bash
route53-recordset-converter example.com.csv example.com.json
```

- Use the JSON in Terraform

```terraform
locals {
    dns_records = jsondecode(file("example.com.json"))
}

resource "google_dns_record_set" "dns_records" {
    for_each     = { for index, dns_record in local.dns_records : index => dns_record }
    name         = each.value.name
    managed_zone = "dns-zone-name"
    type         = each.value.type
    ttl          = each.value.ttl
    rrdatas      = each.value.value
}
```

### CSV Formats

The following CSV formats are supported:

- `aws`: AWS Route 53 standard format, as outputted by `route53-transfer`
- `register.it`: Register.it format, as exported by [www.register.it](https://www.register.it)

## In Python

You can convert the CSV without dumping them to a JSON.

```python
from route53_recordset_converter import Route53RecordsetConverter

c = Route53RecordsetConverter()

converted_results = c.convert("example.com.csv")
```
