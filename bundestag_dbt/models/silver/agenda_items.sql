
WITH  agenda_level AS ( SELECT
    legaslative_period,
    session_nr,
    agenda_name,
    agenda_title,
    agenda_subtitle,
    agenda_docs, -- to be exploded into a seperate table with one row per document, list of document urls for now
    MIN(speech_id) AS first_speech_id -- to be used for ordering the agenda items chronologically, not ideal but we don't have any other option

FROM {{ ref('stg_bundestag__speeches') }}
GROUP BY legaslative_period, session_nr, agenda_name, agenda_title, agenda_subtitle, agenda_docs)

SELECT 
    'WP' || legaslative_period || '-' || LPAD(session_nr, 3, '0') AS session_id,
    'WP' || legaslative_period || '-' || LPAD(session_nr, 3, '0') || '-' || LPAD(ROW_NUMBER() OVER (
    PARTITION BY legaslative_period, session_nr ORDER BY first_speech_id),3, '0') AS agenda_item_id,
    agenda_name,
    agenda_title,
    agenda_subtitle,
    agenda_docs
FROM agenda_level
ORDER BY legaslative_period DESC, session_nr DESC, first_speech_id ASC

