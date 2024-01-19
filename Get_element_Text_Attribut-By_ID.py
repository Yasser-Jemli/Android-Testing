# Developed by Yasser JEMLI 
# Date : 24 Nov 2023
# Purpose : Get specifique element attribute based on provided ressource-ID by examining the XML file of the UI dump .

import xml.etree.ElementTree as ET
import sys

def get_element_values(xml_file, resource_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    elements = root.findall(".//*[@resource-id='" + resource_id + "']")

    values = []
    for element in elements:
        value = element.get('text')
        if value:
            values.append(value)

    return values if values else ["No values found for this resource ID"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_values.py xml_file resource_id")
        sys.exit(1)

    xml_file = sys.argv[1]
    resource_id = sys.argv[2]
    values = get_element_values(xml_file, resource_id)
    for value in values:
        print(value)  # Output each value on a separate line

