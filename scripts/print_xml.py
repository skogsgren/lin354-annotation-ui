import xml.etree.ElementTree as ET
import os
import sys


def print_xml(directory):
    """ Prints tweets of XML files in a readable way """
    c = 1
    for i in os.listdir(directory):
        root = ET.parse("%s/%s" % (directory, i)).getroot()
        tweet = root[0].text.replace('\n', '')
        print(f"{i}: {tweet}\n")
        c += 1


if __name__ == "__main__":
    print_xml(sys.argv[1])
