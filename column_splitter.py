"""
Delimited Columns splitten. Funktioniert nur für Spalten mit einmaligen
Namen, weil csv.DictReader verwendet wird.
"""

from argparse import ArgumentParser
import collections
from csv import DictReader, DictWriter, QUOTE_ALL
from pathlib import Path

parser = ArgumentParser(
    description='Split output created by xml_extract.py while retaining the '
                'original columns. Useful for splitting multiple occurrences '
                'of the same field into their own columns. After that you '
                'may split all subfields with --subfields.',
    epilog="CAUTION: If the same output file is used twice, data will be "
           "appended to the existing file!"
)
parser.add_argument(
    'input_csv',
    type=Path,
    help="File containing output from xml_extract.py"
)
parser.add_argument(
    'output_csv',
    type=Path,
    help="File to write the split version of the csv to."
)
parser.add_argument(
    '--subfields',
    help="Use to split further into subfields after field-split. Indicators "
         "will be removed from the result.",
    action='store_true'
)
parser.add_argument(
    '--delimiter',
    type=str,
    help="Use if your data contains '-||-' and you need to override the "
         "default delimiter."
)
args = parser.parse_args()

csv_input = args.input_csv
csv_output = args.output_csv

subfields = args.subfields

if args.delimiter:
    delim = args.delimiter
else:
    delim = '-||-'

sf_delim = '$$'


def rewrite_csv(input_file, output_file):
    """
    Analyse the number of columns necessary to do the splitting.
    :param input_file: Path to the input file including the file's name
    :param output_file: Path to the output file including the file's name
    :return: Dictionary with number of columns per column
    """
    header_dict = collections.defaultdict(int)

    # https://stackoverflow.com/questions/13590749/reading-unicode-file-data-with-bom-chars-in-python/44573867#44573867
    with open(input_file, 'r', encoding="utf-8-sig", newline="") as file:

        reader = DictReader(file, delimiter=';')

        for row in reader:
            for name in row.keys():
                split_row = row[name].split(delim)
                num_splitted = len(split_row)
                if header_dict[name] < num_splitted:
                    header_dict[name] = num_splitted

    header_list = []
    for col_name in header_dict.keys():
        header_list.append(col_name)
        if header_dict[col_name] > 1:
            for x in range(header_dict[col_name]):
                key = col_name + "(" + str(x + 1) + ")"
                header_list.append(key)

    with open(input_file, 'r', encoding="utf-8-sig") as file:

        reader = DictReader(file, delimiter=';')

        with open(
                output_file,
                'w+', encoding="utf-8-sig",
                newline=""
        ) as outfile:

            writer = DictWriter(
                outfile,
                delimiter=';',
                fieldnames=header_list,
                quoting=QUOTE_ALL
            )
            writer.writeheader()

            for row in reader:
                row_dict = collections.defaultdict(str)
                for name in row.keys():

                    row_dict[name] = row[name]

                    if subfields:
                        split_row = []
                        first_split = row[name].split(delim)
                        for element in first_split:
                            second_split = element.split(sf_delim)
                            second_split.pop(0)   # remove indicators
                            split_row += second_split
                    else:
                        split_row = row[name].split(delim)

                    num_splitted = len(split_row)

                    if header_dict[name] > 1:
                        for x in range(header_dict[name]):
                            key = name + "(" + str(x + 1) + ")"
                            if x < num_splitted:
                                row_dict[key] = split_row[x]
                            else:
                                row_dict[key] = ""

                writer.writerow(row_dict)


rewrite_csv(csv_input, csv_output)
