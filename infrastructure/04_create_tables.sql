CREATE TABLE bundestag_dev.bronze.raw_sessions (
  filename STRING NOT NULL,
  legislative_period INT NOT NULL,
  session_nr INT NOT NULL,
  file_url STRING NOT NULL,
  status STRING,
  inserted_at TIMESTAMP NOT NULL,
  source_path STRING NOT NULL
) USING DELTA;

ALTER TABLE bundestag_dev.bronze.raw_sessions SET
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'supported');

ALTER TABLE bundestag_dev.bronze.raw_sessions 
ALTER COLUMN status SET DEFAULT 'ingested';

ALTER TABLE bundestag_dev.bronze.raw_sessions ADD CONSTRAINT chk_legislative_period CHECK (legislative_period > 0);

ALTER TABLE bundestag_dev.bronze.raw_sessions ADD CONSTRAINT chk_session_nr CHECK (session_nr > 0);
ALTER TABLE bundestag_dev.bronze.raw_sessions ADD CONSTRAINT chk_status CHECK (status IN ('ingested', 'processed'));



CREATE TABLE IF NOT EXISTS bundestag_dev.silver_staging.speeches_staging (
          -- session level
          issn_id STRING NOT NULL,
          legaslative_period INT NOT NULL,
          session_nr INT NOT NULL,
          session_date DATE NOT NULL,
          session_start_time STRING,
          session_end_time STRING,
          next_session_date DATE,
          -- agenda level
          agenda_name STRING NOT NULL,
          agenda_title STRING,
          agenda_subtitle STRING,
          agenda_docs ARRAY<STRING>,
          -- speech level
          speaker_id STRING NOT NULL,
          name STRING NOT NULL,
          lastname STRING NOT NULL,
          role STRING,
          party_affiliation STRING,
          speech_id STRING NOT NULL,
          speech STRING NOT NULL,
          comments ARRAY<STRUCT<index_position:INT,comment_text:STRING>>,
          processed_at TIMESTAMP NOT NULL,
          updated_at TIMESTAMP,
          source_path STRING NOT NULL
) USING DELTA;

ALTER TABLE bundestag_dev.silver_staging.speeches_staging SET
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'supported');

-- CONSTRAINTS
-- legaslative period >0
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_legaslative_period CHECK (legaslative_period > 0);
-- session_nr >0
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_session_nr CHECK (session_nr > 0);
-- name min len 2
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_name_length CHECK(length(name) >=2);
-- lastname min len 2
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_lastname_length CHECK(length(lastname) >= 2);
-- party affilation min len 2
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_party_affiliation_length CHECK(length(party_affiliation) >= 2);
-- speech min len 10
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ADD CONSTRAINT chk_speech_length CHECK(length(speech) >= 10);


-- processed at DEFAULT current_timestamp
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ALTER COLUMN processed_at SET DEFAULT current_timestamp();
-- updated at DEFAULT NULL
ALTER TABLE bundestag_dev.silver_staging.speeches_staging
ALTER COLUMN updated_at SET DEFAULT NULL;





        

