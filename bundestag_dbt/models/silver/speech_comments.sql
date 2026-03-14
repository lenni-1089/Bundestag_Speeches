-- speech_comments.sql
-- Explodes the comments ARRAY<STRUCT> into one row per interjection per speech.
-- Uses POSEXPLODE to get array position, which feeds the hierarchical comment ID
-- (e.g. WP20-042-003-007-C01). Each comment carries its character index_position
-- within the speech text, enabling reconstruction of where interjections occurred.
-- Speeches without comments are naturally excluded (EXPLODE drops empty arrays).

WITH distinct_comments AS (
    SELECT DISTINCT
        speech_id, 
        POSEXPLODE(comments) as (position,comment_struct)
FROM {{ ref('int_bundestag__speeches') }}
)

SELECT speech_id,
        speech_id || '-C' || LPAD(position + 1, 2, '0') AS comment_id,
        comment_struct.index_position as index_position,
        REGEXP_REPLACE(comment_struct.comment_text, '[()]', '') as comment_text
FROM distinct_comments


