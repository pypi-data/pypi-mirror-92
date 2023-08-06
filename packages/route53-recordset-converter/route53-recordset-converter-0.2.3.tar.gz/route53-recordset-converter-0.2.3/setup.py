import os
from setuptools import setup

from route53_recordset_converter import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='route53-recordset-converter',
    version=__version__,
    description='Converts an input CSV file from route53-transfer to a JSON file which can be then used in a Terraform google_dns_record_set',
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    url='http://github.com/giefferre/route53-recordset-converter',
    author='Gianfranco Reppucci',
    author_email='gianfranco@reppucci.it',
    license='Apache License 2.0',
    packages=['route53_recordset_converter'],
    scripts=['bin/route53-recordset-converter'],
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Utilities'
    ]
)
