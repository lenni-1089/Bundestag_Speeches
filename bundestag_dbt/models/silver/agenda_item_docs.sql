-- agenda_item_docs.sql
-- Explodes the agenda_docs array into one row per document URL per agenda item.
-- Agenda items without documents (empty arrays) are naturally excluded
-- since EXPLODE drops rows with empty arrays.
--
-- References int_bundestag__speeches rather than agenda_items to maintain
-- a consistent flat DAG where all silver models share a single upstream dependency.
-- This keeps models independent, modular, and concurrently executable —
-- no silver model blocks another during dbt run.

SELECT DISTINCT
    agenda_item_id,
    EXPLODE(agenda_docs) AS document_url
FROM {{ ref('int_bundestag__speeches') }}