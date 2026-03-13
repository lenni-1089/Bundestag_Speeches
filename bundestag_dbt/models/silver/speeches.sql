-- speeches.sql
-- Extracts individual speeches from the intermediate model.
-- Each row represents one speech, linked to its agenda item and speaker
-- via hierarchical keys (e.g. speech_id = 'WP21-060-008-001').
-- The comments column (ARRAY<STRUCT>) is retained temporarily
-- and will be exploded into a dedicated comments table.

SELECT DISTINCT
    agenda_item_id,
    speech_id,
    speaker_id,
    speech,
    comments
FROM {{ ref('int_bundestag__speeches') }}
ORDER BY agenda_item_id DESC, speech_id