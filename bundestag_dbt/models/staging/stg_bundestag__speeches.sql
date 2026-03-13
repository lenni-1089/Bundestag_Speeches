SELECT *
FROM {{source('bundestag', 'speeches_staging') }}

-- even though ordering serves no real technical purpose
-- it is helpful for debugging and testing to have the most recent sessions at the top of the table
ORDER BY  legaslative_period DESC, session_nr DESC, speech_id ASC