-- Engine: SQLite-compatible SQL. Anchor is a known root employee.
-- UNION (not UNION ALL) deduplicates the projected employee ID for a graph
-- containing cycles; adding a changing depth column would invalidate this guard.
WITH RECURSIVE reports(employee_id) AS (
    SELECT employee_id
    FROM employees
    WHERE employee_id = 1
    UNION
    SELECT e.employee_id
    FROM employees AS e
    JOIN reports AS r ON e.manager_id = r.employee_id
)
SELECT employee_id
FROM reports
ORDER BY employee_id;
