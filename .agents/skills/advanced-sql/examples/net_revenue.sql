-- Engine: SQLite-compatible SQL; one row per order.
-- Order items and refunds each have many rows per order. Aggregate separately
-- before joining to avoid multiplying amounts. Missing refunds = zero by policy.
WITH line_totals AS (
    SELECT order_id, SUM(amount_cents) AS gross_cents
    FROM order_items
    GROUP BY order_id
),
refund_totals AS (
    SELECT order_id, SUM(amount_cents) AS refund_cents
    FROM order_refunds
    GROUP BY order_id
)
SELECT
    o.order_id,
    COALESCE(l.gross_cents, 0) AS gross_cents,
    COALESCE(r.refund_cents, 0) AS refund_cents,
    COALESCE(l.gross_cents, 0) - COALESCE(r.refund_cents, 0) AS net_cents
FROM orders AS o
LEFT JOIN line_totals AS l ON l.order_id = o.order_id
LEFT JOIN refund_totals AS r ON r.order_id = o.order_id
ORDER BY o.order_id;
