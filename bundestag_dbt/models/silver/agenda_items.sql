-- agenda_items.sql
-- Extracts distinct agenda items from the intermediate model.
-- Each row represents one unique agenda item within a session,
-- identified by its hierarchical key (e.g. 'WP21-060-008').

SELECT DISTINCT
    session_id,
    agenda_item_id,
    agenda_name,
    agenda_title,
    agenda_subtitle,
    agenda_docs
FROM {{ ref('int_bundestag__speeches') }}
ORDER BY session_id DESC, agenda_item_id