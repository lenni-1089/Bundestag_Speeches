-- int_bundestag__speeches.sql
-- Intermediate model that constructs hierarchical string keys (session, agenda item, speech)
-- from the flat staging data. All downstream silver models ref this instead of staging
-- to avoid duplicating the key construction logic.
-- Materialized as a view to avoid duplicating the staging data physically.

-- Step 1: Identify distinct agenda items by grouping on their defining attributes.
-- MIN(speech_id) captures the first speech per agenda item, which we use as a 
-- proxy for chronological ordering (since agenda items have no explicit order in the source XML).
WITH distinct_agenda_items AS (
    SELECT
        legaslative_period,
        session_nr,
        agenda_name,
        agenda_title,
        agenda_subtitle,
        agenda_docs,
        MIN(speech_id) AS first_speech_id
    FROM {{ ref('stg_bundestag__speeches') }}
    GROUP BY legaslative_period, session_nr, agenda_name, agenda_title, agenda_subtitle, agenda_docs
),

-- Step 2: Assign a sequential position number to each agenda item within its session,
-- ordered by first_speech_id to reflect the actual debate sequence.
agenda_items_ordered AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY legaslative_period, session_nr 
            ORDER BY first_speech_id
        ) AS agenda_item_nr
    FROM distinct_agenda_items
),

-- Step 3: Build session and agenda item keys at the agenda-item grain (66 rows).
-- Format: session_id = 'WP21-060', agenda_item_id = 'WP21-060-008'
-- Still operating at agenda-item grain — no speech-level data yet.
add_session_and_agenda_item_keys AS (
    SELECT
        *,
        'WP' || legaslative_period || '-' || LPAD(session_nr, 3, '0') AS session_id,
        session_id || '-' || LPAD(agenda_item_nr, 3, '0') AS agenda_item_id
    FROM agenda_items_ordered
),

-- Step 4: Join back to speech-grain staging data (854 rows) to attach the constructed keys.
-- stg.* pulls all 22 staging columns; we add session_id, agenda_item_id from the key CTEs,
-- plus speech_key built via ROW_NUMBER within each agenda item.
-- IS NOT DISTINCT FROM handles NULL-safe equality on nullable agenda fields.
add_speech_keys AS (
    SELECT
        stg.*,
        a.session_id,
        a.agenda_item_id,
        a.agenda_item_id || '-' || LPAD(
            ROW_NUMBER() OVER (PARTITION BY a.agenda_item_id ORDER BY stg.speech_id), 3, '0'
        ) AS speech_key 
    FROM {{ ref('stg_bundestag__speeches') }} AS stg
    LEFT JOIN add_session_and_agenda_item_keys AS a ON 
        stg.legaslative_period = a.legaslative_period
        AND stg.session_nr = a.session_nr
        AND stg.agenda_name = a.agenda_name
        AND stg.agenda_title IS NOT DISTINCT FROM a.agenda_title
        AND stg.agenda_subtitle IS NOT DISTINCT FROM a.agenda_subtitle
        AND stg.agenda_docs IS NOT DISTINCT FROM a.agenda_docs
)

-- Final SELECT: curate column order and rename keys for downstream consumption.
-- speech_key becomes speech_id; the original Bundestag speech_id is preserved for traceability.
SELECT 
    session_id,
    issn_id,
    legaslative_period,
    session_nr,
    session_date,
    session_start_time,
    session_end_time,
    next_session_date,
    agenda_item_id,
    agenda_name,
    agenda_title,
    agenda_subtitle,
    agenda_docs,
    speech_key AS speech_id,
    speech_id AS original_bundestag_speech_id,
    speaker_id,
    name,
    lastname,
    role,
    party_affiliation,
    speech,
    comments
FROM add_speech_keys
ORDER BY legaslative_period DESC, session_nr DESC, speech_id