WITH distinct_speakers AS(
    SELECT DISTINCT speaker_id, name, lastname, role, party_affiliation
    FROM {{ ref('stg_bundestag__speeches') }}
)

SELECT *
FROM distinct_speakers
WHERE speaker_id IN ('11004678','11004437','11004182')
ORDER BY speaker_id