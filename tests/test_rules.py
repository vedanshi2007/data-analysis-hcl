import unittest
import pandas as pd
import numpy as np
from src.rules import FEATURE_COLUMNS, fit_rule_thresholds, apply_rules
from src.metrics import evaluate_flags

class FraudRuleTests(unittest.TestCase):
    def setUp(self):
        data = {c: np.zeros(10) for c in FEATURE_COLUMNS}
        data.update({'Time': np.arange(10)*600, 'Amount': np.arange(10,20)})
        self.frame = pd.DataFrame(data)
    def test_three_rules_created(self):
        t = fit_rule_thresholds(self.frame, .8, .8, .8, 3600)
        scored = apply_rules(self.frame, t)
        self.assertTrue({'rule_high_amount','rule_feature_outlier','rule_time_bucket_density_proxy','rule_flag'}.issubset(scored.columns))
    def test_metrics(self):
        m = evaluate_flags([0,0,1,1],[0,1,1,1])
        self.assertEqual(m['true_positive'],2)
        self.assertEqual(m['false_positive'],1)
        self.assertEqual(m['false_negative'],0)
        self.assertAlmostEqual(m['precision'],2/3)
        self.assertAlmostEqual(m['recall'],1.0)

if __name__ == '__main__': unittest.main()
