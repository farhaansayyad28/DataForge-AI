import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.ingestion.loader import load_dataset


class LoadDatasetTests(unittest.TestCase):
    def temporary_directory(self):
        return tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parent
        )

    def test_zero_byte_csv_raises_clear_error(self):
        with self.temporary_directory() as temporary_directory:
            csv_path = Path(temporary_directory) / "empty.csv"
            csv_path.write_bytes(b"")

            with csv_path.open("rb") as csv_file:
                with self.assertRaisesRegex(ValueError, "CSV file is empty"):
                    load_dataset(csv_file)

    def test_header_only_csv_loads_with_zero_rows(self):
        with self.temporary_directory() as temporary_directory:
            csv_path = Path(temporary_directory) / "headers.csv"
            csv_path.write_text("name,age\n", encoding="utf-8")

            with csv_path.open("rb") as csv_file:
                data = load_dataset(csv_file)

        self.assertEqual(list(data.columns), ["name", "age"])
        self.assertEqual(len(data), 0)

    def test_valid_csv_loads_data(self):
        with self.temporary_directory() as temporary_directory:
            csv_path = Path(temporary_directory) / "valid.csv"
            csv_path.write_text("name,age\nAda,36\n", encoding="utf-8")

            with csv_path.open("rb") as csv_file:
                data = load_dataset(csv_file)

        expected = pd.DataFrame({"name": ["Ada"], "age": [36]})
        pd.testing.assert_frame_equal(data, expected)


if __name__ == "__main__":
    unittest.main()
