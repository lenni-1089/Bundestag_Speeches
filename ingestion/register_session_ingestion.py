
from pyspark.sql import SparkSession
def register_xml_fetch(spark:SparkSession,filepath:str, source_path:str):
    filename = filepath.split('/')[-1]
    legislative_period, session_nr = filename.replace(".xml","").split("_")
    legislative_period = int(legislative_period)
    session_nr = int(session_nr)

    spark.sql(f"""
                INSERT INTO bundestag_dev.bronze.raw_sessions
                (filename, legislative_period, session_nr, file_url,status,inserted_at,source_path)
                VALUES ('{filename}',{legislative_period},{session_nr},'{filepath}','ingested',CURRENT_TIMESTAMP(),'{source_path}');
                """)

