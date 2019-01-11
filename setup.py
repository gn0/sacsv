#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='sacsv',
    version='1.1',
    description=u'Swiss Army csv: command-line tools to manipulate csv-formatted data',
    author=u'Gabor Nyeki',
    url='http://www.gabornyeki.com/',
    packages=['sacsv'],
    install_requires=['argh'],
    provides=['sacsv (1.1)'],
    entry_points={
        'console_scripts': [
            'csvaddrandom = sacsv.csvaddrandom:dispatch',
            'csvadduniqueid = sacsv.csvadduniqueid:dispatch',
            'csvaggregate = sacsv.csvaggregate:dispatch',
            'csvappend = sacsv.csvappend:dispatch',
            'csvdropdups = sacsv.csvdropdups:dispatch',
            'csvfindsortkey = sacsv.csvfindsortkey:dispatch',
            'csvkeepmax = sacsv.csvkeepmax:dispatch',
            'csvleftjoin = sacsv.csvleftjoin:dispatch',
            'csvop = sacsv.csvop:dispatch',
            'csvrename = sacsv.csvrename:dispatch',
            'csvreorder = sacsv.csvreorder:dispatch',
            'csvsed = sacsv.csvsed:dispatch',
            'csvsort = sacsv.csvsort:dispatch',
            'csvtranspose = sacsv.csvtranspose:dispatch',
            'longcsv2wide = sacsv.longcsv2wide:dispatch',
            'widecsv2long = sacsv.widecsv2long:dispatch',
        ],
    }
    )
