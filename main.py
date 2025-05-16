from bs4 import BeautifulSoup
import requests
from utils import extract, transform, load
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Konfigurasi kredensial
SERVICE_ACCOUNT_FILE = './google-sheets-api.json'  # File JSON dari Google Service Account
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '136Q8BKDsyuXFVYnOS_D0s9oVIr6b1RQ6OSeGFGEoCpA'
RANGE_NAME = 'Sheet1!A1'

def fetch_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data from {url}")


def scrape_data(base_url: str, initial_page: int, total_pages: int, delay: int = 2):
    all_data = []

    for i in range(initial_page, total_pages + 1):
        url = base_url if i == 1 else f"{base_url}/page{i}"
        print(f"[INFO] Scraping page {i}: {url}")

        try:
            html_content = fetch_data(url)
            soup = BeautifulSoup(html_content, 'html.parser')

            for item in soup.find_all('div', class_='product-details'):
                all_data.append(extract.data_products(item))

            time.sleep(delay)

        except Exception as e:
            print(f"[ERROR] Gagal scrape halaman {i}: {e}")
            continue

    return all_data

def main():
    # Ganti dengan URL yang sesuai
    base_url = "https://fashion-studio.dicoding.dev/"
    initial_page = 1
    total_pages = 50  # Ganti dengan jumlah halaman yang ingin di-scrape
    all_data = scrape_data(base_url, initial_page, total_pages)
    df = transform.transform_dataframe(all_data)
    try:
        df = transform.clean_data(df)
        df = transform.clean_currency_column(df, 'Price')
        df = transform.convert_currency(df, 'Price', 'IDR')
    except ValueError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] Gagal membersihkan data: {e}")


    # Simpan ke CSV
    load.export_to_csv(df, 'fashion_products.csv')
    # Simpan ke PostgreSQL
    load.export_to_postgresql(df, 'fashion_products', 'postgresql://postgres:123@localhost:5432/fashion_products')
    # Simpan ke Google Sheets
    load.export_to_google_sheets(df=df, services_json=SERVICE_ACCOUNT_FILE, spreadsheet_id=SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES)

    print("Data berhasil disimpan!")
    print("Scraping selesai!")

if __name__ == "__main__":
    main()