-- ==========================================
-- TAB 1: OVERVIEW
-- ==========================================

-- Card 1 [FIXED]: Total usage days recorded (Jan–Jun 2025)
SELECT COUNT(*) AS total_usage_days
FROM usage_daily;


-- Card 3 [FILTERED]: Data per active day & per observed calendar day
SELECT
    ROUND(AVG(mb_per_active_day), 2) AS mb_per_active_day,
    ROUND(AVG(mb_per_observed_day), 2) AS mb_per_calendar_day
FROM customer_features
WHERE (:conn = 'All' OR connection_type = :conn)
  AND (:grp = 'All' OR ab_group = :grp);


-- Hero Visual: Monthly data per usage day (Group A vs Group B)
SELECT
    strftime('%Y-%m', u.usage_date) AS month,
    c.ab_group,
    COUNT(*) AS usage_day_rows,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_usage_day
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY month, c.ab_group
ORDER BY month, c.ab_group;


-- Supporting Visual 1: Active subscribers per month
SELECT
    m.month,
    COUNT(DISTINCT m.customer_id) AS active_subs
FROM v_usage_month m
JOIN customer_features c ON c.customer_id = m.customer_id
WHERE (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY m.month
ORDER BY m.month;


-- Supporting Visual 2 (Bars): Allowance usage % for every plan
SELECT
    plan_name,
    monthly_gb,
    COUNT(*) AS subs,
    ROUND(AVG(total_data_mb / 1024.0 / 6.0), 2) AS actual_gb_per_month,
    ROUND(100.0 * AVG((total_data_mb / 1024.0 / 6.0) / monthly_gb), 1) AS pct_of_allowance
FROM customer_features
WHERE usage_days > 0
  AND (:conn = 'All' OR connection_type = :conn)
  AND (:grp = 'All' OR ab_group = :grp)
GROUP BY plan_name, monthly_gb
ORDER BY monthly_gb;


-- Supporting Visual 2 (Reference Line): Filtered base average allowance usage %
SELECT
    ROUND(100.0 * AVG((total_data_mb / 1024.0 / 6.0) / monthly_gb), 1) AS base_pct_of_allowance
FROM customer_features
WHERE usage_days > 0
  AND (:conn = 'All' OR connection_type = :conn)
  AND (:grp = 'All' OR ab_group = :grp);


-- Additional Visual: Total monthly network traffic in TB
SELECT
    m.month,
    COUNT(DISTINCT m.customer_id) AS active_subs,
    ROUND(SUM(m.total_mb) / 1024.0 / 1024.0, 1) AS total_tb
FROM v_usage_month m
JOIN customer_features c ON c.customer_id = m.customer_id
WHERE (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY m.month
ORDER BY m.month;


-- ==========================================
-- TAB 2: MONTH DETAIL
-- ==========================================

-- Cards 1, 2 & 3: Active subscribers, Total TB, and Data per usage day
SELECT
    COUNT(DISTINCT u.customer_id) AS active_subs,
    ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS total_tb,
    ROUND(AVG(u.data_mb), 2) AS mb_per_usage_day
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
  AND (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp);


-- Hero Visual: Daily data carried (TB) throughout the selected month
SELECT
    u.usage_date,
    COUNT(*) AS usage_day_rows,
    ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS daily_tb
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
  AND (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY u.usage_date
ORDER BY u.usage_date;


-- Hero Visual (Reference Line): Daily average TB for the selected month
SELECT
    ROUND(AVG(daily_tb), 2) AS avg_daily_tb
FROM (
    SELECT
        u.usage_date,
        SUM(u.data_mb) / 1024.0 / 1024.0 AS daily_tb
    FROM usage_daily u
    JOIN customer_features c ON c.customer_id = u.customer_id
    WHERE strftime('%Y-%m', u.usage_date) = :selected_month
      AND (:conn = 'All' OR c.connection_type = :conn)
      AND (:grp = 'All' OR c.ab_group = :grp)
    GROUP BY u.usage_date
);


-- Supporting Visual 1: Group A vs Group B data per usage day
SELECT
    c.ab_group,
    COUNT(*) AS usage_day_counts,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_usage_day
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
  AND (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY c.ab_group
ORDER BY c.ab_group;


-- Supporting Visual 2: Data per usage day by device type
SELECT
    c.device_type,
    COUNT(*) AS usage_day_counts,
    ROUND(AVG(u.data_mb), 2) AS avg_mb_per_usage_day
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
  AND (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY c.device_type
ORDER BY avg_mb_per_usage_day DESC;


-- Additional Visual: Data per usage day by day of week
SELECT
    strftime('%w', u.usage_date) AS dow_num,
    COUNT(*) AS usage_day_counts,
    ROUND(AVG(u.data_mb), 1) AS avg_mb_per_usage_day
FROM usage_daily u
JOIN customer_features c ON c.customer_id = u.customer_id
WHERE strftime('%Y-%m', u.usage_date) = :selected_month
  AND (:conn = 'All' OR c.connection_type = :conn)
  AND (:grp = 'All' OR c.ab_group = :grp)
GROUP BY dow_num
ORDER BY dow_num;