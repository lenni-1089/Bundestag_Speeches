import requests
import xml.etree.ElementTree as ET
import os
from session_extraction import session_extraction

def fetch_xml(URL: str) ->str:

    response = requests.get(URL)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    session_info = root.attrib
    legaslative_period = session_info["wahlperiode"]
    session_nr = session_info["sitzung-nr"]

    output_path = f"./xml_files/{legaslative_period}_{session_nr}.xml"

    if not os.path.exists(output_path):
        with open(output_path, 'wb') as file:
            file.write(response.content)
        return output_path
    else:
        print(f"File already exists: {output_path}")
        return None


if __name__ == "__main__":
    import sys
    url_path = sys.argv[1]
    fetch_xml(URL= url_path)