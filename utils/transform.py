import pandas as pd
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)

# Konstanta nilai tukar
CURRENCY_CONVERSION_RATES = {
    "IDR": 16000,
    "USD": 1.0,
    "EUR": 0.85,
}

import logging

logger = logging.getLogger(__name__)

def clean_currency_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if column_name not in df.columns:
        logger.debug(f"Kolom '{column_name}' tidak ditemukan di DataFrame. Melewati pembersihan.")
        return df
    try:
        df[column_name] = df[column_name].replace({'\$': '', ',': ''}, regex=True).astype(float)
    except Exception as e:
        logger.error(f"Gagal membersihkan kolom '{column_name}': {e}")
    return df


def convert_currency(df: pd.DataFrame, column_name: str, to_currency: str = "IDR") -> pd.DataFrame:
    if to_currency not in CURRENCY_CONVERSION_RATES:
        raise ValueError(f"Mata uang '{to_currency}' tidak didukung.")

    df = clean_currency_column(df, column_name)
    df[column_name] *= CURRENCY_CONVERSION_RATES[to_currency]
    return df


def transform_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        raise ValueError("Input harus berupa list of dictionaries.")
    
    return pd.DataFrame(data)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if 'Title' not in df.columns:
        raise ValueError("DataFrame tidak memiliki kolom 'Title' untuk filter produk unknown.")
    
    df = df.dropna()  # drop NA khusus kolom penting
    df = df.drop_duplicates()
    df = df[df['Title'] != 'Unknown Product']
    df = df.reset_index(drop=True)
    return df

