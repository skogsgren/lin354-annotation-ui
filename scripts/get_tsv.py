import sys
import os
import xml.etree.ElementTree as ET
import pandas as pd


def main(directory, filename):
    """ exports a directory of XML files to one single TSV file """
    export = pd.DataFrame({'id':int(), 'text':str(), 'label':int()}, index=[])
    for i in os.listdir(directory):
        root = ET.parse(f"{directory}/{i}").getroot()
        if root.get("annotation") == 'k':
            label = 0
        elif root.get("annotation") == 'h':
            label = 1
        else:
            label = 2
        new_row = pd.DataFrame({
            'id': root.get("id"),
            'word': root.get("word"),
            'label': label,
            'text': root[0].text.replace('\n', ' ')},
            index=[0])
        export = pd.concat([export, new_row], ignore_index=True)
    export.to_csv(filename, sep='\t')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
