import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def export_to_csv(df:pd.DataFrame, filename:str) -> None:
    df.to_csv(filename, index=False)

def export_to_postgresql(df: pd.DataFrame, table_name: str, db_url: str) -> None:
    """
    Menyimpan DataFrame ke PostgreSQL.
    
    Parameters:
    - df: DataFrame yang ingin disimpan
    - table_name: nama tabel tujuan di database
    - db_url: URL koneksi PostgreSQL (format: 'postgresql://user:password@host:port/dbname')
    """
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, index=False, if_exists='replace')  # or append
    print(f"Sukses menyimpan ke tabel '{table_name}' di database.")


# Fungsi utama
def export_to_google_sheets(services_json: str, df: pd.DataFrame, spreadsheet_id: str, range_name: str, scopes: list) -> None:
    try:
        # Autentikasi
        credentials = Credentials.from_service_account_file(services_json, scopes=scopes)
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Konversi DataFrame ke list of lists (termasuk header)
        values = [df.columns.tolist()] + df.values.tolist()

        # Buat body request
        body = {
            'values': values
        }

        # Kirim ke Google Sheets
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("✅ Data berhasil dikirim ke Google Sheets!")

    except Exception as e:
        print(f"❌ Gagal mengirim data: {e}")

