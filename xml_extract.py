"""
Alma BIB Exporte in CSV-Listen umwandeln.
"""

import collections
from os import sys
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element

try:
    xml_dateipath = sys.argv[1]
except IndexError:
    print("Keine Input-Datei? Sollte Dateipfad zum XML als ersten Parameter "
          "nach Skriptnamen angeben.")
    sys.exit(1)

try:
    csv_filepath = sys.argv[2]
except IndexError:
    print("Keine Output-Datei? Sollte Dateipfad zum CSV als zweiten Parameter "
          "nach Skriptnamen angeben.")
    sys.exit(1)

try:
    list_of_fields = sys.argv[3]
except IndexError:
    print("Keine Liste an Kategorien übergeben? Bitte als dritten Parameter "
          "angeben.")
    sys.exit(1)

xml_iterator = etree.iterparse(xml_dateipath)
delim = '-||-'


def parse_record(header: list, xml: Element) -> list:

    current_row_dict = collections.defaultdict(str)
    current_row = []

    for field in header:

        xpath_subfield = "subfield"

        if field[0:2] == "00" and int(field[2]) <= 9:
            field_type = "controlfield"
        elif field == "leader":
            field_type = "leader"
        else:
            field_type = "datafield"

        if field_type == "datafield" and len(field) == 6:
            xpath_subfield += f"[@code='{field[5]}']"

        xpath_field = f"{field_type}"

        if field == "leader":
            pass  # no need to add anything to xpath_field

        elif len(field) == 3:
            xpath_field += f"[@tag='{field[0:3]}']"

        elif len(field) in [5, 6]:
            field = field.replace('#', ' ')

            # Kudos to Karl Thornton for chaining attribute queries
            # https://kaijento.github.io/2017/04/21/xml-parsing-python-xpath-logical-and/
            xpath_field += f"[@tag='{field[0:3]}']"

            if field[3] != '*':
                xpath_field += f"[@ind1='{field[3]}']"

            if field[4] != '*':
                xpath_field += f"[@ind2='{field[4]}']"
        else:
            print("Given list of fields did not meet expectations ('leader' "
                  "or length is 3, 5, or 6).")
            sys.exit(1)

        field_nodes = xml.findall(xpath_field)
        field_nodes_concat = []

        for field_node in field_nodes:
            if field_type != "datafield":
                field_node_cell_content = field_node.text
            else:
                field_node_ind1 = field_node.attrib['ind1']
                field_node_ind2 = field_node.attrib['ind2']
                field_node_cell_content = field_node_ind1 + field_node_ind2

                subfield_nodes = field_node.findall(xpath_subfield)

                if len(subfield_nodes) == 0:
                    continue
                else:
                    for subfield_node in subfield_nodes:
                        code = subfield_node.attrib['code']
                        subfield_node_content = f"$${code}{subfield_node.text}"
                        field_node_cell_content += subfield_node_content

            field_nodes_concat.append(
                field_node_cell_content.replace('"', '""')
            )  # replace " for csv compatibility

        current_row_dict[field] += '"' + delim.join(field_nodes_concat) + '"'

    for field_value in current_row_dict:
        current_row.append(current_row_dict[field_value])

    return current_row


with open(csv_filepath, 'a', encoding="utf-8-sig") as csv_file:

    csv_header = list_of_fields.split(',')

    if csv_file.tell() == 0:
        csv_file.write('"' + '";"'.join(csv_header) + '"\n')
        # print(csv_header)

    for found in xml_iterator:
        if found[1].tag == 'record':
            csv_row = parse_record(csv_header, found[1])
            # print(csv_row)
            csv_file.write(";".join(csv_row) + '\n')
