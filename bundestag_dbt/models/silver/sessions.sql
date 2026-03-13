SELECT DISTINCT
    'WP' || legaslative_period || '-' || LPAD(session_nr,3,'0') AS session_id,
    legaslative_period,
    session_nr,
    session_date,
    session_start_time,
    session_end_time,
    next_session_date

FROM {{ ref('stg_bundestag__speeches') }}

-- even though ordering serves no real technical purpose
-- it is helpful for debugging and testing to have the most recent sessions at the top of the table
ORDER BY legaslative_period DESC, session_nr DESC, session_date  DESC