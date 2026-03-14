-- agenda_item_docs.sql
-- Explodes the agenda_docs array into one row per document URL per agenda item.
-- Uses POSEXPLODE to get array position, which feeds the hierarchical document ID
-- (e.g. WP20-042-003-DOC01). Agenda items without documents are naturally excluded
-- since EXPLODE drops rows with empty arrays.
--
-- References int_bundestag__speeches rather than agenda_items to maintain
-- a consistent flat DAG where all silver models share a single upstream dependency.
-- This keeps models independent, modular, and concurrently executable —
-- no silver model blocks another during dbt run.

WITH exploded AS (
    SELECT DISTINCT
    agenda_item_id,
    POSEXPLODE(agenda_docs)  AS (position, document_url)
FROM {{ ref('int_bundestag__speeches') }})

SELECT agenda_item_id,
       agenda_item_id || '-DOC' || LPAD(position +1 ,2, '0') AS document_id,
       document_url
FROM exploded

