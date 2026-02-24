import os.path

from xml_fetcher import fetch_xml,parse_session_info_from_url
from session_extraction import session_extraction



def run_ingestion_pipeline(xml_request_url):

    # checking what tasks are required (whether we already have processed that session and if not whether
    # we have already fetched the xml file)
    legalative_period, session_nr = parse_session_info_from_url(xml_request_url)

    csv_path = f"./csv_files/{legalative_period}_{session_nr}.csv"
    xml_path = f"./xml_files/{legalative_period}_{session_nr}.xml"

    # if we already have the a csv file of processed speeches and
    # fetched the xml the pipeline does not need to run
    if os.path.exists(csv_path) and os.path.exists(xml_path):
        print(f"Session {session_nr}  of legaslative period {legalative_period} already fully processed.")
        print(f"Processed file can be found at: {csv_path}")
        return

    #else we fetch the xml file
    if not os.path.exists(xml_path):
        try:
            print("Trying to fetch new session protocol")
            print(f"Protocol url: {xml_request_url}")
            xml_output_path = fetch_xml(xml_request_url)
        except Exception as e:
            print(f"Fetching Error: {e}")
            return
        else:
            print(f"XML file succesfully fetched and saved!")
            print(f"File saved at: {xml_output_path}")
    else:
        print(f"XML file has already been downloaded, proceeding with session extraction.")
        xml_output_path = xml_path

    # if processed speeches csv does not yet exist and xml file
    # was fetched, we process that xml file to extract speeches from
    try:
        print("Starting to extract speeches.")
        csv_output_path = session_extraction(xml_output_path)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return
    else:
        print(f"Session extraction successfull!")
        print(f"Extracted speeched saved at: {csv_output_path}")


    print(f"Ingestion session {legalative_period}_{session_nr} complete")


# test run

urls = ["https://www.bundestag.de/resource/blob/1129442/21048.xml",
        "https://www.bundestag.de/resource/blob/1137042/21053.xml",
        "https://www.bundestag.de/resource/blob/1134422/21051.xml",
        "https://www.bundestag.de/resource/blob/1134418/21050.xml"]

for url in urls:
    run_ingestion_pipeline(url)