"""
Delimited Columns splitten. Funktioniert nur für Spalten mit einmaligen
Namen, weil csv.DictReader verwendet wird.
"""

import collections
from csv import DictReader, DictWriter
from os import sys

try:
    csv_input = sys.argv[1]
except IndexError:
    print("Keine Input-Datei? Sollte Dateipfad zum CSV als ersten Parameter "
          "nach Skriptnamen angeben.")
    sys.exit(1)

try:
    csv_output = sys.argv[2]
except IndexError:
    print("Keine Output-Datei? Sollte Dateipfad zum gesplitteten CSV als "
          "zweiten Parameter nach Skriptnamen angeben.")
    sys.exit(1)

delim = '---'


def rewrite_csv(input_file, output_file) -> dict:
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

    with open(input_file, 'r', encoding="utf-8-sig", newline="") as file:

        reader = DictReader(file, delimiter=';')

        with open(output_file, 'w+', encoding="utf-8-sig") as outfile:

            writer = DictWriter(outfile, delimiter=';', fieldnames=header_list)
            writer.writeheader()

            for row in reader:
                row_dict = collections.defaultdict(str)
                for name in row.keys():
                    row_dict[name] = row[name]
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
