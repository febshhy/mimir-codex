-- Engine: SQLite-compatible SQL; one row per order with ≥1 event.
-- Explicit tie-breakers make ROW_NUMBER deterministic. Here event_id is unique.
WITH numbered AS (
    SELECT
        order_id, event_id, event_at, received_at, status,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY event_at DESC, received_at DESC, event_id DESC
        ) AS rn
    FROM order_events
)
SELECT order_id, event_id, status
FROM numbered
WHERE rn = 1
ORDER BY order_id;
