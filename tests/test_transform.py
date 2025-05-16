import unittest
import pandas as pd
from utils.transform import (
    clean_currency_column,
    convert_currency,
    transform_dataframe,
    clean_data,
    CURRENCY_CONVERSION_RATES
)

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {'Title': 'T-shirt 20', 'Price': '$82.85', 'Rating': 3.4, 'Colors': '3', 'Size': 'XXL', 'Gender': 'Women', 'Timestamp': '2025-05-15T08:48:57.137867'},
            {'Title': 'Unknown Product', 'Price': '$82.85', 'Rating': 3.4, 'Colors': '3', 'Size': 'XXL', 'Gender': 'Women', 'Timestamp': '2025-05-15T08:48:57.137867'},
            {'Title': 'T-shirt 20', 'Price': None, 'Rating': 3.4, 'Colors': '3', 'Size': 'XXL', 'Gender': 'Women', 'Timestamp': '2025-05-15T08:48:57.137867'},
            {'Title': 'Unknown Product', 'Price': '0.00', 'Rating': 0.0, 'Colors': '0', 'Size': 'N/A', 'Gender': 'Women', 'Timestamp': '2025-05-15T08:48:57.137867'}
        ]
        self.df = pd.DataFrame(self.sample_data)

    def test_transform_dataframe(self):
        result_df = transform_dataframe(self.sample_data)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(result_df.shape[0], 4)

    def test_clean_currency_column(self):
        df = clean_currency_column(self.df.copy(), "Price")
        self.assertTrue(pd.api.types.is_float_dtype(df["Price"]))
        self.assertAlmostEqual(df.loc[0, "Price"], 82.85)

    def test_convert_currency(self):
        df = convert_currency(self.df.copy(), "Price", to_currency="IDR")
        expected_value = 82.85 * CURRENCY_CONVERSION_RATES["IDR"]
        self.assertAlmostEqual(df.loc[0, "Price"], expected_value)

    def test_clean_data(self):
        df = transform_dataframe(self.sample_data)
        df = clean_currency_column(df, "Price")
        df_cleaned = clean_data(df)
        self.assertEqual(len(df_cleaned), 1)  # Hanya satu baris T-shirt yang valid
        self.assertNotIn("Unknown Product", df_cleaned["Title"].values)

    def test_invalid_currency_column(self):
        df = clean_currency_column(self.df.copy(), "NonExistent")
        # Pastikan kolom tetap tidak ditambahkan atau dimodifikasi
        self.assertNotIn("NonExistent", df.columns)

    def test_invalid_currency_code(self):
        with self.assertRaises(ValueError):
            convert_currency(self.df.copy(), "Price", to_currency="ABC")

if __name__ == '__main__':
    unittest.main()