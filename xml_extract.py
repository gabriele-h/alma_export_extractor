"""
Sehr spezifischer Use-Case: Aus einem XML, das MetaLib zwecks Migration von einem Server zum andern anbietet,
sollen bestimmte Daten in eine TSV-Datei übernommen werden, welche dann nach Excel importiert werden kann.
"""

from os import sys
from xml.etree import ElementTree as etree

try:
    xml_dateipfad = sys.argv[1]
except IndexError:
    print("Keine Datei? Sollte Dateipfad zum XML als ersten Parameter nach Skriptnamen angeben.")
    sys.exit(1)

try:
    tsv_dateipfad = sys.argv[2]
except IndexError:
    print("Keine Output-Datei? Sollte Dateipfad zum TSV als zweiten Parameter nach Skriptnamen angeben.")
    sys.exit(1)

ns = {'all': "http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd",
      'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

xml_etree = etree.parse(xml_dateipfad)

with open(tsv_dateipfad, 'w+', encoding="utf-8") as tsv_datei:
    tsv_header = []
    tsv_data_lines = []
    counters = {}
    for ku in xml_etree.findall('all:knowledge_unit', ns):
        for record in ku.findall('all:record', ns):
            controlfields = record.findall('all:controlfield', ns)
            local_counters = {}
            for controlfield in controlfields:
                controlfield_tag = controlfield.attrib['tag']

                try:
                    local_counters[controlfield_tag]
                except KeyError:
                    local_counters[controlfield_tag] = 1
                else:
                    local_counters[controlfield_tag] += 1

                try:
                    counters[controlfield_tag]
                except KeyError:
                    counters[controlfield_tag] = 1
                else:
                    if local_counters[controlfield_tag] > counters[controlfield_tag]:
                        counters[controlfield_tag] = local_counters[controlfield_tag]
                        print(f'counter for {controlfield_tag}: {local_counters[controlfield_tag]}')

                if controlfield_tag not in tsv_header:
                    tsv_header.append(controlfield_tag)
            for datafield in record.findall('all:datafield', ns):
                datafield_tag = datafield.attrib['tag']

                try:
                    datafield_ind1 = datafield.attrib['ind1']
                except KeyError:
                    datafield_ind1 = None

                try:
                    datafield_ind2 = datafield.attrib['ind2']
                except KeyError:
                    datafield_ind2 = None

                for subfield in datafield.findall('all:subfield', ns):
                    try:
                        subfield_code = subfield.attrib['code']
                    except KeyError:
                        print('No subfield for datafield?')
                    else:
                        datafield_description = datafield_tag
                        if datafield_ind1:
                            datafield_description += datafield_ind1
                        if datafield_ind2:
                            datafield_description += datafield_ind2
                        if subfield_code:
                            datafield_description += subfield_code
                        if datafield_description not in tsv_header:
                            tsv_header.append(datafield_description)

                        try:
                            local_counters[datafield_description]
                        except KeyError:
                            local_counters[datafield_description] = 1
                        else:
                            local_counters[datafield_description] += 1

                        try:
                            counters[datafield_description]
                        except KeyError:
                            counters[datafield_description] = 1
                        else:
                            if local_counters[datafield_description] > counters[datafield_description]:
                                counters[datafield_description] = local_counters[datafield_description]
                                print(f'counter for {datafield_description}: {counters[datafield_description]}')

    for ku in xml_etree.findall('all:knowledge_unit', ns):
        tsv_line = {}
        tsv_header.sort()
        if ku.find('all:record', ns):
            for field_type in tsv_header:
                content = []

                if counters[field_type] > 1:
                    iterate = True
                else:
                    iterate = False

                if len(field_type) == 3:
                    controlfield_tag = field_type
                    for controlfield in ku.findall('all:record/all:controlfield', ns):
                        if controlfield.attrib['tag'] == controlfield_tag:
                            field_type_content = controlfield.text
                            if iterate:
                                content.append(field_type_content)
                elif len(field_type) == 6:
                    datafield_tag = field_type[0:3]
                    datafield_ind1 = field_type[3]
                    datafield_ind2 = field_type[4]
                    subfield_code = field_type[5]
                    for datafield in ku.findall('all:record/all:datafield', ns):
                        if datafield.attrib['tag'] == datafield_tag \
                            and datafield.attrib['ind1'] == datafield_ind1 \
                                and datafield.attrib['ind2'] == datafield_ind2:
                            for subfield in datafield.findall('all:subfield', ns):
                                if subfield.attrib['code'] == subfield_code:
                                    field_type_content = subfield.text
                                    if iterate:
                                        content.append(field_type_content)
                try:
                    tsv_line[field_type] = field_type_content
                    if iterate:
                        tsv_line[field_type] = ';'.join(content)
                except NameError:
                    tsv_line[field_type] = ""
                field_type_content = ''
            categories = []
            for category in ku.findall('all:category', ns):
                main_found = category.findall('all:main', ns)
                sub_found = category.findall('all:sub', ns)
                for main, sub in zip(main_found, sub_found):
                    categories.append(main.text + ': ' + sub.text)
            tsv_line['category'] = ', '.join(categories)
            print(tsv_line)
            try:
                tsv_line_string = '\t'.join(tsv_line.values())
            except TypeError:
                print('Knowledge Unit kaputt?')
            else:
                tsv_data_lines.append(tsv_line_string)
    tsv_header.append('categories')
    tsv_header_string = '\t'.join(tsv_header)
    tsv_datei.write(tsv_header_string)
    tsv_datei.write('\n')
    n = 1
    for line in tsv_data_lines:
        tsv_datei.write(line)
        tsv_datei.write('\n')
        n = n+1
