
from ingestion.xml_fetcher import fetch_xml
from ingestion.register_session_ingestion import register_xml_fetch

urls_to_be_fetched = dbutils.jobs.taskValues.get(taskKey="discover_protocols", 
                            key= "urls_to_fetch", 
                            debugValue= "Urls to be fetched coudlnt be found")

nr_urls = len(urls_to_be_fetched)
                        
print(f"{nr_urls} files to be fetched")

nr_processed = 0
nr_registered = 0

for url in urls_to_be_fetched:
    try:
        print(F"Fetching files: {url}")
        file_path= fetch_xml(input_url =url,
                             output_directory = '/Volumes/bundestag_dev/bronze/raw_xml')
    except FileExistsError as e:
        # File arleady exists, e contains the path to the file
        # continue to registration, in case file is not registered
        file_path = e.replace("File already exists: ","")
        print(f"File already exists:{file_path}. proceeding to registration")
    except Exception as e:
        print(f"Unexpected fetch error: {e}")
        continue
    
    nr_processed +=1
    print(f"{nr_processed}/{nr_urls} fetched.")
    
    try:
        print(f"Registering file: {file_path}")
        register_xml_fetch(spark= spark, 
                            filepath = file_path, 
                            source_path = url)

    except Exception as e:
        print(f"Registration Error: {e}")
    else:
        nr_registered +=1
        print(f"{nr_registered}/{nr_urls} registered.")
        print("File succesfully registered {file_path}")
      
