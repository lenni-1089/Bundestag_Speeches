from ingestion.session_extraction import session_extraction
from ingestion.cleaning import cleaning_raw_speeches
from ingestion.schemas_bronze import bronze_schema, silver_staging_spark_schema
import pandas as pd

# get xml file paths
## declaring raw sessions table as df
raw_sessions_df = spark.table("bundestag_dev.bronze.raw_sessions")
# filter only plenary sessions that are ingested but not yet have been processed 
pending_sessions_df = raw_sessions_df.filter(raw_sessions_df.status != "processed")

# Getting xml file paths of all sessions to be processed
# for that converting spark df to pandas df, selecting only file url column
# converting values to list
xml_data = pending_sessions_df.toPandas()[["filename","file_url"]].to_dict(orient="records")

print(f"Found {len(xml_data)} sessions to process")
  
# for each xml file extract speeches, clean, validate and save speeches
# starting count from 1
for i, xml in enumerate(xml_data, start= 1):
    filename = xml["filename"]
    file_url = xml["file_url"]
    print(f"\n[{i}/{len(xml_data)}] Processing {filename}...")

    try:
        # extract raw speeches
        raw_speeches_df = session_extraction(file_url)
    except Exception as e:
        print(f"Extraction error of file {filename}: {e}")
        print("Proceeding with next file...")
        continue
    try:
        # clean raw speeches
        clean_speeches_df = cleaning_raw_speeches(raw_speeches_df)
    except Exception as e:
        print(f"Cleaning error of file {filename}: {e}")
        print("Proceeding with next file...")
        continue
    
    print(f"Found and extracted {len(clean_speeches_df)} speeches from {filename}.")
    # validate cleaned speeches 
    try:
        validated_speeches_df = bronze_schema.validate(clean_speeches_df)
    except Exception as e:
        print(f"Validation error of file {filename}: {e}")
        print("Proceeding with next file...")
        continue
    
    print(f"  Validated {len(validated_speeches_df)} speeches from {filename}.")
    # add source_path column
    validated_speeches_df["source_path"] = file_url
        
    # converting pandas df to spark df to leverage native spark 
    # delta table writing
    try:
        validated_spark_df = spark.createDataFrame(data=validated_speeches_df
                                                    ,schema=silver_staging_spark_schema)
    except Exception as e:
        print(f"Spark conversion error of {filename}: {e}")
        print("Proceeding with next file...")
        continue
        
        # writing validated speeches to delta table
    try:
        validated_spark_df.write.format("delta").mode("append").saveAsTable("bundestag_dev.silver_staging.speeches_staging")
    except Exception as e:
            print(f"Saving error of {filename}: {e}")
            print("Proceeding with next file...")
            continue
            
 
    # if saving of speeches was successful
    # update session as processed
    spark.sql(f"""
                UPDATE bundestag_dev.bronze.raw_sessions
                SET status = 'processed',
                    processed_at = current_timestamp()
                WHERE filename = '{filename}';
                """)
    print(f"Speeches successfully saved to delta table and session updated")

    print(f"\nProcessing of {filename} complete.")