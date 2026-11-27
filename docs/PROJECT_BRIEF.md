# Project Brief

## Title
Credit Card Transaction and Fraud Pattern Analysis

## Problem statement
Financial institutions need to identify suspicious payment activity while limiting false alerts. This project demonstrates data preparation, transparent fraud-rule development, SQL analysis and dashboard design using a public labelled transaction benchmark.

## Objectives
- Profile transaction data and assess data quality.
- Implement at least three explainable anomaly flags.
- Compare flags with labelled fraud.
- Report precision, recall and F1 with confusion counts.
- Prepare Oracle SQL queries and a Power BI monitoring view.

## Project list acceptance criteria
- Three fraud-rule flags: implemented in Python.
- Compare flagged rows with labelled fraud: implemented by holdout evaluation.
- Precision and recall: calculated and exported.
- Imbalanced labels: addressed by reporting precision/recall and F1 rather than relying on accuracy.
- Duplicate rows: exact duplicate removal performed.
- Midnight edge case: source `Time` represents elapsed seconds, not wall-clock timestamp; queries use numeric time buckets and avoid timezone conversion. The benchmark does not expose a calendar midnight.

## Deliverables
Python source and tests; Oracle DDL and analysis SQL; data dictionary; methodology; Power BI authoring guide; README. Dataset and `.pbix` are not committed.
