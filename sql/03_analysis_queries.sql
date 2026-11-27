-- Overall volume and fraud prevalence
SELECT COUNT(*) AS total_transactions,
       SUM(CASE WHEN FRAUD_LABEL = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
       ROUND(100 * AVG(FRAUD_LABEL), 4) AS fraud_rate_pct
FROM CC_FRAUD_TRANSACTIONS;

-- Amount profile by label
SELECT FRAUD_LABEL, COUNT(*) AS transaction_count,
       ROUND(AVG(AMOUNT),2) AS avg_amount,
       ROUND(MEDIAN(AMOUNT),2) AS median_amount,
       ROUND(MAX(AMOUNT),2) AS max_amount
FROM CC_FRAUD_TRANSACTIONS
GROUP BY FRAUD_LABEL ORDER BY FRAUD_LABEL;

-- Relative time buckets; Time is elapsed seconds from benchmark reference
SELECT FLOOR(TRANSACTION_TIME_SECONDS / 3600) AS time_bucket_hour,
       COUNT(*) AS transaction_count, SUM(FRAUD_LABEL) AS fraud_count,
       ROUND(100 * SUM(FRAUD_LABEL) / NULLIF(COUNT(*),0), 3) AS fraud_rate_pct
FROM CC_FRAUD_TRANSACTIONS
GROUP BY FLOOR(TRANSACTION_TIME_SECONDS / 3600)
ORDER BY time_bucket_hour;


-- 4) Rolling transaction-activity window with analytic functions.
-- This is an overall dataset activity proxy because the source has no card ID;
-- it must not be interpreted as per-card transaction velocity.
WITH activity_window AS (
  SELECT SOURCE_ROW_ID,
         TRANSACTION_TIME_SECONDS,
         TRANSACTION_TIME_SECONDS
           - LAG(TRANSACTION_TIME_SECONDS) OVER (
               ORDER BY TRANSACTION_TIME_SECONDS, SOURCE_ROW_ID
             ) AS SECONDS_SINCE_PREVIOUS_TRANSACTION,
         COUNT(*) OVER (
           ORDER BY TRANSACTION_TIME_SECONDS
           RANGE BETWEEN 3600 PRECEDING AND CURRENT ROW
         ) AS TRANSACTIONS_IN_PREVIOUS_3600_SECONDS
  FROM CC_FRAUD_TRANSACTIONS
)
SELECT SOURCE_ROW_ID, TRANSACTION_TIME_SECONDS,
       SECONDS_SINCE_PREVIOUS_TRANSACTION,
       TRANSACTIONS_IN_PREVIOUS_3600_SECONDS
FROM activity_window
ORDER BY TRANSACTION_TIME_SECONDS, SOURCE_ROW_ID;

-- 5) Confusion counts after loading Python flag output
SELECT
  SUM(CASE WHEN t.FRAUD_LABEL=1 AND f.RULE_FLAG=1 THEN 1 ELSE 0 END) AS true_positive,
  SUM(CASE WHEN t.FRAUD_LABEL=0 AND f.RULE_FLAG=1 THEN 1 ELSE 0 END) AS false_positive,
  SUM(CASE WHEN t.FRAUD_LABEL=1 AND f.RULE_FLAG=0 THEN 1 ELSE 0 END) AS false_negative,
  SUM(CASE WHEN t.FRAUD_LABEL=0 AND f.RULE_FLAG=0 THEN 1 ELSE 0 END) AS true_negative
FROM CC_FRAUD_TRANSACTIONS t
JOIN CC_FRAUD_FLAG_RESULTS f ON f.SOURCE_ROW_ID = t.SOURCE_ROW_ID;
