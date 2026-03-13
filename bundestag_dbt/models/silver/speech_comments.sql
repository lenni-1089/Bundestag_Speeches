-- speech_comments.sql
-- Explodes the comments ARRAY<STRUCT> into one row per interjection per speech.
-- Each comment carries its character index_position within the speech text,
-- enabling reconstruction of where interjections occurred.
-- Speeches without comments are naturally excluded (EXPLODE drops empty arrays).

WITH distinct_comments AS (
    SELECT DISTINCT
        speech_id, 
        explode(comments) as comment_struct
FROM {{ ref('int_bundestag__speeches') }}
)

SELECT speech_id, 
        comment_struct.index_position as index_position,
        comment_struct.comment_text as comment_text
FROM distinct_comments

