# Requirements Traceability

| Project-list requirement | Implementation evidence | Status / qualification |
|---|---|---|
| Python data cleaning and fraud rule flags | `src/run_analysis.py`, `src/rules.py` | Implemented; run after placing source CSV in `data/` |
| Oracle tables and analytical SQL | `sql/01_create_tables.sql`, `sql/03_analysis_queries.sql` | Scripts supplied; not run against an Oracle instance |
| Power BI flagged transaction view | `powerbi/POWER_BI_GUIDE.md` | Layout and DAX guide supplied; no PBIX binary included |
| At least three fraud rules | Three rule flags emitted by the Python workflow | One is a dataset-level time-density proxy, not card-specific velocity |
| Compare flagged vs labelled fraud | `src/metrics.py` and `evaluation_summary.json/csv` | Computed when actual dataset is run |
| Precision and recall | Evaluation summary | Computed when actual dataset is run |
| Imbalanced classes | Precision, recall and F1 reported; accuracy not used as headline metric | Design implemented |
| Duplicate rows | Exact duplicate row count and removal in runner | Not a substitute for entity-level duplicate detection |
| Midnight/time boundary case | Numeric elapsed-time buckets; no timezone conversion | Source time is relative seconds, not calendar wall-clock time |

No quantitative finding is reported in this document until the real source dataset has been downloaded and the analysis executed.
