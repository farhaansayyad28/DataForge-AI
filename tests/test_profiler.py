import unittest

import pandas as pd

from src.profiling.profiler import profile_dataset


class ProfileDatasetTests(unittest.TestCase):
    def test_scores_for_normal_dataset(self):
        data = pd.DataFrame({"name": ["A", "B"], "age": [20, 30]})

        profile = profile_dataset(data)

        self.assertEqual(profile["completeness_score"], 100)
        self.assertEqual(profile["uniqueness_score"], 100)
        self.assertEqual(profile["quality_score"], 100)
        self.assertEqual(profile["duplicate_rows"], 0)

    def test_missing_values_reduce_completeness(self):
        data = pd.DataFrame({"name": ["A", None], "age": [20, 30]})

        profile = profile_dataset(data)

        self.assertEqual(profile["completeness_score"], 75)
        self.assertEqual(profile["uniqueness_score"], 100)
        self.assertEqual(profile["quality_score"], 87.5)

    def test_duplicate_rows_reduce_row_uniqueness(self):
        data = pd.DataFrame({"name": ["A", "A"], "age": [20, 20]})

        profile = profile_dataset(data)

        self.assertEqual(profile["duplicate_rows"], 1)
        self.assertEqual(profile["completeness_score"], 100)
        self.assertEqual(profile["uniqueness_score"], 50)
        self.assertEqual(profile["quality_score"], 75)

    def test_zero_rows_has_undefined_scores_and_safe_statistics(self):
        data = pd.DataFrame(columns=["name", "age"])

        profile = profile_dataset(data)

        self.assertIsNone(profile["completeness_score"])
        self.assertIsNone(profile["uniqueness_score"])
        self.assertIsNone(profile["quality_score"])
        self.assertEqual(set(profile["statistics"]), {"name", "age"})
        self.assertEqual(profile["statistics"]["name"]["count"], 0)
        self.assertEqual(profile["statistics"]["age"]["count"], 0)

    def test_zero_columns_has_undefined_scores_and_safe_statistics(self):
        data = pd.DataFrame(index=range(2))

        profile = profile_dataset(data)

        self.assertIsNone(profile["completeness_score"])
        self.assertIsNone(profile["uniqueness_score"])
        self.assertIsNone(profile["quality_score"])
        self.assertEqual(profile["statistics"], {})

    def test_completely_empty_dataset_has_undefined_scores_and_safe_statistics(self):
        profile = profile_dataset(pd.DataFrame())

        self.assertEqual(profile["rows"], 0)
        self.assertEqual(profile["columns"], 0)
        self.assertIsNone(profile["completeness_score"])
        self.assertIsNone(profile["uniqueness_score"])
        self.assertIsNone(profile["quality_score"])
        self.assertEqual(profile["statistics"], {})


if __name__ == "__main__":
    unittest.main()
