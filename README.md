
# sacsv: Swiss Army csv

This Python package provides an assortment of command-line tools to manipulate csv-formatted data.
The tools are:

- `csvaddrandom`: adds a column with a random number
- `csvadduniqueid`: adds a column with a unique record identifier
- `csvaggregate`: applies an arbitrary Python function to every value of a column, possibly within groups
- `csvappend`: appends two or more csv files
- `csvdropdups`: drops duplicate records
- `csvfindsortkey`: attempts to find the column that the input is sorted by
- `csvleftjoin`: merges two csv files
- `csvop`: applies an arbitrary Python function to every record and saves the return value in a new column
- `csvreorder`: changes the order of columns
- `csvsed`: applies a substitution rule, using regular expressions, to every value of a column
- `csvsort`: sorts the input
- `csvtranspose`: transposes the input
- `longcsv2wide`: converts the input from long to wide form
- `widecsv2long`: converts the input from wide to long form

## Installation

To install this package using pip, type

```
pip install git+https://github.com/gn0/sacsv
```

or, alternatively,

```
git clone https://github.com/gn0/sacsv
pip install ./sacsv
```

## Author

Gabor Nyeki.  Contact information is on http://www.gabornyeki.com/.

## License

This package is licensed under the Creative Commons Attribution 4.0 International License: http://creativecommons.org/licenses/by/4.0/.

