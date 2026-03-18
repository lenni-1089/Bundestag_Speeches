import requests
import xml.etree.ElementTree as ET
import os

def parse_session_info_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    session_info = root.attrib
    legaslative_period = session_info["wahlperiode"]
    session_nr = session_info["sitzung-nr"]

    return legaslative_period, session_nr

def verify_xml(root):

    if not root.tag == "dbtplenarprotokoll":
        raise ValueError(f"Unexpected root element: {root.tag}")

    if not root.find(".//sitzungsverlauf"):
        raise ValueError(f"Missing sitzungsverlauf element.")



def fetch_xml(input_url: str, output_directory:str) ->str:

    response = requests.get(input_url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    verify_xml(root)
    session_info = root.attrib
    legaslative_period = session_info["wahlperiode"]
    session_nr = session_info["sitzung-nr"]

    DIR_PATH = f'{output_directory}/{legaslative_period}'
    FILE_PATH = f'{DIR_PATH}/{legaslative_period}_{session_nr}.xml'

    if not os.path.isdir(DIR_PATH):
        os.makedirs(DIR_PATH)

    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'wb') as file:
            file.write(response.content)
        return FILE_PATH
    else:
        raise FileExistsError(f"File already exists: {FILE_PATH}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        xml_path = sys.argv[1]
        output_path = sys.argv[2]
        fetch_xml(input_url= xml_path, output_directory=output_path)
    else:
        print("Usage: python fetch_xml.py <input_url> <output_directory>")
        sys.exit()