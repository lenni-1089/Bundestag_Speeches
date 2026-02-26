import os.path

from xml_fetcher import fetch_xml,parse_session_info_from_url
from session_extraction import session_extraction
from cleaning import cleaning_raw_speeches
from schemas_bronze import bronze_schema
import pandera.pandas as pa
from save_speeches import save_speeches_to_parquet


def run_ingestion_pipeline(xml_request_url):

    # checking what tasks are required (whether we already have processed that session and if not whether
    # we have already fetched the xml file)
    legaslative_period, session_nr = parse_session_info_from_url(xml_request_url)

    parquet_path = f"./parquet_files/{legaslative_period}_{session_nr}.parquet"
    xml_path = f"./xml_files/{legaslative_period}_{session_nr}.xml"

    # if we already have the a parquet file of processed speeches and
    # fetched the xml the pipeline does not need to run
    if os.path.exists(parquet_path) and os.path.exists(xml_path):
        print(f"Session {session_nr}  of legaslative period {legaslative_period} already fully processed.")
        print(f"Processed file can be found at: {parquet_path}")
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

    # if processed speeches parquet does not yet exist and xml file
    # was fetched, we process that xml file to extract speeches from
    try:
        print("Starting to extract speeches.")
        raw_speeches_df = session_extraction(xml_output_path)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return
    else:
        print(f"Session extraction successfull!")

    # clean speeches (text cleaning and type conversion)
    try:
        clean_df = cleaning_raw_speeches(raw_speeches_df)
    except Exception as e:
        print(f"Cleaning Error: {e}")
        return
    else:
        print("Speeches cleaning done.")

    # validating cleaned data before saving
    try:
        validated_df = bronze_schema.validate(clean_df)
    except pa.errors.SchemaError as exc:
        print(exc)
        return
    else:
        print("Data validate, proceeding to save as parquet files.")
    # saving files as parquet
    try:
        output_path = save_speeches_to_parquet(validated_df, parquet_path)
    except FileExistsError as e:
        print(f"File already exists, skipping {e}")
        return
    except PermissionError as e:
        print(f"Permission denied when writing to file: {e}")
        return
    except Exception as e:
        print(f"Unexpected writing error: {e}")
        return
    else:
        print(f"Session {session_nr} of legaslative period {legaslative_period} succesfully ingested!")



    print(f"Ingestion session {legaslative_period}_{session_nr} complete")


# test run

urls = ["https://www.bundestag.de/resource/blob/1129442/21048.xml",
        "https://www.bundestag.de/resource/blob/1137042/21053.xml",
        "https://www.bundestag.de/resource/blob/1134422/21051.xml",
        "https://www.bundestag.de/resource/blob/1134418/21050.xml",
        "https://www.bundestag.de/resource/blob/1140642/21057.xml"]

for url in urls:
    run_ingestion_pipeline(url)