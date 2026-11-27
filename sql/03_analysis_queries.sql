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

-- Confusion counts after loading Python flag output
SELECT
  SUM(CASE WHEN t.FRAUD_LABEL=1 AND f.RULE_FLAG=1 THEN 1 ELSE 0 END) AS true_positive,
  SUM(CASE WHEN t.FRAUD_LABEL=0 AND f.RULE_FLAG=1 THEN 1 ELSE 0 END) AS false_positive,
  SUM(CASE WHEN t.FRAUD_LABEL=1 AND f.RULE_FLAG=0 THEN 1 ELSE 0 END) AS false_negative,
  SUM(CASE WHEN t.FRAUD_LABEL=0 AND f.RULE_FLAG=0 THEN 1 ELSE 0 END) AS true_negative
FROM CC_FRAUD_TRANSACTIONS t
JOIN CC_FRAUD_FLAG_RESULTS f ON f.SOURCE_ROW_ID = t.SOURCE_ROW_ID;
