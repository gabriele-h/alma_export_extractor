"""
Alma BIB Exporte in CSV-Listen umwandeln.
"""

from os import sys
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element

try:
    xml_dateipath = sys.argv[1]
except IndexError:
    print("Keine Input-Datei? Sollte Dateipfad zum XML als ersten Parameter nach Skriptnamen angeben.")
    sys.exit(1)

try:
    csv_filepath = sys.argv[2]
except IndexError:
    print("Keine Output-Datei? Sollte Dateipfad zum TSV als zweiten Parameter nach Skriptnamen angeben.")
    sys.exit(1)

try:
    list_of_fields = sys.argv[3]
except IndexError:
    print("Keine Liste an Kategorien übergeben? Bitte als dritten Parameter angeben.")
    sys.exit(1)

xml_etree = etree.parse(xml_dateipath)


def parse_record(csv_header: list, xml: Element) -> list:

    csv_row = []

    for field in csv_header:

        if field[0:2] == "00" and int(field[2]) <= 9:
            field_type = "controlfield"
        elif field == "leader":
            field_type = "controlfield"
        else:
            field_type = "datafield"

        if len(field) == 3:
            if field_type == "controlfield":
                xpath = f"{field_type}[@tag='{field}']"
            else:
                xpath = f"{field_type}[@tag='{field}']/subfield"
        elif len(field) == 5:
            if field[3] == '*' and field[4] == '*':
                xpath = f"{field_type}[@tag='{field[0:3]}']/subfield"
            else:
                xpath = f"{field_type}[@tag='{field[0:3]}' and ind1='{field[3]}' and ind2='{field[4]}']/subfield"
        elif len(field) == 6:
            if field[3] == '*' and field[4] == '*':
                xpath = f"{field_type}[@tag='{field[0:3]}']/subfield[@code='{field[5]}']"
            else:
                xpath = f"{field_type}[@tag='{field[0:3]}' and ind1='{field[3]}' and ind2='{field[4]}']/subfield[@code='{field[5]}']"
        else:
            print("Given list of fields did not meet expectations.")
            sys.exit(1)

        # print(xpath)

        found_fields = xml.findall(xpath)
        found_fields_concat = []
        for field in found_fields:
            try:
                code = field.attrib['code']
                found_fields_concat.append('$$' + code + field.text)
            except KeyError:
                found_fields_concat.append(field.text.replace('"', '""'))

        csv_row.append('"' + ''.join(found_fields_concat) + '"')

    return csv_row


with open(csv_filepath, 'w+', encoding="utf-8") as csv_file:
    csv_file.write('\ufeff')

    csv_header = list_of_fields.split(',')

    csv_content = []

    for record in xml_etree.findall('.//record'):
        csv_row = parse_record(csv_header, record)
        # print(csv_row)
        csv_content.append(csv_row)

    csv_file.write('"' + '";"'.join(csv_header) + '"\n')

    for line in csv_content:
        csv_file.write(";".join(line) + '\n')
