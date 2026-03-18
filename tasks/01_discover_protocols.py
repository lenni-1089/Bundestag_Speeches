from ingestion.xml_discovery import discover_xml_urls

BASE_URL = "https://www.bundestag.de/ajax/filterlist/de/services/opendata/1058442-1058442"

# check all available urls
discovered_urls = discover_xml_urls(base_url=BASE_URL)

# check all urls that have been fetched already
fetched_rows = spark.sql("SELECT source_path FROM bundestag_dev.bronze.raw_sessions").collect()
fetched_urls = [row.source_path for row in fetched_rows]

# find all urls that not have been fetched but are available
urls_to_fetch = list(set(discovered_urls) - set(fetched_urls))


dbutils.jobs.taskValues.set(key = "urls_to_fetch", value = urls_to_fetch)

print(f"{len(urls_to_fetch)} documents are found that are not yet fetched!")