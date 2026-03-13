-- speakers.sql
-- Extracts distinct speakers from the intermediate model.
-- Each row represents one unique parliamentary speaker.
-- NOTE: Known extraction bug — nested <rede> interjections can cause
-- incorrect speaker metadata. Fix pending: take only the first <redner> per <rede>.

SELECT DISTINCT
    speaker_id,
    name,
    lastname,
    party_affiliation,
    role
FROM {{ ref('int_bundestag__speeches') }}