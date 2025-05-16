import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import (
    export_to_csv,
    export_to_postgresql,
    export_to_google_sheets,
)

class TestExportFunctions(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': [30, 25]
        })
        self.filename = 'test_output.csv'
        self.table_name = 'test_table'
        self.db_url = 'postgresql://user:pass@localhost:5432/testdb'
        self.spreadsheet_id = 'fake_spreadsheet_id'
        self.range_name = 'Sheet1!A1:B3'
        self.services_json = 'fake_path.json'
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']

    @patch("pandas.DataFrame.to_csv")
    def test_export_to_csv(self, mock_to_csv):
        export_to_csv(self.df, self.filename)
        mock_to_csv.assert_called_once_with(self.filename, index=False)

    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_export_to_postgresql(self, mock_to_sql, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        export_to_postgresql(self.df, self.table_name, self.db_url)

        mock_create_engine.assert_called_once_with(self.db_url)
        mock_to_sql.assert_called_once_with(
            self.table_name,
            mock_engine,
            index=False,
            if_exists='replace'
        )

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_export_to_google_sheets(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_service

        export_to_google_sheets(
            self.services_json,
            self.df,
            self.spreadsheet_id,
            self.range_name,
            self.scopes
        )

        mock_creds.assert_called_once_with(self.services_json, scopes=self.scopes)
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds.return_value)

        mock_service.values().update.assert_called_once_with(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
            valueInputOption='RAW',
            body={
                'values': [self.df.columns.tolist()] + self.df.values.tolist()
            }
        )
        mock_service.values().update.return_value.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()