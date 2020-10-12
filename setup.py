#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name="sacsv",
    version="1.5",
    description=u"Swiss Army csv: command-line tools to manipulate csv-formatted data",
    author=u"Gabor Nyeki",
    url="http://www.gabornyeki.com/",
    packages=["sacsv"],
    install_requires=["argh"],
    python_requires=">=3.5",
    provides=["sacsv (1.5)"],
    entry_points={
        "console_scripts": [
            "csv2jsonl = sacsv.csv2jsonl:dispatch",
            "csvaddrandom = sacsv.csvaddrandom:dispatch",
            "csvadduniqueid = sacsv.csvadduniqueid:dispatch",
            "csvaggregate = sacsv.csvaggregate:dispatch",
            "csvappend = sacsv.csvappend:dispatch",
            "csvdropdups = sacsv.csvdropdups:dispatch",
            "csvfindsortkey = sacsv.csvfindsortkey:dispatch",
            "csvkeepmax = sacsv.csvkeepmax:dispatch",
            "csvleftjoin = sacsv.csvleftjoin:dispatch",
            "csvop = sacsv.csvop:dispatch",
            "csvparallel = sacsv.csvparallel:dispatch",
            "csvrename = sacsv.csvrename:dispatch",
            "csvreorder = sacsv.csvreorder:dispatch",
            "csvsed = sacsv.csvsed:dispatch",
            "csvsort = sacsv.csvsort:dispatch",
            "csvtranspose = sacsv.csvtranspose:dispatch",
            "fw2csv = sacsv.fw2csv:dispatch",
            "longcsv2wide = sacsv.longcsv2wide:dispatch",
            "widecsv2long = sacsv.widecsv2long:dispatch",
        ],
    }
    )
