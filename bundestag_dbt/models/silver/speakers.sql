SELECT DISTINCT speaker_id ,
        name,
        lastname,
        party_affiliation,
        role
FROM {{ ref('stg_bundestag__speeches') }}