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


