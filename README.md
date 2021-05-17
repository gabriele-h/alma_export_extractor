# About
For some analyses it is necessary to compare large amounts of data. We
often make exports for that. Since for now it is not possible to make
use of XSLT on BIB exports, we make full exports and then filter them
with a python script.

# xml\_extract.py

## Usage

```bash
python xml_extractor.py input.xml output.csv leader,001,773
```

### All subfields
If no subfields are provided in the filter, all subfields are prefixed 
with "$$<subfield-code>" and concatenated to one cell.

It is possible to provide no indicators at all or to replace one of them
with an asterisk.

```bash
python xml_extractor.py input.xml output.csv 100,245**,77308
```

### Specific subfields with any indicators
If indicators are irrelevant, but you want to filter for specific subfields,
both indicators must be replaced with asterisks

```bash
python xml_extractor.py input.xml output.csv 245**a,245**b
```

It is important to not have any spaces within the filter-parameter.

# column\_splitter.py

If you want to split multiple occurrances of the same field (or subfield)
into their own columns, you can use column_splitter.

## Usage

```bash
python column\_splitter.py input.csv output.csv
```

## Explanation
This will look for the delimiter '-||-', which is used to separate
repeated categories within one cell. If you use the optional
`--subfield`, the script will also look for '$$' and split by these
within the same iteration, splitting all subfields into their own
column regardless of in which field they were found.

All original columns from the input-file are preserved. The split
versions are listed directly after with numeric suffixes in parentheses
(e.g. "773(1)" is the first field).

## Custom Delimiter
If you need to use a custom delimiter, you can use `--delimiter`.

# License
[GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html), see also LICENSE.md

# Author
Gabriele Höfler