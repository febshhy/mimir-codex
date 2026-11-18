-- Engine: SQLite-compatible SQL. One row per (entity, prediction_cutoff).
-- A feature must be both observed and AVAILABLE by decision time.
-- An old event backfilled after cutoff is not a valid historical feature.
WITH candidate AS (
    SELECT
        p.entity_id, p.prediction_cutoff, f.feature_value,
        ROW_NUMBER() OVER (
            PARTITION BY p.entity_id, p.prediction_cutoff
            ORDER BY f.event_at DESC, f.available_at DESC, f.feature_id DESC
        ) AS rn
    FROM prediction_points AS p
    LEFT JOIN feature_events AS f
      ON f.entity_id = p.entity_id
     AND f.event_at <= p.prediction_cutoff
     AND f.available_at <= p.prediction_cutoff
)
SELECT entity_id, prediction_cutoff, feature_value
FROM candidate
WHERE rn = 1
ORDER BY entity_id, prediction_cutoff;
