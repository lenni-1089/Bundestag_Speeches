-- sessions.sql
-- Extracts distinct parliamentary sessions from the intermediate model.
-- Each row represents one unique session, identified by its hierarchical key (e.g. 'WP21-060').

SELECT DISTINCT
    session_id,
    legaslative_period,
    session_nr,
    session_date,
    session_start_time,
    session_end_time,
    next_session_date
FROM {{ ref('int_bundestag__speeches') }}

-- Ordering serves no technical purpose but aids debugging and testing
-- by surfacing the most recent sessions first.
ORDER BY legaslative_period DESC, session_nr DESC, session_date DESC