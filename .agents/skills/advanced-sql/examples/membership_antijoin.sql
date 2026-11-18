-- Engine: SQLite-compatible SQL. Preserves all source entities with no matches.
-- NOT EXISTS is robust when child parent_id contains NULL.
SELECT e.entity_id
FROM entities AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM excluded_entities AS x
    WHERE x.entity_id = e.entity_id
)
ORDER BY e.entity_id;
